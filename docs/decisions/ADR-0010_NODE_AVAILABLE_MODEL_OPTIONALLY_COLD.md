# ADR-0010 — Node Available, Model Optionally Cold

Status: ACCEPTED

## Decision

An ORBI Edge node may remain online, discoverable and healthy while its heavy AI model is unloaded.

## Rationale

Permanent model residency can waste:
- RAM
- battery
- heat budget
- storage I/O over repeated process churn

An infrastructure node should separate its lightweight control plane from its heavier inference plane.

## Rule

```text
control plane availability
!=
inference model residency
```

## Consequence

The scheduler must understand cold-start cost and should prefer already-warm nodes for latency-sensitive work when safe and appropriate.
