# 0005 — Python for the first vertical slice

Status: Accepted
Date: 4 October 2026

## Context

RNS reference implementation is Python; the simulator needs quick deterministic tests.

## Decision

Use Python 3.11+ and standard library runtime only. Separate optional RNS and dev dependencies.

## Alternatives

Embedded C++/Rust belong in hardware experiments; mobile language choice remains open. Forcing one language across products adds constraints.

## Consequences

New contributors run demo/tests offline without PyPI; dev checks and RNS spike require installs. No firmware feasibility follows from Python success.

## Revisit gate

Revisit runtime constraints when selecting actual embedded host.
