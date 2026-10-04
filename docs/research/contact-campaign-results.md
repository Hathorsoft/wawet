# Local contact campaign results — 4 October 2026

**EXPERIMENTAL RESULT:** 490/490 planned trials completed with zero worker failures
on one macOS 26.2 arm64 host, Python 3.11.4, RNS 1.5.5. Eight trials ran concurrently,
each with its own keys, ports, processes and temporary RNS state. This is controlled
loopback TCP-interface contact, not physical-host, moving-peer or radio evidence.

Command:

```sh
PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py campaign --output /tmp/wawet-contact-full --repetitions 30 --jobs 8
```

[Raw archive](results/contact-campaign-2026-10-04.tar.gz) includes the manifest,
per-role JSONL/stderr/exits, original and final-analysis summaries, and exact
executed harness plus its hash. [Summary](results/contact-campaign-summary.json)
contains full distributions, rejections and matched-control traffic comparisons.
[Evidence notes](results/contact-campaign-evidence.json) preserve development and
validation limits. Extract the archive, then run the analyser against its
`contact-campaign/` directory using the [runbook](contact-campaign.md).

| Contact mode/window | Completed trials | Delivered/intended | Median path check (ms) | p95 path check (ms) |
| --- | --- | --- | --- | --- |
| cold / 1s | 30/30 | 30/30 | 53.611 | 55.240 |
| cold / 2s | 30/30 | 30/30 | 54.432 | 55.292 |
| cold / 5s | 30/30 | 30/30 | 54.592 | 55.271 |
| cold / 10s | 30/30 | 30/30 | 54.308 | 55.239 |
| warm / 1s | 30/30 | 30/30 | 0.006 | 0.018 |
| warm / 2s | 30/30 | 30/30 | 0.009 | 0.024 |
| warm / 5s | 30/30 | 30/30 | 0.007 | 0.032 |
| warm / 10s | 30/30 | 30/30 | 0.007 | 0.012 |

Cold discovery was sampled every 50 ms; the approximately 50–55 ms figures include
that polling interval and must not be represented as exact discovery latency.
Warm results measure checking an already cached path, not new network discovery.
Actual gate transitions and socket status are retained in raw monotonic records.
No clock-offset measurement was supplied, so one-way latency is omitted throughout.

Additional observations:

- Stable baseline: **30/30** fresh events delivered at one-second send intervals.
- Five-second outage: the original still-fresh frame was explicitly resent and
  delivered after approximately **5.059 seconds** to socket recovery. One expired
  pending event was withheld; the eligible delivery fraction is 1/1. The raw
  intended-event fraction is 1/2 because it includes that deliberate stale event.
- Absent discovery: bounded path timeout, no send or reception; both workers exited
  cleanly. This expected negative outcome remains 0/1 in delivery accounting.
- Adversarial probes: two signature rejects, one malformed signed-frame reject,
  one expired signed-frame reject, then one valid reception.
- Overload: eight of 32 burst frames retained, **24 capacity drops**, then one
  recovery event accepted; total 9/33. Queue overflow deliberately drops new frames.
- All 245 matched control-only trials completed. Traffic summaries keep sender and
  receiver TX/RX separate and subtract matching control-group means; RNS counters
  are not TCP/IP totals, exact control attribution or radio airtime.

**DESIGN DECISION:** retain prototype HOLD and leave gate 03 open. Short clean
loopback contacts do not establish useful mobile contact performance or legal
radio budgets. Next collect the same raw evidence on two physical private-LAN
hosts, measure clock uncertainty and then propose product thresholds with the
maintainer. No production adapter, purchases, radio transmission or remote
publication occurred.

The full campaign source predates final defensive handling of clock evidence,
incomplete logs, prelaunch errors and deadline waits. Its exact source is archived;
final smoke validation is recorded separately. These are current implementation
results, separate from the earlier foundation and signed-spike milestones.

Final-source smoke validation: **26/26** trials completed with zero worker failures;
stable delivery, fresh resend/expired withholding, adversarial rejection counts,
24 capacity drops and recovery assertions passed. Its [raw archive](results/contact-campaign-final-smoke.tar.gz)
includes the final executed source/hash. The [original signed-spike rechecks](results/contact-campaign-spike-rechecks.json)
also passed delivery, churn and expected absent-discovery timeout independently.

## A01 independent local recheck — 4 October 2026

The [A01 review evidence](results/a01-review.json) verifies both historical archives,
source hashes and worker exits; offline analysis exactly reproduced their recorded
summaries. The current harness matches the historical final-source smoke. A new
**26/26 sequential smoke campaign** (`--repetitions 1 --jobs 1`) passed with zero
worker failures and the expected delivery, expiry, signature, overflow and recovery
assertions. Its [separate raw archive](results/a01-recheck-2026-10-04.tar.gz) preserves
new observations without replacing the earlier concurrent campaign evidence.
See [validation](../validation.md) for commands, updated dev tools and limitations.
Gate 03 remains open and prototype HOLD is unchanged.
