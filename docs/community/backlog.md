# First backlog

Suggested issues only; none created on GitHub. Gate tasks precede product commitments.

| ID | Task / labels | Acceptance criteria | First contributor? |
| --- | --- | --- | --- |
| 01 | Resolve exact-version Reticulum/LXMF distribution scope (`area:licensing`, `priority:gate`) | Document restrictions, permitted Wawet distribution and legal review outcome; do not assume MIT. | No |
| 02 | Select two regional RNode development units (`area:hardware`, `priority:gate`) | Compare exact supported board revisions, UK-suitable antenna/profile and current supplier quotes; select only after host role is understood. | No |
| 03 | Test authenticated RNS delivery and contact churn (`area:network`, `priority:gate`) | Two isolated hosts, SINGLE destinations, discovery/latency/loss overhead, timeouts and stale queue handling; raw results. | No |
| 04 | Measure standalone application-host options (`area:hardware`, `priority:gate`) | Run parser/event queue on candidate MCUs/hosts and record memory/current/cost; state networking capabilities separately. | No |
| 05 | Build the UK radio profile and conformity plan (`area:regulatory`, `priority:gate`) | Complete applicable IR2030 rows and standard editions with exact band/power/antenna/access configuration and lab review. | No |
| 06 | GNSS versus phone location experiment (`area:hardware`, `priority:next`) | Cold/warm starts, no-phone use, bad sky/stale fixes, locked phone permissions/BLE and cost; decision with evidence. | No |
| 07 | Extend contact simulation scenarios (`area:simulation`, `priority:next`) | Passing vehicles, convoy and rural/dense contacts as deterministic fixtures with delivery/expiry metrics. | Yes, with maintainer scope |
| 08 | Measure radio airtime and burst delivery (`area:network`, `priority:next`) | Two radios, complete frames/control traffic, legal access budget, simultaneous senders and contact deadlines. | No |
| 09 | Compare event encodings (`area:protocol`, `priority:next`) | Compare byte sizes/parser footprint with bounded optional fields and signatures, maintain published v1 vectors. | Yes, with maintainer scope |
| 10 | Prototype tactile button taxonomy (`area:hardware`, `priority:next`) | Three/four-input stationary mockups; differentiated touch, accidental activation, feedback and undo study. | No |
| 11 | Validate automotive USB power boundary (`area:hardware`, `priority:next`) | Adapter/cable comparisons, ignition/brownout, abrupt removal and parked standby measurements. | No |
| 12 | Evaluate antenna placement and modular mounting (`area:hardware`, `priority:next`) | Supplied antenna RF measurements in representative vehicles plus safe placement, strain and removal assessment. | No |
| 13 | Define thermal and vibration requirements (`area:hardware`, `priority:next`) | Measured environments, component/enclosure limits, UV/adhesive tests and lab test plan; no invented ratings. | No |
| 14 | Specify authenticated event envelopes and abuse tests (`area:security`, `priority:gate`) | Signature/domain separation, key lifecycle, payload budget, Sybil/flood/replay limitations and corroboration tests. | No |
| 15 | Review event privacy and retention (`area:privacy`, `priority:next`) | Identify wire/link correlations, define erasure schedule and participant-data handling; threat-review findings. | No |
| 16 | Complete prototype BLE control and pairing design (`area:mobile`, `priority:next`) | Define reserved command/result bodies, MTU/replay tests and authenticated no-display ownership flow. | No |
| 17 | Test offline phone speech (`area:mobile`, `priority:next`) | Android/iOS language/device offline matrix, permissions, latency and fail-without-upload behaviour. | Yes, with maintainer scope |
| 18 | Verify Waycast and broader prior-art claims (`area:docs`, `priority:next`) | Find repositories/licences and reproducible independent evidence; document unverified claims without importing code. | Yes, with maintainer scope |
| 19 | Measure UK HaLow infrastructure options (`area:infrastructure`, `priority:later`) | Regional module quotes, driver/firmware licences, legal profiles and measured IP goodput/current. | No |
| 20 | Evaluate Relay versus Gateway minimum roles (`area:infrastructure`, `priority:next`) | Proven forwarding capability, power/airtime budget and total cost; distinguish modem, transport and propagation. | No |

Recommended next five: **01–05**. Legal/host/radio feasibility gates should precede custom PCB, mobile app and public vehicle trials.

## Gates 01–05 progress

See the [desk-first review pack](../research/feasibility-gates.md) for evidence,
review briefs and unresolved acceptance criteria. No gate is complete.

Task **03** now has a [repeatable contact campaign/runbook](../research/contact-campaign.md).
Local controlled IP measurements are preparation; two physical hosts and later
agreed performance thresholds remain outstanding.

A01 review/check/local commits are complete; the [project plan](../project-plan.md)
now schedules **A02: agree feasibility thresholds and host role** next. Gates
01–05 still require their full acceptance evidence; no gate is closed by A01.

## A02 agreed criteria

Tasks 01, 03, 04, 07 and 09 must use the [A02 criteria record](../research/feasibility-thresholds.md)
agreed on 4 October 2026. Task 05 still requires 04; tasks 02/08 retain their
registered prerequisites. Agreed limits are not gate closure or measured results.

## Task 07 completed — 4 October 2026

[Four deterministic contact scenarios](../research/contact-scenarios.md) now cover
passing, convoy, rural and dense contacts with delivery/expiry counters and
reproducible results. Task 07 is complete locally; 53 tests and contributor checks
passed. This is simulation only. Task 09 follows in the software sequence; task 08
still requires 02/03/05/14 and approved RF testing. Gates/HOLD remain unchanged.

## Task 09 completed locally — 4 October 2026

The [bounded encoding comparison](../research/encoding-comparison.md) records
exact bytes, desktop parser timing/allocation and optional/signature-placeholder
bounds for binary and restricted CBOR profiles. Frozen v1 vectors are unchanged.
MCU/whole-host memory acceptance remains task 04. Task 18 is next eligible; task 14
still needs physical-host task 03. Gates and HOLD remain unchanged.
