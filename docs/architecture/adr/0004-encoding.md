# 0004 — Experimental compact encoding

Status: Experimental
Date: 4 October 2026

## Context

Current events have fixed scalar fields; no optional text or signatures. Extremely constrained links require measured size.

## Decision

Use a 38-byte big-endian frame with explicit magic/version and canonical vectors. Freeze v1 layout; new fields require an explicit version.

## Alternatives

CBOR supports extensibility with small encoded integers but needs canonical/schema choices; MessagePack is similarly flexible. Protobuf has strong tooling but field tags/runtime choices; FlatBuffers offers access patterns of little value for a tiny frame and adds structural overhead. None was benchmarked here.

## Consequences

Fixed frame simplifies parser/bounds but reserves no authenticated or variable fields. Plain packets are not secure. Published numbers refer only to the implemented frame.

## Revisit gate

Benchmark equivalent optional/authenticated messages and MCU parser memory before selecting production encoding.

## Task 09 desktop evidence — 4 October 2026

The [bounded comparison](../../research/encoding-comparison.md) measures original
binary-extension and restricted CBOR profiles, including optional fields and
key/signature placeholders. Maximum application sizes are 293 and 309 bytes;
frozen v1 remains 38 bytes. Keep v1 and use binary as the maximum-size research
reference for task 14, retaining CBOR for comparison. No production encoding is
selected. Status remains Experimental; real MCU footprint, whole-host T06 and
authenticated-envelope design remain required before revisiting production use.
