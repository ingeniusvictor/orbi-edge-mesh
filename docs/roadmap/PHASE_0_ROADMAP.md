# Phase 0 — Foundation & Baseline

## Objective

Establish the minimum reproducible baseline required to turn Node-01 into a local AI server.

## Exit criterion

Phase 0 is complete only when the POCO X7 Pro can:

1. run a small local language model fully offline;
2. expose inference through a local-network API;
3. accept a request from a PC on the same Wi-Fi network;
4. produce a repeatable benchmark record;
5. complete a sustained stability run without unsafe thermal behavior.

## Work packages

### P0-A — Repository foundation
- architecture
- hardware inventory
- roadmap
- experiment protocol
- benchmark schema
- project boundaries

### P0-B — Node-01 environment
- install non-root Android terminal/runtime
- obtain/compile local inference runtime
- verify CPU architecture
- verify available RAM/storage
- capture baseline temperatures

### P0-C — Small-model smoke test
Target category: approximately 1B–3B parameters, quantized.

Success:
- model loads
- prompt completes
- no internet requirement during inference

### P0-D — Local API
- bind only to local network during experiment
- verify health endpoint
- send prompt from PC
- record latency and output

### P0-E — Benchmark baseline
Capture:
- model
- quantization
- context size
- prompt tokens
- generated tokens
- time to first token
- generation tokens/s
- peak memory
- start/end/max temperature
- battery percentage change
- runtime duration
- crashes/errors

### P0-F — Stability certification
Minimum initial sustained run target: 15–30 minutes.

Certification result:
- PASS
- PASS WITH LIMITATIONS
- FAIL

## Explicit deferrals

Do not begin yet:
- 30B/35B model targets
- multi-phone scheduling
- MoE streaming
- GPU/NPU tuning
- smart charging hardware
- enclosure/rack design

Those become justified only after the baseline is proven.
