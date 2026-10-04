# Agent handoff

Snapshot: **4 October 2026**, after initial foundation implementation and local
validation. This file is sufficient to understand the work without the founding
chat; linked documents contain the detailed specifications and evidence.

## Goal and current stage

Wawet should let an ordinary person plug a small inexpensive appliance into a
car, report common hazards by touch and benefit nearby users. The broader
ecosystem should support other communications applications and bearers. The
principle is sophisticated network, simple edge device. Hathorsoft intends to
sell official hardware; lawful third-party implementations and commercial
derivatives are permitted. Basic use must not require a cloud service or fee.

The foundation iteration is implemented locally. Radio, host-processing,
security, product-cost and regulatory feasibility remain open. This is phase 0,
not a product launch. A £30–£50 retail price is an aspiration to test.

The foundation is recorded in focused **Conventional Commits**, following
`1323fc6`, the ninth project-history milestone. The original concept notes and
milestone history are preserved. No remote push was performed for this handoff.
Check Git rather than assuming this snapshot is still current; another
user/agent may have committed or published subsequently.

## What works

- Multi-vehicle demo: a 38-byte hazard produces an alert 1.3 km ahead, filters
  the opposite direction, suppresses a duplicate, models an outage and expires.
- Versioned language-independent envelope with field validation, two canonical
  vectors, geographic/directional relevance and safe unknown-category handling.
- Bounded receive state and simulated delivery queue; ID conflicts, malformed
  input, future timestamps and expired reports are handled explicitly.
- Application logic accepts a swappable transport and injected clock; no radio
  frequency, RNS API or persistent reporter identity is embedded in the frame.
- Independently configured RNS 1.5.5 processes exchange exact application bytes
  over loopback TCP. This narrow experiment uses PLAIN destinations: it is
  neither authenticated nor routed and does not constitute a production adapter.
- 31 tests passed, plus Ruff lint/format, strict mypy, local file links and
  dependency checks. An offline wheel installation passed with no RNS installed.
  See [validation](validation.md) for commands, evidence and the repository tree.

## Code map and contracts

| File | Responsibility / entry point |
| --- | --- |
| [protocol.py](../packages/wawet/protocol.py) | Immutable `RoadEvent`, validation, `encode`/`decode`; [wire specification](../protocol/road-event-v1.md) is authoritative for v1 |
| [geo.py](../packages/wawet/geo.py) | `Position`, spherical distance/bearing and approximate relevance; not lanes or map matching |
| [vehicle.py](../packages/wawet/vehicle.py) | `Vehicle.report`, delivery validation/retention and `alerts`; local `Identity` is not an RNS key |
| [transport.py](../packages/wawet/transport.py) | `EventTransport.subscribe/send/close`, callback and `Delivery` metadata |
| [simulation.py](../packages/wawet/simulation.py) | Manual clock, named endpoints, contact links, bounded deterministic delayed delivery |
| [demo.py](../packages/wawet/demo.py) | Reproducible three-vehicle CLI demonstration |
| [tests](../tests) | Protocol vectors, bounds, application lifecycle, link loss, rate/capacity and geometry regression tests |
| [RNS spike](../tools/rns_spike.py) | Isolated real API experiment with timeouts/cleanup; optional [pinned requirements](../tools/rns-requirements.txt) |

Expiry uses the injected application clock. `alerts()` recomputes relevance
against the vehicle's current position but preserves first receive time.
Retention is pruned on access; there is no background erasure task. Global
rate limiting protects local processing but is not Sybil or on-air protection.
Links must exist at transmission and delivery; reconnecting does not replay
missed messages. There is no automatic forwarding or store-and-forward.

## Decisions versus experiments

Accepted: monorepo, Python foundation, application/transport separation,
simple-edge responsibility principle and original-work licence scope.
Experimental: Reticulum product suitability and fixed compact encoding.
Proposed/unresolved: hardware parts/host, production transport/security,
GNSS choice, BLE command bodies/pairing and commercial radio profile.

Read [ADRs](architecture/adr/README.md) for rationale. A changed decision needs
evidence and an ADR update, not an unsupported assumption. The full product
brief is represented in [vision](vision.md), [Drive requirements](../devices/drive/docs/product-requirements.md),
[concepts/costs](../devices/drive/docs/hardware-concepts.md),
[feature matrix](../devices/drive/docs/feature-matrix.md),
[BLE draft](../devices/drive/docs/ble-gatt.md) and
[roadmap](roadmap.md). No access to the original attachment is necessary.

