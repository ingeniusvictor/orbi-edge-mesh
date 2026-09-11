# ADR-0008 — Bounded Self-Recovery

Status: ACCEPTED

## Decision

ORBI Edge nodes may automatically restart failed local AI services, but only within a bounded restart budget.

## Rationale

Unlimited restart loops can waste battery, generate heat, mask a persistent fault and create unnecessary process/storage churn.

## Rule

Automatic recovery stops after a configurable finite number of attempts and marks the node for inspection/quarantine.

## Safety precedence

`thermal/power hard block > recovery desire`

Self-healing is subordinate to device preservation.
