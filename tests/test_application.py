import unittest
from dataclasses import replace

from wawet.geo import Position, angular_difference, distance_m, relevance
from wawet.protocol import RoadEvent, encode
from wawet.simulation import ManualClock, SimulatedNetwork
from wawet.transport import Delivery
from wawet.vehicle import Identity, Vehicle


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.clock = ManualClock(1000)
        self.network = SimulatedNetwork(self.clock, latency=1)
        self.a = Vehicle(
            Identity(b"a" * 16),
            Position(52.2, 0.9, 0),
            self.network.endpoint("a"),
            lambda: self.clock.now,
        )
        self.b = Vehicle(
            Identity(b"b" * 16),
            Position(52.1883, 0.9, 0),
            self.network.endpoint("b"),
            lambda: self.clock.now,
        )
        self.network.connect("a", "b")
        self.event = RoadEvent(b"e" * 16, 1, 5220000, 90000, 0, 1000)

    def deliver(self, event=None):
        self.a.transport.send(encode(event or self.event))
        self.network.advance(1)

    def test_report_and_alert(self):
        self.a.report(event_id=b"x" * 16)
        self.network.advance(1)
        alert = self.b.alerts()[0]
        self.assertAlmostEqual(alert.distance_m, 1300.98, delta=2)
        self.assertEqual(alert.event.event_id, b"x" * 16)
        self.assertEqual(self.b.metrics["unauthenticated"], 1)

    def test_duplicate_and_conflicting_ids(self):
        self.deliver()
        self.deliver()
        self.deliver(replace(self.event, category=2))
        self.assertEqual(len(self.b.alerts()), 1)
        self.assertEqual(self.b.metrics["duplicate"], 1)
        self.assertEqual(self.b.metrics["id_conflict"], 1)
        self.assertEqual(self.b.alerts()[0].event.category, 1)

    def test_alert_preserves_original_receive_time(self):
        self.deliver()
        received_at = self.clock.now
        self.network.advance(20)
        self.assertEqual(self.b.alerts()[0].received_at, received_at)

    def test_rate_limited_messages_do_not_scan_retention(self):
        self.b.receive_limit = 1
        self.deliver()
        original = self.b.prune

        def fail_if_called():
            self.fail("rate-limited input must not scan the cache")

        self.b.prune = fail_if_called
        self.deliver()
        self.b.prune = original
        self.assertEqual(self.b.metrics["rate_limited"], 1)

    def test_stale_rejected_and_retained_events_pruned(self):
        self.deliver()
        self.network.advance(899)
        self.assertEqual(self.b.alerts(), [])
        self.deliver()
        self.assertEqual(self.b.metrics["expired"], 1)

    def test_future_skew_boundary(self):
        self.deliver(replace(self.event, created_at=1031))
        self.assertEqual(self.b.metrics["received"], 1)
        self.deliver(replace(self.event, event_id=b"f" * 16, created_at=1033))
        self.assertEqual(self.b.metrics["future"], 1)

    def test_unknown_category_retained_without_alert(self):
        self.deliver(replace(self.event, category=240))
        self.assertEqual(len(self.b.events), 1)
        self.assertEqual(self.b.alerts(), [])

    def test_opposite_direction_and_behind(self):
        self.b.position = Position(52.1883, 0.9, 180)
        self.deliver()
        self.assertEqual(self.b.alerts(), [])
        self.b.position = Position(52.21, 0.9, 0)
        self.assertEqual(self.b.alerts(), [])

    def test_relevance_recomputed_after_motion(self):
        self.b.position = Position(52.1, 0.9, 0)
        self.deliver()
        self.assertEqual(self.b.alerts(), [])
        self.b.position = Position(52.1883, 0.9, 0)
        self.assertEqual(len(self.b.alerts()), 1)

    def test_outage_and_explicit_resend(self):
        self.network.connect("a", "b", False)
        self.deliver()
        self.network.connect("a", "b")
        self.assertEqual(self.b.alerts(), [])
        self.deliver()
        self.assertEqual(len(self.b.alerts()), 1)

    def test_contact_lost_before_delivery(self):
        self.a.transport.send(encode(self.event))
        self.network.connect("a", "b", False)
        self.network.advance(1)
        self.assertEqual(self.b.alerts(), [])
        self.assertEqual(self.network.dropped, 1)

    def test_malformed_delivery_does_not_stop_next_message(self):
        self.a.transport.send(b"bad")
        self.deliver()
        self.assertEqual(self.b.metrics["invalid"], 1)
        self.assertEqual(len(self.b.alerts()), 1)

    def test_cache_capacity_and_reclamation(self):
        self.b.capacity = 1
        self.deliver()
        self.deliver(replace(self.event, event_id=b"f" * 16))
        self.assertEqual(self.b.metrics["capacity_dropped"], 1)
        self.network.advance(900)
        self.deliver(replace(self.event, created_at=self.clock.now))
        self.assertEqual(len(self.b.events), 1)

    def test_rate_limit_and_reset(self):
        self.b.receive_limit = 2
        self.deliver()
        self.deliver()
        self.deliver()
        self.assertEqual(self.b.metrics["rate_limited"], 1)
        self.network.advance(60)
        self.deliver(replace(self.event, event_id=b"f" * 16))
        self.assertEqual(len(self.b.events), 2)

    def test_alternative_transport_without_simulator_dependencies(self):
        class Transport:
            def subscribe(self, receiver):
                self.receiver = receiver

            def send(self, payload):
                self.receiver(payload, Delivery(1000, "local-test"))

            def close(self):
                pass

        transport = Transport()
        node = Vehicle(Identity.generate(), Position(52.2, 0.9, 0), transport, lambda: 1000)
        node.report()
        self.assertEqual(len(node.alerts()), 1)

    def test_close_and_identity_validation(self):
        self.b.close()
        self.deliver()
        self.assertEqual(self.b.alerts(), [])
        with self.assertRaises(RuntimeError):
            self.b.report()
        with self.assertRaises(ValueError):
            Identity(b"invalid")

    def test_network_limits_and_order(self):
        self.network.capacity = 1
        self.a.transport.send(encode(self.event))
        self.a.transport.send(encode(replace(self.event, event_id=b"f" * 16)))
        self.network.advance(1)
        self.assertEqual(list(self.b.events), [self.event.event_id])
        self.assertEqual(self.network.dropped, 1)
        with self.assertRaises(ValueError):
            self.network.advance(-1)
        with self.assertRaises(ValueError):
            self.network.endpoint("a")
        with self.assertRaises(ValueError):
            self.a.transport.send(b"x" * 513)


class GeographyTests(unittest.TestCase):
    def test_distance_reference_and_symmetry(self):
        self.assertEqual(distance_m(0, 0, 0, 0), 0)
        self.assertAlmostEqual(distance_m(0, 0, 0, 1), 111194.927, places=3)
        self.assertEqual(distance_m(52, 0.9, 53, 1), distance_m(53, 1, 52, 0.9))

    def test_antimeridian_and_poles(self):
        self.assertLess(distance_m(0, 179.999, 0, -179.999), 223)
        self.assertLess(distance_m(90, 0, 90, 180), 0.001)
        self.assertAlmostEqual(angular_difference(359, 1), 2)

    def test_invalid_position(self):
        for values in [
            (91, 0, 0),
            (0, 181, 0),
            (0, 0, 360),
            (float("nan"), 0, 0),
            (0, 0, 0, -1),
            (True, 0, 0),
        ]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                Position(*values)

    def test_unknown_heading_and_radius(self):
        event = RoadEvent(b"x" * 16, 1, 0, 0, None, 1000, radius_m=1)
        self.assertTrue(relevance(Position(0, 0, 180), event)[0])
        self.assertFalse(relevance(Position(0.001, 0, 0), event)[0])
