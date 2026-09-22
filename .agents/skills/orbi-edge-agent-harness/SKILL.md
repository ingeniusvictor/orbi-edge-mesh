---
name: orbi-edge-agent-harness
description: Design or review bounded ORBI Edge Mesh agent/tool workflows, structured observations, recovery and stop conditions while preserving physical-device, pairing, LAN, routing, model and distributed-compute authority boundaries.
version: "0.1.0"
license: MIT
metadata:
  origin: ORBI
  authoritative: false
  runtime_dependency: false
---

# ORBI Edge Agent Harness

Use when creating or changing an agent-like workflow, structured handoff, tool contract, recovery path or evidence report around ORBI Edge Mesh.

Repository code, governed runbooks, exact Git state and physical validation evidence remain authoritative.

## Action-space tiers

### Read-only

Preferred default:

- inspect branch/HEAD and CI evidence;
- inspect contracts, manifests and runtime-readiness reports;
- inspect physical validation records already supplied;
- compare advertised vs verified node/model capabilities;
- review pairing/replay/resource/routing evidence without mutating it.

### Reversible repository mutation

Allowed only inside the authorized development workflow:

- feature-branch code/docs/tests;
- synthetic fixtures;
- adapter/profile updates;
- validator/schema changes.

Require deterministic verification, final diff review and rollback.

### Physical/security/network/runtime authority

This harness does not grant authority to:

- promote a physical N-stage;
- generate, rotate, revoke or disclose pairing secrets;
- widen LAN exposure;
- bypass ALLOW / DEGRADE / BLOCK resource policy;
- admit nodes or mutate real routing state;
- transfer or delete model files;
- claim or enable unified RAM, tensor/expert/KV sharding or distributed single-model execution.

## Structured observation

Schema:

`.orbi/orbi-edge-agent-observation-v1.schema.json`

Validator:

```bash
python scripts/validate_orbi_edge_agent_observation.py <observation.json>
```

Every observation reports explicit boolean impact on:

- physical stage status;
- pairing-secret lifecycle;
- LAN exposure;
- resource-policy bypass;
- node admission or routing;
- model transfer or deletion;
- distributed-execution claims.

Omission is not interpreted as false.

## Evidence discipline

Keep software/CI evidence separate from physical/local evidence.

```text
CI GREEN != PHYSICAL NODE CERTIFIED
APK BUILDS != APK RUNS CORRECTLY ON DEVICE
MODEL HASH MATCH != MODEL LOAD SUCCESS
MODEL LOAD SUCCESS != INFERENCE SUCCESS
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
NODE DISCOVERED != NODE ADMITTED
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
WHOLE-WORKLOAD ROUTING != DISTRIBUTED MODEL EXECUTION
```

A valid observation records evidence shape; it does not make the underlying evidence true.

## Recovery

Error observations require:

- root-cause hint;
- safe retry;
- stop condition.

A retry must change evidence, hypothesis, input, scope or implementation.

Stop when:

- required physical evidence is absent;
- node identity/trust evidence conflicts;
- pairing/replay evidence is incomplete for the requested claim;
- the same failure repeats without new evidence;
- resource policy blocks the action;
- the next step would change secrets, LAN exposure, admission/routing, model placement or physical-stage status without explicit authority;
- a distributed-compute claim exceeds the evidence.

## Skill routing

Use:

- `orbi-edge-physical-evidence-review` for physical N-stage/device/model/headless/resource evidence;
- `orbi-edge-node-trust-review` for identity, pairing, capability and routing-eligibility evidence.

## Non-authority

A valid structured observation does not:

- certify a physical Android stage;
- prove model load/inference;
- prove trusted transport;
- admit a node;
- change routing;
- authorize secrets;
- move/delete models;
- prove distributed model execution.

## Rollback

Remove the harness skill/schema/validator/test and profile/adapter routing entries.

No Android/Kotlin/C++/Python product runtime may depend on this harness.
