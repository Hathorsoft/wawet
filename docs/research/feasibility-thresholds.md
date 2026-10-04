# A02 — Feasibility thresholds and host role

Drafted and agreed **4 October 2026**. **DESIGN DECISIONS**: maintainer agreed
to T01–T09 and the host boundary in this chat. A02 is complete; gates 01–05 and prototype investment **HOLD** remain
unchanged. These are agreed evaluation limits, not measured capabilities,
supplier prices, regulatory permission or product promises.

## Responsibility boundary

The standalone Drive must run event parsing, bounded retention, expiry, relevance,
input handling and feedback without a phone, account or cloud. An explicitly
identified application/network host must run the required Reticulum endpoint
and interface management. Application and networking may share a processor or
use separate processors; task 04 must prove the actual arrangement. RNode is the
radio modem, not evidence of an application or full RNS host. A phone may improve
location, maps and configuration but cannot be required for basic operation.

Count every required processor, bridge, regulator and interconnect in Drive's
memory, power and cost assessment. A separate bench computer is development
equipment only if the final Drive does not require it. Board selection remains
open. Do not infer CPython/RNS compatibility on an MCU or build another routing
stack. Preserve the existing EventTransport boundary and 38-byte v1 vectors.

## Agreed target table

All numbers below are **DESIGN DECISIONS for evaluation**, based on unmeasured
planning assumptions. They prioritise useful brief
encounters and modest USB power while testing the existing retail aspiration.
They do not derive from historical loopback performance.

| ID / metric | Agreed limit | Workload, method and rationale |
| --- | --- | --- |
| T01 latency | One-way p95 ≤ 2.0 s | Fresh single-event contact delivery, separately for cold/warm 5 s and 10 s cells and stable baseline; time from scheduled event availability to authenticated, decoded, unexpired receiver acceptance, including discovery wait. A 2 s budget leaves room within a 5 s encounter. Record send-to-accept latency separately. |
| T02 loss / contact | ≥ 95% eligible delivery in each cold/warm 5 s and 10 s cell and stable baseline; minimum useful contact 5 s | At least 30 independent trials per contact cell and 30 stable events. At 30 observations, require ≥ 29 deliveries. Run 1 s and 2 s cells with the same counts as characterisation, without mandatory delivery limits. These are empirical screening fractions, not statistical reliability certification or a moving-vehicle range claim. |
| T03 clock uncertainty | Combined cross-host offset uncertainty ≤ 100 ms | Save synchronisation evidence before/after runs and bound the error over the whole run. Evaluate T01 using p95 plus that bound; never subtract cross-host monotonic clocks. Missing or excessive uncertainty leaves latency unresolved. |
| T04 cold startup | Application/network readiness ≤ 10 s on every one of 10 cold boots | Measure power-on to parser/queue/input availability and networking stack/interface readiness, with valid injected time/location. Peer discovery is measured separately by T01/T02. This avoids a long appliance boot without disguising GNSS acquisition as software startup. |
| T05 location/time readiness | Valid located-report readiness ≤ 60 s on every one of 10 cold starts under documented favourable sky; invalid/stale data produces zero located reports | Measure separately from T04, with phone absent and an independent reference. Agreed evaluation policy: fix age ≤ 5 s, reported horizontal uncertainty ≤ 50 m, time uncertainty ≤ 1 s. These validity limits are assumptions, not proof of accuracy. Missing uncertainty is invalid. Show degraded feedback and withhold reports until valid. Task 06 validates/revises policy and poor-sky behaviour; A02/04 cannot close it. |
| T06 memory | Peak occupied memory ≤ 75% of usable capacity on each required processor | Exercise 1,024 retained events, valid/stale/malformed bursts, expiry/pruning, report/receive and simultaneous networking. Include application, network, OS/services and buffers. MCU: peak heap/stack/static allocation against usable RAM; OS host: peak system memory demand excluding reclaimable cache, no swap/OOM. Report process RSS separately. Reserve ≥ 25% headroom rather than choose a board prematurely. |
| T07 active power | Steady mean ≤ 2.5 W (500 mA); peak ≤ 5.0 W (1 A), at 5.0 V USB input | Whole standalone assembly, including host(s), modem, valid-location subsystem and feedback. Measure ten minutes idle-ready and ten minutes active/burst workload after warmup; each mean must pass. Capture startup/recovery peaks at ≤ 1 ms sampling, report instrument uncertainty and measured voltage; compare upper error bounds. A modest USB budget discourages hiding a costly extra host. RF workload waits for approved setup; earlier non-RF results are partial. |
| T08 parked standby | ≤ 0.10 W (20 mA) at 5.0 V if powered while parked | Ten-minute mean in explicitly defined standby; no claim of reception while asleep. If no compliant standby exists, document switched-power requirement and leave automotive power acceptance to task 11. This protects the intended parked-use boundary without assuming every socket switches off. |
| T09 recurring delivered cost | ≤ £25 per complete unit at a stated 1,000-unit scenario | Include all processors, radio, GNSS, antennas, power, cables, enclosure/mount, assembly/test, packaging, inbound delivery, unrecoverable taxes, yield/warranty reserve and tooling/conformity allocation. Exclude recoverable VAT and sales/channel margin; show those separately. This ceiling leaves some room within the £30–£50 retail aspiration but is not a margin or tax approval. Record dated quotes, quantities/currency/conversion assumptions and sensitivity; estimates alone cannot pass cost feasibility. |

