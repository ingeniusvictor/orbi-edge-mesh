# ADR-0009 — Recovery Requires Policy Authorization

Status: ACCEPTED

## Decision

An ORBI Edge node may automatically recover a failed AI service only after current thermal/power policy authorizes the restart.

## Rationale

A watchdog that ignores device state can turn resilience into repeated thermal or battery stress.

## Ordering

```text
device preservation
> recovery
> availability
```

Availability is valuable, but not at the cost of unsafe operation.

## Consequence

A node may intentionally remain unavailable while cooling down or protecting battery reserve.

That behavior is correct.
