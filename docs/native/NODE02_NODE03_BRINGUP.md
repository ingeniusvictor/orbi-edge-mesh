# Node-02 / Node-03 Native Bring-Up Plan

Status: PREPARED — DO NOT START UNTIL NODE-01 N0–N9 PHYSICAL CERTIFICATION

## Known permanent Android inventory

### Node-01 — primary reference

- POCO X7 Pro 5G
- 12 GB marketed physical RAM class / 512 GB storage
- Dimensity 8400-Ultra
- current native reference target

### Node-02

- Xiaomi 11T Pro
- 8 GB RAM / likely 256 GB storage
- Snapdragon 888 / Adreno 660
- currently unused

### Node-03

- Xiaomi Mi 10T Lite 5G (M2007J17G)
- 6 GB RAM / 256 GB storage
- Snapdragon 750G / Adreno 619
- cellular service is irrelevant to ORBI Edge Mesh; Wi-Fi is the required path

## Rule

Node-02 and Node-03 must each pass the same minimum native health/trust foundation before participating in routing.

No device is admitted merely because it is on the same Wi-Fi.

## Stage A — install and identity

For each device:

1. install the same cumulative ORBI Edge Node APK candidate;
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

## Stage C — model experiment

Do not assume the Node-01 model is automatically optimal for Node-02 or Node-03.

Start with the smallest model needed to prove the runtime, then test the reference Qwen3 1.7B only if resource policy remains healthy.

Record load time, generation latency, wall-clock tokens/s, battery delta and thermal observation.

## Stage D — pairing

Each device generates its own:

- persistent Node ID;
- pairing token.

Store the three manager credentials separately in process environment variables. Never commit them to the repository.

## Stage E — first three-node registration

The manager should observe all three independent nodes and their actual:

- identity;
- service capability;
- model residency;
- battery;
- thermal/resource policy;
- storage;
- trust state.

Distributed RAM/storage must not be presented as unified.

## Initial role hypotheses

These are hypotheses only and must not be advertised as capabilities until physically validated:

- Node-01: primary CHAT / reference node;
- Node-02: secondary CHAT / fallback candidate;
- Node-03: lightweight fallback or future specialized service candidate.

ASR, TTS and other specialized roles are future validation targets, not current capabilities.

## N10 admission gate

A node is eligible for the first mesh only when:

- native app is stable;
- resource policy is not BLOCK;
- pairing succeeds;
- advertised service is physically validated;
- required model is actually present/loaded;
- trusted-LAN API is reachable;
- its Node ID matches the manager configuration.

## Failure isolation

Failure of one phone must not require rebooting or reconfiguring the other phones.

The first mesh architecture routes complete workloads between independent nodes. Tensor/expert sharding remains a later research topic.
