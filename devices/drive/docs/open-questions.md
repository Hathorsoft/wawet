# Drive open questions

No final electronics SKU is approved. These ten questions gate the product:

| Priority | Question | Evidence that closes it |
| --- | --- | --- |
| 1 | What standalone application/Reticulum host fits cost and power? | Running endpoint on candidate processors, memory/current/latency and licence review |
| 2 | Can brief vehicle encounters deliver fresh events with legal airtime? | Two-radio latency/loss/announce/queue measurements at reviewed profiles |
| 3 | Does recommended Drive need onboard GNSS? | No-phone cold/warm start, poor sky, accuracy/time and BOM comparisons with phone background location |
| 4 | What participation density or relay coverage makes reports useful? | Contact simulations and controlled multi-node pilot across urban/rural traffic |
| 5 | How much abuse protection works without tracking/accounts? | Adversarial corroboration, spoofed location, Sybil and flood experiments |
| 6 | Can certified retail economics reach the aspirational band? | Quoted BOM, yield, assembly, VAT, warranty, certification and channel model |
| 7 | Which UK bearer profiles and whole-product conformity routes apply? | Lab-reviewed spectrum/device classification and GB/NI test plan |
| 8 | What button taxonomy/layout is safe and accessible? | Tactile differentiation, accidental activation, feedback/undo and stationary study |
| 9 | Which antenna, mount and power choices survive vehicle use? | Antenna-placement RF results, heat/UV/vibration tests, cranking and parked draw measurements |
| 10 | Can upstream licensing and contributor rights support the intended ecosystem? | Exact-version legal review and documented distribution scope |

Additional engineering questions: time without a fix, report location offset,
regional provisioning without routine phone dependency, pairing UX without a
display, update recovery, privacy-preserving diagnostics and lifetime support.
Record decisions in ADRs rather than silently treating these as solved.
