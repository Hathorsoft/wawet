# Task 07 — Deterministic contact scenarios

Completed locally **4 October 2026**. **EXPERIMENTAL RESULT:** scripted,
unauthenticated simulation, not moving-vehicle, physical-host, discovery or RF
performance. No T01/T02 acceptance or feasibility gate closure is asserted.

## Run and reproduce

Python 3.11+; standard library only. From the repository root:

```sh
PYTHONPATH=packages python3 -m wawet.scenarios
PYTHONPATH=packages python3 -m wawet.scenarios --scenario rural --json
PYTHONPATH=packages python3 -m wawet.scenarios --json > /tmp/wawet-scenarios.json
cmp docs/research/results/contact-scenarios.json /tmp/wawet-scenarios.json
./scripts/test
PYTHON=.venv/bin/python ./scripts/check
```

The [runner](../../packages/wawet/scenarios.py) contains four typed fixtures.
Each run creates fresh state and closes every vehicle, including on errors.
`--scenario` selects passing, convoy, rural or dense; omission runs all four.
`--json` emits an ordered result array; ordinary output summarises each fixture.
No wall-clock time, random identifiers, RNS installation or new dependencies enter
this path. See [results](results/contact-scenarios.json) and
[source/environment evidence](results/contact-scenarios-evidence.json).

## Fixture assumptions and action ordering

**ASSUMPTIONS:** synthetic positions, fixed event/identity bytes, epoch 1000,
one-second delivery delay, explicitly scripted contact links. Position/speed
never creates a link. No range model, routing, forwarding, discovery, trust or
background erasure is simulated. Application expiry remains access-driven.

Actions are ordered integer-second offsets. Advance the network to each timestamp
before applying its actions in declared order. Deliveries due at that timestamp
precede even a disconnect action. A frame sent and disconnected at the same
timestamp is lost at its later due time. This boundary has a dedicated test.

| Fixture | Timeline / workload | Observed fresh delivery |
| --- | --- | --- |
| Passing | At 0, connect reporter to northbound and southbound peers and report. At 1, observe delivery then move northbound peer beyond hazard. At 2, send second report then disconnect both peers; observe loss at 3. | 2/4 distinct intended pairs; both first-frame receipts, only northbound initially alerts; two contact drops. |
| Convoy | At 0, reporter connects directly to three followers and reports. At 1, observe then resend unchanged bytes. At 2, observe duplicates then move one follower beyond hazard. | 3/3; three duplicate rejections; original acceptance times unchanged. |
| Rural | At 0, report disconnected with TTL 5. Connect at 1, observe no replay at 2, then explicitly resend. Accept at 3. Resend at 4 to deliberately arrive at exact expiry 5. | 1/1; latency 3 seconds from original availability; one separately counted stale probe rejected. |
| Dense | Eight fully connected endpoints, two reporters, queue capacity 7 and retention capacity 1 each. Two reports at 0; further report at 1; observe retention rejection at 2, expiry at 3, then report recovery and observe at 4. | 15/28; seven queue drops, six retention rejections, seven recovery acceptances. |

Default application rate limit stays 120 deliveries/minute; fixtures do not
exceed it. All rate-limit, malformed/future/conflict counters remain explicitly
reported as zero. Dense peak queue is 7 and peak per-vehicle retention is 1.
The dense case intentionally demonstrates failure under chosen small bounds,
not a claim about real traffic capacity.

## Result accounting

Intended pairs are distinct original event ID/recipient pairs, including absent
links. Repeated sends do not inflate their denominator. Only explicitly marked
stale probes are separate; an unmarked fresh event that expires in transit remains
a delivery miss. A test locks this distinction. There is no inference from
surviving deliveries that missed events were successful.

The scenario-local transport wrapper calls the existing receiver, then records
acceptance only when the application's `received` counter increments. It records
frame bytes, original creation time, recipient, first acceptance time and integer
latency from original event creation/availability. Relevant alerts are separate
observations: an accepted event need not produce an alert. Latency includes waits
before explicit resends and reports its full sample list and sample count.

Results expose per-vehicle application counters, fresh numerator/denominator,
stale probes, transmissions, alerts/retention at observations, queue overflow,
contact-delivery drops, observed peak bounds and final retention before cleanup.
No-send disconnected misses appear in intended pairs but not network drop counts;
network drops count actual queue overflow or failed queued delivery only.

## Validation and next gate

New validation on 4 October 2026 used Python 3.11.4: 53 tests passed, local file
links passed, Ruff 0.16.9 lint/format and mypy 2.3.1 strict checks passed. The existing
demo passed and two fresh CLI outputs compared byte-for-byte. Eight new tests
cover fixture outcomes, boundary ordering, denominator integrity, cleanup and CLI
selection/repeatability. Existing application sources and v1 vectors are unchanged.

The evidence record gives the A02 base revision and exact source/result SHA-256
hashes; new source/tests constitute its local implementation difference. The task
07 commit contains those files with this evidence. No historical validation was
rewritten. External URLs/anchors and hosted Python 3.12/3.13 CI are unverified.

Task 07 supplies one prerequisite for task 08. Task 08 still requires tasks
02/03/05/14 and an approved physical RF setup. Task 09 is next in the eligible
software sequence. Gates 01–05 and G01 investment HOLD persist; no purchase,
external outreach, transmission, public-road trial or publication occurred.
