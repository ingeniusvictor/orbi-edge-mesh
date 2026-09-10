# ORBI Edge Mesh — Phase 0 Integration Baseline

Status: CANDIDATE / HARDWARE VALIDATION PENDING

## Purpose

Freeze a coherent Phase 0 software baseline before the first real POCO X7 Pro validation.

## Integrated capabilities

- node discovery source
- heartbeat and registry
- stale-node handling
- thermal/power eligibility
- model locality
- workload classification
- adaptive historical scoring
- request candidate planning
- HTTP request execution with fallback
- local observability
- headless/screen-off operation tooling
- bounded watchdog recovery
- recovery policy gate
- idle/warm/cold power states
- model placement planning
- explicit local trust primitives

## Unified entrypoint

`manager/orbi_manager_phase0.py`

Current unified request execution supports LLM chat through an OpenAI-compatible `/v1/chat/completions` endpoint.

Other service profiles are routable in architecture but not yet executed by the unified adapter.

## Phase 0 hardware gate

The baseline must not be merged as fully certified until Node-01 proves:

1. Termux + llama.cpp builds and runs.
2. A small local model answers offline.
3. The PC reaches the POCO over LAN.
4. Screen-off operation remains stable.
5. At least one inference completes after 20+ minutes screen-off.
6. Thermal/battery telemetry is captured.
7. No unsafe thermal behavior is observed.
8. Watchdog recovery is validated under supervision.
9. Observability records real execution evidence.

## Explicit non-goals

- distributed tensor parallelism
- expert sharding across phones
- cross-node KV-cache migration
- cloud coordination
- public internet exposure
- production mTLS
- automatic model transfer

## Baseline principle

Phase 0 proves that one reused Android phone can behave as a stable local AI node before the system scales to multiple phones.
