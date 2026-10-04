# Security and abuse model

Status: preliminary; v1 simulator is unauthenticated and unsuitable for public
safety use. No security mechanism is described as implemented unless stated.

Assets: relevant fresh reports, availability on constrained links, location
privacy, trustworthy update/recovery paths and radio compliance. Boundaries:
physical button/GNSS, BLE phone, application payload, bearer/gateway and firmware
supply chain. Assume attackers hear, inject, replay and alter traffic, create
many pseudonyms, lie about location and compromise an individual device.

| Threat | Implemented foundation | Missing production protection |
| --- | --- | --- |
| Malformed/oversized input | Exact envelope size, field bounds, controlled errors | Embedded parser fuzzing and secure BLE framing |
| Replay/stale information | Creation/TTL expiry, bounded ID cache, duplicate/conflict rejection | Authenticated creation time and hostile clock handling |
| Flooding | Global receive-window and retention bounds, bounded simulator queue | On-air access fairness, prioritisation and ingress controls |
| False locations/reports | Radius/time checks and conservative relevance | Position plausibility, independent corroboration and trust policy |
| Sybil identities | None | Decentralised resistance is unresolved; fresh keys are not independent people |
| Message tampering | None | End-to-end signed envelope; signature identifies a key, not report truth |
| BLE takeover | Design only | Authenticated pairing, replay-resistant commands, stationary consent |
| Malicious updates | No firmware | Signed release manifests, rollback/recovery, boot validation and debug lifecycle |
| Tracking | No persistent wire source ID | RF/IP metadata correlation and inference protections remain |

The current global limiter can itself be exhausted by an attacker and does not
prevent radio airtime denial. Retention policy drops new reports rather than
forgetting active duplicate IDs; this protects replay memory but can exclude
legitimate new hazards. Record capacity/rate counters so the limitation is visible.

Proposed trust experiments: event-specific signatures; independent observations
rather than raw vote counts; bounded confirmations/disputes; local operator trust
for infrastructure without central login; plausibility windows without persistent
location histories. Do not promote a confidence score until it has an adversarial
calibration method. A single malicious signer remains malicious.

Public pilot gate: threat review, authenticated envelope, clock/fix handling,
receive/send budgets, update recovery, abuse monitoring and opt-in retention.
No automatic emergency dispatch or driving decisions. Upstream network identity
security does not replace application-level source authenticity after forwarding.
