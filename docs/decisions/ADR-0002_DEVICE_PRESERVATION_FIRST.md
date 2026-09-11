# ADR-0002 — Device Preservation First

Status: ACCEPTED

## Decision

ORBI Edge Mesh treats thermal and power protection as a first-class scheduling constraint, not as a later optimization.

## Rationale

The initial hardware pool consists of consumer Android phones, including daily-use devices.

A benchmark that achieves higher throughput by creating unsafe sustained heat or damaging battery behavior is not considered a successful ORBI result.

## Consequences

The scheduler may intentionally choose:
- a slower node;
- a cooler node;
- a better-powered node;
- no node at all.

This is acceptable.

## Principle

```text
Useful compute > maximum compute
Sustainable compute > peak benchmark
Device preservation > short-term throughput
```
