# Node-01 Experiment — POCO X7 Pro

## Device role

Principal experimental node.

Known baseline:
- 12 GB physical RAM
- 512 GB storage
- no root required
- daily-use device

All Phase 0 changes must be reversible.

## Experiment 001 — Local inference smoke test

Status: NOT STARTED

### Goal

Run a small quantized model locally with network access disabled during inference.

### Planned sequence

1. capture Android/device baseline;
2. install terminal/runtime environment;
3. build or install inference runtime;
4. place model in an appropriate local filesystem location;
5. run a local CLI prompt;
6. repeat with Wi-Fi/internet unavailable if practical;
7. record results.

## Experiment 002 — LAN API

Status: BLOCKED BY EXPERIMENT 001

Goal:
- expose local inference endpoint;
- call it from a PC on the same LAN;
- verify no cloud call is required.

## Experiment 003 — Thermal stability

Status: BLOCKED BY EXPERIMENT 002

Goal:
- sustained 15–30 minute inference workload;
- observe temperature, throttling and stability.

## Safety / preservation rules

- no bootloader unlock in Phase 0
- no root in Phase 0
- no destructive repartitioning
- no permanent background service until thermal behavior is understood
- avoid simultaneous fast charging and maximum inference load during initial tests
