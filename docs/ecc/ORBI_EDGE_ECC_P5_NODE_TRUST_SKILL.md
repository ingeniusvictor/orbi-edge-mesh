# EDGE-ECC-P5 — Node Trust and Capability Admission Review Skill

Status: CONTROLLED / INSTRUCTION-ONLY

## Purpose

Materialize the second ORBI Edge Mesh project-specific Agent Kit skill:

`orbi-edge-node-trust-review`

The skill reviews evidence for node identity, trust, capability verification and routing eligibility.

It does **not** admit nodes or mutate product state.

## Grounding

Current repository surfaces reviewed for P5 include:

- `security/pairing.py`;
- `security/signing.py`;
- `security/replay.py`;
- `security/trust_store.py`;
- `contracts/node-capability.schema.json`;
- `manager/native_mesh_manager.py`;
- physical validation runbooks and current `AGENTS.md`.

## Preserved boundaries

```text
NODE IDENTITY != NODE TRUST
NODE DISCOVERED != NODE ADMITTED
PAIRING TOKEN EXISTS != PAIRING VERIFIED
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
MODEL LISTED != MODEL LOADED
ROUTING ELIGIBLE != PHYSICAL CERTIFICATION FOR EVERY CLAIM
PLACEMENT PLAN != MODEL TRANSFER
WHOLE-WORKLOAD ROUTING != DISTRIBUTED MODEL EXECUTION
```

## Current product behavior relevant to the skill

The current Python Native Mesh Manager already fails closed on several conditions before a node is considered eligible:

- node must be reachable;
- reported Node ID must not contradict configured Node ID;
- model must be listed and reported loaded;
- node must report paired;
- resource action must be ALLOW or DEGRADE.

P5 does not modify that logic.

Instead it prevents the Agent Kit layer from overstating what those software checks prove physically.

## Status vocabulary

The skill may report:

- `EVIDENCE_SUFFICIENT_FOR_REVIEW`;
- `EVIDENCE_INCOMPLETE`;
- `IDENTITY_MISMATCH`;
- `SECURITY_EVIDENCE_MISSING`;
- `CAPABILITY_NOT_VERIFIED`;
- `RESOURCE_POLICY_BLOCKS`.

It may not return an authorization such as `ADMIT NODE`.

## Activation

Load conditionally for tasks involving:

- node admission;
- node trust;
- pairing/authentication evidence;
- capability manifests;
- service/model advertisement;
- LAN discovery;
- routing eligibility;
- real-node manager evidence.

## Safety

P5 is instruction-only.

It does not:

- write trust-store entries;
- generate/rotate/revoke pairing secrets;
- send signed requests;
- connect to phones;
- change LAN exposure;
- modify routing;
- transfer/delete models;
- promote physical N-stages;
- enable hooks/MCP/memory/autonomous loops.

## Exit criteria

- project skill registered conditionally;
- no runtime source changes;
- AgentShield no new finding class;
- Phase 0 GREEN;
- Edge ECC gate GREEN.
