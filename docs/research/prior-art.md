# Prior art and provenance

No code, firmware or architecture was imported from Waycast or another
vehicular project. Similar problem statements do not independently establish
technical feasibility or priority. Earlier project concept notes are retained;
author-supplied history is not an independently authenticated archive.

| System | Primary entry point | Comparison and investigation |
| --- | --- | --- |
| Waze | [Road reporting](https://support.google.com/waze/answer/13739290) | Existing hazard UX and spam limits; evaluate tactile offline reporting separately |
| C-V2X | [3GPP V2X study](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2898) | Standards-based vehicle communications; research deployment and cost rather than assert equivalence |
| DSRC / 802.11p | [IEEE standards](https://standards.ieee.org/standard/802_11p-2010.html) | Historical vehicular link approach; compare mobility objectives and current standards evolution |
| Meshtastic | [Official introduction](https://meshtastic.org/docs/introduction/) | LoRa community networking, not the selected Wawet network layer |
| APRS / packet radio | [APRS](https://www.aprs.org/) | Position/message ideas; privacy and operator requirements need separate review |
| Reticulum applications | [Upstream catalogue](https://reticulum.network/manual/programs.html) | Messaging/community/disaster use; examine actual implementations before integration |
| Community networks | [Freifunk](https://freifunk.net/en/) | Distributed maintenance and infrastructure participation; do not infer moving-radio performance |
| Waycast | [Project website](https://waycast.io/) | Similar off-grid vehicle claims; not independently validated here |

**FACT about Waycast's website:** it describes an off-grid vehicular mesh.
That establishes a published claim, not working hardware, tested range, UK
legality or independent provenance. This run did not establish a repository,
release history, licence, reproducible implementation or third-party field data.
Do not repeat suspicions about AI-generated content as verified facts.

Verification task: identify linked source repositories, dated history and
licences; reproduce build and hardware claims independently; seek raw field
measurements. Until then, classify Waycast as unverified prior-art claims.
Never import its code solely because it is publicly visible. Build Wawet from
explicit requirements, primary upstream APIs and measured experiments.
