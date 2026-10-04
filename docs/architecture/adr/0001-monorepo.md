# 0001 — Monorepo organisation

Status: Accepted
Date: 4 October 2026

## Context

The foundation combines language-independent event specifications, executable Python research and future product classes.

## Decision

Use shared packages, protocol, devices, docs, tests and tools/scripts. Keep firmware and mobile projects absent until real code exists.

## Alternatives

Separate repositories increase first-contributor coordination; a single package would obscure future device/language roles.

## Consequences

Allows one demo/check workflow. Separate release/licence boundaries when actual firmware/CAD appears.

## Revisit gate

Revisit when independent release cycles or team boundaries justify splitting.
