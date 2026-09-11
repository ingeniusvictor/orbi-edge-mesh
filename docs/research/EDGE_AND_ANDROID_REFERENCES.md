# Edge AI Research References

This document records external concepts that motivate ORBI Edge Mesh. They are references, not claims of ORBI originality.

## Edge0 concept

Relevant ideas:
- keep most weights on storage
- activate/load only required sparse experts
- predict likely next experts
- overlap I/O and compute
- minimize active memory

The public reproducibility and platform support of external projects must be re-checked before relying on specific benchmark claims.

## edgeMoE / BigMoeOnEdge

Relevant direction:
- Android-focused MoE expert streaming
- flash-backed expert loading
- bounded expert cache
- CPU-first execution path
- llama.cpp integration concepts

Potential use for ORBI:
- reference implementation for a later MoE phase
- benchmark streaming versus fully resident models
- study expert-cache telemetry

## llama.cpp

Potential role:
- first practical Android inference baseline
- GGUF model support
- local server mode
- broad CPU architecture support

## MLC-LLM

Potential role:
- later comparison path for mobile GPU acceleration
- Android deployment research

## Distributed mobile inference research

ORBI should distinguish between:
- independent service nodes coordinated by a scheduler;
- pipeline/model partitioning;
- tensor parallelism;
- MoE expert distribution.

Phase 0 uses the first option because it has the lowest integration and network-latency risk.

## Novelty boundary

ORBI Edge Mesh should not claim that:
- running LLMs on Android is new;
- flash-streamed MoE is new;
- mobile distributed inference is new.

Potential ORBI differentiation is the integrated system around:
- heterogeneous reused Android hardware
- automatic hardware profiling
- local-first routing
- thermal protection
- power-aware scheduling
- model/storage management
- voice/embedding/LLM specialization
- future cross-device expert experiments
