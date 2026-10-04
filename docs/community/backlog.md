# First backlog

**Current status — 4 October 2026:** task 01 is complete for the bounded reviewed scope; see the [adopted maintainer decision](../research/distribution-decision.md). Original Wawet work and optional user-installed RNS research continue with conditions; upstream redistribution and commercial bundles remain unapproved. G01 remains HOLD; tasks 02–05 remain open. Earlier pending-adoption, mandatory-review and uncommitted-status entries below are historical. The maintainer subsequently authorised committing and pushing this decision package.

Suggested issues only; none created on GitHub. Gate tasks precede product commitments.

| ID | Task / labels | Acceptance criteria | First contributor? |
| --- | --- | --- | --- |
| 01 | Resolve exact-version Reticulum/LXMF distribution scope (`area:licensing`, `priority:gate`) | Document exact-version rights, restrictions and notices through maintainer self-review; record unresolved risks and a dated form-specific release decision. External legal review optional; do not assume MIT or claim legal approval. | No |
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
review briefs and unresolved acceptance criteria. Task 01 is complete for its bounded reviewed scope; gates 02–05 remain open and G01 remains HOLD.

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

## Task 18 completed locally — 4 October 2026

The [desk review](../research/prior-art.md) covers all eight existing systems with
sources, licence evidence, reproducibility limits and independent-evidence leads.
Waycast's attributable public repository and GPLv3 text were located; three
upstream test executables passed at a pinned revision without added dependencies.
Independent physical claims, first-publication chronology and full GUI reproduction
remain unverified. Task 18's bounded investigation is complete; no code imported.

Git confirms task 09 is committed at `3e247c8`; earlier uncommitted notes are
historical. Task 14 still needs physical-host task 03; tasks 01/04/03 require
external review or physical resources. Gates 01–05 and G01 HOLD remain unchanged.

## Task 01 dossier prepared — 4 October 2026

The [distribution dossier](../research/distribution-review.md) captures exact
experimental artefacts, licence evidence, native/vendored gaps and reviewer
questions. Qualified written review and a reviewed release approach remain
pending; task 01 is not complete. Task 18 is committed at `2f21ac5`. Gates/HOLD
and all registered prerequisites remain unchanged.

Documentation/evidence only; no runtime changes, outreach, purchasing, RF tests,
commit, push or publication occurred in this follow-up.

## Task 01 reviewer arrangement prepared — 4 October 2026

The [reviewer arrangement package](../research/distribution-review-arrangement.md) adds two UK legal-review
candidates, a community referral route, an unsent enquiry and an engagement
checklist. Starting tree was clean at `ff3df9f`, which commits the dossier;
earlier uncommitted entries remain historical. This package is local/uncommitted.
Reviewer selection, authorised contact, engagement terms and qualified written
review remain pending. Task 01 is open; gates 01–05 and G01 HOLD persist.
No stages or dependencies change: 14 still requires physical-host 03 and 09;
15 requires 14. No outreach, commissioning, spending, runtime changes, commit,
push or publication occurred. Validation is recorded in the validation document.

## Task 01 self-review direction — 4 October 2026

The maintainer declined hiring a reviewer: this is a solo free-time project.
The next package is [bounded maintainer self-review](../research/distribution-review-arrangement.md) of Q01–Q07,
vendor notices and form-specific distribution decisions. Reviewer routes and the
unsent enquiry remain historical preparation; external engagement is deferred.
Self-review can advance evidence and decisions but does not satisfy the existing
qualified-review acceptance criterion. No task dependency or gate criterion is
silently relaxed; task 01 remains open and G01 HOLD persists. No outreach or
spending is needed for the bounded self-review. That review is not yet completed.

## Task 01 bounded self-review completed — 4 October 2026

The [agent-assisted self-review](../research/distribution-self-review.md) assesses Q01–Q07, recovers
complete attributable ConfigObj/i2plib notices and records exact vendored
comparisons plus static macOS research-wheel observations. Notice retrieval gaps
are narrowed; modification authorship, native shipped notices/build provenance,
AI service data use and future-image scope remain unresolved. Its conservative
form-specific approach is proposed for maintainer adoption, not a recorded release
approval. Paid review is deferred; the existing qualified-review criterion remains
unsatisfied. Task 01 stays open, gates 01–05 and G01 HOLD persist. No prerequisites
or stages change. Prior local changes were preserved; this follow-up is uncommitted.
No packages installed/executed, outreach, spending, RF/road test or publication.

## Task 01 assurance decision — 4 October 2026

**DESIGN DECISION:** the maintainer explicitly chose to perform task 01 ourselves
and instructed updating the task accordingly. A documented maintainer self-review
and dated form-specific release/risk decision replace the previous mandatory
qualified external review for task 01. External advice is optional, not a required
paid prerequisite. Earlier qualified-review entries are historical and superseded
by this decision; no professional legal approval is asserted.

The [self-review](../research/distribution-self-review.md) supplies the evidence assessment. Task 01 remains
open until the maintainer records adopted distribution decisions, conditions and
residual risks, including unresolved AI data-use and provenance questions. This
instruction changes the assurance method; it does not itself approve a bundle or
adopt every recommendation. G01 stays HOLD and other task prerequisites and
technical/regulatory gates remain unchanged. Restricted upstream terms and notice
obligations are not waived. Re-review changed uses, releases and shipped builds.

## Task 04 bench preparation — 4 October 2026

Starting tree was clean at `44815e3`; task 01's adopted bounded decision is committed.
The maintainer confirmed no equipment is available. The [candidate comparison and
bench runbook](../research/standalone-host-bench.md) recommends Zero 2 W for the first host-only screen, compares
MCU/separate-host and constrained-endpoint arrangements, and defines equipment,
workloads, evidence and A02 evaluation. Preparation complete; task 04 remains open
for actual hardware/runtime/memory/current/startup/recovery/cost evidence. No
physical measurement, temporary workload driver or integrated readiness/validity
gate has been implemented. Next seek access to the board and measurement chain;
no purchase or external contact is authorised.

Tasks 05/02 retain 04 and 04/05 prerequisites respectively; task 03 still needs two
physical hosts and clock evidence, 14 requires 03/09, and 15 requires 14. G01 stays
HOLD. New validation is recorded separately; earlier status entries are historical.
Documentation only, local/uncommitted; no dependency/runtime/protocol changes,
package installation, upstream restricted-source review, RF/road test, commit,
push, PR or release occurred.
