# Prior art and provenance

Task **18** — bounded desk review completed locally on **4 October 2026**.
[Evidence register, sources and exact searches](results/prior-art-evidence.md)
cover the eight existing comparison entries. [Reproduction records](results/prior-art-reproduction.json)
contain commands, output, environment and hashes for isolated Waycast tests.

No third-party code was imported into Wawet. Similar problem statements do not
establish technical feasibility or priority. Earlier Wawet concept notes are
retained; author-supplied history and Git timestamps are not independently
authenticated publication archives.

## Comparison

All sources accessed 4 October 2026; detailed licence and independent-evidence
limits are in the register. Published descriptions are not Wawet measurements.

| System | Primary entry point | Supported comparison / remaining limit |
| --- | --- | --- |
| Waze | [Road reporting](https://support.google.com/waze/answer/13739290) | Documented reporting, feedback and limits; internet-loss reports are submitted after reconnection. Does not demonstrate offline peer delivery or tactile safety. |
| C-V2X | [3GPP TR 22.885](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2898) | LTE V2X study; independent researcher datasets located. Standards/data do not establish low-cost LoRa equivalence. |
| DSRC / 802.11p | [IEEE catalogue](https://standards.ieee.org/ieee/802.11p/3953/) | Vehicular WLAN amendment marked superseded; a four-vehicle ITS-G5 dataset located. No current Wawet implementation/profile selected. |
| Meshtastic | [Introduction](https://meshtastic.org/docs/introduction/) | Concrete LoRa firmware and independent campus-study lead; no opposing-traffic delivery acceptance inferred. |
| APRS / packet radio | [APRS](https://www.aprs.org/) | Local information/message precedent and concrete Dire Wolf implementation; balloon raw-data lead is not road-contact evidence. |
| Reticulum applications | [Sideband](https://github.com/markqvist/Sideband) | Concrete LXMF client; licence scope is application-specific. Original catalogue retrieval failed; no independent moving-contact dataset established. |
| Community networks | [Freifunk](https://freifunk.net/en/) | Participation/infrastructure precedent and Gluon implementation; no moving-radio performance inferred. |
| Waycast | [Website](https://waycast.io/) / [attributable source](https://github.com/alviso/waycast) | Public source, GPLv3 text, Git history/tags and narrow desktop tests verified. Independent physical/security claims remain unverified. |

## Waycast: what changed

**FACT:** the official website links to `alviso/waycast`, a public vehicular-mesh
repository. This supersedes the earlier review's unresolved repository/licence
finding; similarly named unrelated projects were excluded. The inspected
[revision](https://github.com/alviso/waycast/tree/958f4a6ea6436d145402830c3edd372e2e40f74e)
has source, build instructions and GPLv3 licence text. Git metadata is recorded
in the register; first publication and independently archived chronology remain
unresolved.

**EXPERIMENTAL RESULT:** three upstream unit-test executables compiled and passed
at that revision using Apple clang 17.0.0, without added dependencies. They cover
wire encoding, NMEA/DTU processing and mesh fixtures. This is a narrow independent
software reproduction; the full GUI, radio hardware and moving contacts were not
reproduced. Missing `pkg-config` and additional GUI dependencies are recorded.

**OPEN QUESTION:** searches did not locate independent raw field measurements
supporting Waycast's moving-contact, radio-performance or privacy/security claims.
Its demo and hardware statements remain author-supplied evidence. A third-party
catalogue mention is not replication. UK suitability and product economics were
not established. Searches and retrieval failures are explicitly bounded; they do
not prove evidence is absent everywhere.

## Lessons for Wawet

These are research implications, not new architecture decisions:

- Offline reporting must be distinguished from deferred upload. Test the actual
  phone-absent experience rather than infer it from a reporting interface.
- A working parser or simulated relay rule cannot establish a moving contact
  deadline. Tasks 03 and 08 still need their physical evidence.
- Inspect the application host separately from the modem. Waycast's published
  hardware configuration illustrates that distinction; it does not select or
  cost a standalone Wawet host.
- Votes, short TTLs and absence of a central server do not by themselves prove
  authenticated truth, Sybil resistance or immunity to location observation.
  Tasks 14/15 retain their prerequisites and review duties.
- Review exact component licences before any reuse. Public visibility or a root
  licence label alone is insufficient to approve a bundled product.

## Completion boundary and next gate

Task 18's agreed desk scope is complete: source/licence/history, reproduction
eligibility and independent evidence were investigated, with unresolved claims
labelled. Full GUI/hardware reproduction and independently authenticated chronology
remain unfinished; they are not hidden acceptance results. No code was imported,
no RF transmission or outreach occurred, and no architecture/protocol changed.

This package closes no feasibility gate and satisfies no additional registered
prerequisite. Task 14 still requires physical-host task 03 even though 09 is
complete. Next substantive work requires arranging qualified task 01 review,
task 04 hardware/instruments or task 03's two physical hosts and clock evidence.
Gates 01–05 and G01 investment **HOLD** remain unchanged.
