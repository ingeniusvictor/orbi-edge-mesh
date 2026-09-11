# P0 Model 001 — Qwen3 1.7B Q4_K_M

Status: FIRST LOCAL INFERENCE PASS / OFFLINE RE-RUN PENDING

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


## First measured run — 2026-09-10

Node-01 successfully loaded and executed the model through llama.cpp on Android/Termux.

Measured evidence:

- Device: POCO X7 Pro 5G
- Android: 16
- llama.cpp: 0.4.0-dev
- build: 10902
- commit: df03399b885831b2a1603b3abb0d8c156808e363
- compiler: Clang 21.1.8
- architecture: Android aarch64
- model: Qwen3 1.7B Q4_K_M
- model file: Qwen3-1.7B-Q4_K_M.gguf
- local SHA-256: d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5
- context: 4096
- threads: 4
- prompt processing: 77.6 tokens/s
- generation: 22.5 tokens/s
- result: coherent Spanish response generated locally

Observed model answer:

"Una red local de inteligencia artificial es un sistema o entorno que procesa datos y realiza tareas de inteligencia artificial en un área específica, utilizando recursos locales para mejorar eficiencia y reducir dependencia de servidores remotos."

### Remaining gate

Repeat the same inference with Internet access disabled to certify offline execution.
