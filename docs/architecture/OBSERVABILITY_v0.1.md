# ORBI Edge Mesh — Observability v0.1

## Goal

Store enough execution history to understand which device is actually best for each workload.

## Event model

Each execution attempt records:

```text
timestamp
request_id
node_id
service_type
model_id
success/failure
elapsed time
error
temperature
battery percentage
charging state
```

Storage in Phase 0:

```text
JSON Lines (.jsonl)
```

This is deliberately simple, local and append-only.

## Why attempt-level events

A request may fail over:

```text
Request ABC
  attempt 1 → Node-01 → timeout
  attempt 2 → Node-02 → success
```

Recording only the final result would hide the failure of Node-01.

## Derived metrics

The first local summary computes:

- attempts
- successes
- failures
- success rate
- average successful latency
- average observed temperature

## Future metrics

After real inference benchmarks are available:

- time to first token
- prompt tokens/s
- generation tokens/s
- RAM peak
- storage reads
- thermal slope
- battery drain per generated token
- queue delay
- network RTT
- model load time

## Privacy

Telemetry is local by default.

Do not send prompts, generated text or device telemetry to a cloud analytics service as part of Phase 0.
