# P0 Model 001 — Qwen3 1.7B Q4_K_M

Status: CANDIDATE / NOT YET RUN ON NODE-01

## Purpose

Use a small, current GGUF model to prove the complete Node-01 path before testing larger models.

## Candidate

- Repository: `ggml-org/Qwen3-1.7B-GGUF`
- File: `Qwen3-1.7B-Q4_K_M.gguf`
- Quantization: Q4_K_M
- Approximate published size: 1.28 GB
- Runtime: llama.cpp

## Why this model

- small enough for a conservative first test;
- Qwen family aligns with the broader ORBI local-first direction;
- GGUF distribution is explicitly documented for llama.cpp;
- significantly below Node-01 physical RAM capacity;
- large enough to validate a real conversational model rather than a synthetic stub.

## Initial runtime hypothesis

```text
context = 4096
threads = 4
screen = ON for first smoke test
network = disconnected for offline proof after download
```

These are starting values, not optimized values.

## Required evidence

- exact llama.cpp commit
- exact model file size
- local SHA-256
- prompt
- response
- tokens/s if runtime reports it
- elapsed time
- temperature before/after
- battery before/after

## PASS

The test passes if Node-01 produces a coherent local response with Internet access disabled and without abnormal thermal behavior.
