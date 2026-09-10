# ADR-0011 — Storage Is Distributed, Not Shared

Status: ACCEPTED

## Decision

ORBI Edge Mesh models each phone's storage as an independent local resource.

## Rationale

The three Android devices do not provide one coherent filesystem.

Treating aggregate capacity as one disk would create false assumptions about:
- model availability
- load latency
- transfer cost
- failure isolation

## Rule

Aggregate storage may be reported for inventory purposes, but all placement and execution decisions must use per-node storage state.

## Consequence

Model replicas and transfers are explicit operations, not implicit shared access.
