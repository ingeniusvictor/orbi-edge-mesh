# Node-01 — PC Validation Harness

## Purpose

Provide one repeatable PC-side command to validate the first real POCO inference endpoint.

## Command

```bash
python scripts/pc/node01_validation_harness.py \
  --host <POCO_IP> \
  --model qwen3-1.7b-q4_k_m
```

## Checks

Current Phase 0 harness validates:

1. `/v1/models` is reachable.
2. `/v1/chat/completions` returns a non-empty answer.
3. latency is recorded for each check.
4. a machine-readable evidence JSON is written locally.

Default evidence path:

`runtime/validation/node01-validation.json`

## Interpretation

`PASS` means the PC can reach and use the local LLM endpoint.

It does not by itself certify:

- screen-off stability;
- thermal safety;
- battery behavior;
- watchdog recovery;
- long-duration stability.

Those remain separate Phase 0 gates.
