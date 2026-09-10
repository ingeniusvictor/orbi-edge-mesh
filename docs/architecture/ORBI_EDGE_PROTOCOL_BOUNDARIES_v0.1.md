# ORBI Edge Protocol Boundaries v0.1

## Principle

ORBI Edge Mesh coordinates heterogeneous AI runtimes. It should not assume every future node runs llama.cpp.

## Interfaces

### 1. Inference Adapter

Normalizes runtime-specific calls into ORBI capabilities.

Initial adapter:
- llama.cpp chat completions

Future candidates:
- embeddings
- Whisper-compatible STT
- local TTS
- MLC runtime
- other local inference engines

### 2. Node Capability Document

Describes:
- identity
- hardware
- runtime
- physical resources
- current health
- service inventory

Versioned JSON schema:
`contracts/node-capability.schema.json`

### 3. Manager Registry

Future manager stores the most recent capability document from every discovered node.

No implementation in Phase 0.

### 4. Scheduler Contract

Future scheduler consumes normalized capability state instead of directly reading vendor-specific Android telemetry.

This is important because:
- MediaTek and Snapdragon expose different hardware details;
- thermal visibility may differ by Android build;
- future nodes may not even be phones.

## Failure philosophy

Missing telemetry is represented as unknown/null where allowed.

ORBI must not fabricate:
- temperature;
- RAM;
- battery state;
- accelerator availability;
- benchmark values.

A node with incomplete telemetry can still provide inference if its health and runtime are otherwise known.
