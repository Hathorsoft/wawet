# Reticulum integration spike

Status: actual local experiment, not a production `ReticulumTransport`.

## Reproduce

Review [dependency licensing](../../LICENSING.md). Create a separate environment
if you want to keep the simulator environment free of RNS:

```sh
python3 -m venv /tmp/wawet-rns-venv
/tmp/wawet-rns-venv/bin/python -m pip install -e . -r tools/rns-requirements.txt
PYTHON=/tmp/wawet-rns-venv/bin/python ./scripts/rns-spike
```

The script creates two temporary, independent RNS configurations, disables
shared-instance operation and transport forwarding, and binds a temporary TCP
server to **127.0.0.1 only**. The second process uses a TCP client. Neither joins
public infrastructure nor enables AutoInterface. Temporary state is cleaned up
and child processes have bounded timeouts. Socket-restricted environments may
require permission to run local network tests. No user RNS configuration changes.

API surface inspected in the installed RNS 1.5.5 source: `Reticulum(configdir=)`,
`Destination` with `IN`/`OUT` and `PLAIN`, `set_packet_callback`, `Packet.send()`
and `exit_handler`. Original Wawet glue demonstrates direct packet delivery.

## EXPERIMENTAL RESULT — 4 October 2026

Environment: macOS, Python 3.11.4, RNS 1.5.5; pinned optional dependencies in
[requirements](../../tools/rns-requirements.txt). Command:
`PYTHON=.venv/bin/python ./scripts/rns-spike`.

```json
{
  "rns_version": "1.5.5",
  "medium": "TCP loopback",
  "processes": 2,
  "payload_bytes": 38,
  "payload_match": true,
  "authenticated": false,
  "routed": false,
  "event_id": "0102030405060708090a0b0c0d0e0f10"
}
```

Receiver parsing used Wawet `decode`; the parent verified exact payload equality.
Creation time is current at execution, so the full payload changes between runs.
The deterministic protocol vectors are tested separately. The spike fails
rather than reporting success if dependencies, delivery or equality checks fail.

## Limits and next gate

PLAIN destinations do not supply sender identity, encryption or routed
identity-based reachability. No RNode, LoRa, HaLow, path discovery, automotive
hardware, mobile peers or production application queue was tested. This
experiment establishes that the installed RNS API can carry and deliver the
application bytes across two processes. Next, test authenticated identity-based
delivery with controlled loss and contact deadlines before implementing an
adapter. Run that independently of the lightweight default CI.
