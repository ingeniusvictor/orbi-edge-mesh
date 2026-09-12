# N14 Native Inference Performance Telemetry

## Goal

Make the ORBI Android runtime measure its own inference performance so benchmark evidence no longer depends on Termux console output.

## Metrics

After each completed native generation ORBI records:

- prompt token count;
- generated token count;
- first/prompt decode milliseconds;
- subsequent generation decode milliseconds;
- total generation-loop milliseconds;
- prompt tokens per second;
- generation tokens per second;
- configured context size;
- configured thread count.

## Semantics

The first decode processes the prompt and produces the first sampled token.

`prompt_tokens_per_second` uses prompt token count divided by first-decode time.

`generation_tokens_per_second` uses only generated tokens whose decode time is included in the subsequent-generation timing window.

The values are research metrics and should be compared with the existing Phase 0 Termux reference under similar model/context/thread conditions.

## Surfaces

- in-app performance text after native generation;
- `/diagnostics` as `last_generation_metrics`;
- `/v1/chat/completions` as optional `orbi_metrics` metadata.

The normal assistant response content remains backward compatible.

## Error behavior

Failed generation paths record an explicit metrics error status instead of reusing old successful measurements as if they were current.

## Physical PASS

Run Qwen3 1.7B Q4_K_M on Node-01 with context 4096 and 4 threads, record native metrics, and compare them with the known Termux reference without claiming equivalence until measured.
