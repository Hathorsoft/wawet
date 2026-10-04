# Feasibility gates 01–05: desk-first review pack

Prepared 4 October 2026. This supplements the foundation snapshot, not its history.
**DESIGN DECISION: HOLD** standalone Drive prototype investment. No gate below is
closed by a local TCP experiment. No purchasing, outreach, radio transmission or
publication was performed. Qualified reviewers and physical equipment are absent.

## Gate decision record

| Gate | Status | Evidence now | Required next action |
| --- | --- | --- | --- |
| 01 distribution | Unresolved | [Exact installed inventory](results/dependency-inventory.json), review brief below | Qualified exact-version distribution review |
| 02 radio units | Unresolved | Revision/SKU screen below | Match firmware target and antenna; obtain delivered two-unit quote |
| 03 authenticated/contact delivery | Unresolved | [Signed SINGLE experiment](../../tools/rns_authenticated_spike.py), [raw local run](results/authenticated-loopback.json) | Two physical-host reproduction and measured contact windows |
| 04 standalone host | Unresolved | Workload and measurement brief below | Candidate runtime, memory, power and recovery measurements |
| 05 UK profile/conformity | Unresolved | Primary-source and lab brief below | Current complete row/standard assessment and qualified review |

No gate is marked failed merely because evidence is unavailable. HOLD means the
prototype decision cannot yet be supported; it does not establish infeasibility.

## 01: distribution review brief

**FACT:** installed experiment versions and notice-file SHA-256 hashes are recorded
in the inventory. It is an installed-environment inventory, not a distributable
wheel/image SBOM. LXMF is not installed and no exact release is selected: it remains
outside the experimental dependency set. Its exact-version review is unresolved.

