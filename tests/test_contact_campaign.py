"""Offline regression coverage for the optional contact experiment."""

import importlib.util
import io
import json
import queue
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

path = Path(__file__).resolve().parents[1] / "tools" / "rns_contact_campaign.py"
spec = importlib.util.spec_from_file_location("contact_campaign", path)
assert spec is not None and spec.loader is not None
campaign = importlib.util.module_from_spec(spec)
spec.loader.exec_module(campaign)


class ContactCampaignTests(unittest.TestCase):
    def test_address_allowlist(self):
        for address in ("127.0.0.1", "10.0.0.2", "172.16.0.2", "192.168.1.2"):
            self.assertEqual(campaign.private_address(address), address)
        for address in ("0.0.0.0", "8.8.8.8", "::1", "169.254.1.2", "172.32.0.1"):
            with self.assertRaises(ValueError):
                campaign.private_address(address)

    def test_expiry_preserves_frame_for_resend(self):
        frame = campaign.fresh_frame(1)
        created = campaign.decode(frame).created_at
        original = bytes(frame)
        self.assertTrue(campaign.sendable(frame, created))
        self.assertFalse(campaign.sendable(frame, created + 1))
        self.assertEqual(frame, original)

    def test_signed_malformed_does_not_prevent_fresh_validation(self):
        def validate(signature, body):
            return signature == b"s" * 64

        self.assertEqual(campaign.validate_body(b"short", validate, 1)[0], "signature")
        self.assertEqual(campaign.validate_body(b"s" * 64 + b"bad", validate, 1)[0], "malformed")
        frame = campaign.fresh_frame(1)
        created = campaign.decode(frame).created_at
        self.assertEqual(campaign.validate_body(b"s" * 64 + frame, validate, created)[0], "valid")
        self.assertEqual(
            campaign.validate_body(b"s" * 64 + frame, validate, created + 1)[0], "expired"
        )

    def test_queue_bounds_order_and_recovery(self):
        inbox = queue.Queue(maxsize=8)
        self.assertEqual(
            [campaign.enqueue(inbox, bytes([i])) for i in range(10)], [True] * 8 + [False] * 2
        )
        self.assertEqual([inbox.get_nowait()[0] for _ in range(8)], [bytes([i]) for i in range(8)])
        self.assertTrue(campaign.enqueue(inbox, b"fresh"))

    def test_campaign_trial_accounting(self):
        runs = campaign.scenarios(30)
        self.assertEqual(len(runs), 490)
        self.assertEqual(len({r["run_id"] for r in runs}), len(runs))
        for name in ("cold", "warm"):
            for window in (1, 2, 5, 10):
                subset = [r for r in runs if r["scenario"] == name and r["window"] == window]
                self.assertEqual(sum(not r["control_only"] for r in subset), 30)
                self.assertEqual(sum(r["control_only"] for r in subset), 30)

    def test_scheduled_wait_cannot_extend_deadline(self):
        now = [0.0]

        def clock():
            return now[0]

        def sleep(seconds):
            now[0] += seconds

        campaign.wait_until(0.1, 1, clock, sleep)
        self.assertAlmostEqual(now[0], 0.1)
        with self.assertRaises(TimeoutError):
            campaign.wait_until(100, 1, clock, sleep)
        self.assertAlmostEqual(now[0], 1)

    def test_clock_evidence_requires_finite_measured_values(self):
        good = {
            "receiver_minus_sender_seconds": -0.1,
            "uncertainty_seconds": 0.01,
            "method": "synthetic fixture",
            "measured_at": "fixture",
        }
        campaign.validate_clock(good)
        for invalid in (
            {},
            {**good, "uncertainty_seconds": -1},
            {**good, "receiver_minus_sender_seconds": float("nan")},
            {**good, "uncertainty_seconds": float("inf")},
            {**good, "method": ""},
        ):
            with self.assertRaises(ValueError):
                campaign.validate_clock(invalid)

    def test_prelaunch_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(campaign, "run_local_trial", side_effect=OSError("socket denied")):
                run_id, codes = campaign.local_trial({"run_id": "failed"}, root)
            self.assertEqual(run_id, "failed")
            self.assertEqual(codes["harness_error"], "socket denied")
            self.assertEqual(json.loads((root / "failed-exit.json").read_text()), codes)

    def test_two_host_batch_copies_only_role_material_and_saves_exit(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "config"
            config.mkdir()
            for name in (
                "identity.key",
                "send.public",
                "receive.public",
                "config",
                "settings.json",
                "old-discovery-cache",
            ):
                (config / name).write_bytes(b"fixture")
            manifest = root / "manifest.json"
            campaign.write_json(
                manifest,
                {
                    "runs": [
                        {
                            "run_id": "fixture",
                            "scheduled_at": 100,
                            "scenario": "cold",
                            "window": 1,
                            "control_only": False,
                        }
                    ]
                },
            )

            def launch(command, **kwargs):
                trial_config = Path(command[command.index("--config") + 1])
                self.assertFalse((trial_config / "old-discovery-cache").exists())
                self.assertEqual((trial_config / "identity.key").stat().st_mode & 0o777, 0o600)
                return SimpleNamespace(returncode=7)

            args = SimpleNamespace(
                manifest=manifest, config=config, role="send", output=root / "logs"
            )
            with patch.object(campaign.time, "time", return_value=100):
                with patch.object(campaign.subprocess, "run", side_effect=launch):
                    campaign.batch(args)
            self.assertEqual(
                json.loads((args.output / "fixture-send-exit.json").read_text()), {"exit": 7}
            )
            self.assertTrue((args.output / "fixture-send.stderr").exists())

    def test_two_host_batch_records_missed_start_without_launch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = root / "manifest.json"
            campaign.write_json(manifest, {"runs": [{"run_id": "late", "scheduled_at": 100}]})
            args = SimpleNamespace(
                manifest=manifest, config=root / "unused", role="send", output=root / "logs"
            )
            with patch.object(campaign.time, "time", return_value=101):
                with patch.object(campaign.subprocess, "run") as run:
                    campaign.batch(args)
                    run.assert_not_called()
            self.assertEqual(
                json.loads((args.output / "late-send-exit.json").read_text())["exit"], 1
            )

    def test_configuration_is_isolated_and_rejects_public_listener(self):
        config = campaign.configuration("receive", "192.168.1.10", 4243)
        self.assertIn("enable_transport = No", config)
        self.assertIn("share_instance = No", config)
        self.assertNotIn("AutoInterface", config)
        self.assertEqual(config.count("type = "), 1)
        with self.assertRaises(ValueError):
            campaign.configuration("receive", "0.0.0.0", 4243)
        with self.assertRaises(ValueError):
            campaign.configuration("send", "192.168.1.10", 80)

    def test_frame_hash_mismatch_cannot_count_as_delivery(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            campaign.write_json(
                root / "manifest.json",
                {"runs": [{"run_id": "x", "scenario": "cold", "window": 1, "control_only": False}]},
            )
            for role, row in (
                (
                    "send",
                    {
                        "kind": "event",
                        "outcome": "sent",
                        "event_id": "a",
                        "frame_sha256": "expected",
                    },
                ),
                ("receive", {"kind": "received", "event_id": "a", "frame_sha256": "different"}),
            ):
                (root / f"x-{role}.jsonl").write_text(
                    json.dumps({"run_id": "x", "role": role, **row}) + "\n"
                )
            result = campaign.analyse(root)["groups"]["cold/1/events"]
            self.assertEqual(result["delivered_events"], 0)
            self.assertEqual(result["failed_or_missing_trials"], 1)

    def test_missing_failed_and_truncated_trials_keep_denominator(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runs = [
                {"run_id": name, "scenario": "cold", "window": 1, "control_only": False}
                for name in ("missing", "failed", "success")
            ]
            campaign.write_json(root / "manifest.json", {"runs": runs})
            (root / "failed-send.jsonl").write_text('[]\n{"kind": "event"}\n{"truncated"')
            campaign.write_json(root / "failed-exit.json", {"send": 1, "receive": 0})
            sender = [
                {
                    "kind": "event",
                    "outcome": "sent",
                    "event_id": "a",
                    "sent_wall": 10,
                    "frame_sha256": "x",
                },
                {"kind": "complete", "counters": {"tx": 120, "rx": 50}},
            ]
            receiver = [
                {"kind": "received", "event_id": "a", "received_wall": 10.2, "frame_sha256": "x"},
                {"kind": "complete", "counters": {"tx": 0, "rx": 0}, "rejected": {"malformed": 1}},
            ]
            for role, rows in (("send", sender), ("receive", receiver)):
                (root / f"success-{role}.jsonl").write_text(
                    "".join(
                        json.dumps({"run_id": "success", "role": role, **row}) + "\n"
                        for row in rows
                    )
                )
            campaign.write_json(root / "success-exit.json", {"send": 0, "receive": 0})
            result = campaign.analyse(root)["groups"]["cold/1/events"]
            self.assertEqual(result["planned_trials"], 3)
            self.assertEqual(result["failed_or_missing_trials"], 2)
            self.assertEqual(result["delivery_fraction"], 1 / 3)
            self.assertEqual(result["latency"], {"n": 0})
            clock = {
                "receiver_minus_sender_seconds": 0.1,
                "uncertainty_seconds": 0.01,
                "method": "fixture",
                "measured_at": "fixture",
            }
            result = campaign.analyse(root, clock)["groups"]["cold/1/events"]
            self.assertAlmostEqual(result["latency"]["median"], 0.1)


class ContactTimingTests(unittest.TestCase):
    clock = {
        "receiver_minus_sender_seconds": 0.1,
        "uncertainty_seconds": 0.01,
        "method": "synthetic fixture",
        "measured_at": "fixture",
    }

    def fixture(self, accepted=11.6, outcome="sent", available=10, closed=15):
        event = {"event_id": "a", "frame_sha256": "hash"}
        logs = {
            "send": [
                {"kind": "contact", "phase": "warmup", "enabled": True, "transition_wall": 1},
                {"kind": "contact", "phase": "warmup", "enabled": False, "transition_wall": 2},
                {"kind": "contact", "phase": "measured", "enabled": True, "transition_wall": 10},
                {
                    "kind": "available",
                    **event,
                    "available_wall": available,
                    "deliberate_expiry": False,
                },
                {"kind": "event", **event, "outcome": outcome, "sent_wall": 11},
                {
                    "kind": "contact",
                    "phase": "measured",
                    "enabled": False,
                    "transition_wall": closed,
                },
            ],
            "receive": []
            if accepted is None
            else [{"kind": "received", **event, "received_wall": 11.2, "accepted_wall": accepted}],
        }
        return logs

    def evaluate(self, logs, clock=None, complete=True):
        return campaign.contact_timing(
            {}, logs, complete, 1, self.clock if clock is None else clock
        )

    def test_discovery_and_validation_delay_are_included(self):
        result = self.evaluate(self.fixture())
        self.assertAlmostEqual(result["availability_latency"][0], 1.5)
        self.assertAlmostEqual(result["acceptance_latency"][0], 0.5)
        self.assertEqual(result["within_contact"], 1)
        self.assertEqual(result["missing_timing"], 0)
        negative = self.evaluate(
            self.fixture(), {**self.clock, "receiver_minus_sender_seconds": -0.1}
        )
        self.assertAlmostEqual(negative["availability_latency"][0], 1.7)
        # A delayed stable event retains its schedule, not its eventual send time.
        self.assertAlmostEqual(
            self.evaluate(self.fixture(available=10.5))["availability_latency"][0], 1
        )

    def test_duplicate_receptions_count_once_and_resends_are_ambiguous(self):
        logs = self.fixture()
        logs["receive"].append({**logs["receive"][0], "accepted_wall": 12})
        self.assertEqual(self.evaluate(logs)["within_contact"], 1)
        self.assertEqual(len(self.evaluate(logs)["availability_latency"]), 1)
        logs["send"].insert(-1, dict(logs["send"][-2]))
        self.assertEqual(self.evaluate(logs)["missing_timing"], 1)

    def test_contact_close_is_exclusive_and_uncertainty_is_conservative(self):
        zero = {**self.clock, "receiver_minus_sender_seconds": 0, "uncertainty_seconds": 0}
        for accepted in (15, 16):
            result = self.evaluate(self.fixture(accepted=accepted), zero)
            self.assertEqual(result["within_contact"], 0)
            self.assertEqual(result["missing_timing"], 0)
        result = self.evaluate(self.fixture(accepted=15.095))
        self.assertEqual(result["within_contact"], 0)
        self.assertEqual(result["missing_timing"], 1)

    def test_known_misses_and_invalid_evidence(self):
        for outcome in ("unavailable", "expired_before_send", "send_failed", "sent"):
            result = self.evaluate(self.fixture(accepted=None, outcome=outcome))
            self.assertEqual(result["intended"], 1)
            self.assertEqual(result["missing_timing"], 0)
            self.assertEqual(result["within_contact"], 0)
        for field, value in (
            ("accepted_wall", float("nan")),
            ("accepted_wall", True),
            ("accepted_wall", 9),
            ("frame_sha256", "wrong"),
        ):
            logs = self.fixture()
            logs["receive"][0][field] = value
            result = self.evaluate(logs)
            self.assertEqual(result["within_contact"], 0)
        logs = self.fixture()
        del logs["receive"][0]["accepted_wall"]
        self.assertEqual(self.evaluate(logs)["missing_timing"], 1)
        self.assertEqual(self.evaluate(self.fixture(), complete=False)["missing_timing"], 1)
        self.assertEqual(
            campaign.contact_timing({}, self.fixture(), True, 1, None)["missing_timing"], 1
        )

    def test_thresholds_and_clock_hold(self):
        def summary(delivered=29, latency=1.9, clock=None, missing=0):
            group = {
                "failed_or_missing_trials": 0,
                "contact_timing": {
                    "intended": 30,
                    "within_contact": delivered,
                    "missing_timing": missing,
                    "availability_latency": [latency] * delivered,
                    "acceptance_latency": [0.1] * delivered,
                },
            }
            campaign.timing_summary(group, self.clock if clock is None else clock, True)
            return group["contact_timing"]["criteria"]

        self.assertEqual(summary(), {"T01": "PASS", "T02": "PASS", "T03": "PASS"})
        self.assertEqual(summary(delivered=28)["T02"], "REVISE")
        self.assertEqual(summary(latency=1.995)["T01"], "REVISE")
        self.assertEqual(summary(clock={**self.clock, "uncertainty_seconds": 0.101})["T01"], "HOLD")
        self.assertEqual(summary(missing=1)["T02"], "HOLD")
        self.assertEqual(summary(delivered=0)["T01"], "HOLD")
        self.assertEqual(summary(delivered=0)["T02"], "REVISE")

    def test_sender_orchestration_preserves_schedule_before_discovery(self):
        for scenario in ("cold", "warm", "stable", "absent"):
            now = [0.0]

            class Identity:
                def __init__(self, **kwargs):
                    pass

                @classmethod
                def from_file(cls, path):
                    return cls()

                def load_public_key(self, key):
                    pass

                def get_public_key(self):
                    return b"public"

                def sign(self, body):
                    return b"s" * 64

            class Destination:
                OUT, SINGLE = 1, 2

                def __init__(self, *args):
                    self.hash = b"destination"

            class Stack:
                def __init__(self, **kwargs):
                    pass

                def exit_handler(self):
                    pass

            class Packet:
                def __init__(self, destination, body):
                    self.raw = body

                def send(self):
                    return object()

            tcp = SimpleNamespace(
                process_outgoing=lambda *a: None, process_incoming=lambda *a: None
            )
            transport = SimpleNamespace(
                interfaces=[],
                request_path=lambda *a: None,
                has_path=lambda *a, scenario=scenario, now=now: (
                    scenario != "absent" and now[0] >= 2
                ),
            )
            rns = SimpleNamespace(
                Identity=Identity,
                Destination=Destination,
                Reticulum=Stack,
                Packet=Packet,
                Transport=transport,
            )

            def sleep(seconds, now=now):
                now[0] += seconds

            original_wait = campaign.wait_until

            def wait(target, deadline, original_wait=original_wait, now=now, sleep=sleep):
                return original_wait(target, deadline, lambda: now[0], sleep)

            with tempfile.TemporaryDirectory() as temporary:
                config = Path(temporary)
                settings = {"role": "send", "address": "127.0.0.1", "port": 4243}
                campaign.write_json(config / "settings.json", settings)
                (config / "config").write_text(campaign.configuration(**settings))
                (config / "receive.public").write_bytes(b"public")
                args = SimpleNamespace(
                    config=config,
                    role="send",
                    scenario=scenario,
                    run_id="fixture",
                    deadline=50,
                    window=5,
                    count=3,
                    interval=1,
                    control_only=False,
                )
                output = io.StringIO()
                with (
                    patch.dict(
                        "sys.modules",
                        {
                            "RNS": rns,
                            "RNS.Interfaces.TCPInterface": SimpleNamespace(TCPClientInterface=tcp),
                        },
                    ),
                    patch.object(campaign.importlib.metadata, "version", return_value="1.5.5"),
                    patch.object(campaign.time, "time", side_effect=lambda now=now: 1000 + now[0]),
                    patch.object(campaign.time, "monotonic", side_effect=lambda now=now: now[0]),
                    patch.object(campaign, "wait_until", side_effect=wait),
                    patch.object(campaign.time, "sleep", side_effect=sleep),
                    redirect_stdout(output),
                ):
                    campaign.worker(args)
                rows = [json.loads(line) for line in output.getvalue().splitlines()]
                available = [r for r in rows if r["kind"] == "available"]
                discovery = next(
                    r for r in rows if r["kind"] == "discovery" and r["phase"] == "contact"
                )
                self.assertLess(rows.index(available[-1]), rows.index(discovery))
                events = [r for r in rows if r["kind"] == "event"]
                self.assertEqual(
                    [r["frame_sha256"] for r in events], [r["frame_sha256"] for r in available]
                )
                self.assertEqual(
                    events[0]["outcome"], "unavailable" if scenario == "absent" else "sent"
                )
                if scenario in ("cold", "stable"):
                    self.assertAlmostEqual(available[0]["available_wall"], 1000)
                    self.assertGreaterEqual(events[0]["sent_wall"], 1002)
                if scenario == "stable":
                    self.assertEqual([r["available_wall"] for r in available], [1000, 1001, 1002])
                measured = [r for r in rows if r["kind"] == "contact" and r["phase"] == "measured"]
                self.assertEqual([r["enabled"] for r in measured], [True, False])

    def test_receiver_timestamp_follows_worker_validation(self):
        now = [0.0]

        def validate(signature, body):
            now[0] += 0.3
            return True

        identity = SimpleNamespace(
            get_public_key=lambda: b"public", load_public_key=lambda key: None, validate=validate
        )

        class Identity:
            def __new__(cls, **kwargs):
                return identity

            from_file = staticmethod(lambda path: identity)

        class Inbox(queue.Queue):
            def get(self, timeout=None):
                now[0] += 0.02
                return super().get(block=False)

        class Destination:
            IN, SINGLE = 0, 1

            def __init__(self, *args):
                self.hash = b"destination"

            def set_packet_callback(self, callback):
                callback(b"s" * 64 + campaign.fresh_frame(), None)

        rns = SimpleNamespace(
            Identity=Identity,
            Destination=Destination,
            Reticulum=lambda **kwargs: SimpleNamespace(exit_handler=lambda: None),
            Transport=SimpleNamespace(interfaces=[]),
        )
        tcp = SimpleNamespace(process_outgoing=lambda *a: None, process_incoming=lambda *a: None)
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary)
            settings = {"role": "receive", "address": "127.0.0.1", "port": 4243}
            campaign.write_json(config / "settings.json", settings)
            (config / "config").write_text(campaign.configuration(**settings))
            (config / "send.public").write_bytes(b"public")
            args = SimpleNamespace(
                config=config,
                role="receive",
                scenario="cold",
                run_id="fixture",
                deadline=1,
                control_only=False,
            )
            output = io.StringIO()
            with (
                patch.dict(
                    "sys.modules",
                    {
                        "RNS": rns,
                        "RNS.Interfaces.TCPInterface": SimpleNamespace(TCPClientInterface=tcp),
                    },
                ),
                patch.object(campaign.importlib.metadata, "version", return_value="1.5.5"),
                patch.object(campaign.time, "time", side_effect=lambda: 1000 + now[0]),
                patch.object(campaign.time, "monotonic", side_effect=lambda: now[0]),
                patch.object(campaign.queue, "Queue", Inbox),
                redirect_stdout(output),
            ):
                campaign.worker(args)
            received = next(
                json.loads(line)
                for line in output.getvalue().splitlines()
                if json.loads(line)["kind"] == "received"
            )
            self.assertAlmostEqual(received["received_wall"], 1000)
            self.assertAlmostEqual(received["accepted_wall"], 1000.32)
            self.assertAlmostEqual(
                received["accepted_elapsed"] - received["callback_elapsed"], 0.32
            )

    def test_additive_analysis_and_historical_hold(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runs = [
                {"run_id": str(i), "scenario": "cold", "window": 5, "control_only": False}
                for i in range(30)
            ]
            campaign.write_json(root / "manifest.json", {"runs": runs})
            for item in runs:
                for role, rows in self.fixture().items():
                    rows += [{"kind": "complete", "counters": {"tx": 0, "rx": 0}}]
                    (root / f"{item['run_id']}-{role}.jsonl").write_text(
                        "".join(
                            json.dumps({**r, "run_id": item["run_id"], "role": role}) + "\n"
                            for r in rows
                        )
                    )
                campaign.write_json(root / f"{item['run_id']}-exit.json", {"send": 0, "receive": 0})
            group = campaign.analyse(root, self.clock)["groups"]["cold/5/events"]
            self.assertEqual(group["contact_timing"]["criteria"]["T01"], "PASS")
            self.assertAlmostEqual(group["latency"]["p95"], 0.1)
            self.assertAlmostEqual(group["contact_timing"]["availability_latency"]["p95"], 1.5)
            for path in root.glob("*-receive.jsonl"):
                path.write_text(path.read_text().replace('"accepted_wall": 11.6, ', ""))
            group = campaign.analyse(root, self.clock)["groups"]["cold/5/events"]
            self.assertEqual(group["contact_timing"]["criteria"]["T01"], "HOLD")
            self.assertAlmostEqual(group["latency"]["p95"], 0.1)


if __name__ == "__main__":
    unittest.main()
