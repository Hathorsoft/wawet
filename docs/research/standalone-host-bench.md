# Task 04 — Standalone host candidates and bench readiness

Prepared **4 October 2026**, baseline `44815e3`, clean starting tree. The maintainer
confirmed no equipment is available. **DESIGN DECISION:** recommend the Raspberry
Pi Zero 2 W for the first host-only bench screen. This is a research recommendation,
not a product board selection or purchase authorisation. Preparation is complete;
physical measurements, delivered quotes and task 04 acceptance remain **HOLD**.

Use the [agreed A02 thresholds](feasibility-thresholds.md),
[task register](../project-plan.md) and [backlog](../community/backlog.md).
No runtime, dependencies, EventTransport contract or 38-byte v1 vectors change.

## Primary documentation and candidate comparison

Sources below were opened on 4 October 2026. They establish documented hardware
features, not Wawet performance. Mutable pages must be frozen with title, URL,
retrieval date and hash when assembling the actual bench evidence. No restricted
RNS/LXMF source was retrieved or reviewed for this package. Further such review
uses local/manual inspection under the [task 01 condition](distribution-decision.md).

| Arrangement / exact candidate to investigate | Application and networking responsibilities | Documented facts / remaining work |
| --- | --- | --- |
| Linux host: Raspberry Pi **Zero 2 W**, actual PCB revision pending inspection | Existing Python application and optional CPython RNS experiment on the same processor; USB connection to a later modem | Manufacturer specifies Cortex-A53, 512 MB RAM, microSD and micro-USB OTG/power. Record actual board revision; original Zero/Zero W are not substitutes. ARM installation, memory, startup and power unmeasured. |
| MCU plus host: **ESP32-S3-DevKitC-1-N8R8, PCB v1.1** plus the above Linux host | A future application port on MCU; Linux runs RNS; a future serial bridge connects them | Espressif's v1.1 guide lists WROOM-1-N8R8, 8 MB flash/8 MB PSRAM, USB-UART and native USB. Pin/module variants matter. No Wawet port or bridge exists; both processors, supplies and interconnect belong to Drive. |
| Constrained endpoint: **nRF52840 DK**, actual PCA/PCB revision pending inspection | Future application plus a proven compatible endpoint on MCU, if feasible | Nordic documents buttons/LEDs, debugger, USB and current-measurement pins. No compatible Wawet/RNS endpoint is demonstrated. CPython availability is not inferred; implementing a second general routing stack is outside scope. |
| Phone-assisted comparison | Phone supplies application/network functionality or essential location | No implementation measured. A required phone fails the agreed standalone baseline; it cannot replace a missing Drive processor in cost or power accounting. |

Primary sources:

