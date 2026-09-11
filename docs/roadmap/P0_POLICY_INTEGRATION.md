# P0 — Thermal/Power Policy Integration

Status: IMPLEMENTED IN SIMULATION

## Implemented

- policy evaluation after heartbeat
- registered-but-ineligible state
- thermal block
- low-battery block
- degraded/warm node as fallback candidate
- deterministic policy-aware route order
- unit tests

## Acceptance scenarios

### Scenario A — Hot primary

```text
Node-01: READY / 44°C
Node-02: READY / 36°C

Expected:
Node-01 remains visible in registry.
Node-01 is excluded from new LLM work.
Node-02 is selected.
```

### Scenario B — Low battery primary

```text
Node-01: READY / battery 15% / not charging
Node-02: READY / battery 70%

Expected:
Node-01 remains visible.
Node-01 excluded from new work.
Node-02 selected.
```

### Scenario C — Warm fallback

```text
Node-01: READY / 35°C
Node-02: READY / 41°C

Expected order:
Node-01 -> Node-02
```

### Scenario D — All blocked

```text
Node-01: 49°C
Node-02: 8% battery

Expected:
NO ROUTE
```

## Hardware validation still required

These acceptance scenarios must later be repeated using real Android telemetry from Node-01 and subsequent nodes.