Development equipment (two-host computers, instruments, test radios and fixtures)
has a separate one-off budget ledger. No spending ceiling or purchase is approved
by this document. Task 02 still needs an actual delivered two-unit quote; that
quote does not establish T09 at production volume.

## Evidence and evaluation rules

Use the [campaign runbook](contact-campaign.md) and preserve cold/warm discovery,
interface gating and socket reconnection as separate observations. Controlled IP
windows are not RF contact. Run sequentially on two physical hosts; record source
revision/diff, pinned dependencies, configurations, host identities, actual window
lengths, raw role logs, stderr/exits and clock evidence. No participant locations
or private keys belong in committed evidence.

Use the manifest's intended distinct events as the denominator, including missing
workers. Match delivered event ID and frame hash. Report intended delivery and
eligible delivery separately: only deliberately scheduled expiry probes are
excluded from the eligible denominator, not events expired because delivery was
slow. Count acceptance after the actual contact closes as a contact miss. Preserve
the analyser's existing fractions; calculate this stricter contact result in the
review record without changing runtime/analyser behaviour in A02.

Use nearest-rank p95 and report sample count, min, median and max. Failed/missing
trials cannot improve the denominator; invalid timing evidence requires repetition
and leaves the cell unresolved. T01 covers successful deliveries; T02 prevents
survivor-only latency from hiding losses. Capture intended-event availability as
well as receiver acceptance; if existing logs cannot establish that start point,
latency remains HOLD until task 03 adds the necessary evidence.

Adversarial, outage and overload scenarios must reject stranger/altered/malformed/
expired probes, withhold the deliberately stale outgoing frame, preserve original
bytes/creation time on explicit resend, bound callback queues and admit the recovery
event. Require zero invalid accepted frames, zero stale deliveries and zero worker
failures in the completed acceptance campaign. Maintain fixed worker deadlines;
no silent retries or discarded failure records. RNS byte counters and packed sizes
remain distinct from TCP traffic and radio airtime. Task 08 must later repeat the
relevant contact evaluation and full airtime accounting on a reviewed RF setup.

For hardware, record exact board/runtime, workload, instruments/calibration,
sampling, raw observations and failures. Repeat memory and power workloads three
times; all upper bounds must pass. Startup includes ten abrupt power-loss/restart
cycles with zero corrupted-state or recovery failures. No fresh fix/time means
withholding located reports, not fabricating data. Power manipulation is bench-only.

## Decision rules and worked review cases

- **PASS for an evaluated criterion:** complete appropriate evidence meets its
  agreed limit. This is not an automatic gate or investment approval.
- **HOLD:** agreement, hardware, instrumentation, clock evidence, quotes or required
  scenarios are missing. Local IP results cannot pass radio/product criteria.
- **REVISE:** adequate measurements miss an agreed limit or violate correctness.
  Record the failure, proposed architecture/product change and affected tasks/ADRs.
  Do not relax a limit silently; obtain maintainer agreement and preserve old values.

| Review case (hypothetical, not measured) | Outcome after target agreement |
| --- | --- |
| 29/30 within-window deliveries in each required cell, p95 1.8 s plus 0.1 s clock bound | T01/T02 pass if other evidence requirements hold; gates remain separately reviewed. |
| 28/30 cold 5 s deliveries, even with 30/30 at 10 s | REVISE T02; do not substitute the longer window. |
| 0/30 at 1 s but required 5/10 s cells pass | Characterise the short-contact limit; no T02 failure. |
| Delivery fractions pass but clock uncertainty is absent | Latency HOLD; delivery evidence retained. |
| Application ready in 8 s, no fresh fix at 60 s | T04 may pass; T05 REVISE on a valid favourable-sky test, or HOLD if that test is absent; zero located reports required. |
| Required host uses 80% RAM or 3 W steady input | REVISE T06 or T07; include that host even if marketed as a gateway. |
| Complete quoted recurring cost £29 | REVISE T09; do not omit the host or replace quotes with paper allowances. |

## Agreement and handoff

Maintainer agreement: **4 October 2026**. The maintainer replied “Agreed” to
explicit review of T01–T09 and the host boundary in this chat. All values were
accepted without changes. A02 is complete; this records criteria, not measured
feasibility. Future changes require rationale, dated maintainer agreement and
preservation of the previous values. No accepted limit remains TBD.

With agreement recorded, tasks 01, 04, 03, 07 and 09 become eligible as registered; task 05
still requires 04, task 02 still requires 04/05, and 08 retains all predecessors.
Physical hosts, candidate hardware, calibrated instruments, quotes and qualified
licensing/lab reviews remain outstanding. Gates 01–05 and G01 stay open; HOLD
persists. Task 18 is independently eligible after A01 independently of A02.
