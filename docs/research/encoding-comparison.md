# Task 09 — bounded event-encoding comparison

EXPERIMENTAL RESULT — 4 October 2026. Desktop research only; production protocol
selection and MCU parser footprint remain open. Source: [original harness](../../tools/encoding_comparison.py).
No third-party implementation or dependency was imported.

## Research formats (specified for this experiment)

DESIGN DECISION: both candidates represent the same `RoadEvent` and five bounded
optional values. Accuracy is an integer 0–65535 metres (zero is representable, not
an assertion of perfect measurement). Reference is exactly 16 opaque bytes; text
is at most 128 UTF-8 bytes, including empty text. Key and signature are exactly
32 and 64 bytes and must occur together. Their contents are synthetic placeholders;
there is no signing, verification, trust policy or encryption here. All base
fields retain the [v1 limits](../../protocol/road-event-v1.md), including unknown
categories and the absent-heading sentinel. These choices are research assumptions,
not new application fields or a security specification.

- **Binary:** `57 58 01` (WX, experimental version 1), followed by an exact v1
  38-byte frame, then zero or more extensions. Each extension is one-byte key,
  one-byte length and that many bytes. Keys 1–5 are accuracy, reference, text,
  key and signature, in strictly increasing order. Accuracy is two bytes big
  endian. Maximum complete size is **293 bytes**: 41 + 4 + 18 + 130 + 34 + 66.
- **Restricted CBOR:** one definite-length map of 9–14 pairs. Keys 0–8 are
  experimental version 1, event ID, category, latitude_e5, longitude_e5,
  heading_cdeg (65535 for absent), creation, TTL and radius. Optional keys 9–13
  are accuracy, reference, text, key and signature. Integers use shortest
  encodings; keys increase numerically. Only integer, byte-string and text-string
  field values are supported. Maximum complete size is **309 bytes**: 54 base,
  153 optional and 102 key/signature bytes. This is a schema-specific subset,
  not a general CBOR library. Integer and string representations follow
  [RFC 8949 sections 3 and 4](https://www.rfc-editor.org/rfc/rfc8949.html).

Receivers reject excessive message size before parsing, unsupported versions,
missing base fields, duplicate/out-of-order/unknown keys, invalid scalar ranges,
incorrect byte/string types or lengths, invalid UTF-8, truncation and trailing
unstructured bytes. CBOR additionally rejects nonminimal integers/lengths,
indefinite lengths, arrays, nested maps, tags, floats and simple values. These
closed research profiles intentionally do not implement generic extension skipping.
Version numbers are private experiment identifiers, not a published v2 protocol.

## Reproduction and measurement method

From the repository root, using Python 3.11+ and no runtime dependencies:

```sh
.venv/bin/python tools/encoding_comparison.py --sizes-only > /tmp/wawet-sizes-a.json
.venv/bin/python tools/encoding_comparison.py --sizes-only > /tmp/wawet-sizes-b.json
cmp /tmp/wawet-sizes-a.json /tmp/wawet-sizes-b.json
.venv/bin/python tools/encoding_comparison.py --iterations 1000 --repeats 5 > /tmp/wawet-encoding.json
PYTHON=.venv/bin/python ./scripts/check
PYTHON=.venv/bin/python ./scripts/demo
```

The [raw result](results/encoding-comparison.json) records all fixture sizes,
base/optional/key-signature breakdowns, timing samples, traced allocation samples,
source/input hashes, base Git revision, working status and interpreter/platform.
The two size-only runs matched exactly. Timing is expected to vary between runs.
Fixtures cover both frozen vectors, minimum/maximum scalars, both geographic
extremes and each optional field individually/all together, unsigned and with
placeholders. V1 stays 38 bytes and cannot represent these optional values.

Each codec benchmark runs in its own fresh subprocess, sequentially. Five repeats
of 1,000 operations use `perf_counter_ns`; allocation measurement is a separate
loop with `tracemalloc`. Reported peaks cover transient Python allocations during
that loop, including loop overhead, after imports and fixture construction.
They exclude interpreter/import footprint, retained queues, native allocations,
network buffers and RSS. Baseline is a no-op loop measured separately; raw values
are not silently baseline-subtracted. Alternatives benchmark the same fully
populated maximum report; v1 benchmarks only its base event (its decode wrapper
also constructs the shared Message). This is not an equal-capability timing
comparison with v1. No speed threshold or hardware acceptance is inferred.

## Recorded results

| Fixture | Binary unsigned / placeholder | CBOR unsigned / placeholder |
| --- | --- | --- |
| north-hazard | 41 / 141 | 51 / 153 |
| unknown-category-southwest | 41 / 141 | 49 / 151 |
| boundary_min | 41 / 141 | 37 / 139 |
| boundary_max | 41 / 141 | 54 / 156 |
| boundary_southwest | 41 / 141 | 48 / 150 |
| boundary_northeast | 41 / 141 | 49 / 151 |
| accuracy | 45 / 145 | 58 / 160 |
| reference | 59 / 159 | 72 / 174 |
| text | 171 / 271 | 185 / 287 |
| all_options | 193 / 293 | 207 / 309 |

| Codec | Encode median ns | Decode median ns | Encode / decode peak traced bytes | No-op median ns / peak bytes |
| --- | --- | --- | --- | --- |
| binary | 1746 | 4818 | 997 / 1534 | 24 / 128 |
| cbor | 8391 | 12125 | 3303 / 3013 | 23 / 128 |
| v1 | 186 | 2058 | 151 / 629 | 23 / 128 |

## Recommendation and remaining gates

DESIGN DECISION: keep frozen v1 for the simulator. Carry the binary envelope
forward as the smaller maximum-size research reference for task 14; retain CBOR
as the extensible alternative for later evaluation. CBOR can save bytes for small
scalar values, but this implementation costs more parser time/allocation on this
computer. These observations do not select a production encoding or establish
on-air size: framing, transport authentication and control traffic are excluded.
The explicit key adds cost that a future key-discovery design may distribute
differently. Signature domain separation and lifecycle belong to task 14.

Task 09's bounded desktop comparison is complete locally. ADR 0004 remains
Experimental; task 04 must measure actual MCU/host footprint and whole-host T06
headroom. Task 14 still requires task 03's physical-host acceptance evidence.
Task 18 is next eligible in the software sequence. Gates 01–05 and G01 HOLD remain
unchanged. MessagePack, Protobuf and FlatBuffers are deferred. No RF transmission,
external outreach, dependency addition, purchase, commit, push or publication
occurred in this package. Hosted Python 3.12/3.13 checks remain unverified.
