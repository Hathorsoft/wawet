# 0007 — Simple edge and phone responsibilities

Status: Accepted principle; hardware selection Proposed
Date: 4 October 2026

## Context

BOM, power and usability are product constraints. No-phone reporting conflicts with relying exclusively on phone location.

## Decision

Use phones for maps/dictation/configuration and gateways for complex networking/observability. Retain hardware necessary for useful offline basics. Compare onboard GNSS with phone/hybrid through measurements.

## Alternatives

Adding display/microphone/HaLow to every edge is unsupported. Cheapest phone-only location concept fails independent located reporting until proven otherwise.

## Consequences

Recommended paper concept includes GNSS as an experiment, not a final part selection. Extra application host may invalidate cost allowances.

## Revisit gate

Evidence from no-phone startup, background BLE/location, host cost, antenna and power tests.
