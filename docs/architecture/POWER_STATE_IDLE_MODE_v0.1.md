# ORBI Edge Mesh — Power-State / Idle Mode v0.1

## Goal

Keep a phone available as local infrastructure without forcing the AI model to remain hot when nobody is using it.

## States

```text
ACTIVE
→ request in progress
→ API alive
→ model loaded

IDLE_WARM
→ no active request
→ recent activity
→ API alive
→ model remains loaded

IDLE_COLD
→ long idle period
→ API/control plane alive
→ model may unload

PROTECTED_PAUSE
→ thermal/power block
→ API/control plane may remain alive
→ model unloaded
→ no wake allowed
```

## Key principle

```text
node available != model permanently loaded
```

A phone can remain discoverable and manageable while the heavy inference runtime is asleep.

## Initial idle timeout

Phase 0 default hypothesis:

```text
300 seconds / 5 minutes
```

This is not final.

The real value must balance:
- cold-start latency
- battery consumption
- RAM retention
- model load cost
- flash reads
- thermal behavior

## Wake policy

A cold model may be woken only when:
- thermal/power policy allows work;
- the model is locally available;
- the scheduler decides the cold-start cost is acceptable.

For high-latency-sensitivity work, warm candidates should be preferred over cold candidates where possible.

## Screen-off behavior

The display remains off throughout.

The desired idle architecture is:

```text
screen OFF
control API alive
heartbeat alive
watchdog alive
heavy model optionally unloaded
```

## Future implementation

Later versions may use:
- runtime process suspend/resume
- explicit model unload/reload APIs
- per-model idle timers
- predictive keep-warm windows
- charging-aware warm policy
- wake-on-LAN-like local triggers where Android allows
