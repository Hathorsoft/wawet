# Authenticated contact campaign

Status: isolated experiment tooling. Gate 03 and prototype investment HOLD remain
open. This extends the [signed SINGLE spike](reticulum-spike.md); it does not
implement `EventTransport`, change protocol v1, or establish public trust.

## Experiment and records

[Harness and analyser](../../tools/rns_contact_campaign.py) pin RNS 1.5.5 and use
the existing domain-separated signature over an unchanged 38-byte synthetic event.
Only a provisioned sender's public pin is trusted. The signed body is 102 bytes.
Callbacks place frames into an eight-item FIFO; a bounded overflow counter is
protected by a lock. Signature, parse and expiry validation and logging occur on
the receiver main thread. Signature origin does not establish report truth.

Each trial starts with independent RNS configuration/storage. Cold trials begin
without discovered paths; warm trials first discover, disable contact for one
second, then reopen it with cached path state. Contact windows are 1, 2, 5 and
10 seconds, with 30 independent trials per window and mode. There is one fresh
event per contact trial. Stable baseline sends 30 events at one-second intervals.
Matching control-only trials retain the schedule/discovery but omit events and
adversarial probes. The full campaign comprises 490 trials, including controls.

The sender gates incoming and outgoing traffic at the actual TCPClientInterface
methods. Disabled traffic is discarded, never held for later delivery. TCP sockets
remain connected during short windows: this measures **controlled RNS interface
contact**, not TCP reconnection, physical loss or moving radio encounters. The
outage scenario separately shuts down the socket, disables interface traffic for
five seconds, waits for socket reconnection, then explicitly resends the original
fresh frame. A one-second-TTL pending frame must be withheld. No automatic event
retry or forwarding exists. Contact records include gate state, socket availability,
monotonic elapsed time and counters. OS scheduling affects actual window lengths.

Adversarial probes cover stranger signatures, altered payloads, signed malformed
frames and signed expired frames, followed by a valid event. Overload uses a signed
experiment-only pause marker to suspend receiver draining for one second, then
sends 32 distinct valid frames and a subsequent recovery event. This exercises
queue saturation on actual RNS callbacks; it is not an unbounded sustained flood.

Each role writes JSON Lines: run/scenario/role, wall time, process-local monotonic
elapsed time, software environment, event ID and frame hash, send outcome, receive
time, rejections, discovery/reconnection and final counters. Exit status and stderr
are separate files. `sent` means `Packet.send()` returned a receipt; delivery is
established only by matching the receiver event ID **and frame hash**. Monotonic
values from different hosts must never be subtracted. Only synthetic coordinates
are used; private keys and configuration directories are excluded from evidence.

## Local reproduction

Use the [pinned optional environment](reticulum-spike.md) and review
[dependency licensing](../../LICENSING.md). From the repository root:

```sh
PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py campaign --output /tmp/wawet-contact-smoke --repetitions 1 --jobs 1
PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py campaign --output /tmp/wawet-contact-full --repetitions 30 --jobs 1
PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py analyse /tmp/wawet-contact-full > /tmp/wawet-contact-summary.json
```

Output directories must be new. `--jobs` accepts 1–8; concurrent trials use distinct
ports, processes, identities and storage. Concurrency changes host contention, so
record it and do not compare such timings to a serial bench as equivalent.
Sockets bind only to loopback. A sandbox may require approval for local sockets.
Worker and parent deadlines bound failures; stdout, stderr and exits survive.
The manifest lists planned runs, so missing/failed trials remain in denominators.

## Two-host private-LAN runbook

Physical execution remains pending. Use two existing computers on a controlled
private LAN, with no radio enabled and no public listener/NAT forwarding. Record
host/OS/runtime versions and repository revision plus local diff. Install the same
optional pins separately on each host. Do not copy user RNS settings.

1. On the receiver host, provision its key locally. Substitute its actual RFC1918
   IPv4 address for the example:

   ```sh
   PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py provision --role receive --config /tmp/wawet-receive --peer-ip 192.168.1.10
   ```

2. On the sender host, provision its key locally with the same receiver address:

   ```sh
   PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py provision --role send --config /tmp/wawet-send --peer-ip 192.168.1.10
   ```

3. Exchange only `send.public` and `receive.public`, placing both in each role's
   directory. Compare the printed SHA-256 fingerprints through a trusted channel
   before running. Each `identity.key` stays on its originating host, mode 0600;
   role directories are mode 0700. Generated configs allow only explicit loopback
   or RFC1918 IPv4, disable shared instances/forwarding and are checked verbatim
   against settings before opening sockets. Do not edit them to add interfaces.

