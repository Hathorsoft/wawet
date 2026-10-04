# Wawet Drive product requirements

Status: paper-level product requirements, not a certified hardware specification.
Audience: ordinary drivers; they should not need to understand networking.
Hathorsoft manufactures the official appliance; compatible third-party designs
remain possible. No requirement below claims existing hardware implementation.

## MUST

| ID | Requirement | Acceptance evidence before product release |
| --- | --- | --- |
| D01 | Common reports use multiple tactile physical inputs without opening an app | Stationary prototype study with eyes-off-road, error and accidental-press measures; taxonomy/button count selected from results |
| D02 | Useful basic operation without phone/cloud/account/recurring fee | Demonstrate receipt and suitably located reporting with phone absent; state limitations honestly when no fresh fix/time exists |
| D03 | Never invent current location or time from stale/unavailable data | Fix freshness/accuracy policy, startup/time-loss tests and clear degraded feedback; uncertain reports withheld or explicitly marked in a later protocol |
| D04 | Complete supplied antenna and safe simple plug/mount installation | RF testing in representative vehicles and installation study; user does not assemble antenna |
| D05 | Regional compliant radio profile, independent of event protocol | Reviewed UK matrix, final RF configuration and whole-product conformity evidence |
| D06 | Protected power path, safe restart and abrupt-loss behaviour | Cranking-like brownout, rapid cycling, parked live USB and transient tests; avoid partial persistent writes |
| D07 | BLE pairing/configuration preserves basic operation and privacy | Permission denial/disconnect tests, authenticated control, bounded frames; no compulsory phone onboarding for basic use |
| D08 | Stale events expire; duplicate and input limits enforced | Device tests against published vectors, TTL/flood scenarios and clock/fix fault cases |
| D09 | Minimal identity/location retention; no routine tracking broadcasts | Privacy review, packet inspection and expiry tests; no raw audio on radio |
| D10 | Recoverable firmware updates and ownership/service lifecycle | Power-interrupted update, rollback/recovery, source and installation information consistent with licences |
| D11 | Cost reviewed from first architecture choices | Current supplier quotations, yield/assembly/packaging/warranty/certification model; £30–£50 remains an aspiration |
| D12 | Mount/antenna/cables do not obstruct visibility or create impact hazards | Vehicle placement and distraction assessment; no unsupported legal-compliance claim |
| D13 | Diagnostic/service access without silent public identity disclosure | Local opt-in diagnostics, manufacturing test pads, failure-code documentation |
| D14 | Defined thermal, UV, vibration and lifecycle limits | Requirements derived from measured vehicle environments; test to chosen limits before specifying a rating |
| D15 | Manufacturing traceability, supply continuity and compliance documentation | BOM alternatives, board revision, firmware revision, RF/functional QA, instructions and warranty process |

## SHOULD

- Use USB-powered core electronics with regional accessories, if safe/cost
  comparison supports it. Do not expose the baseline PCB directly to vehicle 12 V.
- Prefer independent GNSS for standalone located reports, with phone location
  as an optional improved source. Onboard GNSS is not instant: acquisition,
  tunnels, heated windscreens, poor sky view and time validity need testing.
- Provide a brief configurable acknowledgement and a separate degraded/no-fix
  indication; no persistent bright display or distracting repetitive alerts.
- Offer modular mount attachment, strain relief and easy removal; do not freeze
  electronics around a vent/adhesive/suction mount before comparative trials.
- Support accessible tactile differentiation and understandable labels/settings
  across languages; stationary configuration, deliberate cancellation and clear
  feedback on accidental presses.
- Document serviceability, teardown, replaceable accessories and support lifetime.
  Retain physical recovery/debug access without making malicious updates easy.
- Use the phone for maps, report history, rich input, offline dictation and
  firmware management. Baseline includes neither microphone nor speech processor.

## COULD

Validated fleet installations, protected hard-wire power, IMU-assisted motion
wake, haptics if useful, richer stationary phone diagnostics and optional vehicle
integration. Every addition must justify cost, power, space, testing and privacy.

## WON'T YET

A final button taxonomy/count, display, consumer camera/enforcement mapping,
vehicle CAN integration, built-in speaker/microphone, HaLow on Drive, battery,
large mobile app, Android Auto/CarPlay approval, custom PCB/enclosure, emergency
service guarantees, autonomous driving decisions or manufacturing certification.

## Unsettled choices

GNSS vs phone location, host processor needed beside RNode, power connector/
adapter, parked power budget, enclosure materials and temperature range are
open. See [open questions](open-questions.md), [concepts](hardware-concepts.md),
[feature matrix](feature-matrix.csv), [BLE design](ble-gatt.md) and
[human factors](human-factors.md). Verify stale-fix and unauthenticated-event
handling before vehicle trials, not after component selection.
