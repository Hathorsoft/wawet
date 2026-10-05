"""Bounded synthetic host workload; never establishes physical feasibility."""

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import TextIO

from wawet.geo import Position
from wawet.protocol import ProtocolError, RoadEvent, decode, encode
from wawet.transport import Delivery, Receiver
from wawet.vehicle import Identity, Vehicle

ROOT = Path(__file__).resolve().parents[1]


class RecordingTransport:
    def __init__(self) -> None:
        self.receiver: Receiver | None = None
        self.sent = 0
        self.latest: bytes | None = None
        self.closed = False

    def subscribe(self, receiver: Receiver) -> None:
        self.receiver = receiver

    def send(self, payload: bytes) -> None:
        if self.closed:
            raise RuntimeError("closed transport")
        self.sent += 1
        self.latest = payload

    def close(self) -> None:
        self.closed = True
        self.receiver = None
        self.latest = None


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class Workload:
    def __init__(self, output: TextIO, monotonic: Callable[[], float] = time.monotonic) -> None:
        self.output, self.monotonic = output, monotonic
        self.now = 1_800_000_000
        self.identifier = 0
        self.transport = RecordingTransport()
        self.vehicle = Vehicle(
            Identity(b"\x01" * 16), Position(0, 0, 0), self.transport, lambda: self.now
        )
        self.cycle = 0
        self.operations = {"alerts": 0, "encode": 0, "decode": 0, "report": 0, "receive": 0}

    def emit(self, phase: str, **extra: object) -> None:
        record = {
            "phase": phase,
            "cycle": self.cycle,
            "utc": datetime.now(UTC).isoformat(),
            "monotonic_seconds": self.monotonic(),
            "synthetic_time": self.now,
            "occupancy": len(self.vehicle.events),
            "metrics": dict(self.vehicle.metrics),
            "operations": dict(self.operations),
            "sent": self.transport.sent,
            **extra,
        }
        self.output.write(json.dumps(record, sort_keys=True) + "\n")
        self.output.flush()

    def next_id(self) -> bytes:
        self.identifier += 1
        return self.identifier.to_bytes(16, "big")

    def event(self) -> RoadEvent:
        return RoadEvent(self.next_id(), 1, 0, 0, 0, self.now, 3600, 5000)

    def receive(self, payload: bytes) -> None:
        self.vehicle.receive(payload, Delivery(self.now, "synthetic", False))
        self.operations["receive"] += 1

    def hold(self, iterations: int = 100) -> None:
        for _ in range(iterations):
            self.vehicle.alerts()
            event = self.event()
            require(decode(encode(event)) == event, "codec round trip")
            self.vehicle.report(ttl=3600, event_id=self.next_id())
            for name in ("alerts", "encode", "decode", "report"):
                self.operations[name] += 1
        require(len(self.vehicle.events) == 1024, "hold occupancy")

    def run_cycle(self) -> None:
        self.cycle += 1
        start = self.monotonic()
        baseline = self.vehicle.metrics.copy()
        self.emit("cycle_start")
        for size in [120] * 8 + [64]:
            self.now += 60
            for _ in range(size):
                self.receive(encode(self.event()))
        require(len(self.vehicle.events) == 1024, "fill occupancy")
        require(
            self.vehicle.metrics - baseline == {"received": 1024, "unauthenticated": 1024},
            "fill counters",
        )
        self.emit("filled")
        self.hold()
        self.emit("held")
        self.now += 60
        before = self.vehicle.metrics.copy()
        self.receive(encode(self.event()))
        self.receive(b"truncated")
        self.receive(encode(replace(self.event(), created_at=self.now - 3600)))
        retained = next(iter(self.vehicle.events.values()))[0]
        self.receive(encode(retained))
        self.receive(encode(replace(retained, category=2)))
        try:
            decode(b"truncated")
        except ProtocolError:
            pass
        else:
            raise RuntimeError("malformed decode accepted")
        require(
            self.vehicle.metrics - before
            == {
                "capacity_dropped": 1,
                "invalid": 1,
                "expired": 1,
                "duplicate": 1,
                "id_conflict": 1,
            },
            "probe counters",
        )
        self.emit("probes")
        self.now += 60
        before = self.vehicle.metrics.copy()
        for _ in range(121):
            self.receive(encode(self.event()))
        require(
            self.vehicle.metrics - before == {"capacity_dropped": 120, "rate_limited": 1},
            "burst counters",
        )
        require(len(self.vehicle.events) == 1024, "burst occupancy")
        self.emit("burst")
        self.now += 3601
        self.vehicle.alerts()
        self.operations["alerts"] += 1
        require(not self.vehicle.events, "expiry pruning")
        self.emit("pruned")
        self.receive(encode(self.event()))
        require(len(self.vehicle.events) == 1, "recovery occupancy")
        self.emit("recovered")
        self.now += 3601
        self.vehicle.alerts()
        self.operations["alerts"] += 1
        require(not self.vehicle.events, "recovery pruning")
        self.emit("cycle_end", duration_seconds=self.monotonic() - start)

    def close(self) -> None:
        self.vehicle.close()
        require(not self.vehicle.events and self.transport.closed, "shutdown")
        self.emit("closed")


def run(
    workload: Workload,
    mode: str,
    sleep: Callable[[float], None] = time.sleep,
    duration: float = 600,
) -> None:
    try:
        if mode == "measure":
            start = workload.monotonic()
            workload.emit("idle_start")
            while workload.monotonic() - start < duration:
                sleep(min(1, max(0, duration - (workload.monotonic() - start))))
            workload.emit("idle_end", duration_seconds=workload.monotonic() - start)
            start = workload.monotonic()
            workload.emit("active_start")
            while workload.monotonic() - start < duration:
                workload.run_cycle()
            workload.emit(
                "active_end",
                duration_seconds=workload.monotonic() - start,
                completed_cycles=workload.cycle,
            )
        else:
            workload.run_cycle()
        workload.emit("complete", physical_acceptance="HOLD")
    except BaseException as error:
        workload.emit("failure", error=f"{type(error).__name__}: {error}")
        raise
    finally:
        workload.close()


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["check", "measure"], default="check")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        with args.output.open("x", encoding="utf-8") as output:
            workload = Workload(output)
            try:
                workload.emit(
                    "metadata",
                    mode=args.mode,
                    python=sys.version,
                    platform=platform.platform(),
                    revision=git_bytes("rev-parse", "HEAD").decode().strip(),
                    status=git_bytes("status", "--short").decode(),
                    diff_sha256=hashlib.sha256(git_bytes("diff", "HEAD", "--binary")).hexdigest(),
                    driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    configuration={
                        "capacity": 1024,
                        "receive_limit": 120,
                        "idle_seconds": 600,
                        "active_seconds": 600,
                        "hold_iterations": 100,
                    },
                    limitations="Synthetic unauthenticated workload; no physical gate acceptance",
                )
                run(workload, args.mode)
            except BaseException as error:
                if not workload.transport.closed:
                    workload.emit("failure", error=f"{type(error).__name__}: {error}")
                raise
            finally:
                if not workload.transport.closed:
                    workload.close()

    except (Exception, KeyboardInterrupt) as error:
        print(f"host workload failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
