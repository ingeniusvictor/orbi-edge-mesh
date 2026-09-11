# ORBI Edge Mesh — Watchdog Policy Gate v0.1

## Goal

Prevent automatic AI-service recovery when the phone is thermally or energetically unsafe.

## Flow

```text
service failure
     ↓
watchdog detects fault
     ↓
read local telemetry
     ↓
ORBI thermal/power policy
     ↓
ALLOW?
  ┌──┴──┐
 yes    no
  ↓      ↓
restart  hold/quarantine
```

## Local telemetry

The Phase 0 bridge attempts to read:

- Android thermal zones from `/sys/class/thermal/thermal_zone*`
- battery capacity from `/sys/class/power_supply/*/capacity`
- charging state from `/sys/class/power_supply/*/status`

Telemetry availability varies by Android/HyperOS device and permissions.

Unknown telemetry must be treated explicitly and never fabricated.

## Conservative temperature selection

Android exposes multiple thermal zones and their meaning varies by device.

Phase 0 uses the highest plausible readable temperature as a conservative input.

This is only a bootstrap strategy.

Real Node-01 certification must identify which thermal sensors best represent sustained SoC/battery risk.

## Recovery rule

A restart is allowed only if:

```text
thermal.allow_new_work
AND
power.allow_new_work
```

Hard policy blocks therefore override watchdog recovery.

## Limitation

The current thermal thresholds remain experimental ORBI policy bands.

They are not manufacturer-certified limits and must be calibrated on real hardware.
