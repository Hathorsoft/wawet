# 0003 — Application and transport separation

Status: Accepted
Date: 4 October 2026

## Context

Simulator and real bearer experiments need the same validation/event logic.

## Decision

EventTransport exposes subscribe/send/close with byte payloads and conservative delivery metadata. Application clocks determine expiry.

## Alternatives

Direct RNS calls throughout domain code hinder testing and alternative bearers. A giant gateway framework is premature.

## Consequences

No transport-specific fields in events. Callback adapters must serialise onto one application thread; no implied authentication/truth.

## Revisit gate

Expand only for measured needs such as backpressure, error reporting or receipt semantics.
