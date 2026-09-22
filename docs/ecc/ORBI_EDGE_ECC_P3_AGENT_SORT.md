# EDGE-ECC-P3 — Evidence-backed Agent and Skill Classification

Status: CLASSIFICATION-ONLY / NO PRODUCT-RUNTIME CHANGE

Base branch: `feature/native-alpha-pairing-ux`  
P2 canonical at start: `766a48a10756969c59f19b85638b54da962d0e51`  
ORBI Agent Kit: v0.2.0

## Purpose

Reduce the ORBI Edge Mesh Agent Kit surface to a small DAILY set and keep specialist capabilities on-demand.

This phase does not install ECC wholesale and does not materialize a new runtime agent.

## Repository evidence

Current Native Alpha tree contains approximately:

- 31 Kotlin files;
- 87 Python files;
- one small but critical C++/JNI native surface;
- Android/Compose + JNI/llama.cpp runtime;
- Python mesh-manager, routing, security and PC validation tooling;
- 32 test files;
- 10 GitHub workflows;
- physical Android validation that CI cannot reproduce.

The dominant recurring engineering problem is therefore not generic app development. It is preserving software-vs-physical evidence boundaries while reviewing Kotlin/Android, Python coordination/security, and a narrow critical native boundary.

## DAILY agents

| Agent | Why DAILY |
|---|---|
| `planner` | phased N-stage work, physical gates and research branches |
| `architect` | Android/native/manager/security/routing boundaries |
| `code-reviewer` | cross-language changes and integration review |
| `security-reviewer` | pairing/HMAC, replay, LAN exposure, model/file paths |
| `tdd-guide` | deterministic Python/Android tests before physical validation |
| `doc-updater` | runbooks and certification status are part of engineering truth |
| `kotlin-reviewer` | Android/Compose is a recurring product surface |
| `python-reviewer` | manager/security/validation tooling is Python-heavy |

## LIBRARY agents

| Agent | Trigger |
|---|---|
| `cpp-reviewer` | **mandatory** for C++/JNI/native boundary changes |
| `build-error-resolver` | Gradle/CMake/NDK/CI failures |
| `performance-optimizer` | inference/latency/resource benchmark work |
| `refactor-cleaner` | explicitly scoped cleanup |
| `e2e-runner` | explicit UI/device automation if introduced |
| `harness-optimizer` | Agent Kit harness work only |
| `loop-operator` | only a separately governed autonomous-loop experiment |
| `mle-reviewer` | model/runtime evaluation work |
| `rag-pipeline-reviewer` | not current; only if retrieval becomes an active surface |

C++ is not always loaded because the file surface is small, but its reviewer becomes mandatory whenever JNI/native code is changed because the risk is disproportionately high.

## DAILY skills

- `architecture-decision-records`
- `coding-standards`
- `contract-first`
- `tdd-workflow`
- `verification-loop`
- `security-review`
- `context-budget`
- `delivery-gate`
- `git-workflow`

## LIBRARY skills

- `agent-sort`
- `codebase-onboarding`
- `agent-harness-construction`
- `ai-regression-testing`
- `eval-harness`
- `benchmark`
- `benchmark-methodology`
- `error-handling`
- Kotlin/Android specialist patterns/testing
- Python specialist patterns/testing
- C++ coding/testing patterns
- performance and distributed-compute research procedures

## Edge-specific rules that generic ECC cannot replace

```text
CI GREEN != PHYSICAL NODE CERTIFIED
APK BUILDS != APK RUNS CORRECTLY ON DEVICE
MODEL HASH MATCH != MODEL LOAD SUCCESS
MODEL LOAD SUCCESS != INFERENCE SUCCESS
INFERENCE SUCCESS != HEADLESS PARITY
SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED
NODE DISCOVERED != NODE TRUSTED / ELIGIBLE
CAPABILITY ADVERTISED != CAPABILITY PHYSICALLY VERIFIED
PLACEMENT PLAN != MODEL TRANSFER
WHOLE-WORKLOAD ROUTING != UNIFIED RAM / DISTRIBUTED MODEL EXECUTION
```

These remain repository-owned invariants.

## First project-skill recommendation

P4 should materialize:

`orbi-edge-physical-evidence-review`

It should distinguish:

- software-preparation evidence;
- CI evidence;
- local-device evidence;
- physical N-stage certification;
- pairing/security evidence;
- network exposure evidence;
- thermal/power evidence;
- multi-node evidence.

The skill must not itself promote a physical N-stage.

## Second project-skill recommendation

P5:

`orbi-edge-node-trust-review`

Focus:

- identity != capability validity;
- discovery != admission;
- signed request != encrypted transport;
- advertised capability != physically verified capability;
- routing eligibility requires current evidence;
- placement plan != transfer/execution.

## Deferred

Still disabled:

- hooks;
- MCP;
- continuous learning;
- unified memory;
- Agent Kit autonomous loops;
- multi-agent runtime roles;
- automatic model transfer;
- automatic physical-stage promotion.

## Exit criteria

P3 passes when:

1. profile matches this classification;
2. no product/runtime files change;
3. AgentShield remains 100/A with zero findings or any new class is explicitly reviewed;
4. Phase 0 static checks remain GREEN;
5. Edge ECC PR Gate remains GREEN;
6. no physical stage status is changed.
