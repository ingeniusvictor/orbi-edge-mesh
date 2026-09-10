# ORBI Edge Mesh — Policy-Aware Routing v0.1

## Goal

Connect heartbeat, node registry, thermal/power policy and fallback routing into one deterministic flow.

## Flow

```text
Node heartbeat
    ↓
Registry update
    ↓
Thermal/Power evaluation
    ↓
Eligibility gate
    ↓
Policy-aware routing
    ↓
Fallback order
```

## Eligibility gate

A node may be registered and healthy from a network perspective but still be ineligible for new work.

Examples:

```text
Node reachable + 49°C
→ registered
→ policy = PAUSE
→ excluded from new work

Node reachable + 15% battery + not charging
→ registered
→ policy = AVOID
→ excluded from new work

Node reachable + 41°C
→ registered
→ policy = DEGRADE
→ still eligible
→ lower routing preference
```

## Routing priority

Eligible nodes are ordered by:

1. service availability;
2. runtime health status;
3. ORBI policy action;
4. consecutive heartbeat failures;
5. temperature;
6. deterministic node_id tie-break.

## Important distinction

```text
NETWORK HEALTH != WORK ELIGIBILITY
```

A node can remain online for telemetry while being intentionally excluded from inference.

This distinction is required for:
- thermal cooldown;
- low-battery protection;
- maintenance;
- later operator-controlled pause states.

## Current limitation

Manager v0.3 computes route/fallback order only.

It does not yet:
- execute inference retries;
- migrate an in-flight request;
- change llama.cpp thread count dynamically;
- enforce OS-level process suspension.

Those belong to later adapters/execution layers.
