"""Default checks exercise callback bounds without importing optional RNS."""

import importlib.util
import queue
import unittest
from pathlib import Path


class SpikeQueueTests(unittest.TestCase):
    def test_overload_preserves_pending_frames_and_recovers_after_drain(self):
        path = Path(__file__).resolve().parents[1] / "tools" / "rns_authenticated_spike.py"
        spec = importlib.util.spec_from_file_location("authenticated_spike", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        inbox = queue.Queue(maxsize=8)
        rejected = {}
        for index in range(10):
            module.enqueue(inbox, rejected, bytes([index]))
        self.assertEqual(inbox.qsize(), 8)
        self.assertEqual(rejected, {"capacity": 2})
        self.assertEqual([inbox.get_nowait() for _ in range(8)], [bytes([i]) for i in range(8)])
        module.enqueue(inbox, rejected, b"fresh")
        self.assertEqual(inbox.get_nowait(), b"fresh")
