# EDGE-ECC-P6 — Fifth Pilot Certification

Status: CERTIFICATION CANDIDATE

## Purpose

Close the ORBI Edge Mesh portability pilot against the remotely certified ORBI Agent Engineering Kit v0.2.0.

Agent Kit canonical reference:

`ingeniusvictor/orbi-agent-kit @ 8ef98f7a5edd7c27bda011ba77ddd3e26c3ee31f`

## Pilot phases

- P1 — repository adapter + Native Alpha integrated PR gate
- P2 — fresh repository-specific AgentShield report-only baseline
- P3 — evidence-backed DAILY / LIBRARY agent and skill classification
- P4 — `orbi-edge-physical-evidence-review` project skill
- P5 — `orbi-edge-node-trust-review` project skill

## Portability result

The shared Agent Kit structure transfers to Edge Mesh without making ECC or the Agent Kit a product runtime dependency.

Reusable shared structure:

- exact-state verification;
- security and authority review;
- context/loading discipline;
- repository adapter;
- conditional skill routing;
- report-only security baseline;
- deterministic CI/software gate;
- explicit local/physical evidence boundary.

Edge-specific authority remains project-owned:

- physical N-stage certification;
- pairing-secret lifecycle;
- trusted-LAN exposure;
- node admission and routing;
- resource policy;
- model placement/transfer;
- distributed-execution claims.

## Preserved evidence boundaries

```text
CI GREEN != PHYSICAL NODE CERTIFIED
APK BUILDS != APK RUNS CORRECTLY ON DEVICE
MODEL HASH MATCH != MODEL LOAD SUCCESS
MODEL LOAD SUCCESS != INFERENCE SUCCESS
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
NODE DISCOVERED != NODE ADMITTED
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
WHOLE-WORKLOAD ROUTING != UNIFIED RAM OR DISTRIBUTED MODEL EXECUTION
```

## Deliberately not enabled

- full ECC install;
- hooks;
- MCP;
- continuous learning;
- unified memory;
- Agent Kit autonomous loops;
- multi-agent runtime roles;
- automatic security fixes;
- automatic node admission;
- automatic model transfer;
- privileged runtime writes.

## Certification rule

The final P6 HEAD must pass:

1. Phase 0 static checks;
2. ORBI Edge ECC integrated gate;
3. ORBI Edge ECC AgentShield report-only with no new finding class.

Only then may the profile move from `candidate` to `certified`.

This certification applies to the Agent Kit portability/adoption surface only. It does not promote any Android physical N-stage.