The [Reticulum licence](https://reticulum.network/license.html) grants rights with
use restrictions. [LXMF's current licence](https://github.com/markqvist/LXMF/blob/master/LICENSE)
is a discovery source, not a pinned release approval. See [project scope](../../LICENSING.md).

| Distribution form | Proposed approach for review | Unresolved obligations |
| --- | --- | --- |
| Original source only | Apache-2.0 application; prose licence separately | Check notices and absence of copied upstream implementation |
| User-installed optional spike | Pin external dependencies; show licence gate | Review applicability of restrictions and installation documentation |
| Bundled commercial image | HOLD release | Exact artefacts, transitive/native notices, restrictions, source obligations and compatibility |

Reviewer questions: confirm rights for civilian road reports, resale, modifications
and third-party forks; interpret restricted uses and ML clauses; determine notice
and downstream obligations; assess RNode GPLv3 separately if firmware is shipped.
Attach exact release artefacts, hashes, complete licence texts and intended use to
the review. Record reviewer, date, scope, written outcome, conditions and approved
release forms. **Review outcome: not obtained; no release approach approved.**

## 04: standalone workload and candidate screen

**DESIGN DECISION:** measure the existing parser and bounded Vehicle retention
(up to 1,024 active events), report/receive paths, expiry pruning and overload
behaviour. Feed synthetic valid, stale, malformed and burst inputs. Include fresh
location/time availability as a separate subsystem; no real participant data.

| Architecture | Demonstrated here | Bench candidate / limitation |
| --- | --- | --- |
| MCU application plus separate RNS host | No MCU port or host bridge | ESP32-S3 application prototype plus Linux host; all host cost/power belongs to Drive if required |
| Linux-class standalone host | Python application and RNS on development macOS only | Raspberry Pi Zero 2 W as a candidate, not proven fit; verify exact OS/runtime and USB serial setup |
| Constrained compatible endpoint | No compatible implementation | ESP32-S3 or nRF52 feasibility study; do not assume CPython RNS runs there or commission a second routing stack |
| Phone-assisted endpoint | No phone implementation | Comparison only; fails baseline independence if phone is required |

Measure candidate/board revision, OS/compiler/runtime, peak RSS or heap/stack,
steady/peak USB input current at measured voltage, cold startup, valid time/fix
readiness, repeated abrupt power removal and recovery, parser throughput, queue
occupancy/drop counts and network workload separately. Use a calibrated power
instrument; software RSS is not electrical current. Archive raw time series,
sampling interval, instrument model/calibration, repetitions and failures.

Cost evidence must include host, radio, GNSS, antennas, power, cables and delivery;
keep current quotes separate from paper 1,000-unit allowances. No candidate price,
current or memory result is asserted. Before bench runs the maintainer must record
numeric latency/loss, startup, current, memory and delivered-cost limits and test
contact durations. These product thresholds remain unagreed, not inferred.

## 02: two-unit purchasing brief

**FACT:** [RNS 1.5.5 hardware documentation](https://reticulum.network/manual/hardware.html)
lists T3S3 and Heltec LoRa32 v3.0 among supported families. Exact revision mapping
must still be checked against a frozen RNode firmware release and installer target.

| Candidate | Supplier evidence | Selection blocker |
| --- | --- | --- |
| LILYGO T3-S3 SX1262 868 MHz H595 | [Listing](https://lilygo.cc/products/t3s3-v1-0) advertises variants; [V1.3 documentation](https://wiki.lilygo.cc/products/t3-series/t3-s3-v1.3/) identifies a newer revision | Delivered PCB revision, exact firmware support, antenna specification and UK shipping/tax unconfirmed |
| Heltec LoRa32 v3.0 SX1262 regional variant | Upstream supported family | Exact purchasable revision/SKU, firmware image and supplied antenna not verified |

The LILYGO listing displayed USD 23.65 during research, but variant-specific stock
and delivered price were not established. This is neither a quotation nor a
purchase recommendation. No delivered quote exists for either candidate.

The installed RNS 1.5.5 `rnodeconf` maps SX1262 T3S3 model 0xA6 to
`rnode_firmware_t3s3.zip`, and Heltec v3 SX1262 model 0xCA to
`rnode_firmware_heltec32v3.zip`. Its T3S3 installer explicitly warns that this target
is experimental. These are installer mappings, not proof of a supplier PCB match
or a frozen firmware version.

**DESIGN DECISION:** prefer two identical Heltec LoRa32 v3.0 regional SX1262 units for further verification,
using USB serial with separate bench RNS hosts. Do not order until the supplier
confirms PCB revision, RF matching, included antenna gain/connector, firmware
mapping, stock, two-unit price, shipping, tax/import charges and quote validity.
Use the alternative only after the same verification. Never substitute a 915 MHz
variant based on a shared board-family name. Supplied antenna is not compliance.

## 05: proposed profile and qualified lab brief

**ASSUMPTION — review candidate only:** GB non-specific SRD under IR2030/1/16;
868.3 MHz centre, 125 kHz bandwidth, SF7, coding rate 4/5, USB-powered RNode modem
and separate application host. Proposed conducted output ceiling 10 dBm with
antenna gain no greater than 2 dBi and documented feed loss. Use the alternative
1% duty-cycle route only if the complete current row permits this device/setup;
budget announces, retries and all control traffic. These values are not enabled
by code and are not permission to transmit. Unknown antenna gain blocks use.

[Ofcom's current SRD entry point](https://www.ofcom.org.uk/spectrum/radio-equipment/short-range-devices)
links the current IR2030. Freeze the complete applicable row, continuation,
access conditions and revision before use. Check occupied bandwidth and actual
ERP, rather than equating conducted output with radiated power.

[GB designated radio standards](https://www.gov.uk/government/publications/designated-standards-radio-equipment)
includes [notice 0130/26](https://assets.publishing.service.gov.uk/media/696f8590c0f4afaa9536a0be/ds-0130-26-radio-equipment-notice.pdf)
of 21 January 2026: Annex I lists EN 300 220-2 V3.3.1 for non-specific SRD spectrum
access and EN 300 328 V2.2.2 for wideband 2.4 GHz equipment. The older EN 300 220 reference in the foundation
is not a verified current designation. Complete the exact applicable editions and
withdrawal dates with the lab; these entries do not establish applicability or whole-product compliance.
[Official equipment guidance](https://www.gov.uk/government/publications/radio-equipment-regulations-2017)
provides separate GB/NI guidance: do not reuse a GB route as an NI approval.

Lab brief: assess classification, complete IR2030 row, spectrum access enforcement,
antenna/power tolerances, radio/EMC/safety standards, automotive USB accessory scope,
RoHS/WEEE, markings, declarations and technical file. Review conducted attenuated
bench isolation and leakage before any RF experiment; define whole-product tests
with final enclosure/cables/antenna. BLE, if enabled, needs its own assessment.
Record lab identity, written profile/setup outcome and conditions. **Lab outcome:
not obtained. No approved profile or radiating test setup exists.**

## 03: reproduction, evidence and remaining experiment

Run the optional pinned environment with:

```sh
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py --churn
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py --absent-discovery
```

The parent creates independent temporary configurations and per-process private
keys; workers share only public pins. The receiver is SINGLE; Ed25519 signs a
spike-specific domain prefix plus the unchanged 38-byte event. Signature checking
uses the expected sender public key, before decoding and expiry checking. This
102-byte signed body is experimental transport glue, not a v2 protocol or public
trust system. Key provisioning is local trusted setup; sender truth, Sybil defence,
rotation and public deployment are not established. SINGLE encryption protects
recipient delivery; signatures provide application integrity and pinned-key origin.

The run requires valid delivery after unexpected-signer, altered-frame and expired
signed probes. It records exact payload, wall times, discovery duration and packed
RNS packet length. It uses two processes on one machine, direct loopback TCP,
no forwarding, one live outgoing event, no automatic retry, an eight-second path
wait, bounded child deadlines and cleanup. It does not implement a production queue.
Expiry is checked again immediately before sending.

The [churn run](results/authenticated-churn.json) injects a drop at the outgoing TCP-interface boundary, then forces socket shutdown and waits
for RNS TCP reconnection; an event with a one-second TTL expires before sending,
while an explicit resend of the original fresh frame is delivered after reconnection.
The injected drop is a software fault, not measured physical link loss. The
[absent-discovery run](results/absent-discovery.json) records an expected bounded
path timeout and child cleanup. Callbacks enqueue into an eight-item queue and
validation occurs on the worker main thread. Interface counters are RNS-accounted
bytes, not TCP/IP packet-capture totals; control-only overhead is not separated.

A standard-library regression test verifies overflow drops new items, preserves
eight queued frames and admits new traffic after draining. Sustained network flood
and physical loss measurements remain open.
Preserve original event bytes across explicit retries; distinguish sent, received,
rejected and timed out. Record RNS interface byte counters and capture methodology;
packed packet size is not total TCP traffic, control overhead or radio airtime.

Then deploy workers on two physically separate private-IP hosts with independently
provisioned keys/configuration; do not expose listeners publicly. Clock-sync error
must accompany one-way latency. Repeat stable and contact-window runs with the
agreed thresholds. Worker bundles can be prepared without opening any socket:

```sh
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py --prepare /tmp/wawet-private-hosts --peer-ip 192.168.1.10
```

Replace the example with the receiver's actual private IPv4 address. Transfer only
`receive/` to the receiver host, only `send/` to the sender host, and both public
files to each role directory's parent. Never transfer the other role's private
key. Run `--worker receive --config /path/to/receive` on the receiver, then
`--worker send --config /path/to/send --payload HEX` on the sender, optionally
adding `--churn`. HEX must be a freshly encoded synthetic v1 event; preserve it for
an explicit resend. The receiver has a 20-second deadline, so start the sender
promptly. Capture both workers' stdout and exit status. Remote bundle transfer and
physical-host execution remain unperformed; no remote success is claimed. Save failed run output as well as successes.

## Follow-up validation — 4 October 2026

Baseline: `./scripts/demo`, `./scripts/test` and
`PYTHON=.venv/bin/python ./scripts/check` passed (31 tests). Follow-up checks pass
32 tests, local Markdown links, Ruff lint/format and strict mypy. Default tests
remain RNS-independent; the optional three commands above verify real local RNS.
Raw outputs preserve run IDs and timing; default protocol vectors are unchanged.

Development failures: initial sandbox socket denial, a receiver callback NameError
and missing timeout output during RNS shutdown were encountered and fixed. See
[development failure record](results/development-failures.json); these are tool/code
failures, not evidence that the architecture fails. RNS shutdown detaches stdout,
so worker exceptions are emitted as JSON before cleanup. No Python 3.12/3.13 hosted
CI run was performed. Changes are local and uncommitted; nothing was pushed.

## Contact campaign continuation — 4 October 2026

The [repeatable campaign and private-LAN runbook](contact-campaign.md) extend gate
03 preparation. Controlled TCP-interface windows and socket reconnection are
reported separately. Physical-host evidence and product thresholds remain pending;
no feasibility gate or prototype investment HOLD is closed by local validation.

The [local report](contact-campaign-results.md) records 490 full campaign trials
and 26 final-source smoke trials with no worker failures. Short-window delivery
and overload/expiry evidence are local controlled-interface observations. No gate
is closed, and no physical-host, radio or product performance approval is claimed.

## A01 status update — 4 October 2026

Review/check/local commits are complete: `ae4ba6e` and `e42ae0e` preserve the
experimental source and evidence. The [new validation record](../validation.md)
separates A01 rechecks from the historical observations above. A02 is next in the
[project plan](../project-plan.md); numeric feasibility limits and host roles remain
unagreed. All five gates remain unresolved and prototype HOLD remains in force.
