# EDGE-ECC-P6 — Structured Agent Harness Contract

Status: CONTROLLED / CONTRACT-DEFINED

## Goal

Adapt the ORBI Agent Engineering Kit structured-observation pattern to Edge Mesh without introducing a second runtime-autonomy system or granting physical-device authority.

## Adds

- `.agents/skills/orbi-edge-agent-harness/SKILL.md`
- `.orbi/orbi-edge-agent-observation-v1.schema.json`
- `scripts/validate_orbi_edge_agent_observation.py`
- `tests/test_edge_agent_harness_contract.py`
- profile/adapter conditional routing

The harness test is included automatically by:

```bash
python -m unittest discover -s tests -v
```

## Explicit authority impact

Every observation reports booleans for:

- physical stage status;
- pairing-secret lifecycle;
- LAN exposure;
- resource-policy bypass;
- node admission or routing;
- model transfer or deletion;
- distributed-execution claims.

The validator checks structure only. It does not authorize those actions or prove evidence true.

## Local evidence

`localEvidenceRequired` remains explicit because CI cannot prove physical Android state.

A successful schema validation does not convert CI evidence into:

- APK installation/runtime evidence;
- model load/inference evidence;
- pairing/replay evidence on a real LAN;
- headless parity;
- thermal/power behavior;
- real node discovery/routing.

## Recovery

Error observations require:

- root-cause hint;
- safe retry;
- stop condition.

Retry must add new evidence or change the tested hypothesis/input/scope. Repetition without new evidence is not progress.

## Safety

P6 adds no product runtime behavior.

It does not:

- promote N-stages;
- mutate pairing secrets;
- widen network exposure;
- bypass resource policy;
- admit/reroute nodes;
- transfer/delete models;
- enable distributed sharding;
- enable hooks/MCP/memory/Agent Kit autonomous loops.

## Exit criteria

- Python deterministic tests PASS;
- Android unit tests PASS;
- optimized release APK build PASS;
- native arm64 library verification PASS;
- AgentShield has no new finding class;
- no Android/Kotlin/C++ product runtime source changes.
