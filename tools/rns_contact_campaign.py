"""Isolated RNS 1.5.5 contact characterisation; never a production adapter."""

import argparse
import concurrent.futures
import hashlib
import importlib.metadata
import ipaddress
import json
import math
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

DOMAIN = b"wawet-auth-spike-v1\x00"
NETWORKS = tuple(
    map(ipaddress.ip_network, ("127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))
)


def private_address(value):
    address = ipaddress.ip_address(value)
    if address.version != 4 or not any(address in network for network in NETWORKS):
        raise ValueError("Use explicit loopback or RFC1918 IPv4")
    return str(address)


def fresh_frame(ttl=60):
    return encode(RoadEvent(uuid.uuid4().bytes, 1, 5220000, 90000, 0, int(time.time()), ttl))


def sendable(frame, now):
    return not decode(frame).expired(int(now))


def validate_body(data, validate, now):
    if len(data) < 64 or not validate(data[:64], DOMAIN + data[64:]):
        return "signature", None
    try:
        event = decode(data[64:])
    except ValueError:
        return "malformed", None
    if event.expired(int(now)):
        return "expired", None
    return "valid", event


def enqueue(inbox, data):
    try:
        inbox.put_nowait((bytes(data), time.time(), time.monotonic()))
        return True
    except queue.Full:
        return False


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def provision(config, role, address, port, announce_pin=True):
    import RNS

    private_address(address)
    if not 1024 <= port <= 65535:
        raise ValueError("Port must be in [1024, 65535]")
    config.mkdir(parents=True, mode=0o700, exist_ok=False)
    identity = RNS.Identity()
    identity.to_file(str(config / "identity.key"))
    (config / "identity.key").chmod(0o600)
    (config / f"{role}.public").write_bytes(identity.get_public_key())
    if announce_pin:
        print(
            json.dumps(
                {"role": role, "pin_sha256": hashlib.sha256(identity.get_public_key()).hexdigest()}
            ),
            flush=True,
        )
    settings = {"role": role, "address": address, "port": port}
    write_json(config / "settings.json", settings)
    (config / "config").write_text(configuration(**settings))


def configuration(role, address, port):
    private_address(address)
    if role not in ("send", "receive") or not 1024 <= port <= 65535:
        raise ValueError("Invalid experiment role or port")
    interface = (
        f"type = TCPServerInterface\nlisten_ip = {address}\nlisten_port = {port}"
        if role == "receive"
        else f"type = TCPClientInterface\ntarget_host = {address}\ntarget_port = {port}"
    )
    return (
        "[reticulum]\nshare_instance = No\nenable_transport = No\n"
        "[logging]\nloglevel = 0\n[interfaces]\n[[Private contact experiment]]\n"
        "enabled = Yes\n" + interface + "\n"
    )


def wait_until(target, deadline, clock=time.monotonic, sleep=time.sleep):
    """Wait on one process's monotonic clock without extending the run deadline."""
    while True:
        now = clock()
        if now >= deadline:
            raise TimeoutError("Run deadline exceeded")
        if now >= target:
            return
        sleep(min(0.02, target - now, deadline - now))


def worker(args):
    import RNS
    from RNS.Interfaces.TCPInterface import TCPClientInterface

    if importlib.metadata.version("rns") != "1.5.5":
        raise ValueError("Experiment requires pinned RNS 1.5.5")
    settings = json.loads((args.config / "settings.json").read_text())
    if settings["role"] != args.role or (args.config / "config").read_text() != configuration(
        **settings
    ):
        raise ValueError("Configuration must match the isolated generated interface")
    own = RNS.Identity.from_file(str(args.config / "identity.key"))
    peer = RNS.Identity(create_keys=False)
    peer_role = "send" if args.role == "receive" else "receive"
    peer.load_public_key((args.config / f"{peer_role}.public").read_bytes())
    start = time.monotonic()
    stack = None
    gate = [args.role == "receive"]
    outgoing = TCPClientInterface.process_outgoing
    incoming = TCPClientInterface.process_incoming
    # Disable both directions at the actual RNS TCP-interface boundary. The TCP
    # socket stays connected; this is controlled interface contact, not RF loss.
    TCPClientInterface.process_outgoing = lambda interface, data: (
        outgoing(interface, data) if gate[0] else None
    )
    TCPClientInterface.process_incoming = lambda interface, data: (
        incoming(interface, data) if gate[0] else None
    )

    def emit(kind, **fields):
        print(
            json.dumps(
                {
                    "run_id": args.run_id,
                    "scenario": args.scenario,
                    "role": args.role,
                    "kind": kind,
                    "wall": time.time(),
                    "elapsed": time.monotonic() - start,
                    **fields,
                }
            ),
            flush=True,
        )

    def counters():
        # Server counters include spawned children: count only root interfaces.
        roots = [
            i for i in RNS.Transport.interfaces if getattr(i, "parent_interface", None) is None
        ]
        return {"tx": sum(i.txb for i in roots), "rx": sum(i.rxb for i in roots)}

    def contact(enabled):
        gate[0] = enabled
        emit(
            "contact",
            enabled=enabled,
            socket_online=any(i.online for i in RNS.Transport.interfaces),
            counters=counters(),
        )

    try:
        stack = RNS.Reticulum(configdir=str(args.config))
        emit(
            "start",
            python=platform.python_version(),
            platform=platform.platform(),
            rns="1.5.5",
            peer_pin_sha256=hashlib.sha256(peer.get_public_key()).hexdigest(),
            medium="controlled TCP interface",
            deadline=args.deadline,
            control_only=args.control_only,
            counters=counters(),
        )
        deadline = time.monotonic() + args.deadline

        def pause(seconds):
            wait_until(time.monotonic() + seconds, deadline)

        if args.role == "receive":
            destination = RNS.Destination(
                own, RNS.Destination.IN, RNS.Destination.SINGLE, "wawet", "spike", "v1"
            )
            inbox = queue.Queue(maxsize=8)
            overflow = [0]
            overflow_lock = threading.Lock()

            def received(data, packet):
                if not enqueue(inbox, data):
                    # Callback communicates counts only; no parsing or output.
                    with overflow_lock:
                        overflow[0] += 1

            destination.set_packet_callback(received)
            (args.config / "ready").write_text(destination.hash.hex())
            rejected = dict.fromkeys(("signature", "malformed", "expired", "capacity"), 0)
            pause_until = None
            accepted = 0
            while time.monotonic() < deadline and not (args.config / "stop").exists():
                with overflow_lock:
                    rejected["capacity"] += overflow[0]
                    overflow[0] = 0
                if pause_until is not None and time.monotonic() < pause_until:
                    time.sleep(0.01)
                    continue
                try:
                    data, wall, monotonic = inbox.get(timeout=0.02)
                except queue.Empty:
                    continue
                # Signed control marker coordinates deterministic overload drain pause.
                if (
                    args.scenario == "overload"
                    and data[64:] == b"pause"
                    and peer.validate(data[:64], DOMAIN + b"pause")
                ):
                    pause_until = time.monotonic() + 1
                    emit("drain_pause", seconds=1)
                    continue
                outcome, event = validate_body(data, peer.validate, time.time())
                if event is None:
                    rejected[outcome] += 1
                    emit("rejected", reason=outcome)
                else:
                    accepted += 1
                    emit(
                        "received",
                        event_id=event.event_id.hex(),
                        received_wall=wall,
                        callback_elapsed=monotonic - start,
                        frame_sha256=hashlib.sha256(data[64:]).hexdigest(),
                    )
            emit("complete", accepted=accepted, rejected=rejected, counters=counters())
        else:
            destination = RNS.Destination(
                peer, RNS.Destination.OUT, RNS.Destination.SINGLE, "wawet", "spike", "v1"
            )
            if args.scenario == "absent":
                destination = RNS.Destination(
                    RNS.Identity(),
                    RNS.Destination.OUT,
                    RNS.Destination.SINGLE,
                    "wawet",
                    "spike",
                    "v1",
                )

            def discover(limit, phase="contact"):
                began = time.monotonic()
                while not RNS.Transport.has_path(destination.hash):
                    if time.monotonic() >= min(limit, deadline):
                        emit(
                            "discovery",
                            outcome="timeout",
                            phase=phase,
                            seconds=time.monotonic() - began,
                        )
                        return False
                    RNS.Transport.request_path(destination.hash)
                    time.sleep(0.05)
                emit("discovery", outcome="found", phase=phase, seconds=time.monotonic() - began)
                return True

            def transmit(frame, attempt="initial", body=None):
                event = decode(frame)
                fields = {
                    "event_id": event.event_id.hex(),
                    "attempt": attempt,
                    "frame_sha256": hashlib.sha256(frame).hexdigest(),
                }
                if not sendable(frame, time.time()):
                    emit("event", outcome="expired_before_send", **fields)
                    return
                if not gate[0] or not RNS.Transport.has_path(destination.hash):
                    emit("event", outcome="unavailable", **fields)
                    return
                packet = RNS.Packet(destination, body or (own.sign(DOMAIN + frame) + frame))
                sent_wall = time.time()
                receipt = packet.send()
                emit(
                    "event",
                    outcome="sent" if receipt is not None else "send_failed",
                    sent_wall=sent_wall,
                    packed_bytes=len(packet.raw),
                    signed_bytes=102,
                    **fields,
                )

            if args.scenario == "warm":
                contact(True)
                if not discover(time.monotonic() + 8, "warmup"):
                    raise TimeoutError("Warm-up discovery failed")
                contact(False)
                pause(1)
            contact(True)
            window_start = time.monotonic()
            window_end = min(window_start + args.window, deadline)
            found = discover(window_end)
            if args.scenario in ("cold", "warm", "absent"):
                if not args.control_only:
                    # A missed discovery is still an intended event in the denominator.
                    transmit(fresh_frame())
                while time.monotonic() < window_end:
                    time.sleep(max(0, min(0.02, window_end - time.monotonic())))
                contact(False)
            elif args.scenario == "stable":
                if not found:
                    raise TimeoutError("Baseline discovery failed")
                for index in range(args.count):
                    target = window_start + index * args.interval
                    wait_until(target, deadline)
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Baseline deadline exceeded")
                    if not args.control_only:
                        transmit(fresh_frame())
                contact(False)
            elif args.scenario == "outage":
                if not found:
                    raise TimeoutError("Outage setup discovery failed")
                live, stale = fresh_frame(), fresh_frame(1)
                contact(False)
                if not args.control_only:
                    transmit(live)
                    transmit(stale)
                client = next(i for i in RNS.Transport.interfaces if getattr(i, "initiator", False))
                old_socket = client.socket
                old_socket.shutdown(socket.SHUT_RDWR)
                began = time.monotonic()
                pause(5)
                contact(True)
                while client.socket is old_socket or not client.online:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Reconnection deadline exceeded")
                    time.sleep(0.05)
                emit("reconnection", seconds=time.monotonic() - began)
                if not args.control_only:
                    transmit(stale, "explicit_resend")
                    transmit(live, "explicit_resend")
                pause(0.3)
                contact(False)
            elif args.scenario in ("adversarial", "overload"):
                if not found:
                    raise TimeoutError("Probe discovery failed")
                if not args.control_only:
                    if args.scenario == "adversarial":
                        frame = fresh_frame()
                        bodies = [
                            RNS.Identity().sign(DOMAIN + frame) + frame,
                            own.sign(DOMAIN + frame) + frame[:-1] + bytes([frame[-1] ^ 1]),
                            own.sign(DOMAIN + b"bad") + b"bad",
                        ]
                        stale = encode(RoadEvent(uuid.uuid4().bytes, 1, 5220000, 90000, 0, 1, 1))
                        bodies.append(own.sign(DOMAIN + stale) + stale)
                        for body in bodies:
                            RNS.Packet(destination, body).send()
                            emit("probe", body_bytes=len(body))
                    else:
                        RNS.Packet(destination, own.sign(DOMAIN + b"pause") + b"pause").send()
                        pause(0.2)
                        for _ in range(32):
                            transmit(fresh_frame(), "burst")
                        pause(1.2)
                    transmit(fresh_frame(), "recovery")
                elif args.scenario == "overload":
                    pause(1.4)
                pause(0.5)
                contact(False)
            emit("complete", counters=counters())
    except Exception as error:
        emit("error", error=str(error), error_type=type(error).__name__)
        raise
    finally:
        if stack is not None:
            stack.exit_handler()


def scenarios(repetitions):
    result = [
        ("stable", 35, 0),
        ("outage", 12, 0),
        ("absent", 2, 0),
        ("adversarial", 3, 0),
        ("overload", 3, 0),
    ]
    result += [
        (name, window, trial)
        for name in ("cold", "warm")
        for window in (1, 2, 5, 10)
        for trial in range(repetitions)
    ]
    return [
        {
            "run_id": str(uuid.uuid4()),
            "scenario": name,
            "window": window,
            "trial": trial,
            "control_only": control,
        }
        for name, window, trial in result
        for control in (False, True)
    ]


def local_trial(item, output):
    try:
        return run_local_trial(item, output)
    except Exception as error:
        codes = {"harness_error": str(error)}
        write_json(output / f"{item['run_id']}-exit.json", codes)
        return item["run_id"], codes


def run_local_trial(item, output):
    with tempfile.TemporaryDirectory(prefix="wawet-contact-") as temporary:
        root = Path(temporary)
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        for role in ("receive", "send"):
            provision(root / role, role, "127.0.0.1", port, announce_pin=False)
        for role, peer_role in (("receive", "send"), ("send", "receive")):
            (root / role / f"{peer_role}.public").write_bytes(
                (root / peer_role / f"{peer_role}.public").read_bytes()
            )
        # Receiver lasts through warmup/outage and one second after sender exits.
        lifetime = item["window"] + (12 if item["scenario"] == "warm" else 3)
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "worker",
            "--run-id",
            item["run_id"],
            "--scenario",
            item["scenario"],
            "--window",
            str(item["window"]),
            "--deadline",
            str(lifetime),
        ]
        if item["control_only"]:
            command.append("--control-only")
        paths = {role: output / f"{item['run_id']}-{role}.jsonl" for role in ("receive", "send")}
        codes = {}
        with paths["receive"].open("w") as receive_log, paths["send"].open("w") as send_log:
            with (output / f"{item['run_id']}-receive.stderr").open("w") as receive_error:
                receiver = subprocess.Popen(
                    command + ["--role", "receive", "--config", str(root / "receive")],
                    stdout=receive_log,
                    stderr=receive_error,
                )
                try:
                    ready_deadline = time.monotonic() + 10
                    while not (root / "receive" / "ready").exists():
                        if receiver.poll() is not None or time.monotonic() >= ready_deadline:
                            raise TimeoutError("Receiver readiness deadline exceeded")
                        time.sleep(0.02)
                    with (output / f"{item['run_id']}-send.stderr").open("w") as send_error:
                        sender = subprocess.run(
                            command + ["--role", "send", "--config", str(root / "send")],
                            stdout=send_log,
                            stderr=send_error,
                            timeout=lifetime + 10,
                        )
                        codes["send"] = sender.returncode
                    time.sleep(0.5)
                    (root / "receive" / "stop").touch()
                    # Allow callbacks to drain then request bounded receiver completion.
                    # Receiver has its own deadline; preserve its final counters.
                    codes["receive"] = receiver.wait(timeout=lifetime + 10)
                except Exception as error:
                    codes["harness_error"] = str(error)
                finally:
                    if receiver.poll() is None:
                        receiver.terminate()
                        try:
                            receiver.wait(timeout=3)
                        except subprocess.TimeoutExpired:
                            receiver.kill()
                            receiver.wait()
                    codes.setdefault("receive", receiver.returncode)
        write_json(output / f"{item['run_id']}-exit.json", codes)
    return item["run_id"], codes


def batch(args):
    """Run one role on its own host; provisioning never crosses host boundaries."""
    manifest = json.loads(args.manifest.read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    write_json(args.output / "manifest.json", manifest)
    for item in manifest["runs"]:
        target = item["scheduled_at"] - (2 if args.role == "receive" else 0)
        if time.time() > target + 0.5:
            write_json(
                args.output / f"{item['run_id']}-{args.role}-exit.json",
                {"exit": 1, "error": "Missed scheduled start; not silently rescheduled"},
            )
            continue
        while time.time() < target:
            time.sleep(min(0.1, target - time.time()))
        with tempfile.TemporaryDirectory(prefix="wawet-host-trial-") as temporary:
            config = Path(temporary)
            # Copy only keys/pins and checked config, never path/discovery state.
            for name in (
                "identity.key",
                "send.public",
                "receive.public",
                "config",
                "settings.json",
            ):
                (config / name).write_bytes((args.config / name).read_bytes())
            (config / "identity.key").chmod(0o600)
            lifetime = item["window"] + 12
            command = [
                sys.executable,
                str(Path(__file__).resolve()),
                "worker",
                "--role",
                args.role,
                "--config",
                str(config),
                "--run-id",
                item["run_id"],
                "--scenario",
                item["scenario"],
                "--window",
                str(item["window"]),
                "--deadline",
                str(lifetime),
            ]
            if item["control_only"]:
                command.append("--control-only")
            with (args.output / f"{item['run_id']}-{args.role}.jsonl").open("w") as log:
                with (args.output / f"{item['run_id']}-{args.role}.stderr").open("w") as errors:
                    try:
                        result = subprocess.run(
                            command, stdout=log, stderr=errors, timeout=lifetime + 3
                        )
                        status = {"exit": result.returncode}
                    except subprocess.TimeoutExpired:
                        status = {"exit": 1, "error": "Worker deadline exceeded"}
            write_json(args.output / f"{item['run_id']}-{args.role}-exit.json", status)


def distribution(values):
    values = sorted(values)
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "min": values[0],
        "median": values[len(values) // 2],
        "mean": sum(values) / len(values),
        "p95": values[math.ceil(len(values) * 0.95) - 1],
        "max": values[-1],
    }


def validate_clock(clock):
    if clock is None:
        return
    required = ("receiver_minus_sender_seconds", "uncertainty_seconds", "method", "measured_at")
    if not isinstance(clock, dict) or any(field not in clock for field in required):
        raise ValueError("Clock evidence requires offset, uncertainty, method and measured_at")
    for field in required[:2]:
        value = clock[field]
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError("Clock offset and uncertainty must be finite numbers")
    if clock["uncertainty_seconds"] < 0 or not clock["method"] or not clock["measured_at"]:
        raise ValueError(
            "Clock evidence requires nonnegative uncertainty and measurement provenance"
        )


def analyse(directory, clock=None):
    validate_clock(clock)
    manifest = json.loads((directory / "manifest.json").read_text())
    groups = {}
    for item in manifest["runs"]:
        key = (
            f"{item['scenario']}/{item['window']}/{'control' if item['control_only'] else 'events'}"
        )
        group = groups.setdefault(
            key,
            {
                "planned_trials": 0,
                "complete_trials": 0,
                "failed_or_missing_trials": 0,
                "intended_events": 0,
                "sent_events": 0,
                "delivered_events": 0,
                "attempts": {},
                "rejections": {},
                "discovery": [],
                "warmup_discovery": [],
                "discovery_timeouts": 0,
                "withheld_expired_events": 0,
                "reconnection": [],
                "latency": [],
                "tx": [],
                "rx": [],
                "receive_tx": [],
                "receive_rx": [],
            },
        )
        group["planned_trials"] += 1
        logs = {}
        corrupt = False
        for role in ("send", "receive"):
            path = directory / f"{item['run_id']}-{role}.jsonl"
            records = []
            if path.exists():
                for line in path.read_text().splitlines():
                    try:
                        row = json.loads(line)
                        if not isinstance(row, dict) or not isinstance(row.get("kind"), str):
                            corrupt = True
                            continue
                        fields = {
                            "event": ("event_id", "outcome", "frame_sha256"),
                            "received": ("event_id", "frame_sha256", "received_wall"),
                            "start": ("counters",),
                            "complete": ("counters",),
                            "discovery": ("outcome", "seconds"),
                            "reconnection": ("seconds",),
                        }.get(row["kind"], ())
                        if any(field not in row for field in fields):
                            corrupt = True
                            continue
                        if "counters" in fields and (
                            not isinstance(row["counters"], dict)
                            or any(metric not in row["counters"] for metric in ("tx", "rx"))
                        ):
                            corrupt = True
                            continue
                        if row.get("run_id") == item["run_id"] and row.get("role") == role:
                            records.append(row)
                    except json.JSONDecodeError:
                        corrupt = True  # Truncated output must count as an incomplete trial below.
            logs[role] = records
        exit_path = directory / f"{item['run_id']}-exit.json"
        try:
            codes = (
                json.loads(exit_path.read_text())
                if exit_path.exists()
                else {
                    role: json.loads(
                        (directory / f"{item['run_id']}-{role}-exit.json").read_text()
                    )["exit"]
                    for role in ("send", "receive")
                    if (directory / f"{item['run_id']}-{role}-exit.json").exists()
                }
            )
        except json.JSONDecodeError:
            codes, corrupt = {}, True
        if not isinstance(codes, dict):
            codes, corrupt = {}, True
        complete = (
            all(
                codes.get(role) == 0 and any(r["kind"] == "complete" for r in logs[role])
                for role in ("send", "receive")
            )
            and "harness_error" not in codes
            and not corrupt
        )
        group["complete_trials" if complete else "failed_or_missing_trials"] += 1
        sends = [r for r in logs["send"] if r["kind"] == "event"]
        intended = {r["event_id"] for r in sends}
        # Missing workers must never improve delivery fractions by shrinking denominator.
        expected = (
            0
            if item["control_only"]
            else (
                30
                if item["scenario"] == "stable"
                else 33
                if item["scenario"] == "overload"
                else 2
                if item["scenario"] == "outage"
                else 1
            )
        )
        group["intended_events"] += max(expected, len(intended))
        sent = {r["event_id"] for r in sends if r["outcome"] == "sent"}
        received = {
            r["event_id"]
            for r in logs["receive"]
            if r["kind"] == "received"
            and any(
                s["event_id"] == r["event_id"]
                and s["outcome"] == "sent"
                and s["frame_sha256"] == r["frame_sha256"]
                for s in sends
            )
        }
        group["withheld_expired_events"] += len(
            {r["event_id"] for r in sends if r["outcome"] == "expired_before_send"}
        )
        group["sent_events"] += len(sent)
        group["delivered_events"] += len(sent & received)
        for row in sends:
            group["attempts"][row["outcome"]] = group["attempts"].get(row["outcome"], 0) + 1
        for row in logs["send"]:
            if row["kind"] == "discovery" and row["outcome"] == "found":
                group["warmup_discovery" if row.get("phase") == "warmup" else "discovery"].append(
                    row["seconds"]
                )
            if row["kind"] == "discovery" and row["outcome"] == "timeout":
                group["discovery_timeouts"] += 1
            if row["kind"] == "reconnection":
                group["reconnection"].append(row["seconds"])
        # Only unambiguous single sends qualify for one-way latency (resends do not).
        if clock is not None:
            for row in logs["receive"]:
                if row["kind"] != "received":
                    continue
                matches = [
                    s
                    for s in sends
                    if s["event_id"] == row["event_id"]
                    and s["outcome"] == "sent"
                    and s["frame_sha256"] == row["frame_sha256"]
                ]
                if len(matches) == 1:
                    group["latency"].append(
                        row["received_wall"]
                        - matches[0]["sent_wall"]
                        - clock["receiver_minus_sender_seconds"]
                    )
        for role in ("send", "receive"):
            starts = [r for r in logs[role] if r["kind"] == "start"]
            ends = [r for r in logs[role] if r["kind"] == "complete"]
            if starts and ends:
                for metric in ("tx", "rx"):
                    # Separate roles: no summing transmit and receive into total traffic.
                    group[metric if role == "send" else "receive_" + metric].append(
                        ends[-1]["counters"][metric] - starts[0]["counters"][metric]
                    )
                for reason, count in ends[-1].get("rejected", {}).items():
                    group["rejections"][reason] = group["rejections"].get(reason, 0) + count
    for group in groups.values():
        group["delivery_fraction"] = (
            group["delivered_events"] / group["intended_events"]
            if group["intended_events"]
            else None
        )
        eligible = group["intended_events"] - group["withheld_expired_events"]
        group["eligible_delivery_fraction"] = (
            group["delivered_events"] / eligible if eligible else None
        )
        for metric in (
            "discovery",
            "warmup_discovery",
            "reconnection",
            "latency",
            "tx",
            "rx",
            "receive_tx",
            "receive_rx",
        ):
            group[metric] = distribution(group[metric])
    comparisons = {}
    for key, group in groups.items():
        if not key.endswith("/events"):
            continue
        control = groups.get(key.removesuffix("/events") + "/control")
        if control is not None:
            comparisons[key] = {
                metric + "_mean_difference": group[metric]["mean"] - control[metric]["mean"]
                if group[metric]["n"] and control[metric]["n"]
                else None
                for metric in ("tx", "rx", "receive_tx", "receive_rx")
            }
    return {
        "traffic_comparisons": comparisons,
        "campaign": manifest,
        "groups": groups,
        "clock_evidence": clock,
        "limitations": [
            "Controlled IP interface contact, not moving radio",
            "RNS interface counters exclude TCP/IP totals and radio airtime",
            "One-way latency omitted without clock evidence; ambiguous multiple sends excluded",
            "Exploratory characterisation, no product pass thresholds",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    provision_parser = commands.add_parser("provision")
    provision_parser.add_argument("--config", type=Path, required=True)
    provision_parser.add_argument("--role", choices=("send", "receive"), required=True)
    provision_parser.add_argument("--peer-ip", required=True)
    provision_parser.add_argument("--port", type=int, default=4243)
    worker_parser = commands.add_parser("worker")
    worker_parser.add_argument("--config", type=Path, required=True)
    worker_parser.add_argument("--role", choices=("send", "receive"), required=True)
    worker_parser.add_argument("--run-id", required=True)
    worker_parser.add_argument(
        "--scenario",
        choices=("stable", "cold", "warm", "outage", "absent", "adversarial", "overload"),
        required=True,
    )
    worker_parser.add_argument("--window", type=float, default=5)
    worker_parser.add_argument("--deadline", type=float, default=60)
    worker_parser.add_argument("--count", type=int, default=30)
    worker_parser.add_argument("--interval", type=float, default=1)
    worker_parser.add_argument("--control-only", action="store_true")
    campaign_parser = commands.add_parser("campaign")
    campaign_parser.add_argument("--output", type=Path, required=True)
    campaign_parser.add_argument("--repetitions", type=int, default=30)
    campaign_parser.add_argument("--jobs", type=int, default=1)
    schedule_parser = commands.add_parser("schedule")
    schedule_parser.add_argument("--output", type=Path, required=True)
    schedule_parser.add_argument(
        "--start-at",
        type=float,
        required=True,
        help="Shared UTC Unix timestamp, well after transfer/setup",
    )
    schedule_parser.add_argument("--repetitions", type=int, default=30)
    batch_parser = commands.add_parser("batch")
    batch_parser.add_argument("--config", type=Path, required=True)
    batch_parser.add_argument("--role", choices=("send", "receive"), required=True)
    batch_parser.add_argument("--manifest", type=Path, required=True)
    batch_parser.add_argument("--output", type=Path, required=True)
    analyse_parser = commands.add_parser("analyse")
    analyse_parser.add_argument("directory", type=Path)
    analyse_parser.add_argument("--clock-evidence", type=Path)
    args = parser.parse_args()
    if args.command == "provision":
        provision(args.config, args.role, args.peer_ip, args.port)
    elif args.command == "worker":
        if (
            any(not math.isfinite(v) or v <= 0 for v in (args.window, args.deadline, args.interval))
            or args.count < 1
        ):
            parser.error("Window, deadline, count and interval must be positive")
        worker(args)
    elif args.command == "schedule":
        if args.repetitions < 1 or not math.isfinite(args.start_at) or args.start_at <= time.time():
            parser.error("Use positive repetitions and a future start timestamp")
        runs = scenarios(args.repetitions)
        scheduled = args.start_at
        for item in runs:
            item["scheduled_at"] = scheduled
            scheduled += item["window"] + 20
        write_json(
            args.output,
            {
                "runs": runs,
                "jobs": 1,
                "environment": "two physical hosts; not yet executed",
                "created_at": time.time(),
                "ends_by": scheduled,
            },
        )
    elif args.command == "batch":
        batch(args)
    elif args.command == "campaign":
        if not 1 <= args.jobs <= 8 or args.repetitions < 1:
            parser.error("Use jobs 1–8 and positive repetitions")
        args.output.mkdir(parents=True, exist_ok=False)
        runs = scenarios(args.repetitions)
        write_json(
            args.output / "manifest.json",
            {
                "runs": runs,
                "jobs": args.jobs,
                "environment": "single-host loopback",
                "created_at": time.time(),
            },
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = [executor.submit(local_trial, item, args.output) for item in runs]
            for future in concurrent.futures.as_completed(futures):
                print(json.dumps({"finished": future.result()}), flush=True)
        write_json(args.output / "summary.json", analyse(args.output))
    else:
        clock = json.loads(args.clock_evidence.read_text()) if args.clock_evidence else None
        try:
            validate_clock(clock)
        except ValueError as error:
            parser.error(str(error))
        print(json.dumps(analyse(args.directory, clock), indent=2))


if __name__ == "__main__":
    main()
