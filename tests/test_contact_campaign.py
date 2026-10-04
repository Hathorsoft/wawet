"""Offline regression coverage for the optional contact experiment."""

import importlib.util
import json
import queue
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
