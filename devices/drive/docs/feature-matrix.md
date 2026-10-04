# Hardware feature decision matrix

The [CSV matrix](feature-matrix.csv) contains capability, value, necessity,
planning cost allowance, power/PCB/enclosure/regulatory/manufacturing/reliability
impacts, substitution and disposition for 20 candidate components.

All cost ranges are **assumptions**, not prices or quotations: hypothetical
1,000-unit GBP electronics allowances, uncertainty at least ±50%, excluding VAT,
assembly, shipping and certification. “Unquoted” is deliberate. Do not sum all
rows: rejected/later components are not baseline and module costs can overlap.
Exact current and size measurements require selected part revisions/datasheets.

Source entry points:
[ESP32-S3](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf),
[SX1262](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262),
[RNode support](https://reticulum.network/manual/hardware.html),
[product requirements](product-requirements.md), [human factors](human-factors.md)
and [cost concepts](hardware-concepts.md). No baseline GNSS/secure-element/battery
part is selected. Update each row with exact SKU, quote quantity/date/currency,
source, current/area measurements and decision before a BOM is approved.
