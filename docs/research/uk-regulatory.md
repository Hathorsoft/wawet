# UK regulatory foundation

Status: research, checked 4 October 2026. Not a transmitter configuration or a
claim of certification. GB and Northern Ireland market routes must be assessed
separately. The application has no country frequency constants.

## Radio matrix

**FACT:** [Ofcom IR2030](https://www.ofcom.org.uk/__data/assets/pdf_file/0028/84970/ir-2030.pdf)
has device-class-specific rules, not one rule for “868 MHz”. Initial extracts
below refer to printed pages 11–14 (PDF pages 20–23); read whole rows and the
referenced standards before adopting a profile. Values are **e.r.p.**, not EIRP.

| Radio candidate / device class | Region / band | Extract or unresolved constraint | Source / gate |
| --- | --- | --- | --- |
| LoRa / non-specific SRD, IR2030/1/16 | UK, 868.0–868.6 MHz | 25 mW e.r.p.; required spectrum-access techniques or alternative ≤1% duty cycle | IR2030 row 1/16, including continuation; occupied bandwidth must fit |
| LoRa / non-specific SRD, IR2030/1/17 | UK, 868.7–869.2 MHz | 25 mW e.r.p.; access techniques or alternative ≤0.1% duty cycle | IR2030 row 1/17 |
| LoRa / non-specific SRD, IR2030/1/19 | UK, 869.40–869.65 MHz | 500 mW e.r.p.; access conditions and continuation need full review | IR2030 row 1/19; not an approved profile |
| BLE / wideband data candidate | UK, 2.4 GHz | Class, power, emissions and access assessment still required | IR2030 and applicable designated EN 300 328 version |
| HaLow / data-network candidate | UK, sub-GHz | Classification, legal bandwidth, channel plan, power and access unresolved | IR2030 complete data-network rows; vendor region is not approval |
| GNSS receiver | UK, receive-only | No intentional GNSS transmission; combined product still needs assessment | Final equipment conformity plan |
| Amateur experiments | UK, licence-dependent bands | Operator and content restrictions; consumer encrypted routing not approved | Ofcom licence/guidance; separate optional network |

**DESIGN DECISION:** a regulatory profile must bind exact device role, region,
frequency, bandwidth, antenna, power and access method. Do not configure a
transmitter by selecting a tempting power limit from another row. Budget all
traffic, including announces, control packets and retries. Assess actual antenna
gain/loss and ERP/EIRP conversions; chip output power alone is insufficient.

## Product obligations and evidence to collect

[GB radio-equipment guidance](https://www.gov.uk/government/publications/radio-equipment-regulations-2017/radio-equipment-regulations-2017-great-britain)
describes essential requirements, technical documentation, conformity routes,
markings and manufacturer/importer obligations. It recognises CE and UKCA routes
in GB under specified conditions; do not assume identical NI/EEA rules or that
certified modules certify the complete accessory.

| Area | Primary source | Required project evidence / open gate |
| --- | --- | --- |
| Radio / EMC / safety | GB guidance above; [ETSI EN 300 220](https://www.etsi.org/deliver/etsi_en/300200_300299/30022002/03.02.01_60/en_30022002v030201p.pdf) | Determine current applicable designated versions and conformity route with test lab; RF/emissions/safety reports, technical file, declaration, labels and instructions |
| Restricted substances | [RoHS guidance](https://www.gov.uk/guidance/rohs-compliance-and-guidance) | Supplier declarations, materials traceability and scope assessment |
| End-of-life electronics | [EEE producer responsibility](https://www.gov.uk/guidance/electrical-and-electronic-equipment-eee-producer-responsibility) | Producer obligations, registration/compliance scheme as applicable, marking and take-back process |
| Batteries, if introduced | [Producer responsibility](https://www.gov.uk/government/collections/producer-responsibility-regulations) | Determine applicable battery obligations; baseline concept avoids a battery |
| Vehicle installation | Automotive test-lab assessment | Determine accessory applicability, electrical transients, EMC and whether vehicle-specific approvals apply; not settled by USB power |
| Driver interaction | [GOV.UK driving-device guidance](https://www.gov.uk/using-mobile-phones-when-driving-the-law) | Mount visibility, distraction, stationary-only configuration; no legal safety assertion |

The cited older ETSI document is a research entry point, not an assertion that
its edition is currently designated. No certification body has assessed Wawet.

Next gate: create a signed-off regional profile and conformity/test plan before
radiating experiments; maintain raw evidence with source edition and date. Use
conducted/attenuated bench setups where appropriate. International variants
require new reviews, not translation of UK frequency settings.
