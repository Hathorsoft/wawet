import json
import random
import unittest
from dataclasses import replace
from pathlib import Path

from wawet.protocol import FRAME, ProtocolError, RoadEvent, decode, encode


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.event = RoadEvent(bytes(range(1, 17)), 1, 5220000, 90000, 0, 1801652400)

    def test_canonical_vectors(self):
        vectors = json.loads(Path("protocol/vectors/v1.json").read_text())
        for vector in vectors:
            with self.subTest(vector=vector["name"]):
                fields = dict(vector["fields"])
                fields["event_id"] = bytes.fromhex(fields["event_id"])
                event = RoadEvent(**fields)
                self.assertEqual(encode(event).hex(), vector["hex"])
                self.assertEqual(decode(bytes.fromhex(vector["hex"])), event)

    def test_round_trip_and_size(self):
        self.assertEqual(decode(encode(self.event)), self.event)
        self.assertEqual(len(encode(self.event)), 38)

    def test_unknown_category_is_preserved(self):
        event = replace(self.event, category=255)
        self.assertEqual(decode(encode(event)), event)

    def test_optional_heading(self):
        event = replace(self.event, heading_cdeg=None)
        self.assertEqual(encode(event)[28:30], b"\xff\xff")
        self.assertIsNone(decode(encode(event)).heading_cdeg)

    def test_invalid_domain_fields(self):
        cases = {
            "category": [0, 256, True, 1.5],
            "latitude_e5": [-9000001, 9000001, float("nan")],
            "longitude_e5": [-18000001, 18000001],
            "heading_cdeg": [-1, 36000, 65535],
            "created_at": [-1, 2**32],
            "ttl_seconds": [0, -1, 3601],
            "radius_m": [0, 10001],
            "event_id": [b"", b"\0" * 16, b"X" * 17, bytearray(b"X" * 16)],
        }
        for field, values in cases.items():
            for value in values:
                with self.subTest(field=field, value=value), self.assertRaises(ProtocolError):
                    replace(self.event, **{field: value})

    def test_coordinate_boundaries(self):
        for lat, lon in [(-9000000, -18000000), (9000000, 18000000)]:
            event = replace(self.event, latitude_e5=lat, longitude_e5=lon)
            self.assertEqual(decode(encode(event)), event)

    def test_invalid_magic_version_length(self):
        frame = encode(self.event)
        for payload in [
            b"",
            frame[:-1],
            frame + b"x",
            b"x" * 10000,
            b"\0\0" + frame[2:],
            frame[:2] + b"\x02" + frame[3:],
            bytearray(frame),
        ]:
            with self.subTest(payload=payload), self.assertRaises(ProtocolError):
                decode(payload)

    def test_invalid_fields_on_wire(self):
        frame = encode(self.event)
        changes = [
            (19, b"\0"),
            (20, (9000001).to_bytes(4, "big", signed=True)),
            (28, (36000).to_bytes(2, "big")),
            (34, b"\0\0"),
            (36, b"\0\0"),
        ]
        for offset, value in changes:
            with self.subTest(offset=offset), self.assertRaises(ProtocolError):
                decode(frame[:offset] + value + frame[offset + len(value) :])

    def test_expiry_boundary(self):
        self.assertFalse(self.event.expired(self.event.expires_at - 1))
        self.assertTrue(self.event.expired(self.event.expires_at))
        self.assertTrue(self.event.expired(self.event.expires_at + 1))

    def test_random_malformed_frames_have_controlled_errors(self):
        rng = random.Random(4)
        for _ in range(500):
            payload = rng.randbytes(FRAME.size)
            try:
                event = decode(payload)
            except ProtocolError:
                continue
            self.assertEqual(encode(event), payload)