4. Measure clock offset and uncertainty before and after the campaign using a
   documented synchronisation/measurement method. Save raw measurement output.
   Record UTC measurement time and both host identities in the clock evidence.
   If synchronisation or its uncertainty cannot be established, omit one-way
   latency and retain delivery fractions and process-local durations.

5. Generate a shared manifest with a future UTC Unix start timestamp far enough
   ahead to transfer it and start both roles. The `schedule` command opens no
   sockets. For example, use an actual agreed timestamp in place of `START_EPOCH`:

   ```sh
   PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py schedule --output /tmp/wawet-manifest.json --start-at START_EPOCH --repetitions 30
   ```

   Transfer this manifest to both hosts and check its hash. Run the following on
   the corresponding hosts before the scheduled start:

   ```sh
   PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py batch --role receive --config /tmp/wawet-receive --manifest /tmp/wawet-manifest.json --output /tmp/wawet-receiver-results
   PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py batch --role send --config /tmp/wawet-send --manifest /tmp/wawet-manifest.json --output /tmp/wawet-sender-results
   ```

   Roles run serially. Receiver starts two seconds before sender; each slot allows
   its contact window plus 20 seconds. The manifest records `ends_by`; reserve
   several hours for the full serial campaign. Missed starts are recorded as
   failures rather than silently rescheduled. Each trial copies only the local
   key, public pins and generated config into fresh temporary RNS state.

6. Combine the two result directories into one analysis directory: one identical
   manifest, both roles' JSONL/stderr and `*-role-exit.json` files. Save both hosts'
   measurement notes. Do not transfer private configs or keys into the archive.

   ```sh
   PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py analyse /tmp/wawet-combined-results > /tmp/wawet-summary.json
   ```

   Optional `--clock-evidence /tmp/wawet-clock.json` accepts a JSON object containing
   `receiver_minus_sender_seconds` (signed receiver clock minus sender clock),
   `uncertainty_seconds` (nonnegative conservative bound), `method` and
   `measured_at`. It subtracts that offset from receive minus send wall time and
   preserves the uncertainty in the report. Repeated sends of the same event
   are excluded from latency because their corresponding reception is ambiguous.
   Supply a bound covering the entire campaign, including measured drift.

7. Review all failures, timeout counts, planned/completed trial counts, matched
   bytes and final rejections before drawing conclusions. Stop workers before
   removing temporary configs. Keep raw evidence under the agreed research
   retention policy; delete private bench keys/configs when no longer needed.
   Never commit keys or real participant location data.

For a single diagnostic trial, use `worker` with explicit `--role`, `--config`,
`--run-id`, `--scenario`, `--window` and `--deadline`; start receiver promptly
before sender. Defaults are 60-second deadlines, 30 baseline events and one-second
intervals. Provision fresh directories when testing cold discovery.

## Analysis and acceptance

The analyser reports planned/completed/failed trials, distinct intended/sent/delivered
events, attempts by outcome, rejections and discovery timeouts. Delivery fraction
uses all intended events, including the deliberately stale outage event; the
separate eligible fraction excludes events withheld for expiry. A missing worker
cannot improve either denominator. Latency is omitted without clock evidence.
Distributions report count, min, upper median, mean, nearest-rank p95 and max;
warm-up discovery is separate from discovery inside the measured contact.

Traffic summaries separate sender TX/RX and receiver TX/RX. Root RNS interfaces
are counted once, avoiding server/child double counting. Means from matching
control groups are subtracted to characterise additional workload; they are not
exact per-packet control attribution. Packed packet length, signed body size and
RNS-accounted bytes are separate quantities. No TCP/IP packet capture or radio
airtime is inferred. Setup traffic before `start` counters is excluded.

Acceptance for this iteration is reproducible tooling and truthful local evidence,
not a product latency/loss pass. Gate 03 stays open until two physical-host runs
and agreed later performance requirements exist. HOLD also depends on the other
[feasibility gates](feasibility-gates.md). No production adapter, equipment purchase,
external outreach, radio transmission or remote publication is part of this work.

## Recorded local validation

See the [4 October 2026 result report](contact-campaign-results.md): 490/490 full
campaign trials and 26/26 final-source smoke trials completed without worker
failures. These are single-host loopback observations. Physical-host execution
remains pending.
