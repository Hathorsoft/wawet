"""Language-independent experimental road event envelope, version 1."""

from dataclasses import dataclass
from struct import Struct

MAGIC = b"\xa7\xe1"
VERSION = 1
FRAME = Struct(">2sB16sBiiHIHH")
MAX_TTL = 3600
MAX_RADIUS = 10000
UNKNOWN_HEADING = 65535
CATEGORIES = {1: "Road hazard", 2: "Stopped traffic", 3: "Collision"}


class ProtocolError(ValueError):
    """A frame or domain field does not conform to version 1."""


def integer(value: int, low: int, high: int, name: str) -> None:
    if type(value) is not int or not low <= value <= high:
        raise ProtocolError(f"{name} must be an integer in [{low}, {high}]")


@dataclass(frozen=True)
class RoadEvent:
    event_id: bytes
    category: int
    latitude_e5: int
    longitude_e5: int
    heading_cdeg: int | None
    created_at: int
    ttl_seconds: int = 900
    radius_m: int = 5000

    def __post_init__(self) -> None:
        if type(self.event_id) is not bytes or len(self.event_id) != 16 or not any(self.event_id):
            raise ProtocolError("event ID must be 16 nonzero-in-aggregate bytes")
        integer(self.category, 1, 255, "category")
        integer(self.latitude_e5, -9000000, 9000000, "latitude_e5")
        integer(self.longitude_e5, -18000000, 18000000, "longitude_e5")
        if self.heading_cdeg is not None:
            integer(self.heading_cdeg, 0, 35999, "heading_cdeg")
        integer(self.created_at, 0, 0xFFFFFFFF, "created_at")
        integer(self.ttl_seconds, 1, MAX_TTL, "ttl_seconds")
        integer(self.radius_m, 1, MAX_RADIUS, "radius_m")

    @property
    def latitude(self) -> float:
        return self.latitude_e5 / 100000

    @property
    def longitude(self) -> float:
        return self.longitude_e5 / 100000

    @property
    def expires_at(self) -> int:
        return self.created_at + self.ttl_seconds

    def expired(self, now: int) -> bool:
        return now >= self.expires_at


def encode(event: RoadEvent) -> bytes:
    return FRAME.pack(
        MAGIC,
        VERSION,
        event.event_id,
        event.category,
        event.latitude_e5,
        event.longitude_e5,
        UNKNOWN_HEADING if event.heading_cdeg is None else event.heading_cdeg,
        event.created_at,
        event.ttl_seconds,
        event.radius_m,
    )


def decode(payload: bytes) -> RoadEvent:
    if type(payload) is not bytes or len(payload) != FRAME.size:
        raise ProtocolError(f"expected exactly {FRAME.size} bytes")
    magic, version, identifier, category, lat, lon, heading, created, ttl, radius = FRAME.unpack(
        payload
    )
    if magic != MAGIC:
        raise ProtocolError("invalid magic")
    if version != VERSION:
        raise ProtocolError("unsupported version")
    return RoadEvent(
        identifier,
        category,
        lat,
        lon,
        None if heading == UNKNOWN_HEADING else heading,
        created,
        ttl,
        radius,
    )
