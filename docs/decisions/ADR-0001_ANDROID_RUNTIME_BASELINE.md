# ADR-0001 — Android Runtime Baseline

Status: ACCEPTED FOR PHASE 0

## Context

ORBI Edge Mesh needs a first inference path that is:
- local;
- reversible;
- measurable;
- compatible with Android;
- usable without root;
- mature enough to provide a CLI and HTTP server.

## Decision

Use **Termux + llama.cpp** as the Phase 0 baseline runtime for Node-01.

## Reasons

- llama.cpp currently documents Android CLI builds under Termux.
- Termux does not require root.
- GGUF provides a practical model packaging path.
- llama.cpp provides both CLI and server executables.
- The baseline is CPU-oriented and therefore avoids prematurely coupling Phase 0 to a specific mobile GPU/NPU stack.

## Consequences

Positive:
- quick route to first measurable inference;
- reproducible runtime commit;
- easy path from CLI to LAN API;
- useful baseline before GPU/NPU experimentation.

Negative:
- initial performance may not represent the maximum capability of the POCO hardware;
- building directly on the phone takes time;
- Android background-process policies may affect long-duration operation.

## Deferred alternatives

- llama.cpp Android GUI binding
- Android NDK cross-compiled binaries
- MLC-LLM
- vendor-specific NPU runtimes
- edgeMoE streaming runtime

These become comparison candidates only after the baseline is certified.
