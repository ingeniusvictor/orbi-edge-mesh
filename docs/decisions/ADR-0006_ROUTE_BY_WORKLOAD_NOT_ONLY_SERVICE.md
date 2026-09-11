# ADR-0006 — Route by Workload, Not Only Service

Status: ACCEPTED

## Decision

ORBI Edge Mesh will model workload characteristics separately from service type.

## Rationale

`llm` alone is too coarse.

Two LLM tasks may differ materially in:
- expected duration
- latency sensitivity
- sustained heat
- model preference

Likewise, speech and embedding workloads may be better assigned to specialized nodes.

## Initial policy

Use deterministic workload classes and explicit service tags.

## Rule

No workload preference may override hard preservation/safety policy.
