# ORBI Edge Mesh — Thermal & Power Policy v0.1

Status: **EXPERIMENTAL / NOT YET HARDWARE-CALIBRATED**

## Purpose

Prevent the scheduler from treating phones as disposable compute.

ORBI Edge Mesh must consider device preservation part of scheduling.

## Thermal bands

Initial Phase 0 bands:

| Temperature | State | Scheduler action |
|---|---|---|
| < 40 °C | normal | normal |
| 40–<43 °C | warm | degrade |
| 43–<46 °C | hot | avoid new work |
| 46–<48 °C | very hot | avoid / prepare migration |
| >=48 °C | critical | pause |

These are **experimental ORBI policy bands**, not official Xiaomi/MediaTek/Qualcomm safety limits.

They must be calibrated with actual Node-01 measurements.

## Thread scaling concept

The policy returns a conceptual thread scale:

- normal: 1.00
- warm: 0.75
- hot: 0.50
- very hot: 0.25
- critical: 0.00

Phase 0 does not yet automatically reconfigure llama.cpp thread counts at runtime. This value is a scheduler/control-plane signal for later integration.

## Battery policy

Initial conservative rules:

- <=10%: pause
- <=20% and not charging: avoid new work
- <=30% and not charging: degraded/reserve mode
- otherwise: normal

Charging at low battery permits work in this first policy, but **does not override thermal protection**.

## Combined decision

A node is eligible for new work only when both:

```text
thermal.allow_new_work
AND
power.allow_new_work
```

Examples:

```text
Battery 90%, Temp 49°C
→ PAUSE

Battery 15%, Temp 34°C, not charging
→ AVOID

Battery 70%, Temp 41°C
→ DEGRADED but usable
```

## Future inputs

Later policy versions may include:
- battery health
- charging wattage
- USB power mode
- charge-cycle strategy
- recent thermal slope
- SoC throttling state
- fan presence
- ambient temperature
- sustained tokens/s degradation

## Design rule

No scheduler optimization may bypass a critical thermal or battery block.
