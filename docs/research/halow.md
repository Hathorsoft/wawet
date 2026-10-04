# Wi-Fi HaLow research track

**FACT:** Morse Micro offers MM6108 and MM8108 families. Its
[chip information](https://www.morsemicro.com/products/chips) is vendor material,
not a Wawet measurement. The [Linux porting guide](https://www.morsemicro.com/resources/appnotes/MM_APPNOTE-24_Linux_Porting_Guide.pdf)
and [OpenWrt evaluation guide](https://www.morsemicro.com/resources/user_guides/MM6108-Eval-Kit-User-Guide-2.5.pdf)
document supported integration paths. PHY headline rates must not be treated as
application throughput. Regional module variants are not universally usable.

**DESIGN DECISION:** investigate HaLow for Gateway-to-Gateway backhaul and
higher-bandwidth infrastructure. Carry RNS over the resulting IP connection;
Wawet road-event fields do not change. Baseline Drive has no HaLow hardware.

**OPEN QUESTIONS:** obtain UK-usable module quotes and antenna options; determine
applicable IR2030 device classification, channels, occupied bandwidth, power and
access conditions. Do not assume US 915 MHz equipment or wider channels can be
used in the UK. Verify exact Linux kernel, driver, firmware/board configuration
and licences; distinguish vendor OpenWrt images from upstream support.

Bench plan: two isolated IP gateways, measure goodput, latency, reconnect time,
idle/active current and temperature at several channel widths, then test RNS
traffic and competing bulk transfers. Record line of sight, antenna height,
interference and legal profile. Compare against Ethernet and conventional Wi-Fi
before accepting additional cost. Current pricing, power and range remain
unmeasured; no hardware recommendation is frozen.
