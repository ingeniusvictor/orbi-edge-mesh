---
name: orbi-edge-node-trust-review
description: Review whether an ORBI Edge Mesh node is sufficiently evidenced for admission, routing and capability use. Use for pairing/trust, node identity, capability manifests, discovery, routing eligibility, model/service advertisement and signed-control evidence. This skill never admits a node or mutates pairing/routing state.
version: "0.1.0"
license: MIT
metadata:
  origin: ORBI
  authoritative: false
  runtime_dependency: false
---

# ORBI Edge Node Trust Review

Use this skill whenever ORBI must decide whether a discovered Android node or advertised capability has enough evidence to be treated as trusted or eligible.

Repository code, current contracts, physical evidence, Git history and `AGENTS.md` remain authoritative.

## Core distinctions

```text
NODE IDENTITY != NODE TRUST
NODE DISCOVERED != NODE ADMITTED
PAIRING TOKEN EXISTS != PAIRING VERIFIED
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
MODEL LISTED != MODEL LOADED
MODEL LOADED != INFERENCE VERIFIED
RESOURCE VALUE REPORTED != RESOURCE VALUE CALIBRATED
ROUTING ELIGIBLE != PHYSICALLY CERTIFIED FOR EVERY CLAIM
PLACEMENT PLAN != MODEL TRANSFER
WHOLE-WORKLOAD ROUTING != DISTRIBUTED MODEL EXECUTION
```

## 1. Identity

Verify, where applicable:

- configured node ID;
- reported node ID;
- device/build identity;
- mismatch behavior;
- source of the identity value.

A matching string identifies the intended node contractually; it does not prove capabilities.

## 2. Pairing and request trust

Treat pairing/HMAC as request authentication and integrity only.

Review:

- pairing is explicitly enabled for the node;
- token/secret is not leaked into Git, logs or evidence;
- request signing uses the expected node ID/method/path/body;
- timestamp/nonce behavior is current;
- replay rejection is evidenced when required;
- revocation state is respected.

Never interpret HMAC authentication as TLS or encrypted transport.

## 3. Discovery

Discovery may prove a node is visible on the LAN.

It does not by itself prove:

- correct node identity;
- pairing/trust;
- model availability;
- resource eligibility;
- capability correctness;
- admission to routing.

Treat mDNS/NSD discovery as a locator signal, not trust authority.

## 4. Capability claims

For every advertised service/model/capability, identify its evidence level:

### DECLARED
Present in a manifest/config only.

### SOFTWARE-VALIDATED
Schema/code/tests confirm the capability can be represented or checked.

### PHYSICALLY-OBSERVED
Observed on the named physical node.

### PHYSICALLY-VERIFIED
The capability has passed the current governed physical procedure for the exact build/node.

Do not skip levels silently.

## 5. Model evidence

A routing node should not be treated as model-ready solely because `/v1/models` returns an entry.

Where real routing is claimed, review evidence for:

- model identity;
- on-device hash when governed by the current stage;
- actual native model-loaded state;
- successful inference where required;
- current process/build identity.

## 6. Resource policy

Eligibility must remain subordinate to the current resource guard.

Review:

- ALLOW / DEGRADE / BLOCK state;
- battery and charging state when available;
- thermal category/value provenance;
- unknown or missing telemetry handling;
- no policy bypass.

A trusted node can still be ineligible for work.

## 7. Admission

Real node admission is an authority-impacting action.

This skill may only return a review status:

- `EVIDENCE_SUFFICIENT_FOR_REVIEW`
- `EVIDENCE_INCOMPLETE`
- `IDENTITY_MISMATCH`
- `SECURITY_EVIDENCE_MISSING`
- `CAPABILITY_NOT_VERIFIED`
- `RESOURCE_POLICY_BLOCKS`

It may not:

- pair a node;
- write the trust store;
- rotate/revoke secrets;
- alter routing config;
- make LAN exposure changes;
- admit a node automatically.

## 8. Routing review

For a candidate routed workload, verify separately:

- reachable;
- expected Node ID;
- paired/authenticated;
- required service advertised;
- required model advertised;
- required capability physically verified where the stage requires it;
- model loaded where required;
- resource action is allowed;
- no known physical gate contradicts readiness.

If any required item is unproven, report it rather than converting absence of evidence into eligibility.

## 9. Distributed-compute boundary

Never infer any of the following from multi-node routing:

- unified RAM;
- unified storage;
- tensor sharding;
- expert sharding;
- KV-cache migration;
- distributed single-model execution.

Whole-request fallback/routing is a different capability.

## 10. Review output

Return:

```text
ORBI EDGE NODE TRUST REVIEW

Node:
- configured ID:
- reported ID:
- device/build:
- branch/HEAD:

Identity:
- match:
- evidence:

Pairing/security:
- paired:
- signed request evidence:
- replay evidence:
- secret exposure:
- transport encryption claim:

Capabilities:
- advertised:
- physically verified:
- unverified:

Model:
- advertised:
- loaded:
- inference verified:

Resources:
- action:
- battery:
- thermal:
- missing telemetry:

Routing:
- requested service/model:
- eligibility evidence:
- blockers:

Authority impact:
- trust-store mutation requested: YES/NO
- pairing-secret lifecycle requested: YES/NO
- LAN exposure change requested: YES/NO
- route/admission mutation requested: YES/NO
- distributed-execution claim changed: YES/NO

Review result:
- EVIDENCE_SUFFICIENT_FOR_REVIEW / EVIDENCE_INCOMPLETE /
  IDENTITY_MISMATCH / SECURITY_EVIDENCE_MISSING /
  CAPABILITY_NOT_VERIFIED / RESOURCE_POLICY_BLOCKS

Missing evidence:
- ...
```

## Rollback

This skill is instruction-only.

Remove `.agents/skills/orbi-edge-node-trust-review/` and its profile/adapter routing entries. Product routing and trust code must not depend on this file.
