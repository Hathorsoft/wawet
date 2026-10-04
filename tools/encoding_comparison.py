"""Original, restricted research codecs; not production wire formats."""

import argparse
import hashlib
import json
import platform
import statistics
import struct
import subprocess
import sys
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "packages"))
from wawet.protocol import RoadEvent, decode, encode  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MAX_BINARY = 293
MAX_CBOR = 309


@dataclass(frozen=True)
class Message:
    event: RoadEvent
    accuracy: int | None = None
    reference: bytes | None = None
    text: str | None = None
    key: bytes | None = None
    signature: bytes | None = None

    def __post_init__(self):
        if not isinstance(self.event, RoadEvent):
            raise ValueError("event required")
        if self.accuracy is not None and (
            type(self.accuracy) is not int or not 0 <= self.accuracy <= 65535
        ):
            raise ValueError("accuracy must be 0..65535 metres")
        for name, size in [("reference", 16), ("key", 32), ("signature", 64)]:
            value = getattr(self, name)
            if value is not None and (type(value) is not bytes or len(value) != size):
                raise ValueError(f"{name} must be {size} bytes")
        if (self.key is None) != (self.signature is None):
            raise ValueError("key and signature must occur together")
        if self.text is not None and (
            type(self.text) is not str or len(self.text.encode("utf-8")) > 128
        ):
            raise ValueError("text exceeds 128 UTF-8 bytes")


def fields(message):
    return {
        key: value
        for key, value in enumerate(
            [message.accuracy, message.reference, message.text, message.key, message.signature], 1
        )
        if value is not None
    }


def binary_encode(message):
    result = b"WX\x01" + encode(message.event)
    for key, value in fields(message).items():
        if key == 1:
            value = struct.pack(">H", value)
        elif key == 3:
            value = value.encode("utf-8")
        result += bytes([key, len(value)]) + value
    return result


def bounded(payload, maximum):
    if type(payload) is not bytes or len(payload) > maximum:
        raise ValueError("invalid payload type or maximum length")


def binary_decode(payload):
    bounded(payload, MAX_BINARY)
    if payload[:3] != b"WX\x01":
        raise ValueError("unsupported experimental binary version")
    event = decode(payload[3:41])
    values = {}
    offset = 41
    previous = 0
    while offset < len(payload):
        if offset + 2 > len(payload):
            raise ValueError("truncated extension header")
        key, length = payload[offset : offset + 2]
        offset += 2
        if key <= previous or key not in range(1, 6) or offset + length > len(payload):
            raise ValueError("invalid extension")
        previous = key
        value = payload[offset : offset + length]
        offset += length
        if key == 1:
            if length != 2:
                raise ValueError("invalid accuracy length")
            value = int.from_bytes(value, "big")
        elif key == 3:
            value = value.decode("utf-8")
        values[key] = value
    return Message(
        event,
        **{
            name: values.get(i)
            for i, name in enumerate(["accuracy", "reference", "text", "key", "signature"], 1)
        },
    )


def head(major, value):
    if value < 24:
        return bytes([major * 32 + value])
    for additional, size in [(24, 1), (25, 2), (26, 4)]:
        if value < 1 << (8 * size):
            return bytes([major * 32 + additional]) + value.to_bytes(size, "big")
    raise ValueError("integer too large")


def atom(value):
    if type(value) is int:
        return head(0 if value >= 0 else 1, value if value >= 0 else -1 - value)
    if type(value) is bytes:
        return head(2, len(value)) + value
    if type(value) is str:
        data = value.encode("utf-8")
        return head(3, len(data)) + data
    raise ValueError("unsupported CBOR type")


def cbor_encode(message):
    event = message.event
    data = dict(
        enumerate(
            [
                1,
                event.event_id,
                event.category,
                event.latitude_e5,
                event.longitude_e5,
                65535 if event.heading_cdeg is None else event.heading_cdeg,
                event.created_at,
                event.ttl_seconds,
                event.radius_m,
            ]
        )
    )
    data.update({key + 8: value for key, value in fields(message).items()})
    return head(5, len(data)) + b"".join(atom(k) + atom(v) for k, v in data.items())


def cbor_decode(payload):
    bounded(payload, MAX_CBOR)
    offset = 0

    def read():
        nonlocal offset
        if offset >= len(payload):
            raise ValueError("truncated CBOR")
        first = payload[offset]
        offset += 1
        major, extra = divmod(first, 32)
        value = extra
        if extra >= 24:
            if extra not in (24, 25, 26):
                raise ValueError("unsupported CBOR length")
            size = 1 << (extra - 24)
            if offset + size > len(payload):
                raise ValueError("truncated CBOR argument")
            value = int.from_bytes(payload[offset : offset + size], "big")
            offset += size
            if value < {24: 24, 25: 256, 26: 65536}[extra]:
                raise ValueError("nonminimal CBOR")
        if major in (2, 3):
            if offset + value > len(payload):
                raise ValueError("truncated CBOR string")
            raw = payload[offset : offset + value]
            offset += value
            return major, raw if major == 2 else raw.decode("utf-8")
        if major not in (0, 1, 5):
            raise ValueError("unsupported CBOR major type")
        return major, -1 - value if major == 1 else value

    major, count = read()
    if major != 5 or not 9 <= count <= 14:
        raise ValueError("expected bounded map")
    data = {}
    previous = -1
    for _ in range(count):
        key_type, key = read()
        if key_type != 0 or not previous < key <= 13:
            raise ValueError("invalid or duplicate map key")
        previous = key
        value_type, value = read()
        expected = 2 if key in (1, 10, 12, 13) else 3 if key == 11 else 0
        if value_type != expected and not (key in (3, 4) and value_type == 1):
            raise ValueError("invalid field type")
        data[key] = value
    if offset != len(payload) or not set(range(9)).issubset(data) or data[0] != 1:
        raise ValueError("trailing data, missing fields or unsupported version")
    event = RoadEvent(
        data[1],
        data[2],
        data[3],
        data[4],
        None if data[5] == 65535 else data[5],
        data[6],
        data[7],
        data[8],
    )
    return Message(
        event,
        **{
            name: data.get(i)
            for i, name in enumerate(["accuracy", "reference", "text", "key", "signature"], 9)
        },
    )


