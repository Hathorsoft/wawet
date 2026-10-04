# 0002 — Reticulum networking direction

Status: Experimental
Date: 4 October 2026

## Context

Upstream offers heterogeneous networking; the local spike proves only direct TCP event delivery. Current upstream licence includes restrictions.

## Decision

Prefer Reticulum as the network foundation subject to licence, standalone host, mobile encounter and radio tests. No Wawet general routing protocol.

## Alternatives

Meshtastic is the historical concept layer; a custom mesh would duplicate work. Direct transport-only approaches remain possible if requirements cannot fit.

## Consequences

No production adapter or standalone cheap endpoint is established. LXMF remains optional for messaging; not forced into hazard dissemination.

## Revisit gate

Accept only after authenticated delivery, legal airtime/contact tests, host cost and distribution scope pass. See ../../research/reticulum.md.
