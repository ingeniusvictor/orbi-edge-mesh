# ADR-0003 — Prefer Model Locality

Status: ACCEPTED

## Decision

ORBI Edge Mesh prefers executing a task on a node where the requested model is already local and loaded, subject to thermal/power eligibility.

## Rationale

Model movement and repeated loading can be expensive on mobile hardware.

Locality reduces:
- load latency;
- storage reads;
- network transfer;
- battery impact;
- avoidable heat.

## Important constraint

Model locality never overrides device-preservation policy.

```text
loaded model + critical temperature
→ do not route

cold model + healthy node
→ may be preferred over unsafe loaded node
```

## Consequence

The scheduler must understand model identity separately from generic service identity.
