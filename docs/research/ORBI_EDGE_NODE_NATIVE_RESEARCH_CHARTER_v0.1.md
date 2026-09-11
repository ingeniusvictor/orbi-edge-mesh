# ORBI Edge Node Native — Research Charter v0.1

Status: ACTIVE RESEARCH
Branch: `feature/native-edge-node-research`

## Intent

ORBI Edge Mesh is being developed first as a research and engineering challenge, not as a commercial product.

The objective is to push toward a capability that is unusual and technically difficult:

> turn ordinary/reused Android phones into autonomous, private, local AI infrastructure that can operate headless, coordinate with peers, host local models, protect itself thermally and electrically, and progressively behave as a distributed AI fabric without depending on cloud inference.

We do not need to claim that nobody in the world has attempted any individual component. The research value is in proving the complete system on real consumer Android hardware and documenting what is and is not technically achievable.

## North Star

A user should eventually be able to install one APK on multiple Android devices and obtain:

- local AI inference;
- no cloud requirement for normal operation;
- screen-off/headless operation;
- model lifecycle management;
- battery and thermal protection;
- local API exposure;
- explicit secure pairing;
- node discovery;
- workload routing between phones;
- automatic recovery;
- role specialization by device;
- optional future distributed model execution research.

## Termux role

Termux is frozen as the Phase 0 reference laboratory.

It is useful for:
- proving feasibility;
- benchmarking;
- low-level diagnostics;
- reproducing failures;
- validating behavior before native implementation.

It is NOT the intended runtime dependency of the final research system.

## Research constraints

For the native path:

1. No root requirement.
2. No mandatory cloud inference.
3. No mandatory proprietary API.
4. Android arm64 is the first platform.
5. POCO X7 Pro / Node-01 is the first hardware target.
6. Qwen3 1.7B Q4_K_M is the first parity model.
7. The native app must eventually reproduce the proven Phase 0 gates:
   - local inference;
   - offline inference;
   - LAN serving;
   - screen-off operation;
   - supervised 30-minute headless stability.
8. Resource protection has priority over availability.
9. Commercial polish is explicitly out of scope for the research phase.

## Native architecture target

```text
Android
  |
  +-- ORBI Edge Node APK
       |
       +-- Device Profiler
       +-- Native Runtime
       |    +-- llama.cpp
       |    +-- JNI bridge
       |
       +-- Model Manager
       +-- Inference Manager
       +-- Local API
       +-- Headless Service
       +-- Thermal/Power Guard
       +-- Node Supervisor
       +-- Pairing/Trust
       +-- Mesh Agent
```

## Stage plan

### N0 — Android foundation
Build/install/open a minimal arm64 APK on Node-01.

### N1 — Native hardware profiler
Read device, RAM, storage, battery, network and available thermal state through Android APIs.

### N2 — llama.cpp native integration
Build and load llama.cpp through Android NDK/JNI.

### N3 — Local model loading
Select and validate the existing Qwen3 1.7B Q4_K_M GGUF.

### N4 — First native inference
Generate a local completion entirely inside the APK.

### N5 — Local API
Expose health, models and OpenAI-compatible chat-completion endpoints over the trusted LAN.

### N6 — Native headless parity
Repeat the Phase 0 30-minute screen-off test without Termux.

### N7 — Native watchdog and recovery
Detect inference/runtime failure and recover only when resource policy allows it.

### N8 — Native thermal/power management
Protect the device using Android-observable signals and calibrated ORBI policies.

### N9 — Secure pairing and node identity
Require explicit local trust before privileged mesh actions.

### N10 — Multi-node mesh
Bring Node-02 and Node-03 into coordinated local operation.

## Explicit non-goals for now

- Play Store release;
- monetization;
- marketing UI;
- account system;
- cloud backend;
- subscriptions;
- public Internet exposure;
- distributed tensor sharding;
- distributed KV cache;
- cross-device expert sharding.

Those last distributed-inference ideas remain future research tracks only after autonomous native nodes are proven.

## Research success criterion

The first major success is NOT a polished app.

It is:

> Node-01 runs Qwen locally from the ORBI APK, serves it over LAN, remains operational with the screen off, and requires no Termux process to provide the AI runtime.
