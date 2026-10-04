"""Scripted, deterministic, unauthenticated contacts; no RF or discovery model."""

import argparse
import json
from dataclasses import dataclass
from typing import Literal

from wawet.geo import Position
from wawet.protocol import decode, encode
from wawet.simulation import ManualClock, SimulatedNetwork, SimulatedTransport
from wawet.transport import Delivery, Receiver
from wawet.vehicle import Identity, Vehicle

Kind = Literal["link", "position", "report", "resend", "observe"]


@dataclass(frozen=True)
class Action:
    at: int
    kind: Kind
    actor: str = "a"
    peer: str = ""
    enabled: bool = True
    event: int = 1
    recipients: tuple[str, ...] = ()
    ttl: int = 10
    position: Position | None = None
    label: str = ""
    stale_probe: bool = False


@dataclass(frozen=True)
class Fixture:
    names: tuple[str, ...]
    actions: tuple[Action, ...]
    latency: int = 1
    queue_capacity: int = 4096
    retention: int = 1024


class ObservedTransport:
    """Observe acceptance without changing the application callback contract."""

    def __init__(self, transport: SimulatedTransport, name: str, clock: ManualClock) -> None:
        self.transport, self.name, self.clock = transport, name, clock
        self.vehicle: Vehicle | None = None
        self.accepted: list[dict[str, int | str]] = []

    def subscribe(self, receiver: Receiver) -> None:
        def observe(payload: bytes, delivery: Delivery) -> None:
            assert self.vehicle is not None
            before = self.vehicle.metrics["received"]
            receiver(payload, delivery)
            if self.vehicle.metrics["received"] > before:
                event = decode(payload)
                self.accepted.append(
                    {
                        "event": event.event_id.hex(),
                        "recipient": self.name,
                        "created_at": event.created_at,
                        "accepted_at": self.clock.now,
                        "latency_seconds": self.clock.now - event.created_at,
                        "frame": payload.hex(),
                    }
                )

        self.transport.subscribe(observe)

    def send(self, payload: bytes) -> None:
        self.transport.send(payload)

    def close(self) -> None:
        self.transport.close()


def fixtures() -> dict[str, Fixture]:
    ahead = Position(52.21, 0.9, 0)
    passing = Fixture(
        ("a", "b", "c"),
        (
            Action(0, "position", actor="c", position=Position(52.1883, 0.9, 180)),
            Action(0, "link", peer="b"),
            Action(0, "link", peer="c"),
            Action(0, "report", recipients=("b", "c")),
            Action(1, "observe", label="during contact"),
            Action(1, "position", actor="b", position=ahead),
            Action(1, "observe", label="after passing"),
            Action(2, "report", event=2, recipients=("b", "c")),
            Action(2, "link", peer="b", enabled=False),
            Action(2, "link", peer="c", enabled=False),
            Action(3, "observe", label="contact lost"),
        ),
    )
    convoy = Fixture(
        ("a", "b", "c", "d"),
        tuple(Action(0, "link", peer=n) for n in ("b", "c", "d"))
        + (
            Action(0, "report", recipients=("b", "c", "d")),
            Action(1, "observe", label="fresh"),
            Action(1, "resend", recipients=("b", "c", "d")),
            Action(2, "observe", label="duplicates"),
            Action(2, "position", actor="b", position=ahead),
            Action(2, "observe", label="leader passed"),
        ),
    )
    rural = Fixture(
        ("a", "b"),
        (
            Action(0, "report", recipients=("b",), ttl=5),
            Action(1, "link", peer="b"),
            Action(2, "observe", label="no replay"),
            Action(2, "resend", recipients=("b",)),
            Action(3, "observe", label="explicit resend"),
            Action(4, "resend", recipients=("b",), stale_probe=True),
            Action(5, "observe", label="exact expiry"),
        ),
    )
    names = tuple("abcdefgh")
    dense = Fixture(
        names,
        tuple(
            Action(0, "link", actor=a, peer=b) for i, a in enumerate(names) for b in names[i + 1 :]
        )
        + (
            Action(0, "report", recipients=names[1:], ttl=3),
            Action(0, "report", actor="b", event=2, recipients=("a",) + names[2:], ttl=3),
            Action(1, "observe", label="queue overload"),
            Action(1, "report", actor="b", event=3, recipients=("a",) + names[2:], ttl=2),
            Action(2, "observe", label="retention pressure"),
            Action(3, "observe", label="expired retention"),
            Action(3, "report", actor="b", event=4, recipients=("a",) + names[2:], ttl=3),
            Action(4, "observe", label="recovery"),
        ),
        queue_capacity=7,
        retention=1,
    )
    # Each fixture uses explicit positions, not motion-derived contact links.
    return {"passing": passing, "convoy": convoy, "rural": rural, "dense": dense}


