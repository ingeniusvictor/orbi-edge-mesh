# AGENTS.md — ORBI Edge Mesh

Scope: this entire repository.

## Source of truth

- Follow the user's current task first, then current repository code/tests/governed docs, then these instructions.
- Git, deterministic tests, physical validation records and exact branch/HEAD evidence are canonical.
- Agent memory, generated summaries, assumptions about a phone, and CI output are non-authoritative beyond what they actually prove.
- The active Native Alpha line for this pilot is `feature/native-alpha-pairing-ux`.
- EDGE-ECC-P1 baseline: `22f857c556ef572a8b53f723f678b69ce2959fa9`.
- `main` is not the current Native Alpha implementation baseline.
- Inspect current branch/HEAD and open Native Alpha/N10 research PRs before editing.
- Keep agent-engineering changes separate from native-runtime/product changes.

## Product identity

ORBI Edge Mesh is local-first AI infrastructure built from reused Android devices.

Current active surfaces include:

- Android/Kotlin/Compose node application;
- C++17 JNI/native llama.cpp runtime;
- model import/hash verification;
- local inference;
- trusted-LAN API;
- foreground/headless service;
- thermal/power resource guard;
- local pairing/HMAC request authentication;
- replay protection;
- node identity/capability reporting;
- manager-side whole-workload routing;
- model placement research;
- PC-side validation probes.

## Current baseline

Active Android identity on the pilot base:

`0.10.3-native-alpha-pairingux`

Target Android stack:

- compileSdk 35;
- minSdk 26;
- targetSdk 35;
- JDK 17;
- Kotlin 2.0.21;
- Android Gradle Plugin 8.7.3;
- NDK 27.0.12077973;
- CMake 3.22.1;
- arm64-v8a;
- C++17.

## Core evidence boundaries

Preserve these distinctions:

```text
CI GREEN != PHYSICAL NODE CERTIFIED
APK BUILDS != APK RUNS CORRECTLY ON DEVICE
MODEL HASH MATCH != MODEL LOAD SUCCESS
MODEL LOAD SUCCESS != INFERENCE SUCCESS
INFERENCE SUCCESS != HEADLESS PARITY
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
PAIRING TOKEN EXISTS != PAIRING IS PHYSICALLY VERIFIED
LAN API READY != SAFE FOR PUBLIC INTERNET EXPOSURE
NODE DISCOVERED != NODE TRUSTED / ELIGIBLE
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
PLACEMENT PLAN != MODEL TRANSFER
WHOLE-WORKLOAD ROUTING != UNIFIED RAM / DISTRIBUTED MODEL EXECUTION
BENCHMARK RESULT != DISTRIBUTED SHARDING FEASIBILITY
```

## Work method

1. Identify exact branch/HEAD and whether the task is software-prep, physical validation, or both.
2. Preserve existing physical gate semantics: compile/build PASS is software preparation only.
3. Make the smallest isolated change.
4. Run focused Python/Kotlin/native tests first.
5. Run the exact integrated CI-compatible gate.
6. Record local/physical evidence separately.
7. Never upgrade a physical N-stage to PASS from CI-only evidence.
8. Review final diff for secret exposure, LAN/public exposure, capability inflation, or false distributed-compute claims.

## CI-compatible verification baseline

For the active Native Alpha line:

```bash
python -m unittest discover -s tests -v

cd android/edge-node-native
gradle :app:testDebugUnitTest --stacktrace
gradle :app:assembleRelease --stacktrace --info
```

The integrated EDGE ECC gate additionally verifies that the release APK exists and contains:

`lib/arm64-v8a/liborbi_native.so`

## Physical evidence is separate

GitHub CI cannot prove:

- actual APK installation on POCO/Xiaomi hardware;
- model import SHA-256 on the device;
- model load;
- real native generation latency/quality;
- no ANR under real inference;
- pairing-token copy/rotation/revocation behavior;
- signed LAN request from another device;
- replay rejection over the real LAN;
- headless/screen-off survival;
- real battery/thermal behavior;
- Android NSD/mDNS visibility;
- multi-node discovery/routing;
- real per-node resource/capability values.

Use the existing physical runbooks/probes for those claims.

## Pairing and secret boundary

- Pairing tokens are secrets.
- Never commit tokens, pairing secrets, HMAC keys, signed request secrets or private node credentials.
- Do not place secrets in public screenshots, docs, CI output or evidence JSON.
- Copy-to-clipboard UX does not make the token non-secret.
- Pairing/HMAC authenticates requests; it is **not transport encryption**.
- Keep the research API on a trusted LAN. Do not add public exposure or port forwarding as an incidental change.

## Node identity and routing

- Node ID is identity metadata, not proof that capabilities are valid.
- Capability manifests must not claim services/models that have not been validated.
- Whole-request routing does not pool phone RAM.
- Storage across devices is not one filesystem.
- Model placement planning must not silently copy/download/delete models.
- Prefer fail-closed behavior for unknown/incompatible node capability.

## Resource safety

- Respect the N8 thermal/power policy and Android-native resource signals.
- Do not invent Celsius temperatures when only Android thermal categories are available.
- Do not bypass BLOCK/DEGRADE policy to make an inference test pass.
- Repeated recovery must remain bounded and observable.

## Agent Kit state

Source kit:

- `ingeniusvictor/orbi-agent-kit`
- v0.2 development through K2-05
- canonical commit: `52af5d401566720f7ba4a429d1612dcc640c7962`

Initial pilot constraints:

- no full ECC install;
- no hooks;
- no MCP;
- no continuous learning;
- no unified memory;
- no Agent Kit autonomous loops;
- no multi-agent runtime roles.

Product-owned Edge Mesh automation/recovery/routing is separate and remains governed by its existing contracts.

## Completion report

Record separately:

- software/CI evidence;
- physical/local evidence;
- node(s) tested;
- model/runtime identity;
- security/pairing impact;
- network exposure impact;
- resource-policy impact;
- remaining physical gate(s).
