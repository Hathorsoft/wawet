# LoRa and RNode research

**FACT:** LoRa is a radio PHY; LoRaWAN is a separate networking system. Neither
implies Meshtastic or Reticulum. The [Semtech SX1262 product page](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262)
is the datasheet entry point. The [RNS supported hardware documentation](https://reticulum.network/manual/hardware.html)
lists RNode platforms. The [RNode firmware](https://github.com/markqvist/RNode_Firmware)
uses GPLv3. Its modem/interface role does not supply an autonomous Wawet app.

**DESIGN DECISION:** initial radio proof uses two upstream-supported development
boards and a host running RNS. This avoids conflating firmware interoperability
with standalone product feasibility. Do not import Meshtastic's networking into
Wawet's application layer. Do not fork RNode firmware before finding a concrete
missing capability.

## Candidate comparison, not a purchasing recommendation

| Class | Opportunity | Must verify |
| --- | --- | --- |
| ESP32 + SX1262 development unit supported by RNode | BLE-capable MCU and inexpensive sub-GHz modem | Exact board revision, firmware target, RF matching, UK antenna, host interface |
| Existing TTGO T-Beam variant | Historical concept candidate; GNSS integration on some variants | Exact radio/GNSS revision and current upstream support, not name alone |
| Custom BLE MCU + SX1262 | Potential BOM/PCB control | Porting, host application processor, RF layout, supply, compliance |

No current delivered prices or component quotes were obtained. Board names are
families, not verified interchangeable SKUs. Use the supported list and suppliers'
current schematics to choose two identical regional boards.

## Experiment plan

First test on bench with hosts: exact firmware version, interface serial/BLE
settings, raw event bytes, receive latency and loss. Then compare antenna
locations and orientations without transmitting outside a reviewed UK profile.
Record frequency, bandwidth, spreading factor, coding rate, conducted power,
antenna gain/loss, access constraints and total on-air packet length.
Measure airtime per report and background traffic, simultaneous reporters,
queue starvation and ignition-like power interruptions. No range promises.

**OPEN QUESTION:** RNode firmware plus an application MCU versus a compatible
constrained endpoint. Updates must preserve recovery, identity privacy and radio
limits. Regional profiles live in validated device configuration, not event
encoding; signed settings are not a substitute for a compliance assessment.
