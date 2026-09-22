# EDGE-ECC-P4 — Physical Evidence Review Project Skill

Status: CONTROLLED / FIRST EDGE PROJECT SKILL

## Skill

`.agents/skills/orbi-edge-physical-evidence-review/SKILL.md`

## Why this skill first

Edge Mesh differs from the previous Agent Kit pilots because real Android-device evidence is part of the product/research truth.

The highest recurring risk is accidentally promoting:

- a green CI build into a physical stage PASS;
- a model hash into inference readiness;
- pairing/HMAC into encrypted transport;
- node discovery into trust/admission;
- whole-request routing into distributed model execution.

P4 encodes the repository's existing physical-evidence semantics rather than inventing a new validation system.

## Grounding

The skill explicitly defers acceptance criteria to current repository sources such as:

- `docs/native/NATIVE_ALPHA_VALIDATION_RUNBOOK.md`;
- stage-specific native validation documents;
- `docs/hardware/DEVICE_MATRIX.md`;
- `docs/policy/THERMAL_POWER_POLICY_v0.1.md`;
- PC-side physical validation probes.

## Routing

Load this skill conditionally for tasks involving:

- physical N-stage claims;
- APK installation/device readiness;
- model import/hash/load/inference;
- pairing/signed/replay testing;
- headless parity;
- thermal/power observations;
- discovery/routing on real nodes;
- physical certification reports.

Do not load it for unrelated documentation or pure software refactors.

## Safety

Instruction-only.

P4 does not:

- run ADB;
- connect to phones;
- read/store pairing secrets;
- expose LAN services;
- load/transfer/delete models;
- change resource policy;
- promote an N-stage;
- enable hooks/MCP/memory/autonomy.

## Exit criteria

- skill registered and conditionally routed;
- AgentShield remains clean or new class is reviewed;
- Phase 0 static checks GREEN;
- Edge ECC PR Gate GREEN;
- no Android/Kotlin/C++/Python product runtime source changes;
- no physical stage status changed.
