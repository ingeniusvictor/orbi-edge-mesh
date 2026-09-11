# ADR-0005 — Adaptive but Explainable

Status: ACCEPTED

## Decision

The first adaptive scheduler will remain deterministic and explainable.

## Rationale

ORBI Edge Mesh will operate on constrained, heterogeneous hardware.

Before introducing learned scheduling, every routing decision should be explainable using visible inputs such as:
- locality
- health
- temperature
- battery
- reliability
- latency

## Rule

No learned model may later override hard safety gates without an explicit architecture decision.

## Principle

```text
Adaptive != opaque
Learning != loss of control
Safety gates remain deterministic
```
