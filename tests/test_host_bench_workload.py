"""Verify the bench experiment contract without a twenty-minute test."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.host_bench_workload import RecordingTransport, Workload, main, run


class HostBenchTests(unittest.TestCase):
    def records(self, output):
        return [json.loads(line) for line in output.getvalue().splitlines()]

    def test_cycle_contract_and_repeat(self):
        output = io.StringIO()
        workload = Workload(output)
        run(workload, "check")
        records = {row["phase"]: row for row in self.records(output)}
        self.assertEqual(records["filled"]["occupancy"], 1024)
        self.assertEqual(records["filled"]["metrics"], {"received": 1024, "unauthenticated": 1024})
        self.assertEqual(
            records["burst"]["metrics"],
            {
                "received": 1024,
                "unauthenticated": 1024,
                "sent": 100,
                "capacity_dropped": 121,
                "invalid": 1,
                "expired": 1,
                "duplicate": 1,
                "id_conflict": 1,
                "rate_limited": 1,
            },
        )
        self.assertEqual(records["pruned"]["occupancy"], 0)
        self.assertEqual(records["recovered"]["occupancy"], 1)
        self.assertEqual(records["closed"]["occupancy"], 0)
        self.assertTrue(workload.transport.closed)
        self.assertIsNone(workload.transport.receiver)
        other = Workload(io.StringIO())
        try:
            other.run_cycle()
            other.run_cycle()
            self.assertEqual(other.vehicle.metrics["received"], 2050)
            self.assertEqual(other.transport.sent, 200)
            self.assertEqual(len(other.transport.latest), 38)
            self.assertEqual(len(other.vehicle.events), 0)
        finally:
            other.close()

    def test_bounded_transport(self):
        transport = RecordingTransport()
        for i in range(10000):
            transport.send(i.to_bytes(2, "big"))
        self.assertEqual(transport.sent, 10000)
        self.assertEqual(transport.latest, (9999).to_bytes(2, "big"))
        transport.close()
        self.assertIsNone(transport.latest)
        with self.assertRaises(RuntimeError):
            transport.send(b"x")

    def test_measure_orchestration(self):
        now = [0.0]
        output = io.StringIO()
        workload = Workload(output, lambda: now[0])
        original = workload.run_cycle

        def cycle():
            original()
            now[0] += 2

        def sleep(seconds):
            now[0] += seconds

        with patch.object(workload, "run_cycle", cycle):
            run(workload, "measure", sleep, duration=3)
        records = {row["phase"]: row for row in self.records(output)}
        self.assertEqual(records["idle_end"]["duration_seconds"], 3)
        self.assertEqual(records["active_start"]["monotonic_seconds"], 3)
        self.assertEqual(records["active_end"]["duration_seconds"], 4)
        self.assertEqual(records["active_end"]["completed_cycles"], 2)
        self.assertTrue(workload.transport.closed)

    def test_failure_and_interrupt_close(self):
        for error in (RuntimeError("injected"), KeyboardInterrupt()):
            output = io.StringIO()
            workload = Workload(output)
            with patch.object(workload, "run_cycle", side_effect=error):
                with self.assertRaises(type(error)):
                    run(workload, "check")
            self.assertEqual([r["phase"] for r in self.records(output)], ["failure", "closed"])
            self.assertTrue(workload.transport.closed)

    def test_cli_failure_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.jsonl"
            with patch(
                "tools.host_bench_workload.Workload.run_cycle", side_effect=RuntimeError("bad")
            ):
                self.assertEqual(main(["--output", str(path)]), 1)
            records = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(records[-2]["phase"], "failure")
            original = path.read_bytes()
            self.assertEqual(main(["--output", str(path)]), 1)
            self.assertEqual(path.read_bytes(), original)

    def test_metadata_failure_closes_and_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metadata-failure.jsonl"
            with patch(
                "tools.host_bench_workload.git_bytes", side_effect=RuntimeError("git failed")
            ):
                self.assertEqual(main(["--output", str(path)]), 1)
            records = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual([r["phase"] for r in records], ["failure", "closed"])
