"""Two-process SINGLE delivery with pinned sender signatures; loopback only."""

import argparse
import importlib.metadata
import ipaddress
import json
import os
import platform
import queue
import socket
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path

from wawet.protocol import RoadEvent, decode, encode


def enqueue(inbox, rejected, data):
    """Never block an RNS callback or exceed the fixed inbox capacity."""
    try:
        inbox.put_nowait(bytes(data))
    except queue.Full:
        rejected["capacity"] = rejected.get("capacity", 0) + 1


def worker(role, config, payload, churn=False, absent_discovery=False):
    import RNS

    stack = RNS.Reticulum(configdir=str(config))
    try:
        domain = b"wawet-auth-spike-v1\x00"
        identity = RNS.Identity(create_keys=False)
        identity.load_public_key((config.parent / "receiver.public").read_bytes())
        sender_identity = RNS.Identity(create_keys=False)
        sender_identity.load_public_key((config.parent / "sender.public").read_bytes())
        if role == "receive":
            identity = RNS.Identity.from_file(str(config / "identity.key"))
            finished = threading.Event()
            rejected = {"signature": 0, "expired": 0}
            destination = RNS.Destination(
                identity, RNS.Destination.IN, RNS.Destination.SINGLE, "wawet", "spike", "v1"
            )

            inbox = queue.Queue(maxsize=8)

            def received(data, packet):
                enqueue(inbox, rejected, data)

            destination.set_packet_callback(received)
            (config / "ready").write_text(destination.hash.hex())
            destination.announce()
            deadline = time.monotonic() + 20
            while not finished.is_set():
                if time.monotonic() >= deadline:
                    raise TimeoutError("No valid RNS packet received")
                try:
                    data = inbox.get(timeout=0.1)
                except queue.Empty:
                    continue
                signature, frame = data[:64], data[64:]
                if not sender_identity.validate(signature, domain + frame):
                    rejected["signature"] += 1
                    continue
                event = decode(frame)
                if event.expired(int(time.time())):
                    rejected["expired"] += 1
                    continue
                print(
                    json.dumps(
                        {
                            "hex": frame.hex(),
                            "event_id": event.event_id.hex(),
                            "received_at": time.time(),
                            "rejected": rejected,
                            "category": event.category,
                        }
                    ),
                    flush=True,
                )
                finished.set()
        else:
            if absent_discovery:
                identity = RNS.Identity()
            destination = RNS.Destination(
                identity, RNS.Destination.OUT, RNS.Destination.SINGLE, "wawet", "spike", "v1"
            )
            if not any(interface.online for interface in RNS.Transport.interfaces):
                raise RuntimeError("No online RNS interface")
            sender_identity = RNS.Identity.from_file(str(config / "identity.key"))
            started = time.monotonic()
            while not RNS.Transport.has_path(destination.hash):
                if time.monotonic() - started > 8:
                    raise TimeoutError("Discovery deadline exceeded")
                RNS.Transport.request_path(destination.hash)
                time.sleep(0.25)
            discovery_seconds = time.monotonic() - started
            frame = bytes.fromhex(payload)
            if decode(frame).expired(int(time.time())):
                raise TimeoutError("Queued event expired before send")
            signature = sender_identity.sign(domain + frame)
            # Adversarial probes precede the valid event on the same TCP contact.
            stranger = RNS.Identity()
            RNS.Packet(destination, stranger.sign(domain + frame) + frame).send()
            RNS.Packet(destination, signature + frame[:-1] + bytes([frame[-1] ^ 1])).send()
            stale = RoadEvent(bytes(range(1, 17)), 1, 5220000, 90000, 0, 1, 1)
            stale_frame = encode(stale)
            RNS.Packet(destination, sender_identity.sign(domain + stale_frame) + stale_frame).send()
            time.sleep(0.2)
            reconnect_seconds = None
            expired_before_send = 0
            injected_loss_bytes = []
            if churn:
                client = next(i for i in RNS.Transport.interfaces if getattr(i, "initiator", False))
                original_outgoing = client.process_outgoing
                try:
                    client.process_outgoing = lambda data: injected_loss_bytes.append(len(data))
                    RNS.Packet(destination, signature + frame).send()
                finally:
                    client.process_outgoing = original_outgoing
                queued = RoadEvent(bytes(range(1, 17)), 1, 5220000, 90000, 0, int(time.time()), 1)
                outage_start = time.monotonic()
                old_socket = client.socket
                old_socket.shutdown(socket.SHUT_RDWR)
                while client.socket is old_socket or not client.online:
                    if time.monotonic() - outage_start > 9:
                        raise TimeoutError("Reconnect deadline exceeded")
                    time.sleep(0.05)
                reconnect_seconds = time.monotonic() - outage_start
                if queued.expired(int(time.time())):
                    expired_before_send += 1
                else:
                    raise RuntimeError(
                        "Short-lived queued event did not expire during contact loss"
                    )
            if decode(frame).expired(int(time.time())):
                raise TimeoutError("Live event expired during contact loss")
            packet = RNS.Packet(destination, signature + frame)
            sent_at = time.time()
            packet.send()
            print(
                json.dumps(
                    {
                        "sent_at": sent_at,
                        "discovery_seconds": discovery_seconds,
                        "rns_packet_bytes": len(packet.raw),
                        "reconnect_seconds": reconnect_seconds,
                        "expired_before_send": expired_before_send,
                        "injected_interface_loss_bytes": injected_loss_bytes,
                        "interface_tx_bytes": sum(i.txb for i in RNS.Transport.interfaces),
                        "interface_rx_bytes": sum(i.rxb for i in RNS.Transport.interfaces),
                    }
                ),
                flush=True,
            )
            time.sleep(0.5)
    except Exception as error:
        print(json.dumps({"error": str(error), "type": type(error).__name__}), flush=True)
        raise
    finally:
        stack.exit_handler()