- [Zero 2 W specifications](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/).
- [Raspberry Pi OS editions](https://www.raspberrypi.com/documentation/computers/os.html):
  Linux/Debian-based OS and command-line Lite edition. Use **64-bit Lite** as the
  initial bench choice; exact compatible image/version/hash and Python version
  must be recorded at installation, not assumed from a changing download page.
- [Pi setup and USB connections](https://www.raspberrypi.com/documentation/computers/getting-started.html):
  Lite storage recommendation is at least 8 GB; Zero uses a separate power input
  and OTG adapter. USB peripherals can cause voltage drops; account for hubs and
  all power paths if required.
- [Espressif v1.1 guide and ordering table](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html).
  Both v1.0/v1.1 exist; the LED pin differs. Match board markings and module code.
- [Nordic nRF52840 DK](https://www.nordicsemi.com/Products/Development-hardware/nRF52840-DK).
  Family-level documentation does not resolve the revision of a borrowed unit.

**INFERENCE / recommendation:** Linux offers the fewest missing software pieces
because the repository already uses Python 3.11+ with no default runtime packages.
It avoids starting an MCU port, bridge and new endpoint together. It may fail the
10-second startup, power or cost limits; that is useful evidence, not grounds to
hide its OS/storage or choose a more powerful board without review. Stop at a
failed criterion and record REVISE or HOLD. Do not designate this as the final host.

## Borrow-or-acquire checklist

Prefer borrowing; nothing below has been ordered, quoted or budget-approved.

| Item | Minimum bench requirement | Accounting / unresolved details |
| --- | --- | --- |
| One Zero 2 W | Photograph labels and PCB revision; verify undamaged unit | Candidate DUT; delivered quote and exact revision absent |
| microSD and reader | Use 16 GB or larger as a bench allowance; keep recoverable image backup | Card is required host storage; reader is development equipment. Record make/capacity and image SHA-256 |
| Supply and cable | Regulated 5 V source with adequate transient capacity, micro-USB power cable; measure voltage at DUT | Supply rating is not measured consumption. Record lead loss; no back-power from data connections |
| Wired data path | Micro-USB OTG adapter, USB Ethernet adapter and Ethernet cable; private wired LAN | Disable Wi-Fi/Bluetooth for this non-RF bench. Freeze adapter chipset/driver. If needed in the final device, adapter belongs to Drive |
| USB expansion, only if needed | Hub for simultaneous Ethernet/modem; document port and power topology | Avoid powered-hub backfeed. Include every independently powered DUT component in electrical totals |
| Measurement chain | Borrow/rent calibrated current/voltage logger or shunt plus acquisition system, simultaneous V/I export, interval ≤ 1 ms, sufficient bandwidth and ≥ 1 A measurable range without clipping | Exact model, range, calibration date, burden voltage, accuracy and peak response unresolved. A slow USB display meter alone cannot pass T07 |
| Power control / readiness capture | Bench switch, common acquisition trigger for power-on and readiness marker, isolated observer/logger | No raw vehicle supply; observer must not power the DUT. Backup disposable test card before abrupt cuts |
| Observer/peer computer | Setup/image preparation and private wired peer with its own keys for later contact tests | Development-only if final Drive operates without it. Two-host task 03 resources are still absent |
| Later assembly components | Reviewed modem, GNSS/time source, feedback/input hardware, antennas, protected power, mount/enclosure | Not selected by this package; radio selection retains tasks 04/05 prerequisites |

Maintain two ledgers: (1) one-off development borrow/rental/purchase costs including
instruments and peer; (2) recurring complete-unit T09 costs. For every row record
supplier, exact SKU/revision, quantity, dated delivered quote, validity, currency,
conversion source/date, delivery and tax treatment. A published headline price is
not a delivered quote. No price evidence obtained here establishes feasibility.

T09 must include processors, storage, bridges, radio/GNSS/antennas, power/cables,
enclosure/mount, assembly/test, packaging, inbound delivery, unrecoverable taxes,
yield/warranty and tooling/conformity allocation at 1,000 units. Show recoverable VAT
and sales/channel margin separately; do low/base/high sensitivity. Missing quotes
leave T09 HOLD; a complete quoted cost above £25 is REVISE.

## Bench procedure and existing executable coverage

Run from a checkout of the recorded revision. First preserve `git status --short`
and `git diff`, board identity, `/etc/os-release`, kernel/architecture, Python and
package versions, OS image hash, enabled services, storage and instrument setup.
Use Python 3.11+; freeze the exact runtime. Disable onboard radios and use only
private wired IP or loopback. No modem transmission or public listeners.

Default baseline (future commands on the candidate, not executed here):

```sh
./scripts/demo
./scripts/test
PYTHONPATH=packages python3 -m wawet.scenarios --json
PYTHONPATH=packages python3 tools/encoding_comparison.py --iterations 1000 --repeats 3
```

Save stdout, stderr and exit status per command. Encoding comparison exercises
research codecs, not signature verification or integrated RNS memory. Simulator
success is not physical delivery. Optional networking uses a separate venv and the
existing [pinned installation/runbook](reticulum-spike.md); keep installation logs,
architecture-specific artefact hashes and package versions. Failure to install
pins on ARM is HOLD, not permission to silently upgrade or redistribute bundles.

```sh
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py --churn
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py --absent-discovery
PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py campaign --output /tmp/wawet-host-smoke --repetitions 1 --jobs 1
```

Use a new output directory. Local smoke verifies install/lifecycle only. Follow
[physical-host campaign instructions](contact-campaign.md) for task 03; no two-host
acceptance is replaced by running two processes on this candidate.

### Workload specification for the measurement session

The existing demo/tests/encoding CLI do **not** hold a full Vehicle workload while
networking. The original [host workload driver](../../tools/host_bench_workload.py)
now implements the recipe below using current APIs and a bounded recording
transport. It is research tooling, not firmware or a production transport adapter.
Archive its source/hash with results and verify its correctness before measurements.

```sh
PYTHONPATH=packages python3 tools/host_bench_workload.py --mode check --output /tmp/wawet-host-check.jsonl
PYTHONPATH=packages python3 tools/host_bench_workload.py --mode measure --output /tmp/wawet-host-measure.jsonl
```

Each output path must be new; existing evidence is never overwritten. Check mode
runs one cycle. Measure mode holds an empty, initialised application idle for ten
minutes, then repeats complete fill/hold/probe/burst/prune/recovery cycles for at
least ten active minutes. The last cycle finishes even if it crosses the deadline;
actual durations and completed cycles are recorded. Hold exercises 100 iterations
per cycle. Synthetic application time advances independently of real elapsed time.
Do warmup before the instrumented run; repeat physical runs three times as below.

JSONL records flush at every phase boundary and include UTC and process-local
monotonic markers, occupancy, counters, cumulative operation counts, cycle duration,
source revision/status/diff hash, driver hash, configuration and runtime. Reporting
adds the application's `sent` counter. Compare phase markers to derive phase elapsed
times. There is no throughput pass threshold. Failure or interruption records a
failure, closes the transport and exits nonzero; never discard failed-run evidence.
The transport retains only the latest outgoing frame, and shutdown clears it.

Capture external memory and electrical observations continuously through idle and
active phases, including transitions. Align the flushed phase markers to the
observer's acquisition timebase using a documented common trigger or measured
clock mapping and uncertainty. UTC alone is not certified synchronisation; these
software markers cannot establish electrical power-on or full T04 readiness.
Keep acquisition, warmup, ambient conditions and process-lifetime logs alongside
JSONL. The driver does not collect RSS, system memory, voltage or current itself.

For the additional contention screen, start the existing isolated RNS smoke in a
separate terminal during `active_start` through `active_end`, using the pinned
optional environment and commands above. Record both process lifetimes, command
outputs and failures. Repeat the workload run if overlap is insufficient. This is
simultaneous execution only: no integrated application/RNS receive path or physical
contact acceptance is implied. Default driver execution requires no RNS.

1. Use `Vehicle(capacity=1024, receive_limit=120)`, fixed synthetic `Position`, an
   injected integer clock and a recording `EventTransport` test double. Unique
   event IDs are nonzero 16-byte counters. Start at synthetic epoch 1,800,000,000;
   valid events use category 1, heading 0, TTL 3600, radius 5000 and fixed synthetic
   coordinates. Call `receive` with unauthenticated `Delivery`; do not imply trust.
2. Fill eight groups of 120 and one of 64 events, advancing the clock 60 seconds
   between groups. All created-at values equal their group's clock. Expect 1,024
   retained and received events without expiry; preserve default rate limiting.
   Hold occupancy while repeatedly calling `alerts`, encode/decode and `report`
   with fixed IDs. Measure durations/counts; no standalone throughput threshold
   has been agreed, so report throughput without inventing one.
3. Advance to a fresh rate window; submit one distinct valid event at capacity
   (one capacity drop), one truncated frame (one invalid), and one already-expired
   frame (one expired). Receive one exact duplicate and one changed frame sharing
   an existing ID (one duplicate/one conflict). Separately decode the malformed
   frame and require `ProtocolError`. Save counters before/after each phase.
4. Start another window; submit 121 valid distinct frames while full. Expect
   120 capacity drops and one rate-limit drop. Advance clock beyond every retained
   expiry, call `alerts` to prune, and require zero retained. In a fresh window
   deliver a new event and require recovery to one retained event. `close` must
   leave zero retained and close the recording transport.
5. Repeat fill/hold/prune/recovery cycles throughout ten active minutes. Keep an
   idle-ready period of ten minutes separately. Repeat memory and power runs
   three times, each with warmup completed and environmental conditions recorded.
   Run the isolated RNS smoke alongside the application driver for an additional
   contention screen. Record overlapping process lifetimes; this is simultaneous
   workload, **not** an integrated application/RNS receive path.

Use process-local monotonic durations for throughput. Sample `/proc/meminfo`,
`/proc/vmstat`, process RSS/high-water marks and swap/OOM logs across all phases
(at least 10 Hz host snapshots). Use the conservative occupied-memory estimate
`MemTotal - MemFree - Buffers - max(0, Cached - Shmem)` (all fields in the same
units). Do not subtract reclaimable slab for this screen; retain raw snapshots
and report that conservative choice.
`MemAvailable` alone is not an exact occupied-memory measure. Sampling may miss
peaks; combine high-water marks and a documented conservative bound, otherwise
T06 remains HOLD. Never call 75% of nominal 512 MB the usable-RAM threshold.

### Startup, power loss and integration boundary

Capture power-on electrically and readiness with a marker observed on the same
measurement timebase. Ten cold boots and ten additional abrupt power-loss/restart
cycles are required. During cuts alternate full occupancy/reporting and idle;
remove power for at least ten seconds, then restore. Record filesystem recovery,
errors, source/vector hashes and whether the workload restarts without manual
repair. Keep failures and count all cycles; do not replace failed boots silently.

The current application has no autonomous service, physical input/feedback or
valid-location gate. A shell import marker or SSH login time is **not** T04
acceptance. Host-only boot/import/network-stack timings are partial evidence;
full readiness requires later bench startup wiring and explicit parser/queue/input
and stack/interface markers. No fresh-fix readiness or invalid-location withholding
is claimed from `Vehicle`: its injected position/time are always supplied.

Record input voltage/current simultaneously at ≤ 1 ms intervals, integrating V×I
for ten-minute means and retaining startup/restart peaks. Add instrument uncertainty
to reported upper bounds; clipping, missing voltage, calibration or inadequate
bandwidth leaves power HOLD. Disconnect debugger/display power paths; include
hub and peripherals if powered separately. Do not infer current from software RSS.

## Acceptance matrix and next action

| Criterion | Evidence / evaluation | What remains blocked |
| --- | --- | --- |
| Runtime / correctness | Exact ARM runtime/pins and successful baseline/workload logs; zero invalid acceptance, bounded state and successful recovery | Driver implemented; physical host unavailable |
| T01/T02/T03 networking | Physical private-LAN campaign: p95 availability-to-accept plus ≤100 ms clock uncertainty ≤2 s; ≥29/30 within-contact deliveries in each cold/warm 5/10 s cell and stable cell; 1/2 s characterisation; raw discovery/loss/overhead and rejection logs | Two hosts/clock evidence absent; existing logs' event-availability start must be verified; task 03 stays open |
| T04 startup | Every one of ten cold boots ≤10 s; ten abrupt recovery cycles with no corruption/recovery failure | Host-only timings partial; explicit application/input/network readiness wiring absent |
| T05 location/time | Ten favourable-sky starts ≤60 s; fix age ≤5 s, uncertainty ≤50 m, time uncertainty ≤1 s; zero invalid/stale located reports | GNSS, independent reference and validity gate absent; task 06 owns policy/poor-sky validation |
| T06 memory | Three runs, every required processor ≤75% usable memory including OS/network/buffers, no swap/OOM; RSS separately | Full-occupancy simultaneous workload and peak bound unmeasured; extra processors included if required |
| T07 power | Three idle/active ten-minute runs, each upper mean ≤2.5 W and upper peak ≤5 W at 5 V | Host-only screen partial; complete assembly and approved RF workload absent |
| T08 standby | Defined standby ten-minute upper mean ≤0.10 W; no reception claim when asleep | Otherwise record switched-power requirement; automotive acceptance belongs to task 11 |
| T09 cost | Complete quoted recurring cost ≤£25 at stated 1,000-unit scenario, full ledger/sensitivity | Quotes and final assembly scope absent; paper allowances cannot pass |

For each run archive run ID, UTC date, source revision/diff and driver hash,
configuration/workload, board/runtime, instrument/calibration/uncertainty, ambient
conditions, timing markers, raw V/I and memory series, counters, exits/stderr,
failures and evaluated PASS/HOLD/REVISE criteria. Hash raw files; redact private
keys/configs and real participant data. Synthetic coordinates only. No measured
result exists in this package.

**Next physical action:** seek access to the recommended board and a suitable
measurement chain, with the equipment checklist and separate budget ledger ready
for maintainer review. If unavailable, retain HOLD rather than repeating completed
software packages. Task 04 completion still requires physical evidence; task 05
requires 04, task 02 requires 04/05, task 14 requires physical-host 03 plus completed
09, and task 15 requires 14. G01 remains HOLD. No purchase, outreach, RF transmission,
commit, push or release is authorised by this runbook.

## Software preparation validation — 5 October 2026

The [desktop evidence archive](results/host-bench-workload-2026-10-05/README.md)
records two equivalent short runs and a full 600.003-second idle / 600.178-second
active rehearsal with 2,424 complete cycles and zero failures. Six new regression
tests and the 68-test contributor check passed, plus explicit strict driver typing.
These are synthetic desktop observations only; no physical criteria are passed.
See [validation](../validation.md) for exact commands, corrections and limitations.
