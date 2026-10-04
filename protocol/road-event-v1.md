# Experimental road event v1

SPDX-License-Identifier: Apache-2.0

Status: Experimental. Version 1 is a research envelope, not a secure production
protocol. The numeric magic has no branding dependency and no registered
allocation. It can cross any byte transport; regional radio settings are not
fields in the event. Implementations must not claim production compatibility.

## Wire representation

Exactly **38 bytes**, network byte order (big endian), no padding, compression,
checksums, signature, identifier of the reporting vehicle or trailing bytes.
Integers are unsigned unless marked signed. Coordinates use WGS84 degrees.

| Offset | Bytes | Field | Valid values |
| --- | --- | --- | --- |
| 0 | 2 | Magic | `a7 e1` |
| 2 | 1 | Version | `01` |
| 3 | 16 | Event ID | Opaque random 128-bit ID; all-zero value invalid |
| 19 | 1 | Category | 1–255; unknown values preserved |
| 20 | 4 | Latitude, signed | Degrees × 100000; −9000000…9000000 |
| 24 | 4 | Longitude, signed | Degrees × 100000; −18000000…18000000 |
| 28 | 2 | Affected travel heading | Centidegrees 0…35999; 65535 means unknown |
| 30 | 4 | Creation time | Unix UTC seconds 0…4294967295 |
| 34 | 2 | TTL | 1…3600 seconds |
| 36 | 2 | Relevance radius | 1…10000 metres |

The size and bounds are application design choices, not inferred LoRa limits.
Unknown heading is the only optional value in this version. The simulator uses
vehicle heading as a proxy for affected travel direction; these can differ.
Never infer lanes from this field. Coordinates have approximately metre-scale
quantisation; the protocol does not encode accuracy or source quality yet.

Categories: 1 road hazard, 2 stopped traffic, 3 collision. These are provisional
experiment labels, not a settled physical-button taxonomy. Category zero is
reserved and rejected. Unknown categories can be retained until expiry but
must not be guessed into a named alert. A different version or magic is rejected.

## Receiver behaviour

1. Enforce exact length before parsing. Validate every field; no partial frames.
2. Expire at `now >= created_at + ttl`. Do not extend lifetime on receipt.
3. Reject creation more than 30 seconds in the future. This tolerance is an
   experimental local policy, not a guarantee of synchronised clocks.
4. Suppress identical event IDs and bytes. Same ID with different bytes is a
   conflict: retain the first, count and reject the conflicting payload.
5. Prune expired state before retention. Defaults: at most 1024 events and 120
   delivery attempts per 60-second window, including malformed messages. Drop
   new events at capacity instead of evicting active duplicate records.
6. Alert only for known categories within the event radius. For a known affected
   heading require at most 60° difference; outside 25 m require the hazard to
   be within 90° of the vehicle's forward bearing. Recompute after movement.

Rate limiting is global local protection, not Sybil resistance. Neither an
attacker's claimed radius nor position is trusted. A compromised sender can
choose many fresh IDs. There is no production broadcast profile.

## Identity, renewal and extensions

The event ID identifies a report, not a person. Reference code generates random
UUID bytes; examples freeze IDs for reproducibility. Retransmit identical bytes
for the same report. Renewal requires a new observation and new ID. Confirmation,
dispute and supersession are not encoded or implemented: a later design must
reference a prior ID, bound authority and preserve the original expiry.

Free text, confidence, accuracy, lane/road context and extension metadata are
not transmitted. A future version must add explicit versioned structure and
bounds rather than appending undocumented bytes. Investigate a signed envelope
with event-specific keys and exact signature domain separation before public
radio pilots. Transport authentication cannot authenticate a forwarded report's
origin by itself. There is no encryption or integrity protection in v1.

## Examples

The [canonical vectors](vectors/v1.json) specify all fields and exact bytes.
The north-hazard example has latitude 52.2°, longitude 0.9°, heading 0°,
creation time 1801652400, TTL 900 s and radius 5000 m:

```text
a7e1010102030405060708090a0b0c0d0e0f1001004fa6a000015f9000006b6308b003841388
```

The second vector covers negative coordinates, unknown category and absent
heading. Tests decode and encode both directions. Invalid-frame tests enforce
version, bounds, sentinel, length and expiry policies.
