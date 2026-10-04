"""Research profile bounds, semantic parity and frozen production compatibility."""

import json
import random
import subprocess
import sys
import unittest
from dataclasses import replace

from wawet.protocol import ProtocolError, encode

from tools import encoding_comparison as study


class EncodingComparisonTests(unittest.TestCase):
    def test_fixture_roundtrips_and_maximum(self):
        for message in study.fixtures().values():
            for signed in (False, True):
                value = replace(
                    message,
                    key=b"K" * 32 if signed else None,
                    signature=b"S" * 64 if signed else None,
                )
                for pack, unpack in study.CODECS.values():
                    self.assertEqual(unpack(pack(value)), value)
        maximum = replace(study.fixtures()["all_options"], key=b"K" * 32, signature=b"S" * 64)
        self.assertEqual(len(study.binary_encode(maximum)), study.MAX_BINARY)
        self.assertEqual(len(study.cbor_encode(maximum)), study.MAX_CBOR)

    def test_published_vectors_unchanged(self):
        vectors = json.loads((study.ROOT / "protocol/vectors/v1.json").read_text())
        for vector in vectors:
            self.assertEqual(encode(study.fixtures()[vector["name"]].event).hex(), vector["hex"])

    def test_optional_bounds(self):
        message = study.fixtures()["boundary_min"]
        for changes in [
            dict(accuracy=-1),
            dict(accuracy=65536),
            dict(accuracy=True),
            dict(reference=b"x" * 15),
            dict(reference=bytearray(16)),
            dict(text="é" * 65),
            dict(text="\ud800"),
            dict(text=1),
            dict(key=b"x" * 32),
            dict(signature=b"x" * 64),
            dict(key=b"x" * 31, signature=b"x" * 64),
        ]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                replace(message, **changes)
        for text in ("", "x" * 128, "é" * 64):
            value = replace(message, accuracy=0, text=text)
            for pack, unpack in study.CODECS.values():
                self.assertEqual(unpack(pack(value)), value)

    def test_binary_rejections(self):
        base = study.binary_encode(study.fixtures()["boundary_min"])
        payloads = [
            base[:2],
            b"WX\x02" + base[3:],
            base + b"\x01",
            base + b"\x00\x00",
            base + b"\x01\x01x",
            base + b"\x02\x10x",
            base + b"\x03\x01\xff",
            base + b"\x01\x02\x00\x00" * 2,
            base + b"\x06\x00",
            base + b"x" * 300,
            base[:22] + b"\x00" + base[23:],
        ]
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                study.binary_decode(payload)

    def test_cbor_independent_wire_example(self):
        # Nine sorted keys; version=1, ID=16 ones, category=1, coordinates=0,
        # absent heading=65535, creation=0, TTL=1, radius=1.
        expected = bytes.fromhex("a900010150" + "01" * 16 + "0201030004000519ffff060007010801")
        message = study.fixtures()["boundary_min"]
        self.assertEqual(study.cbor_encode(message), expected)
        self.assertEqual(study.cbor_decode(expected), message)

    def test_cbor_rejections(self):
        base = study.cbor_encode(study.fixtures()["boundary_min"])
        pairs = base[1:]
        payloads = [
            b"",
            base[:-1],
            base + b"\x00",
            b"\xbf" + pairs,
            b"\xa9\x00\x02" + base[3:],
            b"\xaa" + pairs + b"\x08\x01",
            b"\xa9\x18\x00" + base[2:],
            b"\xa9\x00\xf5" + base[3:],
            b"\xa9\x00\xa1" + base[3:],
            b"\xaa" + pairs + b"\x09\x20",
            b"\xaa" + pairs + b"\x0b\x61\xff",
            b"x" * 310,
            b"\xa9\x00\x01\x01\x5a\xff\xff\xff\xff",
        ]
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                study.cbor_decode(payload)

    def test_random_malformed_inputs_controlled(self):
        rng = random.Random(9)
        for _, unpack in study.CODECS.values():
            for _ in range(500):
                try:
                    unpack(rng.randbytes(rng.randrange(320)))
                except (ValueError, ProtocolError):
                    pass

    def test_size_cli_is_repeatable(self):
        command = [sys.executable, "tools/encoding_comparison.py", "--sizes-only"]
        first = subprocess.check_output(command)
        self.assertEqual(first, subprocess.check_output(command))
        result = json.loads(first)
        for row in result["rows"]:
            self.assertEqual(
                row["bytes"], row["base_bytes"] + row["optional_bytes"] + row["key_signature_bytes"]
            )

    def test_benchmark_samples(self):
        for codec in ["v1", *study.CODECS]:
            result = study.benchmark(codec, 2, 2)
            for operation in ("baseline", "encode", "decode"):
                self.assertEqual(len(result[operation]["ns_per_operation_samples"]), 2)
                self.assertEqual(len(result[operation]["peak_python_bytes_samples"]), 2)
