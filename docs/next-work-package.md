# Next work packages — 5 October 2026

## TL;DR

Next is **04: measure a real standalone application host**, starting with the
already recommended Zero 2 W host-only screen. This is the next unfinished stage
in the feasibility plan: we must find out whether the application and networking
can fit a practical device before selecting radios or designing hardware.
You will get reproducible memory, power, startup/recovery and runtime evidence,
a cost ledger and a clear PASS/HOLD/REVISE recommendation. A host-only result
is partial evidence, not approval of a complete Drive.

Completing task 04 unlocks task 05's radio/conformity review; task 02 still needs
both 04 and 05. Independently, **03: run the authenticated two-host contact
campaign** can proceed once two physical computers and clock evidence are
available. Completing 03 unlocks task 14 together with completed task 09.
G01 remains HOLD until all its registered predecessors are complete.

The repository records that no equipment is available. The next input needed
from the maintainer is access to the board and measurement chain, or a decision
on borrowing/acquiring them. For task 03, identify two available computers and a
private wired test arrangement. No new software implementation is needed to
start these packages; this plan authorises no spending or external contact.

## Repository assessment

Inspected a clean `main` checkout at `69bed67`, with no uncommitted work and no
local ahead/behind count against the cached `origin/main`. Recent Git history
confirms task 01's adopted bounded decision (`44815e3`), task 07 (`c0dd25b`),
task 09 (`3e247c8`) and task 18 (`2f21ac5`). Host bench preparation (`a2f40d8`),
the workload driver (`a5bba59`) and contact timing corrections (`69bed67`) are
committed. Earlier local/uncommitted notes remain historical. Cached tracking
state alone does not prove the live remote state.

Read AGENTS.md, README, handoff, project plan, backlog, licensing, architecture,
ADR index and research rules. The [task register](project-plan.md),
[backlog acceptance criteria](community/backlog.md) and
[A02 thresholds](research/feasibility-thresholds.md) govern this plan.
Preparation is complete; physical acceptance is not. No task status,
prerequisite, threshold or investment decision changes here.

## Package 04 — physical host screen

Follow the [existing bench runbook](research/standalone-host-bench.md), rather than
creating another driver or repeating completed desktop preparation. Divide the
work into sequential sessions; these are checkpoints, not effort estimates.

1. **Access and setup:** confirm the exact board revision, storage, power/data
   topology, observer and calibrated simultaneous V/I acquisition chain. Check
   sampling interval ≤1 ms, range/bandwidth, uncertainty and readiness-trigger
   capability before arranging a measurement session. Keep one-off equipment
   costs separate from recurring complete-unit cost. If access is unavailable,
   stop with HOLD and an explicit missing-equipment list.
2. **Runtime correctness:** freeze the OS image/hash, Python, optional pins,
   source/diff and services. Disable onboard radios; use private wired IP or
   loopback. Run the runbook's demo, tests, scenarios, encoding comparison and
   host workload check. Archive stdout/stderr/exits and source/vector hashes.
   Run the pinned authenticated smoke separately, including churn and absent
   discovery. Installation failures remain evidence; do not silently change pins.
3. **Memory and electrical screen:** warm up, then collect three complete
   ten-minute idle/ten-minute active workload runs, continuous memory snapshots
   at ≥10 Hz and simultaneous V/I at ≤1 ms. Document phase alignment and timing
   uncertainty. Add the separate overlapping RNS contention screen, recording
   process lifetimes. This does not prove an integrated application/RNS path.
   Retain high-water marks, swap/OOM evidence and a conservative peak bound.
4. **Startup/recovery:** collect ten cold boots and ten abrupt-loss/restart cycles
   with electrical power-on and readiness on a common timebase. Current software
   lacks autonomous input/network readiness wiring: record host-only observations
   as partial, with T04 HOLD until those markers exist and are validated. Do not
   substitute SSH login or import time. Record failures and filesystem recovery.
5. **Assessment:** preserve raw files with hashes, calibration and environmental
   notes; produce a criterion-by-criterion report and dated cost ledger. Use
   current delivered quotes when obtainable within authorised arrangements;
   estimates and missing assembly scope leave T09 HOLD. If the first candidate
   fails, propose a bounded alternative and explain the tradeoff before porting
   to an MCU or changing the architecture.

