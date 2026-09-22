---
name: orbi-edge-context-budget
description: Keep ORBI Edge Mesh agent instructions layered so physical/security invariants stay persistent while project procedures, schemas and machine-readable state remain conditional or on-demand.
version: "0.1.0"
license: MIT
metadata:
  origin: ORBI
  authoritative: false
  runtime_dependency: false
---

# ORBI Edge Context Budget

Use when adding or expanding `AGENTS.md`, Edge project skills, repository-adapter/profile rules or structured-observation configuration.

## Loading model

- `AGENTS.md` -> persistent invariants;
- Edge project skills -> discoverable/conditional;
- profile/adapter/observation schema -> config-reference/on-demand.

Available does not mean permanently loaded.

## Rules

- keep CI-vs-physical evidence boundaries in `AGENTS.md`;
- keep pairing-secret and trusted-LAN boundaries persistent;
- keep resource-policy and distributed-compute truthfulness persistent;
- keep detailed physical procedures in `orbi-edge-physical-evidence-review`;
- keep node trust/admission procedures in `orbi-edge-node-trust-review`;
- keep action-space/recovery/observation rules in `orbi-edge-agent-harness`;
- keep machine-readable routing/state in profile/adapter/schema;
- do not duplicate full runbooks or contracts into persistent instructions;
- do not remove authority/safety guidance solely to reduce estimates.

## Auditor

```bash
python scripts/ecc_orbi_edge_context_budget.py
python scripts/ecc_orbi_edge_context_budget.py --json
```

Estimates are revision-comparison signals, not exact model-token accounting.

The auditor also fails closed if required persistent Edge invariants disappear from `AGENTS.md`.

## Safety

Context optimization must never weaken:

- physical-stage evidence discipline;
- pairing-secret handling;
- trusted-LAN/public-exposure boundary;
- resource ALLOW / DEGRADE / BLOCK policy;
- node trust/admission evidence;
- model-transfer authority;
- distributed-compute claim boundaries.

## Rollback

Remove the skill, auditor/test and profile/adapter routing registration.

No Android/Kotlin/C++/Python product runtime depends on this skill.