def run_scenario(name: str, fixture: Fixture | None = None) -> dict[str, object]:
    fixture = fixtures()[name] if fixture is None else fixture
    clock = ManualClock(1000)
    network = SimulatedNetwork(clock, fixture.latency, fixture.queue_capacity)
    vehicles: dict[str, Vehicle] = {}
    transports: dict[str, ObservedTransport] = {}
    frames: dict[int, bytes] = {}
    intended: set[tuple[str, str]] = set()
    probes: list[dict[str, object]] = []
    transmissions: list[dict[str, object]] = []
    observations: list[dict[str, object]] = []
    queue_dropped = 0
    contact_dropped = 0
    max_queue = 0
    max_retained = 0
    try:
        for i, actor in enumerate(fixture.names, 1):
            transport = ObservedTransport(network.endpoint(actor), actor, clock)
            transports[actor] = transport
            position = Position(52.2 if actor == "a" else 52.1883, 0.9, 0)
            vehicle = Vehicle(
                Identity(bytes([i]) * 16),
                position,
                transport,
                lambda: clock.now,
                capacity=fixture.retention,
            )
            transport.vehicle = vehicle
            vehicles[actor] = vehicle
        previous = 0
        for action in fixture.actions:
            if action.at < previous:
                raise ValueError("actions must be ordered by timestamp")
            # Due deliveries precede all actions at this timestamp, including disconnects.
            before_drops = network.dropped
            network.advance(action.at - previous)
            contact_dropped += network.dropped - before_drops
            previous = action.at
            vehicle = vehicles[action.actor]
            if action.kind == "link":
                network.connect(action.actor, action.peer, action.enabled)
            elif action.kind == "position":
                if action.position is None:
                    raise ValueError("position action requires a position")
                vehicle.position = action.position
            elif action.kind in ("report", "resend"):
                before_drops = network.dropped
                if action.kind == "report":
                    if action.event in frames:
                        raise ValueError("report IDs must be unique")
                    event = vehicle.report(
                        event_id=action.event.to_bytes(16, "big"), ttl=action.ttl
                    )
                    frames[action.event] = encode(event)
                else:
                    vehicle.transport.send(frames[action.event])
                payload = frames[action.event]
                event = decode(payload)
                # A probe deliberately scheduled to arrive expired is separate from fresh intent.
                queue_dropped += network.dropped - before_drops
                stale = action.stale_probe
                if stale and not event.expired(clock.now + fixture.latency):
                    raise ValueError("stale probe must arrive at or after expiry")
                for recipient in action.recipients:
                    if stale:
                        probes.append({"event": event.event_id.hex(), "recipient": recipient})
                    else:
                        intended.add((event.event_id.hex(), recipient))
                transmissions.append(
                    {
                        "at": clock.now,
                        "sender": action.actor,
                        "kind": action.kind,
                        "frame": payload.hex(),
                        "stale_probe": stale,
                    }
                )
            else:
                observations.append(
                    {
                        "at": clock.now,
                        "label": action.label,
                        "alerts": {
                            n: [a.event.event_id.hex() for a in v.alerts()]
                            for n, v in vehicles.items()
                        },
                        "retained": {n: len(v.events) for n, v in vehicles.items()},
                    }
                )
            max_queue = max(max_queue, len(network.queue))
            max_retained = max(max_retained, *(len(v.events) for v in vehicles.values()))
        if network.queue:
            raise ValueError("fixture must observe through all pending deliveries")
        for v in vehicles.values():
            v.prune()
        accepted = [record for transport in transports.values() for record in transport.accepted]
        pairs = {(str(r["event"]), str(r["recipient"])) for r in accepted}
        latencies = sorted(int(r["latency_seconds"]) for r in accepted)
        return {
            "scenario": name,
            "evidence": "deterministic unauthenticated simulation; no physical/RF acceptance",
            "intended_pairs": [{"event": e, "recipient": r} for e, r in sorted(intended)],
            "accepted_pairs": accepted,
            "fresh_delivery": {"numerator": len(pairs & intended), "denominator": len(intended)},
            "stale_probes": probes,
            "latency": {
                "sample_count": len(latencies),
                "seconds": latencies,
                "origin": "original event creation/availability, including explicit resend wait",
            },
            "observations": observations,
            "transmissions": transmissions,
            "metrics": {
                n: {
                    key: v.metrics[key]
                    for key in (
                        "sent",
                        "received",
                        "expired",
                        "duplicate",
                        "invalid",
                        "future",
                        "id_conflict",
                        "rate_limited",
                        "capacity_dropped",
                        "unauthenticated",
                    )
                }
                for n, v in vehicles.items()
            },
            "queue_dropped": queue_dropped,
            "contact_dropped": contact_dropped,
            "network_dropped": network.dropped,
            "limits": {"queue": fixture.queue_capacity, "retention_per_vehicle": fixture.retention},
            "peak_queue": max_queue,
            "peak_retained_per_vehicle": max_retained,
            "final_retained": {n: len(v.events) for n, v in vehicles.items()},
        }
    finally:
        for vehicle in vehicles.values():
            vehicle.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=tuple(fixtures()))
    parser.add_argument("--json", action="store_true", help="emit deterministic structured results")
    args = parser.parse_args()
    results = [run_scenario(n) for n in ([args.scenario] if args.scenario else fixtures())]
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        print("Deterministic unauthenticated simulation — no RF or feasibility acceptance")
        for result in results:
            print(
                f"{result['scenario']}: fresh delivery {result['fresh_delivery']}; "
                f"latency {result['latency']}; network drops {result['network_dropped']}"
            )


if __name__ == "__main__":
    main()
