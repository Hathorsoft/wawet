# Foundation adversarial review

Reviewed 4 October 2026 against the founding brief. This is a software/document
review, not an independent hardware or legal assessment.

| Area | Attack / finding | Resolution or explicit remaining risk |
| --- | --- | --- |
| Architecture | A “mesh” application might recreate Reticulum routing | Domain uses EventTransport; no routing/gossip implementation, radio constants or false production adapter |
| Networking | A local packet could be presented as secure routed integration | Spike is explicitly two-process direct PLAIN TCP, unauthenticated and unrouted; authenticated/mobile tests remain gates |
| Edge device | RNode might be confused with a standalone full application node | Research, device roles and concepts distinguish modem and host; standalone processor remains a gate |
| Cost | Cool components and optimistic BOM could undermine £30–£50 goal | Matrix rejects baseline display/microphone/speaker/HaLow; assumptions labelled; midpoint delivered model challenges target |
| Product | Phone-only location contradicts independent located reporting | Minimum concept's limitation explicit; recommended GNSS experiment, no instant-fix assumption |
| Mobility | Stable topology, automatic retransmit or perfect lanes could be assumed | Deterministic links must exist at send and delivery; outage/loss tests; no RF or lane model; no hidden store-and-forward |
| Geography | Stored reports could remain relevant after driving past | Alerts recompute distance/bearing/heading at access; movement regression test |
| Event identity | A reused ID with modified bytes could masquerade as confirmation | First payload retained, conflicting bytes counted/rejected; confirmations not claimed |
| Memory | Dropping oldest records at capacity could admit repeated active events | New records dropped when full; expired records pruned before retention; capacity test |
| Availability | Flood traffic could scan all retained events even after rate limiting | Moved limiter before cache pruning; regression test proves rate-limited inputs skip cache scans |
| Time reporting | Alerts initially restamped their receive time on each read | Preserve original receive time in retention; regression test |
| Privacy | Removing a source ID might be called anonymity | Correlation by location/time/RF/IP remains explicit; local token not sent; no routine tracking or persistent logs |
| Abuse | Signatures could be equated with report truth or Sybil resistance | Neither signatures nor Sybil defences implemented; threat model separates authentication from truth; global limiter can itself be exhausted |
| Encoding | Custom frame could become unversioned magic or fake forward compatibility | Full byte offsets/bounds and canonical vectors; unknown categories preserved without alerts; unsupported versions/trailing bytes rejected |
| Open source | Reticulum/LXMF could be wrongly described as MIT | Current restricted Reticulum License inspected; independent Apache work and optional dependency scope documented; distribution review is a gate |
| Commercial | Branding could be used to forbid lawful forks | Commercial derivatives permitted; official endorsement/trademarks distinct; no subscription/central-service requirement |
| Regulation | US settings or “868 always 1%” could leak into design | No frequency constants; specific UK rows/ERP distinction and unresolved BLE/HaLow profiles; no certified-product assertion |
| Safety | Button examples could silently become mandatory mappings | Provisional taxonomy; stationary three/four-button study; cancellation limits and no public-road distraction testing |
| Prior art | Waycast claims or suspicions could be treated as field evidence | Website claim distinguished from unverified source/hardware/licence/measurements; no imported code or AI-authorship accusation |
| Contributor path | Many files but no executable value | Offline demo and unit tests, packaged CLI, dev checks and optional actual RNS experiment |

## Remaining gates

A malicious node can still flood airtime, spoof position and use unlimited IDs.
No authenticated envelope, outgoing radio-access budget, safe location/time
fault handling, production BLE pairing, firmware recovery or mobile discovery
policy exists. The simulator is single-threaded; a real transport must marshal
callbacks or add explicitly tested concurrency. Expiry pruning is access-driven,
not a background privacy-erasure schedule.

A useful car network needs participation density or infrastructure, legal airtime
and brief-contact performance. A cheap standalone Reticulum-compatible host is
unproven. Current upstream licensing complicates the unrestricted ecosystem goal.
These can materially change the product or architecture. No simulation or local
TCP result closes them. Prioritise the first five backlog gates before custom
PCB, consumer app or public pilot.
