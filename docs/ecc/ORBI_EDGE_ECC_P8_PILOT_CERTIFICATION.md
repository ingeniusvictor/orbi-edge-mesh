# EDGE-ECC-P8 — ORBI Edge Mesh Agent Kit Pilot Certification

Status: SELECTIVE ADOPTION READY  
Pilot repository: `ingeniusvictor/orbi-edge-mesh`  
Canonical Edge branch: `feature/native-alpha-pairing-ux`  
Certified baseline before P8: `6b26d81664c4d546e22383b40befeaa0a78992dd`

## Purpose

Close the fifth ORBI Agent Engineering Kit portability pilot with an evidence-backed Edge-specific certification and portable profile.

This certifies the **engineering/agent-governance layer around ORBI Edge Mesh**, not physical Android-node readiness, model runtime readiness, trusted transport, or distributed single-model execution.

## Source Kit

- repository: `ingeniusvictor/orbi-agent-kit`
- version: **v0.2.0**
- certified through: **K2-06**
- canonical Kit commit: `8ef98f7a5edd7c27bda011ba77ddd3e26c3ee31f`
- adapter schema: `orbi.repository.adapter.v1`

## Upstream references

- ECC 2.2.2 — `91ba9b4cf6c47c8130829004f8bb64762a76ccbb`
- AgentShield 1.6.0 — `b0891303bdcd6037376a94263d45cfd2ff3dfb98`

## Pilot history

| Phase | PR | Result |
|---|---:|---|
| P1 | #68 | repository adapter + governed instructions + Native Alpha PR gate |
| P2 | #69 | fresh Edge-specific AgentShield report-only baseline |
| P3 | #70 | evidence-backed DAILY/LIBRARY classification |
| P4 | #71 | `orbi-edge-physical-evidence-review` |
| P5 | #72 | `orbi-edge-node-trust-review` |
| P6 | #73 | structured Edge agent observation harness |
| P7 | #74 | context budget + protected selective loading |

## Materialized Edge engineering layer

### Root governance

`AGENTS.md` preserves the permanent evidence and authority invariants.

### Edge-owned skills

- `orbi-edge-physical-evidence-review`
- `orbi-edge-node-trust-review`
- `orbi-edge-agent-harness`
- `orbi-edge-context-budget`

All four remain conditional/discoverable and non-runtime.

### Structured harness

- `.orbi/orbi-edge-agent-observation-v1.schema.json`
- `scripts/validate_orbi_edge_agent_observation.py`
- deterministic contract tests

Authority-impact fields explicitly cover physical stage, pairing secrets, LAN exposure, resource bypass, admission/routing, model transfer/deletion and distributed-execution claims.

### Repository adapter

`.orbi/repository-adapter.json` declares exact software verification, local/physical evidence, authority domains, AgentShield scope and conditional skill routing.

## Final pre-certification evidence

P7 canonical merge:

`6b26d81664c4d546e22383b40befeaa0a78992dd`

P7 final HEAD:

`b3952e683925daa89d1cc310f7a32476ffdcd57b`

### Phase 0

Run: `35757257010`

PASS:

- Python syntax;
- Python unit tests;
- shell syntax;
- JSON parse.

### ORBI Edge ECC Pull Request Gate

Run: `35757257518`

PASS:

- Python tests: **90 / 90**;
- Android unit tests;
- optimized release APK build;
- release APK contains `lib/arm64-v8a/liborbi_native.so`.

Release APK SHA-256:

`b98be875bb54a05e75fd45f198d00882d54d969a46f361445696bb0e7194c154`

### AgentShield

Run: `35757257087`

- workflow: SUCCESS;
- score: **100 / 100**;
- grade: **A**;
- findings: **0**;
- unique finding classes: **0**;
- supply chain: **CLEAN**;
- evidence-pack verification: **PASSED**;
- evidence-pack digest: `sha256:f25b6e43451c7651500785b39f1a8e3dce6b3d5056c9aa3d1b0b3379106acde4`.

## Certified Edge evidence boundaries

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
```

Certification does not weaken any of these distinctions.

## Physical and security authority

The Agent Kit layer has no authority to:

- promote a physical N-stage;
- generate, rotate, revoke or disclose real pairing secrets;
- widen the trusted-LAN API to public exposure;
- bypass ALLOW / DEGRADE / BLOCK resource policy;
- admit or reroute real physical nodes without governed evidence;
- transfer or delete model binaries;
- claim unified RAM, tensor/expert/KV sharding or distributed single-model execution;
- treat CI as physical readiness.

## Physical evidence not proven by CI

CI does **not** prove:

- APK installation/running on POCO or Xiaomi hardware;
- device-side model SHA-256;
- native model load;
- real inference latency/quality/stability;
- pairing/replay behavior on the real LAN;
- screen-off/headless parity;
- real thermal/battery behavior;
- Android NSD/mDNS discovery;
- multi-node routing on physical nodes.

Those claims remain governed by the product's physical runbooks and evidence.

## Context-budget result

The Edge loading model is:

- `AGENTS.md` = persistent invariants;
- 4 Edge project skills = conditional/discoverable;
- profile/adapter/observation schema = on-demand config references.

P7 measured approximately:

- persistent: **1,459** estimate tokens;
- discoverable if all loaded: **4,800**;
- config if all loaded: **4,557**.

These estimates are deterministic revision signals, not exact tokenizer accounting.

## What is portable from Edge

### Portable with review

- repository adapter with explicit local/physical evidence;
- CI-vs-physical certification separation;
- node identity/trust/capability evidence separation;
- structured observations with target-owned authority fields;
- independent report-only security baseline;
- conditional domain-skill loading;
- protected context-budget invariants.

### Edge-specific and must not be copied blindly

- Android/Kotlin/JNI runtime details;
- physical N-stage semantics;
- pairing/HMAC/replay implementation;
- trusted-LAN assumptions;
- thermal/power thresholds and policy;
- model placement/runtime evidence;
- discovery/admission/routing semantics;
- distributed-compute research claims;
- exact build/test commands.

## Deliberately disabled

- full ECC install;
- Agent Kit hooks;
- MCP;
- continuous learning;
- unified memory;
- Agent Kit autonomous loops;
- multi-agent runtime roles;
- automatic physical-stage promotion;
- automatic node admission;
- automatic model transfer.

## Rollback

The Edge Agent Kit layer remains removable independently from product runtime:

- remove project skills;
- remove observation schema/validator/tests;
- remove context-budget auditor/tests;
- remove adapter/profile/docs/workflows;
- retain Android/Kotlin/C++ product runtime and physical runbooks unchanged.

## Certification conclusion

ORBI Edge Mesh validates the Agent Kit pattern on a fifth, materially different project with Android hardware, local inference, LAN trust, physical evidence, resource policy and multi-node routing boundaries.

Certified pattern:

`Kit adapter -> Edge evidence inventory -> fresh security baseline -> selective skills -> structured harness -> protected context budget -> certification`

EDGE-ECC-P8 certifies the current selective Edge engineering layer for continued use while physical-node readiness and runtime authority remain separately governed.
