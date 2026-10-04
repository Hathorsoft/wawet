# Task 18 evidence register — 4 October 2026

Access date for every entry: **2026-10-04**. Baseline Wawet HEAD:
`3e247c8f16045b8891df2d38ae74fac80d960710`; starting Git status clean.
This is a bounded public-source review, not exhaustive prior-art/patent research,
legal clearance or an independently authenticated project chronology.

## Method and source limits

Official pages and public repository files were inspected using the web reader.
Waycast was additionally cloned into `/private/tmp/wawet-task18-waycast` for
read-only source/history inspection and isolated upstream tests. No source was
copied into Wawet. Search results were discovery leads, not measurements. Links
below were opened unless explicitly marked retrieval-limited. Mutable pages have
no frozen version guarantee; only the Waycast reproduction is pinned and hashed.
No real participant data or downloaded external datasets are included.

## Eight-system register

| System / claim investigated | Primary source and implementation / revision | Licence evidence | Independent evidence and reproduction limit |
| --- | --- | --- | --- |
| Waze: hazard reporting, feedback and reporting limits | [Official help](https://support.google.com/waze/answer/13739290), mutable service documentation; no application release/source revision established | Help is not a source-code grant; implementation redistribution rights not established | [TDOT research report landing page](https://rosap.ntl.bts.gov/view/dot/66932), *WAZE Data Reporting*, 2022, describes data-quality/use-case research. Report existence checked; raw data and analyses not reproduced. No offline peer-radio evidence inferred. |
| C-V2X: standards-based vehicle communication | [3GPP TR 22.885](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2898), Release 14, v14.0.0 listing; a study report, not a selected Wawet implementation | Catalogue does not establish implementation, patent or redistribution rights | [UCR SEE-V2X](https://cisl.ucr.edu/SEE-V2X/) describes commercial-radio experiments, application/MAC traces and linked code/data. Methods/data availability described by experiment authors; raw records not downloaded/reanalysed. Not a LoRa benchmark. |
| DSRC / 802.11p: vehicular WLAN | [IEEE catalogue](https://standards.ieee.org/ieee/802.11p/3953/), 802.11p-2010, marked superseded; full standard not acquired | Catalogue offers purchase/subscription; no software grant inferred | [BME dataset repository](https://github.com/BMEAutomatedDrive/v2xdatasets) describes four-vehicle ITS-G5 measurements on 19 May 2023, equipment, transmitted/received messages and an external dataset link. Independent of Wawet/Waycast; records not downloaded, licence applicability to external data not reviewed. |
| Meshtastic: off-grid LoRa networking | [Introduction](https://meshtastic.org/docs/introduction/); [firmware](https://github.com/meshtastic/firmware/blob/master/LICENSE), mutable master | Inspected firmware LICENSE contains GPLv3; component/file exceptions and exact release obligations not audited | [Campus study, arXiv v1](https://arxiv.org/abs/2605.20379v1), 19 May 2026, describes equipment and RSSI/SNR observations. Abstract inspected, not full methods/raw-data reproduction; campus evidence does not establish opposing-vehicle deadlines. Firmware build would require additional toolchain/dependency review. |
| APRS / packet radio: local information and messaging | [APRS overview](https://www.aprs.org/); [Dire Wolf](https://github.com/wb2osz/direwolf), mutable repository, provides a concrete modem/encoder-decoder example | [Dire Wolf LICENSE](https://raw.githubusercontent.com/wb2osz/direwolf/master/LICENSE) contains GPLv2; not a licence for every APRS implementation | [LoRa APRS flight-data repository](https://github.com/SQ2CPA/lora-aprs-balloon-flight-data) describes raw frames and processed balloon telemetry. No records copied/reanalysed; balloon reception is not road-contact delivery evidence. Operator/profile review remains separate. |
| Reticulum applications: actual client software | Original [catalogue](https://reticulum.network/manual/programs.html) retrieval failed; inspected [Sideband repository](https://github.com/markqvist/Sideband) instead, mutable main, an LXMF client | [Sideband root LICENSE](https://raw.githubusercontent.com/markqvist/Sideband/main/LICENSE) contains CC BY-NC-SA 4.0. Do not conflate this with RNS/LXMF or assume every file has identical scope | Bounded independent-performance search found no inspected dataset establishing Wawet moving-contact acceptance. Existing Wawet loopback evidence is local preparation. Sideband installation/dependencies were not executed. |
| Community networks: distributed participation/infrastructure | [Freifunk](https://freifunk.net/en/); [Gluon licence](https://raw.githubusercontent.com/freifunk-gluon/gluon/main/LICENSE), mutable main, concrete firmware framework example | Gluon states BSD-2-Clause with file/subtree exceptions and separately identifies GPLv2 OpenWrt repositories; no blanket firmware-image clearance | [Community performance-test thread](https://forum.freifunk.net/t/performance-test-online/12533) discovered, but reader retrieval failed. Search lead only; no independently reproduced measurements. Firmware build/hardware setup outside desktop review. |
| Waycast: off-grid vehicular reports | [Official site](https://waycast.io/) links [alviso/waycast](https://github.com/alviso/waycast); inspected revision `958f4a6ea6436d145402830c3edd372e2e40f74e` | [Pinned LICENSE](https://github.com/alviso/waycast/blob/958f4a6ea6436d145402830c3edd372e2e40f74e/LICENSE) contains GPLv3; separate dependency notices need review before reuse | Three dependency-free upstream test executables reproduced; [raw commands/results/hashes](prior-art-reproduction.json). No independent raw radio/moving-contact measurements located through recorded searches. Full GUI and physical reproduction remain unattempted. |

Licence names above identify inspected evidence, not legal interpretation or
permission to bundle code. The broader entries establish relevant examples and
research leads; they are not comprehensive reviews of those ecosystems.

## Waycast findings

**FACT — attribution/source:** the official site's GitHub link resolves to the
vehicular project `alviso/waycast`. The similarly named `javif89/waycast` is a
Wayland launcher and was excluded; the docs.rs `waycast` crate describes an LLM
observability service and was also excluded. Name matches are not attribution.

**FACT — dated Git history:** the fetched main history has 30 commits. Earliest
reachable commit is `855c39b5115725cdb53425e2cc8021158970d01e`, with author and
committer timestamps `2026-07-24T15:27:49-07:00`, described as the initial public
release. HEAD's author/committer timestamp is `2026-07-26T21:28:10-07:00`.
Fetched tags run from v0.5.0 through v0.8.7 (13 tags); v0.8.7 resolves to HEAD.
These are repository metadata, not proof of when development or publication
began. The site's July release narrative was not independently dated. GitHub
release-page and Wayback CDX retrieval failed; release assets and archived first
publication remain unresolved, not absent.

**FACT — licence/build:** root GPLv3 text is present. The pinned
[Makefile](https://github.com/alviso/waycast/blob/958f4a6ea6436d145402830c3edd372e2e40f74e/Makefile)
contains three standalone C test recipes. Reviewed tests and their sources use
memory fixtures and stdout, without sockets, serial-device access or transmission.
The GUI recipe needs `pkg-config`, SDL2, LVGL and cJSON; `deps` fetches additional
sources. `pkg-config` is unavailable here, so no GUI build/dependency installation
was attempted. The [workstation guide](https://github.com/alviso/waycast/blob/958f4a6ea6436d145402830c3edd372e2e40f74e/wiki/workstation.md)
also describes tile-fetching and radio-transmitter paths; neither was run.

**EXPERIMENTAL RESULT — bounded reproduction:** direct clang commands equivalent
to the three Makefile test recipes compiled and ran successfully, with no warnings
or dependency installation. Apple clang 17.0.0, arm64 macOS; all six commands exit
0. Wire and mesh executables each print nine cases passed; net prints NMEA and
DTU success. Report the upstream output rather than invent an aggregate test
count (wire also calls a query/reply check). Exact command arrays, environment,
output and 16 inspected-file SHA-256 values are in the linked JSON. This tests
upstream assertions, not a security audit or a complete simulator reproduction.

**PUBLISHED CLAIMS / OPEN QUESTIONS — physical and security evidence:** the
[hardware page](https://waycast.io/hardware.html) describes an ESP32-P4 touchscreen
host with separate LoRa/GPS interfaces and a Pi-based town node. The site presents
a simulator demo and claims radio exchange, short moving contacts, self-moderation
and privacy. No independent raw field observations establishing these claims
were located. A third-party [project catalogue](https://github.com/s0lness/awesome-esp32)
mentions Waycast; it supplies no inspected measurement dataset. Listing is not
independent replication. No UK conformity, delivered quotation, authenticated
voting or resistance to radio observation is established by this review.

## Repeatable search and retrieval log

Exact web-search queries issued (results depend on index/date):

| Queries | Outcome used in this review |
| --- | --- |
| `Waycast vehicular mesh github source license`; `Waycast off grid vehicle mesh independent test measurements` | Generic matches included unrelated launcher/observability projects; official link resolved identity. |
| `"waycast.io" test github archive`; `"alviso/waycast" test measurements`; `"Waycast" vehicular mesh independent review`; `site:web.archive.org "waycast.io"` | Official pages, catalogue mention and unrelated services; no inspected independent raw field evidence or usable archive chronology. |
| `"Waycast" "LoRa" field test raw data`; `site:gitlab.com "Waycast" LoRa`; `site:codeberg.org "Waycast" LoRa` | Official/candidate catalogue leads; no attributable alternative source or raw field dataset established; Codeberg access reported robots blocking. |
| `Waze road hazard reporting independent evaluation study`; `C-V2X 802.11p comparative field measurements dataset` | Research/report and dataset leads; retained the primary TDOT, UCR and BME pages. |
| `Meshtastic APRS independent packet delivery measurements dataset`; `Reticulum Sideband Freifunk independent performance measurements` | Initial combined searches; refined below to reduce irrelevant matches. |
| `Meshtastic independent packet delivery measurements dataset LoRa`; `APRS packet radio independent measurements dataset` | Campus study and APRS flight-data leads, inspected at their primary pages. |
| `Reticulum Sideband independent performance measurements dataset`; `Freifunk independent performance measurement study` | Sideband and community measurement leads; no inspected applicable moving-contact dataset. |

Additional failed opens: `https://waycast.io/journal.html`,
`https://waycast.io/wiki/workstation.html` and the wiki's linked workstation page;
pinned local wiki substituted for build inspection. GitHub browser opens of
`https://github.com/alviso/waycast/commits/main/`, `/releases`, `/blob/main/LICENSE`
and `/blob/main/Makefile` failed; local clone substituted for file/history evidence.
Raw main LICENSE/Makefile URLs also returned reader cache misses.
Archive endpoint attempted:
`https://web.archive.org/cdx/search/cdx?url=waycast.io%2F&output=json&filter=statuscode%3A200&collapse=timestamp%3A6`
(reader failure). A Waze paper at `https://pmc.ncbi.nlm.nih.gov/articles/PMC6537760/`
returned a browser challenge; no full-paper findings are asserted.
Failures describe this access path, not website availability for everyone.

Local reproduction preparation: initial sandboxed
`git clone --quiet https://github.com/alviso/waycast.git /private/tmp/wawet-task18-waycast`
failed DNS resolution (exit 128); the same approved network fetch succeeded (exit 0).
Inspected `git rev-parse HEAD`, `git log -3`, reverse history, `git tag`,
`git rev-list --count HEAD`, `git show -s v0.8.7`, Makefile/licence/test sources,
`clang --version` and `pkg-config --modversion sdl2` (last command exit 127).
Clone remained clean after direct compiler reproduction; binaries reside outside it.
To repeat, clone into a new temporary checkout, check out the recorded revision,
verify source hashes, then run the JSON command arrays with fresh temporary binary
paths. Do not run hardware, provisioning, tile-fetching or `deps` recipes.

## Interpretation and remaining work

**DESIGN DECISION:** task 18's bounded investigation is complete; no new Wawet
architecture decision is made. Independent evidence can remain explicitly
unverified after documented searching. GUI reproduction, independent chronology
and Waycast physical/security validation remain unfinished. Negative searches
are not proof of nonexistence; none of the results establishes priority or
Wawet's radio, cost, safety or legal feasibility.
