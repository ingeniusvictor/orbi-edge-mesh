# ORBI Edge Mesh Architecture v0.1

## Purpose

ORBI Edge Mesh is a local-first edge AI platform that reuses heterogeneous Android devices as coordinated inference and AI-service nodes.

The initial architecture intentionally avoids distributed tensor/model sharding. Each node first runs complete services locally; the manager coordinates requests between nodes.

## Logical architecture

```text
                    ORBI EDGE MANAGER
                           |
        +------------------+------------------+
        |                  |                  |
     NODE-01            NODE-02            NODE-03
    POCO X7 Pro       Xiaomi 11T Pro      Mi 10T Lite
      Main LLM        Secondary LLM      Voice / Embed
```

## Core components

### Android Node Agent
Runs on every device and reports:
- device identity
- physical RAM
- storage capacity/free space
- model inventory
- service availability
- temperature
- battery state
- current load
- basic benchmark results

### Hardware Profiler
Creates a normalized capability profile per node. Physical RAM and storage-backed memory must never be reported as equivalent.

### Thermal Protection Layer
Observes thermal state and can:
- reduce threads
- reject new work
- migrate work to another node
- pause inference when limits are exceeded

Thresholds must be calibrated per device. Early temperature bands are experimental, not manufacturer limits.

### Power Manager
Tracks charging and battery conditions. Future versions may integrate smart charging or controlled power delivery.

### Local API
Each inference-capable node should expose a local HTTP API. OpenAI-compatible request/response semantics are preferred where practical.

### Discovery
Nodes should become discoverable on the local network without manual IP bookkeeping in later phases.

### Scheduler / Router
Chooses the best available node based on:
- requested capability/model
- availability
- RAM pressure
- temperature
- recent latency
- queue depth
- power state

### Model Storage Manager
Tracks model location, version, quantization, free space, and replication policy.

## Non-goals for Phase 0

Phase 0 does not implement:
- distributed tensor parallelism
- expert sharding across phones
- automatic charging hardware
- production remote access
- cloud dependency
- root-only features

## Long-term research direction

Later research may evaluate:
- MoE expert streaming from flash
- cross-device expert placement
- mobile GPU/NPU acceleration
- fault tolerance
- opportunistic task migration
- distributed speech, embedding, retrieval and generation pipelines
