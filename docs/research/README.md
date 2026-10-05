# Research index and evidence standards

**Current status — 4 October 2026:** task 01 is complete for the bounded reviewed scope; see the [adopted maintainer decision](distribution-decision.md). Original Wawet work and optional user-installed RNS research continue with conditions; upstream redistribution and commercial bundles remain unapproved. G01 remains HOLD; tasks 02–05 remain open. Earlier pending-adoption, mandatory-review and uncommitted-status entries below are historical. The maintainer subsequently authorised committing and pushing this decision package.

Research checked on **4 October 2026**. Mutable upstream URLs are discovery
sources, not frozen manufacturing specifications. Record exact dependency
versions and part revisions before releasing a product.

Use these labels: **FACT** (primary source), **ASSUMPTION** (unmeasured estimate),
**EXPERIMENTAL RESULT** (commands, environment and output), **DESIGN DECISION**
(explicit policy), **OPEN QUESTION** (not resolved). Marketing performance
claims are not measured Wawet results. Do not infer regulatory compliance from
a module listing, a video or a simulation.

| Track | Current result |
| --- | --- |
| [Reticulum](reticulum.md) / [local spike](reticulum-spike.md) | Actual direct local delivery; licensing and standalone edge work remain |
| [LoRa/RNode](lora-rnode.md) | Modem/host distinction; two-board experiment defined |
| [HaLow](halow.md) | Infrastructure candidate; UK profile and quotations unverified |
| [UK regulation](uk-regulatory.md) | Primary-source matrix, not permission to transmit |
| [Amateur radio](amateur-radio.md) | Optional track; encrypted consumer carriage not approved |
| [Phone speech](phone-speech.md) | Platform APIs exist; offline language/device tests needed |
| [Prior art](prior-art.md) | Task 18 desk review complete; eight-system evidence register and pinned Waycast unit-test reproduction; physical claims unverified, no imported code |

Each experiment should record hypothesis, source revisions, physical setup,
configuration, measurement method, raw observations, limitations and next gate.
Publish negative results. A proposed ADR is not a fact; a simulator result is
not a field result.

The [feasibility gate review pack](feasibility-gates.md) records follow-up evidence
and the current HOLD decision for gates 01–05.

The [authenticated contact campaign](contact-campaign.md) adds repeated controlled
IP contact measurements and a two-host private-LAN runbook. Physical-host
acceptance remains pending.

[Deterministic contact scenarios](contact-scenarios.md) complete task 07 with
passing, convoy, rural and dense fixtures, delivery/expiry metrics and reproducible
synthetic results. They do not establish physical or radio acceptance.

[Event-encoding comparison](encoding-comparison.md) completes task 09's bounded
desktop research with original binary/CBOR codecs and reproducible size/parser
measurements. Signature placeholders are not cryptographic verification; MCU
memory and production protocol selection remain open.

[Task 01 distribution review dossier](distribution-review.md): exact experimental
artefacts and licence evidence prepared; qualified written review pending.

[Task 01 self-review](distribution-self-review.md): bounded agent-assisted evidence
assessment complete; recovered vendored notices and static native observations.
Maintainer adoption and qualified-review acceptance remain pending; paid review
is deferred and G01 remains HOLD.

Task 01 assurance update: maintainer self-review and a dated release/risk decision
now replace mandatory external review. Earlier pending-qualified-review notes are
historical. Task 01 remains open pending the maintainer decision; G01 stays HOLD.

[Task 04 host comparison and bench readiness](standalone-host-bench.md): Zero 2 W
first-screen recommendation, equipment checklist and measurement/evidence runbook.
Preparation complete; no equipment or measurements, task 04 open and G01 HOLD.

Task 04 follow-up — 5 October 2026: the [bench workload driver](../../tools/host_bench_workload.py)
implements the documented synthetic recipe. Software preparation is complete;
physical acceptance and G01 HOLD remain unchanged. See the bench runbook for
measurement commands, phase alignment and remaining equipment requirements.
