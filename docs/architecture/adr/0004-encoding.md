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
