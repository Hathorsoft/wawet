# Drive paper hardware concepts and cost model

**ASSUMPTION:** GBP ranges below are planning allowances for a hypothetical
1,000-unit production run, excluding VAT, enclosure, assembly, tooling,
certification, shipping and margin. No supplier quotations were obtained;
uncertainty is at least ±50%. They are not current component prices or promises.
No concept has established a viable standalone Reticulum application processor.

| Concept | Tentative component classes | Function / phone dependency | Electronics BOM allowance | Advantages / limits | Compliance implications |
| --- | --- | --- | --- | --- | --- |
| A — Minimum | BLE MCU with internal flash, SX1262-class modem, supplied antenna, buttons, LED, USB protection/regulation | Receives/basic local events; phone supplies fresh location for located reporting | £10–£18 | Cheapest paper option; no-phone located reporting fails the desired independence unless another fresh location source is proven | Whole radio/EMC/safety assessment; phone reliance does not remove radio duties |
| B — Drive, preferred experiment | A plus GNSS and suitable antenna; application host still to validate | Independent location/time when GNSS fix is valid; optional phone maps/dictation | £16–£28 | Best match to standalone goal; acquisition/antenna/thermal cost, no instant fix guarantee | Combined-radio layout, final antennas, automotive conditions and power tests |
| C — Fleet / Pro, investigate only | B plus justified protected hard-wire accessory, retention/recovery flash, optional motion sensor | Managed installations/diagnostics; no cloud dependency for local events | £24–£42 | Fleet install flexibility; cost/complexity/privacy increase; secure element only after threat justification | Installation/transients and accessory conformity scope increase; verify vehicle approval applicability |

If a Linux-class host is required in every Drive, these allowances are likely
invalid. Cost the processor and power supply before presenting B as feasible.
These are three architectural comparisons, not three proposed commercial SKUs.
Aim for one useful product plus installation accessories.

## GNSS tradeoff

Onboard: independent source of position/time but acquisition is not guaranteed
on startup; cost, antenna, power and poor sky view matter. Phone: lower device
BOM and fused location, but permissions, BLE disconnect and locked/background
behaviour can prevent reports. Hybrid: onboard baseline with phone improvement,
if measured performance justifies cost. Never extrapolate a last-known fix as
current location without explicit validity and confidence. Simulator location
is exact; production uncertainty requires additional protocol/design work.

## Power alternatives

| Choice | Cost / install | Main experiment / risk |
| --- | --- | --- |
| USB-C core + USB-A adapter cable | Regional accessories, existing car adapter | Connector retention/strain, adapter quality, brownouts, live parked power |
| USB-C vehicle socket | Simple where available | Socket current/ignition behaviour and cable orientation; no assumption of PD |
| External 12 V accessory adapter | Protects core from raw vehicle supply | Adapter transient/conformity evidence, enclosure heat and accessory QA |
| Integrated 12 V plug | Fewer parts to consumer | Placement/antenna limitations, bigger enclosure, wider power qualification |
| Hard-wire fleet accessory | Controlled install later | Fusing, reverse polarity, standby budget, qualified installation |

USB power changes the exposure boundary but does not eliminate whole-product
vehicle testing. No battery/RTC backup is assumed; startup time and time validity
must be handled before sending a report.

## Commercial model example, not quotation

Test low/mid/high electronics £10/£20/£30, assembly/test £2/£4/£6,
enclosure/mount £2/£4/£6, packaging £1/£2/£3, logistics £1/£2/£4,
certification/tooling allocation £1/£5/£15 and warranty reserve £1/£2/£4.
That gives indicative delivered allowances £18/£39/£68 before commercial margin
and VAT. Certification allocation must be actual programme cost divided by
credible shipped volume, not a fixed optimistic £1. These figures illustrate
sensitivity, not independent supplier evidence.

For example, a hypothetical £40 VAT-inclusive sale at an assumed 20% rate
provides £33.33 before VAT, transaction fees and channel margin. The midpoint
allowance already exceeds this. The aspirational £30–£50 band needs lower costs,
volume or a different product, not optimistic rounding. Validate tax treatment
and distribution terms in the real business model. Direct sales and retailers
have different support/acquisition/channel costs; include both before a price.