## Material risks and deferred work

1. A cheap autonomous Reticulum-compatible application host is unproven; an
   RNode modem alone does not close this requirement.
2. Real moving-peer delivery, total legal airtime and useful participation
   density have not been measured.
3. Current Reticulum/LXMF terms include use restrictions. Do not assume MIT
   or unrestricted compatibility of a bundled product; [licensing](../LICENSING.md)
   separates original-work scope from dependencies.
4. Paper economics can exceed net consumer revenue even before margin. No
   current supplier quotes or certified BOM establish the target price.
5. Public reports remain unauthenticated; spoofing, tampering, Sybil attacks and
   radio flooding are unsolved. There are no confirmations/disputes or trust scores.

No firmware, mobile frontend, custom CAD/PCB/enclosure, signed update path,
production BLE protocol, manufacturing qualification or certification exists.
No real radio or vehicle experiment was performed. Read [adversarial review](architecture/adversarial-review.md),
[threat model](security/threat-model.md), [privacy](security/privacy.md),
[UK regulation](research/uk-regulatory.md) and
[human factors](../devices/drive/docs/human-factors.md) before a pilot.

## Next work and acceptance

Use the requested item in the [20-task backlog](community/backlog.md); it has
acceptance criteria. The next five priorities are:

| ID | Task | Required outcome |
| --- | --- | --- |
| 01 | Reticulum/LXMF distribution scope | Exact-version rights/restrictions and a documented reviewed release approach; an agent cannot substitute for legal approval |
| 02 | Two regional RNode units | Exact supported board revisions, antenna/profile and current quotes; no purchasing commitment inferred |
| 03 | Authenticated RNS delivery/contact churn | Two isolated hosts, SINGLE destinations, discovery/latency/loss evidence, timeouts and stale-queue handling |
| 04 | Standalone application host | Actual processing/network capabilities, memory/current/cost measurements |
| 05 | UK profile/conformity plan | Exact device classification, band/access/power/antenna configuration and current standards/lab review |

For the next software-only implementation, **03** is the clearest continuation:
extend the isolated experiment first, record results, then promote an adapter
only if its lifecycle, authentication semantics, callback serialisation, bounded
state, expiry and shutdown are genuinely tested. This does not close radio or
product feasibility gates. Tasks 07 and 09 are bounded alternative contributor
work for contact scenarios and encoding comparisons.

Finish each task with executable/reproducible evidence, updated documentation,
remaining limitations and a clear statement of what was committed/published.
Do not manufacture field results, quote estimates as prices or label a stub
implementation as integration.

## Feasibility follow-up — 4 October 2026

The [gate review pack](research/feasibility-gates.md) adds distribution/host/radio/lab
briefs and a separate signed SINGLE loopback experiment. All five gates remain
unresolved; prototype investment is on hold. Physical-host contact runs,
qualified reviews, delivered quotes and host measurements remain open. No
production adapter, radio transmission, purchasing or remote publishing occurred.

## Contact characterisation continuation — 4 October 2026

The [campaign harness and runbook](research/contact-campaign.md) add repeated
signed SINGLE events, timed TCP-interface windows, socket reconnection, bounded
overload/recovery, JSONL evidence and offline analysis. Production interfaces and
v1 vectors are unchanged. The earlier local work is preserved. Physical-host
execution remains pending; gate 03 and prototype HOLD remain open. No equipment
purchase, radio transmission, external outreach or remote publication occurred.

[Local results](research/contact-campaign-results.md): 490/490 full campaign trials
and 26/26 final-source smoke trials completed without worker failures; the final
contributor check passes 45 tests plus links/lint/format/types. Exact source and
raw records are archived. All measurements remain single-host controlled IP
observations; no clock-certified cross-host latency or radio result is claimed.

## A01 completed — 4 October 2026

All existing local research/source/evidence was reviewed and committed locally:
`ae4ba6e` (signed spike, queue test and initial evidence) and `e42ae0e` (contact
campaign, feasibility briefs, tests and verified historical/new evidence). The
project-plan documentation commit records A01 completion. Nothing was pushed.

New [validation](validation.md) passed 45 tests and contributor checks using
Ruff 0.16.9/mypy 2.3.1, dependency checks, all three signed-spike scenarios and
26/26 sequential smoke trials. Historical archive/source hashes and offline
summaries reproduced exactly. No executable corrections, protocol changes or
production adapter were needed. Hosted Python 3.12/3.13 remains unverified.