def prepare(root, peer_ip, port):
    import RNS

    for role in ["receive", "send"]:
        config = root / role
        config.mkdir()
        key = RNS.Identity()
        key.to_file(str(config / "identity.key"))
        (config / "identity.key").chmod(0o600)
        (root / ("receiver.public" if role == "receive" else "sender.public")).write_bytes(
            key.get_public_key()
        )
        interface = (
            f"type = TCPServerInterface\nlisten_ip = {peer_ip}\nlisten_port = {port}"
            if role == "receive"
            else f"type = TCPClientInterface\ntarget_host = {peer_ip}\ntarget_port = {port}"
        )
        (config / "config").write_text(
            "[reticulum]\nshare_instance = No\nenable_transport = No\n"
            "[logging]\nloglevel = 1\n[interfaces]\n[[Loopback experiment]]\n"
            "enabled = Yes\n" + interface + "\n"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prepare", type=Path, help="Create private-IP worker bundles; never starts networking"
    )
    parser.add_argument("--peer-ip", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4243)
    parser.add_argument("--churn", action="store_true")
    parser.add_argument("--absent-discovery", action="store_true")
    parser.add_argument("--worker", choices=["receive", "send"])
    parser.add_argument("--config", type=Path)
    parser.add_argument("--payload")
    args = parser.parse_args()
    try:
        version = importlib.metadata.version("rns")
    except importlib.metadata.PackageNotFoundError:
        raise SystemExit(
            "Install the optional spike environment: pip install -r tools/rns-requirements.txt"
        ) from None
    if version != "1.5.5":
        raise SystemExit(f"This experiment pins RNS 1.5.5, found {version}")
    if args.worker:
        if args.config is None or (args.worker == "send" and args.payload is None):
            parser.error("Workers require --config; send also requires --payload")
        worker(args.worker, args.config, args.payload, args.churn, args.absent_discovery)
        return
    if args.prepare:
        address = ipaddress.ip_address(args.peer_ip)
        if not address.is_private or address.is_unspecified or address.is_multicast:
            parser.error("Use an explicit private or loopback peer address")
        if not 1024 <= args.port <= 65535:
            parser.error("Port must be in [1024, 65535]")
        args.prepare.mkdir(parents=True, mode=0o700, exist_ok=False)
        prepare(args.prepare, str(address), args.port)
        print("Created bundles; transfer the matching role directory and both public files")
        return
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    event = RoadEvent(bytes(range(1, 17)), 1, 5220000, 90000, 0, int(time.time()))
    payload = encode(event).hex()
    with tempfile.TemporaryDirectory(prefix="wawet-rns-") as directory:
        root = Path(directory)
        prepare(root, "127.0.0.1", port)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "packages")
        command = [sys.executable, str(Path(__file__).resolve())]
        if args.churn:
            command.append("--churn")
        if args.absent_discovery:
            command.append("--absent-discovery")
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
                timeout=22,
            )
            if args.absent_discovery:
                if (
                    sender.returncode == 0
                    or "Discovery deadline exceeded" not in sender.stdout + sender.stderr
                ):
                    raise RuntimeError(
                        "Absent discovery did not fail with the expected timeout: "
                        + sender.stdout
                        + sender.stderr
                    )
                print(
                    json.dumps(
                        {
                            "run_id": str(uuid.uuid4()),
                            "rns_version": version,
                            "recorded_at": time.time(),
                            "scenario": "absent discovery",
                            "expected_timeout": True,
                            "sender_stdout": sender.stdout,
                            "sender_stderr": sender.stderr,
                        },
                        indent=2,
                    )
                )
                return
            if sender.returncode:
                raise RuntimeError(sender.stdout + sender.stderr)
            stdout, stderr = receiver.communicate(timeout=22)
            if receiver.returncode:
                raise RuntimeError(stdout + stderr)
            results = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
            if len(results) != 1 or results[0]["hex"] != payload:
                raise RuntimeError(f"Unexpected receiver output: {stdout}")
            if results[0]["rejected"] != {"signature": 2, "expired": 1}:
                raise RuntimeError("Adversarial probes did not produce expected rejection counts")
            print(
                json.dumps(
                    {
                        "run_id": str(uuid.uuid4()),
                        "recorded_at": time.time(),
                        "platform": platform.platform(),
                        "python": platform.python_version(),
                        "sender": json.loads(sender.stdout.strip().splitlines()[-1]),
                        "receiver": results[0],
                        "rns_version": version,
                        "medium": "TCP loopback",
                        "processes": 2,
                        "payload_bytes": len(bytes.fromhex(payload)),
                        "payload_match": True,
                        "authenticated": True,
                        "authentication": "domain-separated Ed25519 signature; pinned sender",
                        "signed_application_bytes": 102,
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
