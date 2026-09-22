# EDGE-ECC-P1 — Agent Kit Adapter and Native Alpha PR Gate

Status: CONTROLLED / NO PRODUCT-RUNTIME CHANGE

Base branch: `feature/native-alpha-pairing-ux`  
Audited baseline: `22f857c556ef572a8b53f723f678b69ce2959fa9`

## Purpose

Start the fifth ORBI Agent Engineering Kit portability pilot on ORBI Edge Mesh without changing Android/native/runtime behavior.

P1 introduces:

- root `AGENTS.md`;
- `.orbi/repository-adapter.json`;
- `.orbi/ecc-profile.json`;
- dedicated SHA-pinned PR gate;
- this inventory/adoption record.

## Why this pilot is materially different

Edge Mesh adds trust/evidence surfaces not covered by the four previous pilots:

- real Android hardware;
- Kotlin/Compose + JNI + C++ native runtime;
- imported model binaries;
- trusted-LAN APIs;
- pairing/HMAC secrets;
- replay protection;
- foreground/headless services;
- thermal/power policy;
- multi-device discovery/routing;
- physical device validation;
- distributed-compute research.

## Active line selection

`main` is not the active Native Alpha implementation.

The selected pilot base is:

`feature/native-alpha-pairing-ux @ 22f857c556ef572a8b53f723f678b69ce2959fa9`

This line is 22 commits ahead of `feature/native-n10-mesh-prep` and includes the later ANR/performance/Native Alpha validation/pairing UX work.

## Current product identity

Android version:

`0.10.3-native-alpha-pairingux`

P1 does not merge or close any existing research/draft PR and does not change N-stage status.

## Core evidence separation

P1 formalizes:

```text
CI GREEN != PHYSICAL NODE CERTIFIED
APK BUILDS != APK RUNS CORRECTLY ON DEVICE
MODEL HASH MATCH != MODEL LOAD SUCCESS
MODEL LOAD SUCCESS != INFERENCE SUCCESS
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
NODE DISCOVERED != NODE TRUSTED / ELIGIBLE
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
PLACEMENT PLAN != MODEL TRANSFER
WHOLE-WORKLOAD ROUTING != UNIFIED RAM / DISTRIBUTED MODEL EXECUTION
```

## Integrated PR gate

The new gate targets PRs into `feature/native-alpha-pairing-ux`.

It uses immutable SHAs for:

- checkout;
- setup-python;
- setup-java;
- Gradle setup.

The gate intentionally uses the Android SDK already present on the GitHub-hosted Ubuntu runner and calls `sdkmanager` directly. The previous `android-actions/setup-android@v3` path is not used because its current setup path attempts to install the obsolete SDK package `tools` on the 2026 runner image.

It runs:

1. Python unit tests;
2. Android unit tests;
3. optimized release APK build;
4. APK existence/native-library verification;
5. APK SHA-256 generation.

## What the gate does not prove

It does not prove:

- real installation;
- model import/load/inference;
- no ANR on a phone;
- physical pairing;
- signed PC→phone request;
- replay rejection over actual LAN;
- 30-minute screen-off survival;
- battery/thermal behavior;
- mDNS visibility;
- multi-node routing.

## Security baseline

AgentShield is deliberately deferred to EDGE-ECC-P2.

P2 must create a **fresh Edge Mesh baseline**. No accepted finding from Creative Studio, PVMetrics, L.U.M.I.A. or News is inherited automatically.

## Non-goals

P1 does not:

- change product/runtime source;
- rotate/generate pairing tokens;
- modify LAN exposure;
- install a model;
- transfer a model;
- certify a physical N-stage;
- enable hooks/MCP/memory/continuous learning;
- enable Agent Kit autonomous loops;
- claim distributed inference.

## Next

After P1 is GREEN:

1. EDGE-ECC-P2 — fresh AgentShield baseline;
2. EDGE-ECC-P3 — DAILY/LIBRARY classification;
3. first Edge-specific skill should likely focus on **physical-vs-CI evidence and node trust/capability admission**.