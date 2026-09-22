# EDGE-ECC-P7 — Context Budget and Selective Loading

Status: CONTROLLED / DETERMINISTIC AUDITOR

## Purpose

Measure and preserve the selective loading model for ORBI Edge Mesh without weakening physical, security, network, resource or routing boundaries.

## Loading classes

- `AGENTS.md`: persistent invariant guidance;
- 4 Edge project skills: conditional/discoverable;
- profile/adapter/observation schema: on-demand config references.

The existence of a skill does not mean its full text should be injected into every Edge task.

## Adds

- `.agents/skills/orbi-edge-context-budget/SKILL.md`
- `scripts/ecc_orbi_edge_context_budget.py`
- `tests/test_edge_context_budget.py`
- profile/adapter conditional routing

The tests are included by:

```bash
python -m unittest discover -s tests -v
```

## Protected persistent invariants

The auditor fails closed if `AGENTS.md` loses the governed boundaries for:

- CI vs physical certification;
- signed authentication vs encrypted transport;
- trusted LAN vs public exposure;
- discovery vs node trust/admission;
- whole-request routing vs unified RAM/distributed execution;
- resource-policy bypass.

## Estimate semantics

Token estimates are approximate revision-comparison signals using a deterministic heuristic. They are not claims about exact tokenizer accounting.

The objective is not to minimize every byte. It is to keep persistent context focused while preserving safety and authority invariants.

## Safety

No product/runtime behavior changes.

P7 does not alter:

- Android/Kotlin/C++ runtime;
- physical stage status;
- pairing secrets;
- LAN exposure;
- node admission/routing;
- resource policy;
- model files;
- distributed execution.

## Exit criteria

- Python tests PASS, including context-budget tests;
- Android unit tests PASS;
- optimized release APK build PASS;
- native arm64 library verification PASS;
- AgentShield has no new finding class;
- project skills remain conditional rather than persistent.