The current next package is **A02: agree feasibility thresholds and host role**;
see the [task register](project-plan.md). The earlier recommendation to extend
software task 03 has now been prepared, not accepted: physical hosts and clock
uncertainty evidence remain outstanding. Task 18 is independently eligible after
A01. Gates 01–05 remain open and prototype investment remains HOLD.

## A02 drafted — 4 October 2026

The [threshold/host-role proposal](research/feasibility-thresholds.md) now provides
T01–T09 targets, measurement methods and worked HOLD/REVISE cases. Maintainer
agreement is pending, so A02 remains open; no feasibility gate is closed. Hardware,
instruments, physical hosts, quotes and qualified reviews remain outstanding.
Task 18 remains independently eligible. This follow-up is local documentation
only; no runtime changes, new experiments, purchases, outreach or publication.

## A02 completed — 4 October 2026

The maintainer agreed to [T01–T09 and the host boundary](research/feasibility-thresholds.md)
without changes. A02 is complete locally; the preceding draft entry is historical.
Tasks 01/04/03/07/09 are eligible, with physical resources and qualified reviews
still outstanding. Task 07 is the first software-only package in the registered
sequence if those resources are unavailable; task 18 remains independently eligible.
Gates 01–05 and investment HOLD remain open. Documentation remains uncommitted.

## Task 07 completed — 4 October 2026

A02's existing agreement/documentation was validated and committed separately at
`b46261b`. [Task 07](research/contact-scenarios.md) adds a typed four-fixture runner
(`python -m wawet.scenarios`, with `--scenario`/`--json`), acceptance observation,
delivery/expiry/drop metrics and eight regression tests. All 53 tests, local links,
Ruff lint/format and strict mypy passed; the existing demo passed and two fresh
CLI JSON runs were byte-identical. Source/environment hashes and results are linked
from the runbook. Application/transport contracts and frozen v1 vectors remain
unchanged. Results are deterministic unauthenticated simulation only.

Task 09 is the next software package. Tasks 01/04/03 retain their external/resource
blockers; task 18 remains independently eligible. Task 08 now has task 07 completed
but still needs 02/03/05/14 and reviewed RF setup. Gates 01–05 and investment HOLD
persist. Hosted Python 3.12/3.13 is unverified; no purchase, outreach, transmission,
road trial, push or publication occurred. Earlier uncommitted entries are historical.

## Task 09 completed locally — 4 October 2026

The [encoding comparison](research/encoding-comparison.md) adds an isolated
standard-library research CLI, bounded binary and restricted CBOR codecs,
regression tests and raw size/timing/allocation evidence. Maximum placeholder
messages are 293/309 bytes. Production APIs and frozen 38-byte v1 remain unchanged.
Task 09's desktop comparison is complete; actual MCU/whole-host T06 measurement
remains task 04 and ADR 0004 stays Experimental. Task 18 is next eligible; task 14
still requires physical-host task 03. Gates 01–05 and G01 HOLD persist. This work
is uncommitted locally; no purchase, outreach, RF test or remote publication.
See the new validation entry for commands/results; earlier records are historical.

## Task 18 completed locally — 4 October 2026

Starting tree was clean at `3e247c8`: task 09 is committed, superseding its earlier
uncommitted handoff status without rewriting the historical entry. Task 07 and
A02 are committed at `c0dd25b` and `b46261b`.

The [prior-art review](research/prior-art.md) and linked evidence cover eight
systems. Waycast now has verified attributable source, GPLv3 text, pinned Git
history/tags and three independently reproduced upstream unit-test executables.
Independent radio/moving-contact/security claims and first-publication chronology
remain unresolved; full GUI reproduction was not attempted. No third-party source
was imported into Wawet, and no dependency/runtime/protocol change occurred.

Task 18 is complete for the agreed desk scope. Its completion unlocks no registered
dependent task. There is no remaining unblocked software package in the feasibility
sequence: task 14 still requires physical-host 03, and 15 requires 14. Next arrange
qualified review for 01, candidate hardware/instruments for 04 or two physical hosts
and clock evidence for 03. All five feasibility gates and G01 HOLD remain open.
New documentation checks are in [validation](validation.md); no unit/RNS campaign
rerun was needed. This follow-up is local/uncommitted; no purchase, outreach, RF
transmission, road trial, commit, push or publication occurred.
