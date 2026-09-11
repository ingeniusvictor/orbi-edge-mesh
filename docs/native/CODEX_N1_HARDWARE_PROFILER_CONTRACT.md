# Codex Contract — N1 Native Hardware Profiler

Status: PREPARED — DO NOT IMPLEMENT UNTIL N0 PHYSICAL PASS

## Goal

Use Android APIs to produce a typed Node-01 hardware/health snapshot without shelling out to Termux.

## Required data

### Identity
- manufacturer
- model
- device/codename when available
- Android release
- API level
- supported ABIs

### Memory
- total memory
- available memory
- low-memory flag if exposed

### Storage
- total bytes
- available bytes
- source/path category

### Battery / power
- battery percentage
- charging state
- charge source where exposed

### Network
- connected/not connected
- transport type
- local IPv4/IPv6 addresses when Android grants them

### Thermal
- Android thermal status where supported
- do not convert thermal status to fake Celsius
- temperature in Celsius only if an actual supported sensor/API supplies it

## Data model requirement

Every field that may be unavailable must be nullable/unknown.

No sentinel guesses such as 0°C or 100% battery.

## Architecture

`DeviceProfiler` gathers static identity.

Separate providers gather:
- MemorySnapshot
- StorageSnapshot
- BatterySnapshot
- NetworkSnapshot
- ThermalSnapshot

A composed `NodeHealthSnapshot` is exposed to UI.

## Acceptance

- physical values visible on POCO;
- no shell command execution;
- no Termux dependency;
- no root;
- airplane/offline mode does not crash;
- missing permissions/signals degrade cleanly.
