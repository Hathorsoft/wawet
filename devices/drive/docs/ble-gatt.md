# Proposed BLE GATT design

Status: Proposed, no firmware or mobile implementation. This is an application
control channel, not a replacement radio network. Baseline reporting cannot
require a continuously paired phone. Do not reserve production UUIDs before
reviewing interoperability and pairing UX.

For prototype interoperability use service
`5e7c1000-6c7d-4c98-a278-1a7f2d34a001`; characteristic UUIDs replace `1000`
with `1001`…`1005`. These are project-chosen prototype UUIDs, not Bluetooth SIG
assigned numbers or a certified profile.

| Suffix | Characteristic | Properties / access | Purpose |
| --- | --- | --- | --- |
| 1001 | Capabilities | Read; public non-identifying data | BLE protocol version, device role, supported envelope versions, max message size |
| 1002 | Command | Write with response; encrypted authenticated pairing | Stationary configuration, consent, fresh phone fix, optional report request |
| 1003 | Result | Indicate; paired | Correlated command acknowledgement/error, never assume a radio recipient received it |
| 1004 | Events | Notify; paired opt-in | Bounded received/report stream to phone; no raw movement broadcast |
| 1005 | Diagnostics | Read/notify; paired explicit opt-in | Aggregate counts and fault state; no stable identity/location by default |

Capabilities is the fixed 8-byte structure: uint8 BLE version (=1), uint8 role
(1 Drive), uint16 event-version bitset (bit0 v1), uint16 maximum logical message
(512), uint16 feature bitset (initially 0), all big endian. Unknown bits ignored.

## Proposed framing

Every fragment begins with 8 bytes: uint8 framing version (=1), uint8 operation,
uint16 request ID, uint16 total body length, uint16 body offset, big endian.
Fragment data must fit negotiated ATT MTU minus ATT overhead and this header.
For default MTU 23 that leaves 12 body bytes. Capabilities uses its fixed format,
not this header. Reassembly accepts one request per connection, total ≤512 bytes,
contiguous offsets only, no overlap, and a five-second timeout. Reject gaps,
wrong versions, changing lengths or replayed completed request IDs. Disconnect
clears pending state. Body syntax is documented per operation, not arbitrary JSON.

Prototype operations: 0x01 read configuration, 0x02 request stationary
configuration change, 0x03 supply fresh location/time, 0x04 submit event envelope,
0x05 diagnostics consent, 0x06 request firmware-update handoff, 0x80 result.
Only 0x04 has a body specified now (the exact 38-byte v1 envelope). Other command
bodies and the result format remain reserved pending the firmware prototype;
unsupported commands must be rejected, not guessed. This is therefore a draft
GATT design, not a complete production control protocol.

Pairing/control questions: a no-display product needs tested authenticated
out-of-band provisioning or another suitable mechanism. Do not label “Just Works”
MITM-resistant. Require deliberate physical confirmation while stationary for
ownership/reset operations. Keep secret provisioning material out of public
capabilities/diagnostics. Firmware transfer needs a separate signed, resumable,
recoverable design; a BLE write response does not authorise arbitrary flashing.

Negative tests required for implementation: MTU 23, long frames, interleaved IDs,
replay, pairing downgrade, partial transfer/disconnect, expired phone fix,
permission denial, update power loss and ownership reset. Phone background
limitations and reliable stationary-state detection remain open.
