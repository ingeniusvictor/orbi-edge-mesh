---
name: orbi-edge-physical-evidence-review
description: Review ORBI Edge Mesh software, local-device and physical N-stage evidence without promoting physical readiness from CI. Use for APK/device validation, model import/load/inference, pairing, signed/replay probes, headless parity, thermal/power observations, node discovery or any physical-stage claim.
version: "0.1.0"
license: MIT
metadata:
  origin: ORBI
  authoritative: false
  runtime_dependency: false
---

# ORBI Edge Physical Evidence Review

Use this skill whenever a change, issue, report or PR could change what ORBI claims about a real Android node.

Repository code, governed runbooks, physical observations, Git history and current `AGENTS.md` remain authoritative.

## Core rule

```text
CI GREEN != PHYSICAL NODE CERTIFIED
APK BUILDS != APK RUNS CORRECTLY ON DEVICE
MODEL HASH MATCH != MODEL LOAD SUCCESS
MODEL LOAD SUCCESS != INFERENCE SUCCESS
INFERENCE SUCCESS != HEADLESS PARITY
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
PAIRING TOKEN EXISTS != PAIRING IS PHYSICALLY VERIFIED
NODE DISCOVERED != NODE TRUSTED / ELIGIBLE
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
PLACEMENT PLAN != MODEL TRANSFER
WHOLE-WORKLOAD ROUTING != UNIFIED RAM / DISTRIBUTED MODEL EXECUTION
```

A tool, agent, CI workflow or model response may summarize evidence. It cannot promote an N-stage by itself.

## 1. Identify the evidence lane

Classify every claim as one or more of:

### Software-preparation evidence

Examples:

- source compiles;
- Python tests pass;
- Android unit tests pass;
- release APK exists;
- arm64 native library is packaged;
- contract/schema tests pass.

This can come from CI.

### Local-device evidence

Examples:

- APK installed on the named phone;
- exact app/build version observed;
- device/ABI identity observed;
- model file hash measured on-device;
- JNI/runtime state observed;
- local model load/inference result;
- Android thermal/power state.

This requires local/physical evidence.

### Cross-device / LAN evidence

Examples:

- PC can reach actual phone IPv4;
- signed request accepted;
- unsigned request rejected;
- replay rejected;
- discovery/mDNS observed;
- manager sees the correct Node ID/capabilities.

This requires real network/device evidence.

### Sustained physical evidence

Examples:

- 30-minute screen-off/headless parity;
- post-20-minute real inference;
- foreground service survival;
- bounded recovery after injected failure;
- thermal/power behavior under real workload.

CI cannot substitute for this.

## 2. Read the current runbook before judging PASS

For Native Alpha physical validation, inspect current repository versions of:

- `docs/native/NATIVE_ALPHA_VALIDATION_RUNBOOK.md`;
- the relevant N-stage contract/runbook;
- `docs/hardware/DEVICE_MATRIX.md`;
- `docs/policy/THERMAL_POWER_POLICY_v0.1.md`;
- relevant PC probe scripts and tests.

Do not use this skill as a stale replacement for those documents.

## 3. Build identity

For physical evidence record:

- node ID / device name without leaking secrets;
- APK/app version;
- source commit or artifact identity;
- APK SHA-256 when available;
- model identity and model SHA-256 when applicable;
- runtime identity;
- test date/context.

A screenshot alone is not enough if it does not identify the build under test.

## 4. Model evidence ladder

Treat these as separate gates:

1. expected model identified;
2. on-device file imported;
3. SHA-256 measured;
4. hash matches expected;
5. model loads in native runtime;
6. inference completes;
7. output is coherent enough for the stated smoke test;
8. stability/latency/resource observations recorded.

Do not collapse the ladder into `model_ready=true`.

For the current Native Alpha runbook, the expected Qwen model and hash come from the runbook; always re-read the current file instead of hardcoding them here.

## 5. Pairing and signed-control evidence

Pairing tokens are secrets.

Never put the token/HMAC secret in:

- Git;
- public screenshots;
- evidence JSON;
- logs;
- issue/PR comments;
- agent memory.

For physical signed-request validation, evidence should show outcomes without disclosing the secret.

Current runbook expects behavior such as:

- unsigned request rejected;
- signed request accepted;
- exact replay rejected.

These outcomes prove request authentication/replay behavior. They do **not** prove transport encryption.

## 6. Headless parity

A quick screen-off check is not the same as the governed headless protocol.

Use the current runbook. The current Native Alpha protocol includes sustained reachability and a real inference after an extended screen-off interval.

Record:

- start/end battery;
- Android thermal state;
- warnings;
- foreground notification/service survival;
- inference result;
- duration/timestamps.

Do not promote N6/headless parity from CI or a short local smoke test.

## 7. Resource-policy evidence

Respect the current resource policy.

Never:

- bypass BLOCK/DEGRADE to obtain a test result;
- invent battery temperature or Celsius values when unavailable;
- present experimental policy bands as OEM safety limits;
- deliberately overheat a phone just to trigger a transition.

Natural observations and deterministic policy tests can complement each other but are not interchangeable.

## 8. Multi-node evidence

For discovery/routing/capability work:

- record each physical node separately;
- preserve actual resource values per node;
- distinguish discovery from admission;
- distinguish advertised capability from verified capability;
- distinguish advisory placement from model transfer;
- distinguish whole-request routing from distributed model execution.

Never sum device RAM/storage and present it as one unified machine.

## 9. Physical-stage result vocabulary

Use:

### SOFTWARE READY

Required software/CI preparation for the stage is complete, but physical evidence is pending.

### PHYSICAL PASS

Use only when the current runbook/contract's required real-device evidence has been collected for the exact build/node.

### PHYSICAL FAIL

A required real-device criterion failed.

### PARTIALLY VERIFIED

Some physical evidence exists but required criteria remain unobserved.

Do not invent a stronger status.

## 10. Review report

Return:

```text
ORBI EDGE PHYSICAL EVIDENCE REVIEW

Scope:
- stage:
- node(s):
- branch/HEAD:
- app/APK identity:
- model/runtime identity:

Software evidence:
- Python tests:
- Android tests:
- APK build:
- native library packaging:

Physical evidence:
- install/launch:
- model hash:
- model load:
- inference:
- pairing:
- signed/replay:
- headless:
- thermal/power:
- discovery/routing:

Secret exposure:
- none / issue

Authority impact:
- physical stage changed: YES/NO
- LAN exposure changed: YES/NO
- pairing-secret lifecycle changed: YES/NO
- model transfer/deletion introduced: YES/NO
- distributed-execution claim changed: YES/NO

Result:
- SOFTWARE READY / PHYSICAL PASS / PHYSICAL FAIL / PARTIALLY VERIFIED

Missing evidence:
- ...
```

## Rollback

This skill is instruction-only.

Remove `.agents/skills/orbi-edge-physical-evidence-review/` and its manifest/adapter routing entry. Edge Mesh product runtime must not depend on this file.
