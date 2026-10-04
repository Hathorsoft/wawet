"""Approximate spherical relevance, not a road or lane model."""

import math
from dataclasses import dataclass

from wawet.protocol import RoadEvent


def finite_range(value: float, low: float, high: float, name: str) -> None:
    if isinstance(value, bool) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"invalid {name}")


@dataclass(frozen=True)
class Position:
    latitude: float
    longitude: float
    heading: float
    speed_mps: float = 0

    def __post_init__(self) -> None:
        finite_range(self.latitude, -90, 90, "latitude")
        finite_range(self.longitude, -180, 180, "longitude")
        finite_range(self.heading, 0, 359.999999, "heading")
        finite_range(self.speed_mps, 0, 100, "speed")


def distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    for lat, lon in ((lat1, lon1), (lat2, lon2)):
        finite_range(lat, -90, 90, "latitude")
        finite_range(lon, -180, 180, "longitude")
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371000 * 2 * math.asin(math.sqrt(min(1, max(0, a))))


def bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2, dl = math.radians(lat1), math.radians(lat2), math.radians(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(y, x)) % 360


def angular_difference(a: float, b: float) -> float:
    return abs((a - b + 180) % 360 - 180)


def relevance(position: Position, event: RoadEvent) -> tuple[bool, float]:
    distance = distance_m(position.latitude, position.longitude, event.latitude, event.longitude)
    if distance > event.radius_m:
        return False, distance
    if event.heading_cdeg is not None:
        if angular_difference(position.heading, event.heading_cdeg / 100) > 60:
            return False, distance
    if distance > 25:
        bearing = bearing_deg(
            position.latitude, position.longitude, event.latitude, event.longitude
        )
        if angular_difference(position.heading, bearing) > 90:
            return False, distance
    return True, distance
