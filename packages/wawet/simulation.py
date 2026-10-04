"""Deterministic contact network; no RF, routing or store-and-forward claims."""

import heapq
from dataclasses import dataclass, field

from wawet.transport import Delivery, Receiver


@dataclass
class ManualClock:
    now: int = 1801652400

    def __post_init__(self) -> None:
        if type(self.now) is not int or self.now < 0:
            raise ValueError("clock requires a nonnegative integer timestamp")


@dataclass(order=True)
class Pending:
    due: int
    sequence: int
    sender: str = field(compare=False)
    recipient: str = field(compare=False)
    payload: bytes = field(compare=False)


class SimulatedNetwork:
    def __init__(self, clock: ManualClock, latency: int = 1, capacity: int = 4096) -> None:
        if type(latency) is not int or latency < 0 or type(capacity) is not int or capacity < 1:
            raise ValueError("invalid network limits")
        self.clock = clock
        self.latency = latency
        self.capacity = capacity
        self.endpoints: dict[str, SimulatedTransport] = {}
        self.links: set[frozenset[str]] = set()
        self.queue: list[Pending] = []
        self.sequence = 0
        self.dropped = 0

    def endpoint(self, name: str) -> "SimulatedTransport":
        if not name or name in self.endpoints:
            raise ValueError("endpoint name must be unique and nonempty")
        endpoint = SimulatedTransport(self, name)
        self.endpoints[name] = endpoint
        return endpoint

    def connect(self, a: str, b: str, enabled: bool = True) -> None:
        if a == b or a not in self.endpoints or b not in self.endpoints:
            raise ValueError("two existing, different endpoints required")
        link = frozenset((a, b))
        if enabled:
            self.links.add(link)
        else:
            self.links.discard(link)

    def publish(self, sender: str, payload: bytes) -> None:
        if type(payload) is not bytes or len(payload) > 512:
            raise ValueError("transport requires at most 512 bytes")
        for name in sorted(self.endpoints):
            if frozenset((sender, name)) in self.links:
                if len(self.queue) >= self.capacity:
                    self.dropped += 1
                    continue
                self.sequence += 1
                heapq.heappush(
                    self.queue,
                    Pending(
                        self.clock.now + self.latency,
                        self.sequence,
                        sender,
                        name,
                        payload,
                    ),
                )

    def advance(self, seconds: int) -> None:
        if type(seconds) is not int or seconds < 0:
            raise ValueError("clock cannot move backwards or by fractional seconds")
        target = self.clock.now + seconds
        while self.queue and self.queue[0].due <= target:
            pending = heapq.heappop(self.queue)
            self.clock.now = pending.due
            endpoint = self.endpoints.get(pending.recipient)
            if (
                endpoint is not None
                and endpoint.receiver is not None
                and frozenset((pending.sender, pending.recipient)) in self.links
            ):
                endpoint.receiver(pending.payload, Delivery(self.clock.now, "simulation"))
            else:
                self.dropped += 1
        self.clock.now = target


class SimulatedTransport:
    def __init__(self, network: SimulatedNetwork, name: str) -> None:
        self.network = network
        self.name = name
        self.receiver: Receiver | None = None
        self.closed = False

    def subscribe(self, receiver: Receiver) -> None:
        if self.closed:
            raise RuntimeError("transport is closed")
        self.receiver = receiver

    def send(self, payload: bytes) -> None:
        if self.closed:
            raise RuntimeError("transport is closed")
        self.network.publish(self.name, payload)

    def close(self) -> None:
        self.closed = True
        self.receiver = None
        self.network.links = {link for link in self.network.links if self.name not in link}
