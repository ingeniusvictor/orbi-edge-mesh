# N8 Android-Native Resource Guard

## Objective

Protect Node-01 before admitting inference work or automatic model recovery.

## Signals

N8 uses signals that Android exposes through supported APIs:

- battery percentage;
- charging state;
- Android thermal status category.

It does **not** invent a device temperature in Celsius when Android does not expose one.

The earlier ORBI Celsius bands remain a separate experimental calibration track and are not silently mapped onto Android thermal categories.

## Research policy

### BLOCK

- Android thermal status: SEVERE / CRITICAL / EMERGENCY / SHUTDOWN; or
- battery <= 10% while not confirmed charging; or
- both battery and thermal safety telemetry unavailable.

### DEGRADE

- Android thermal status MODERATE; or
- battery <= 20% while not confirmed charging.

### ALLOW

Observed signals are below the above protection conditions.

Partial telemetry may be allowed only when the remaining signal does not indicate danger.

## Enforcement

The decision is applied to:

- manual model loading;
- manual in-app inference;
- trusted-LAN chat completion requests;
- N7 automatic recovery.

A DEGRADE decision reduces the initial generation ceiling.

Automatic recovery requires ALLOW; DEGRADE is not sufficient because model reload is a relatively heavy operation.

## PASS

Physical N8 certification requires controlled observations on Node-01, not deliberate overheating.

Required evidence:

1. normal cool device -> ALLOW;
2. low-battery simulation/unit tests -> BLOCK/DEGRADE as designed;
3. thermal categorical tests -> BLOCK/DEGRADE as designed;
4. missing telemetry tests -> safe bounded behavior;
5. API reports the same resource decision visible in the app;
6. supervisor obeys a blocked recovery decision.

Do not intentionally heat the phone to dangerous temperatures merely to trigger a thermal state. Thermal blocking can be validated through unit/simulation tests plus natural observation.
