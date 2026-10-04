"""A small reproducible demonstration of the application boundary."""

from wawet.geo import Position
from wawet.protocol import CATEGORIES, encode
from wawet.simulation import ManualClock, SimulatedNetwork
from wawet.vehicle import Identity, Vehicle


def main() -> None:
    clock = ManualClock()
    network = SimulatedNetwork(clock, latency=9)
    vehicles = {
        name: Vehicle(
            Identity(bytes([i]) * 16), position, network.endpoint(name), lambda: clock.now
        )
        for i, (name, position) in enumerate(
            [
                ("A", Position(52.2, 0.9, 0, 25)),
                ("B", Position(52.1883, 0.9, 0, 25)),
                ("C", Position(52.1883, 0.9, 180, 25)),
            ],
            start=1,
        )
    }
    network.connect("A", "B")
    network.connect("A", "C")
    print("Wawet local vehicle simulator — unauthenticated research events")
    print("Drive A and B travelling north; Drive C travelling south")
    event = vehicles["A"].report(event_id=bytes(range(1, 17)))
    print(
        f"\nDrive A reports ROAD HAZARD\nencoded ({len(encode(event))} bytes): "
        f"{encode(event).hex()}"
    )
    print("transmitting...")
    network.advance(9)
    for alert in vehicles["B"].alerts():
        seconds = alert.event.expires_at - clock.now
        print(
            f"Drive B received event: {CATEGORIES[alert.event.category]} "
            f"{alert.distance_m / 1000:.1f} km ahead; "
            f"expires in {seconds // 60}m {seconds % 60:02d}s"
        )
    print(f"Drive C: {len(vehicles['C'].alerts())} relevant alerts (opposite direction)")
    vehicles["A"].transport.send(encode(event))
    network.advance(9)
    print(f"Drive B suppressed {vehicles['B'].metrics['duplicate']} duplicate")
    network.connect("A", "B", False)
    vehicles["A"].report(event_id=b"\x55" * 16)
    network.advance(9)
    print(f"During outage: Drive B still has {len(vehicles['B'].alerts())} alert")
    network.connect("A", "B")
    network.advance(900)
    vehicles["A"].transport.send(encode(event))
    network.advance(9)
    print(
        f"After expiry: Drive B has {len(vehicles['B'].alerts())} alerts; "
        f"stale reports rejected: {vehicles['B'].metrics['expired']}"
    )
    print("No automatic retransmission, RF model, signatures or road-map matching are simulated.")


if __name__ == "__main__":
    main()
