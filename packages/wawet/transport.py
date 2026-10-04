"""Application-facing delivery boundary, independent of underlying networks."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Delivery:
    received_at: int
    medium: str
    authenticated: bool = False


Receiver = Callable[[bytes, Delivery], None]


class EventTransport(Protocol):
    def subscribe(self, receiver: Receiver) -> None: ...
    def send(self, payload: bytes) -> None: ...
    def close(self) -> None: ...