CODECS = {"binary": (binary_encode, binary_decode), "cbor": (cbor_encode, cbor_decode)}


def fixtures():
    result = {}
    for vector in json.loads((ROOT / "protocol/vectors/v1.json").read_text()):
        values = dict(vector["fields"])
        values["event_id"] = bytes.fromhex(values["event_id"])
        result[vector["name"]] = Message(RoadEvent(**values))
    event = RoadEvent(b"\xff" * 16, 255, -9000000, 18000000, 35999, 0xFFFFFFFF, 3600, 10000)
    result["boundary_min"] = Message(RoadEvent(b"\x01" * 16, 1, 0, 0, None, 0, 1, 1))
    result["boundary_max"] = Message(event)
    result["boundary_southwest"] = Message(
        RoadEvent(b"\x02" * 16, 255, -9000000, -18000000, 0, 0, 3600, 10000)
    )
    result["boundary_northeast"] = Message(
        RoadEvent(b"\x03" * 16, 1, 9000000, 18000000, 35999, 0xFFFFFFFF, 1, 1)
    )
    result["accuracy"] = Message(event, accuracy=65535)
    result["reference"] = Message(event, reference=b"R" * 16)
    result["text"] = Message(event, text="é" * 64)
    result["all_options"] = Message(event, 65535, b"R" * 16, "é" * 64)
    return result


def sizes():
    rows = []
    for name, unsigned in fixtures().items():
        for signed in (False, True):
            message = Message(
                unsigned.event,
                unsigned.accuracy,
                unsigned.reference,
                unsigned.text,
                b"K" * 32 if signed else None,
                b"S" * 64 if signed else None,
            )
            for codec, (pack, unpack) in CODECS.items():
                payload = pack(message)
                assert unpack(payload) == message
                base = len(pack(Message(message.event)))
                plain = len(pack(unsigned))
                rows.append(
                    {
                        "fixture": name,
                        "signed_placeholder": signed,
                        "codec": codec,
                        "bytes": len(payload),
                        "base_bytes": base,
                        "optional_bytes": plain - base,
                        "key_signature_bytes": len(payload) - plain,
                    }
                )
    return {"v1_bytes": 38, "maximum_bytes": {"binary": MAX_BINARY, "cbor": MAX_CBOR}, "rows": rows}


def benchmark(codec, iterations, repeats):
    pack, unpack = (
        (lambda m: encode(m.event), lambda p: Message(decode(p)))
        if codec == "v1"
        else CODECS[codec]
    )
    message = Message(
        fixtures()["all_options"].event, 65535, b"R" * 16, "é" * 64, b"K" * 32, b"S" * 64
    )
    payload = pack(message)
    result = {}
    for name, operation in [
        ("baseline", lambda: None),
        ("encode", lambda: pack(message)),
        ("decode", lambda: unpack(payload)),
    ]:
        elapsed, peaks = [], []
        for _ in range(repeats):
            start = time.perf_counter_ns()
            for _ in range(iterations):
                operation()
            elapsed.append((time.perf_counter_ns() - start) / iterations)
            tracemalloc.start()
            for _ in range(iterations):
                operation()
            peaks.append(tracemalloc.get_traced_memory()[1])
            tracemalloc.stop()
        result[name] = {
            "ns_per_operation_samples": elapsed,
            "median_ns": statistics.median(elapsed),
            "peak_python_bytes_samples": peaks,
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes-only", action="store_true")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--worker", choices=["v1", *CODECS], help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not 1 <= args.iterations <= 100000 or not 2 <= args.repeats <= 20:
        parser.error("iterations must be 1..100000; repeats 2..20")
    if args.worker:
        result = benchmark(args.worker, args.iterations, args.repeats)
    else:
        result = sizes()
        if not args.sizes_only:
            result["environment"] = {
                "input_sha256": {
                    str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [
                        ROOT / "packages/wawet/protocol.py",
                        ROOT / "protocol/vectors/v1.json",
                        ROOT / "tests/test_encoding_comparison.py",
                    ]
                },
                "python": sys.version,
                "platform": platform.platform(),
                "iterations": args.iterations,
                "repeats": args.repeats,
                "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "head": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
                ).strip(),
                "git_status": subprocess.check_output(
                    ["git", "status", "--short"], cwd=ROOT, text=True
                ),
            }
            result["benchmarks"] = {
                codec: json.loads(
                    subprocess.check_output(
                        [
                            sys.executable,
                            str(Path(__file__).resolve()),
                            "--worker",
                            codec,
                            "--iterations",
                            str(args.iterations),
                            "--repeats",
                            str(args.repeats),
                        ],
                        text=True,
                    )
                )
                for codec in ["v1", *CODECS]
            }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
