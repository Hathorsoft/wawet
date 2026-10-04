import contextlib
import io
import json
import unittest
from unittest.mock import patch

from wawet.protocol import decode
from wawet.scenarios import Action, Fixture, main, run_scenario
from wawet.simulation import SimulatedTransport


def observation(result, label):
    return next(o for o in result["observations"] if o["label"] == label)


class ScenarioTests(unittest.TestCase):
    def test_passing_delivery_is_distinct_from_relevance(self):
        result = run_scenario("passing")
        self.assertEqual(result["fresh_delivery"], {"numerator": 2, "denominator": 4})
        self.assertEqual([r["recipient"] for r in result["accepted_pairs"]], ["b", "c"])
        during = observation(result, "during contact")["alerts"]
        self.assertEqual(len(during["b"]), 1)
        self.assertEqual(during["c"], [])
        self.assertEqual(observation(result, "after passing")["alerts"]["b"], [])
        self.assertEqual(result["contact_dropped"], 2)
        self.assertEqual(result["queue_dropped"], 0)
        self.assertEqual(result["latency"]["seconds"], [1, 1])

    def test_convoy_duplicates_motion_and_first_receive_time(self):
        result = run_scenario("convoy")
        self.assertEqual(result["fresh_delivery"], {"numerator": 3, "denominator": 3})
        for name in "bcd":
            self.assertEqual(result["metrics"][name]["duplicate"], 1)
            self.assertEqual(result["metrics"][name]["received"], 1)
            self.assertEqual(len(observation(result, "duplicates")["alerts"][name]), 1)
        self.assertEqual(observation(result, "leader passed")["alerts"]["b"], [])
        self.assertEqual([r["accepted_at"] for r in result["accepted_pairs"]], [1001] * 3)
        self.assertEqual(result["transmissions"][0]["frame"], result["transmissions"][1]["frame"])

    def test_rural_no_replay_original_frame_and_exact_expiry(self):
        result = run_scenario("rural")
        self.assertEqual(observation(result, "no replay")["retained"]["b"], 0)
        self.assertEqual(observation(result, "explicit resend")["retained"]["b"], 1)
        self.assertEqual(observation(result, "exact expiry")["retained"]["b"], 0)
        self.assertEqual(result["metrics"]["b"]["expired"], 1)
        frames = [t["frame"] for t in result["transmissions"]]
        self.assertEqual(frames, [frames[0]] * 3)
        event = decode(bytes.fromhex(frames[0]))
        self.assertEqual(event.created_at, 1000)
        self.assertEqual(event.expires_at, 1005)
        self.assertEqual(
            result["latency"],
            {
                "sample_count": 1,
                "seconds": [3],
                "origin": "original event creation/availability, including explicit resend wait",
            },
        )
        self.assertEqual(result["fresh_delivery"], {"numerator": 1, "denominator": 1})
        self.assertEqual(len(result["stale_probes"]), 1)

    def test_dense_bounds_drops_expiry_and_recovery(self):
        result = run_scenario("dense")
        self.assertEqual(result["fresh_delivery"], {"numerator": 15, "denominator": 28})
        self.assertEqual(result["queue_dropped"], 7)
        self.assertEqual(result["contact_dropped"], 0)
        self.assertEqual(sum(m["capacity_dropped"] for m in result["metrics"].values()), 6)
        self.assertEqual(result["peak_queue"], 7)
        self.assertEqual(result["peak_retained_per_vehicle"], 1)
        self.assertEqual(set(observation(result, "expired retention")["retained"].values()), {0})
        recovery = (4).to_bytes(16, "big").hex()
        self.assertEqual(sum(r["event"] == recovery for r in result["accepted_pairs"]), 7)
        self.assertEqual(result["latency"]["sample_count"], 15)

    def test_due_delivery_precedes_same_timestamp_disconnect(self):
        fixture = Fixture(
            ("a", "b"),
            (
                Action(0, "link", peer="b"),
                Action(0, "report", recipients=("b",)),
                Action(1, "link", peer="b", enabled=False),
                Action(1, "observe"),
            ),
        )
        result = run_scenario("boundary", fixture)
        self.assertEqual(result["fresh_delivery"], {"numerator": 1, "denominator": 1})
        self.assertEqual(result["contact_dropped"], 0)

    def test_unmarked_slow_expiry_remains_in_denominator(self):
        fixture = Fixture(
            ("a", "b"),
            (
                Action(0, "link", peer="b"),
                Action(0, "report", recipients=("b",), ttl=1),
                Action(1, "observe"),
            ),
        )
        result = run_scenario("slow", fixture)
        self.assertEqual(result["fresh_delivery"], {"numerator": 0, "denominator": 1})
        self.assertEqual(result["stale_probes"], [])
        self.assertEqual(result["metrics"]["b"]["expired"], 1)

    def test_closes_endpoints_even_on_fixture_error(self):
        closed = []
        original = SimulatedTransport.close

        def close(transport):
            closed.append(transport.name)
            original(transport)

        fixture = Fixture(("a", "b"), (Action(1, "observe"), Action(0, "observe")))
        with patch.object(SimulatedTransport, "close", close):
            with self.assertRaises(ValueError):
                run_scenario("invalid", fixture)
        self.assertEqual(closed, ["a", "b"])

    def test_cli_selection_and_repeatable_json(self):
        def output(args):
            stream = io.StringIO()
            with patch("sys.argv", ["scenarios", *args]), contextlib.redirect_stdout(stream):
                main()
            return stream.getvalue()

        first = output(["--json"])
        self.assertEqual(first, output(["--json"]))
        self.assertEqual(
            [r["scenario"] for r in json.loads(first)], ["passing", "convoy", "rural", "dense"]
        )
        selected = json.loads(output(["--scenario", "rural", "--json"]))
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["scenario"], "rural")
        self.assertIn("unauthenticated", output([]))
        with (
            patch("sys.argv", ["scenarios", "--scenario", "unknown"]),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            with self.assertRaises(SystemExit) as error:
                main()
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
