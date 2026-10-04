"""Road-event application logic shared by every transport."""

from collections import Counter, OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from uuid import uuid4

from wawet.geo import Position, relevance
from wawet.protocol import CATEGORIES, ProtocolError, RoadEvent, decode, encode
from wawet.transport import Delivery, EventTransport


@dataclass(frozen=True)
class Identity:
    """Local pseudonym, not an RNS key or an authentication assertion."""

    token: bytes

    def __post_init__(self) -> None:
        if type(self.token) is not bytes or len(self.token) != 16:
            raise ValueError("identity requires 16 bytes")

    @classmethod
    def generate(cls) -> "Identity":
        return cls(uuid4().bytes)


@dataclass(frozen=True)
class Alert:
    event: RoadEvent
    distance_m: float
    received_at: int


class Vehicle:
    def __init__(
        self,
        identity: Identity,
        position: Position,
        transport: EventTransport,
        clock: Callable[[], int],
        capacity: int = 1024,
        receive_limit: int = 120,
    ) -> None:
        if capacity < 1 or receive_limit < 1:
            raise ValueError("positive capacity and receive limit required")
        self.identity, self.position, self.transport, self.clock = (
            identity,
            position,
            transport,
            clock,
        )
        self.capacity, self.receive_limit = capacity, receive_limit
        self.events: OrderedDict[bytes, tuple[RoadEvent, bytes, int]] = OrderedDict()
        self.metrics: Counter[str] = Counter()
        self.window_start, self.window_count = clock(), 0
        transport.subscribe(self.receive)

    def prune(self) -> None:
        now = self.clock()
        for identifier, (event, _, _) in list(self.events.items()):
            if event.expired(now):
                del self.events[identifier]

    def report(
        self,
        category: int = 1,
        ttl: int = 900,
        radius: int = 5000,
        event_id: bytes | None = None,
    ) -> RoadEvent:
        heading = min(35999, round(self.position.heading * 100))
        event = RoadEvent(
            uuid4().bytes if event_id is None else event_id,
            category,
            round(self.position.latitude * 100000),
            round(self.position.longitude * 100000),
            heading,
            self.clock(),
            ttl,
            radius,
        )
        self.transport.send(encode(event))
        self.metrics["sent"] += 1
        return event

    def receive(self, payload: bytes, delivery: Delivery) -> None:
        now = self.clock()
        if now - self.window_start >= 60:
            self.window_start, self.window_count = now, 0
        self.window_count += 1
        if self.window_count > self.receive_limit:
            self.metrics["rate_limited"] += 1
            return
        self.prune()
        try:
            event = decode(payload)
        except ProtocolError:
            self.metrics["invalid"] += 1
            return
        if event.expired(now):
            self.metrics["expired"] += 1
            return
        if event.created_at > now + 30:
            self.metrics["future"] += 1
            return
        if event.event_id in self.events:
            metric = "duplicate" if self.events[event.event_id][1] == payload else "id_conflict"
            self.metrics[metric] += 1
            return
        if len(self.events) >= self.capacity:
            self.metrics["capacity_dropped"] += 1
            return
        self.events[event.event_id] = (event, payload, now)
        self.metrics["received"] += 1
        if not delivery.authenticated:
            self.metrics["unauthenticated"] += 1

    def alerts(self) -> list[Alert]:
        self.prune()
        alerts = []
        for event, _, received_at in self.events.values():
            relevant, distance = relevance(self.position, event)
            if relevant and event.category in CATEGORIES:
                alerts.append(Alert(event, distance, received_at))
        return sorted(alerts, key=lambda alert: (alert.distance_m, alert.event.event_id))

    def close(self) -> None:
        self.transport.close()
        self.events.clear()
