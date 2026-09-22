# Node-02 / Node-03 Native Bring-Up Plan

Status: **ACTIVE — NODE-01 N0–N9 CERTIFIED; NODE-02 BASELINE OBSERVED; NODE-03 PENDING**

## Certified reference

Node-01 has completed cumulative physical certification through N0–N9.

That certification does not automatically transfer to another phone. Every additional node must establish its own identity, resource, model, API and trust evidence before N10 admission.

## Known permanent Android inventory

### Node-01 — certified reference

- POCO X7 Pro 5G
- Android 16 / arm64-v8a in certified evidence
- ~11.05 GiB Android-reported RAM
- 512 GB storage class
- Qwen3 1.7B Q4_K_M native path physically certified through N0–N9
- role: primary reference CHAT node

### Node-02 — baseline observed

- Xiaomi 11T Pro
- Android 14 / arm64-v8a
- ORBI Edge Node 0.10.3-native-alpha-pairingux observed running
- RAM total: 7.05 GiB
- RAM available at capture: 2.52 GiB
- storage total: 224.19 GiB
- storage available at capture: 111.12 GiB
- Wi-Fi IPv4 observed: 192.168.1.12
- Android thermal: NONE / raw 0
- resource policy: ALLOW
- low-memory flag: NO

Battery caveat: the physical battery is heavily degraded and reported percentage can collapse rapidly. Treat Node-02 as a stationary / externally-powered validation node. Stop testing if power instability or abnormal heat appears.

**Node-02 is not yet N10-admitted.** The observed baseline proves the app/telemetry surface, not model load, pairing, signed inference or routing eligibility.

### Node-03 — planned

- Xiaomi Mi 10T Lite 5G (M2007J17G)
- 6 GB RAM / 256 GB storage class
- Snapdragon 750G / Adreno 619
- Wi-Fi is the required ORBI path; cellular service is irrelevant

All Node-03 capabilities remain hypotheses until physically observed.

## Rule

Node-02 and Node-03 must each pass the same minimum native health/trust foundation before participating in routing.

No device is admitted merely because it is on the same Wi-Fi.

## Stage A — install and identity

For each candidate node:

1. install the current governed ORBI Edge Node APK;
2. record app version, source commit and APK SHA-256;
3. verify manufacturer/model/device/API/ABI;
4. verify JNI bridge;
5. verify llama.cpp system info;
6. compare battery/RAM/storage values with Android.

## Stage B — resource baseline

Record with the device cool and idle:

- battery percentage and charge state;
- Android thermal category;
- total/available memory;
- total/available storage;
- Wi-Fi address;
- logical CPU count.

Memory Extension / swap must never be reported as physical RAM.

## Stage C — model admission

Do not assume a Node-01 model is automatically suitable.

For a CHAT candidate:

1. import an explicitly selected GGUF;
2. verify SHA-256;
3. load it under the native runtime;
4. verify `/v1/models` advertises a concrete model ID;
5. run one local inference;
6. record latency/resource observations.

The N10 manager consumes the advertised model identity; it must not invent a Node-01-specific ID for another node.

## Stage D — pairing

Each device generates its own:

- persistent Node ID;
- pairing token.

Store manager credentials only in process environment variables. Never commit tokens or place them in public evidence.

## Stage E — incremental mesh rehearsal

Before all three phones are ready, a **two-node rehearsal** with Node-01 + Node-02 may validate:

- both identities observed by `--status-only`;
- both nodes reachable;
- both independently paired;
- both advertise loaded models;
- one workload routes to an eligible node;
- taking the selected node unavailable causes whole-request fallback when the other node remains eligible.

This is useful progress evidence, but it is not N10 final certification.

## Stage F — final three-node registration

N10 final PASS requires the manager to observe all three independent nodes and their actual:

- identity;
- model advertisement/residency;
- battery;
- thermal/resource policy;
- trust state;
- LAN reachability.

Then demonstrate whole-request routing and fallback without cloud inference.

Distributed RAM/storage must not be presented as unified.

## Initial role hypotheses

These are hypotheses only until physically validated:

- Node-01: primary CHAT / reference node;
- Node-02: secondary CHAT / fallback candidate;
- Node-03: lightweight fallback or future specialized-service candidate.

ASR, TTS and other specialized roles remain future validation targets.

## N10 admission gate

A node is eligible only when:

- native app is stable;
- resource policy is ALLOW or DEGRADE, never BLOCK;
- pairing succeeds;
- required model is actually loaded and advertised;
- trusted-LAN API is reachable;
- reported Node ID matches manager configuration.

## Failure isolation

Failure of one phone must not require rebooting or reconfiguring the other phones.

The first mesh routes complete workloads between independent nodes. Tensor/expert/KV sharding remains later research.
