"""Two-process RNS 1.5.5 direct delivery experiment on loopback only."""

import argparse
import importlib.metadata
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from wawet.protocol import RoadEvent, decode, encode


def worker(role, config, payload):
    import RNS

    stack = RNS.Reticulum(configdir=str(config))
    if role == "receive":
        finished = threading.Event()
        destination = RNS.Destination(
            None, RNS.Destination.IN, RNS.Destination.PLAIN, "wawet", "spike", "v1"
        )

        def received(data, packet):
            event = decode(data)
            print(
                json.dumps(
                    {
                        "hex": data.hex(),
                        "event_id": event.event_id.hex(),
                        "category": event.category,
                    }
                ),
                flush=True,
            )
            finished.set()

        destination.set_packet_callback(received)
        (config / "ready").write_text("ready")
        if not finished.wait(12):
            raise TimeoutError("No RNS packet received")
    else:
        destination = RNS.Destination(
            None, RNS.Destination.OUT, RNS.Destination.PLAIN, "wawet", "spike", "v1"
        )
        if not any(interface.online for interface in RNS.Transport.interfaces):
            raise RuntimeError("No online RNS interface")
        RNS.Packet(destination, bytes.fromhex(payload)).send()
        time.sleep(0.5)
    stack.exit_handler()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", choices=["receive", "send"])
    parser.add_argument("--config", type=Path)
    parser.add_argument("--payload")
    args = parser.parse_args()
    if args.worker:
        worker(args.worker, args.config, args.payload)
        return
    try:
        version = importlib.metadata.version("rns")
    except importlib.metadata.PackageNotFoundError:
        raise SystemExit(
            "Install the optional spike environment: pip install -r tools/rns-requirements.txt"
        ) from None
    if version != "1.5.5":
        raise SystemExit(f"This experiment pins RNS 1.5.5, found {version}")
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    event = RoadEvent(bytes(range(1, 17)), 1, 5220000, 90000, 0, int(time.time()))
    payload = encode(event).hex()
    with tempfile.TemporaryDirectory(prefix="wawet-rns-") as directory:
        root = Path(directory)
        for role in ["receive", "send"]:
            config = root / role
            config.mkdir()
            interface = (
                f"type = TCPServerInterface\nlisten_ip = 127.0.0.1\nlisten_port = {port}"
                if role == "receive"
                else f"type = TCPClientInterface\ntarget_host = 127.0.0.1\ntarget_port = {port}"
            )
            (config / "config").write_text(
                "[reticulum]\nshare_instance = No\nenable_transport = No\n"
                "[logging]\nloglevel = 1\n[interfaces]\n[[Loopback experiment]]\n"
                "enabled = Yes\n" + interface + "\n"
            )
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "packages")
        command = [sys.executable, str(Path(__file__).resolve())]
        receiver = subprocess.Popen(
            command + ["--worker", "receive", "--config", str(root / "receive")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        try:
            deadline = time.monotonic() + 10
            while not (root / "receive" / "ready").exists():
                if receiver.poll() is not None or time.monotonic() > deadline:
                    raise RuntimeError("Receiver failed to start")
                time.sleep(0.05)
            sender = subprocess.run(
                command
                + ["--worker", "send", "--config", str(root / "send"), "--payload", payload],
                capture_output=True,
                text=True,
                env=env,
                timeout=15,
            )
            if sender.returncode:
                raise RuntimeError(sender.stdout + sender.stderr)
            stdout, stderr = receiver.communicate(timeout=15)
            if receiver.returncode:
                raise RuntimeError(stdout + stderr)
            results = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
            if len(results) != 1 or results[0]["hex"] != payload:
                raise RuntimeError(f"Unexpected receiver output: {stdout}")
            print(
                json.dumps(
                    {
                        "rns_version": version,
                        "medium": "TCP loopback",
                        "processes": 2,
                        "payload_bytes": len(bytes.fromhex(payload)),
                        "payload_match": True,
                        "authenticated": False,
                        "routed": False,
                        "event_id": event.event_id.hex(),
                    },
                    indent=2,
                )
            )
        finally:
            if receiver.poll() is None:
                receiver.terminate()
                try:
                    receiver.communicate(timeout=3)
                except subprocess.TimeoutExpired:
                    receiver.kill()
                    receiver.communicate()


if __name__ == "__main__":
    main()