**Acceptance and validation:** task 04 needs actual candidate parser/queue and
networking evidence, bounded 1,024-event behaviour, successful expiry/recovery,
exact runtime and measured memory/current/startup/cost. T06 requires every
required processor's peak occupied memory ≤75% usable capacity and no swap/OOM;
RSS alone is insufficient. Compare host-only power upper bounds against T07's
2.5 W mean and 5 W peak, while retaining whole-assembly power HOLD. T04 requires
all ten fully instrumented readiness results ≤10 s; T08 is ≤0.10 W standby or an
explicit switched-power requirement; T09 is a complete quoted recurring cost
≤£25 at 1,000 units. Missing readiness, GNSS, modem, integrated workloads or quotes
must stay visible. T05 belongs to task 06; RF power evidence waits for an approved
setup. Do not mark task 04 complete merely because the host-only screen passes.

Deliver a new research results directory with raw series, JSONL, commands,
configuration/runtime identities, uncertainties, hashes, failures and evaluation.
Update handoff, validation and task 04 evidence links after actual execution;
update ADRs only if the evidence supports a changed decision. Run contributor
checks on any later source changes, plus the physical validation above.

## Package 03 — independently eligible two-host campaign

Task 03 does not depend on task 04. If two computers become available first, run
this package first; keep task 04 open. Follow the
[physical-host campaign runbook](research/contact-campaign.md).

1. Record two distinct physical hosts, OS/runtime/pins and identical source
   revision. Use isolated private wired IP, no public listeners or radio. Provision
   independent local keys/configs; exchange only public pins and verify fingerprints.
2. Establish sender/receiver clock offset and a conservative uncertainty/drift
   bound covering the entire run, with raw before/after observations. A clock
   configuration label alone is insufficient. Missing evidence leaves T03 and
   one-way latency HOLD; never subtract different hosts' monotonic clocks.
3. Run a short two-host diagnostic to check manifests, timing fields, lifecycle
   and collection. Then schedule the full serial 30-repetition campaign, reserving
   the runbook's several-hour continuous window. Preserve cold/warm 1/2/5/10 s
   cells, stable baseline, controls, socket reconnection, absent discovery and
   overload/recovery. Retain missed starts and failed workers in denominators.
4. Merge both role logs/exits/stderr and the identical manifest, verify hashes,
   then analyse with clock evidence. Review actual contact boundaries, distinct
   event/frame matching, signature/expiry rejection, stale queues, timeouts,
   discovery and traffic overhead. Archive failures as well as successful trials.
5. Publish a bounded physical-IP report and update task 03/handoff/validation.
   Controlled wired contacts establish no radio range, moving-peer performance,
   public report truth or production adapter readiness.

**Acceptance and validation:** two isolated physical hosts and SINGLE destinations;
reproducible raw discovery/latency/loss/overhead and timeout/stale-queue/recovery
results. Each cold/warm 5/10 s cell and stable baseline needs ≥30 observations,
≥29/30 distinct within-contact deliveries, and availability-to-validated-acceptance
p95 plus clock uncertainty ≤2 s. Combined uncertainty must be ≤100 ms. Keep 1/2 s
cells as characterisation. Missing/ambiguous timing or incomplete workers cannot
pass; invalid, expired or wrong-frame acceptance is a failure. Preserve historical
metrics and stricter contact results separately. Analyse against current T01–T03
rules and manually review provenance; the analyser cannot certify clock evidence.
Redact private keys/configs and use synthetic coordinates only.

## Repeated selection and stopping point

Reapplied dependency selection after planning 04, then independently eligible 03.
Neither planning completion nor committed preparation closes either task.

| Remaining work | Why it cannot be the next implementation package now |
| --- | --- |
| 04 | Board/instruments/physical measurements/quotes require maintainer arrangements |
| 03 | Two physical hosts/private wired setup and justified clock evidence require arrangements |
| 05 | Requires completed 04 and qualified lab assessment |
| 02 | Requires completed 04 and 05 |
| 14 | Requires completed physical task 03; task 09 alone is insufficient |
| 15 | Requires completed 14 |
| 08 | Requires completed 02, 03, 05, 07 and 14 and approved RF setup |
| G01 and all scheduled prototype/product/expansion tasks | Registered predecessor gates remain incomplete |
| D01/D02 | Explicitly deferred; require a separately chosen scope, not automatic expansion |

Stop here. Further planning commits would duplicate existing preparation or
pretend an unmet prerequisite had passed. No implementation was performed.
