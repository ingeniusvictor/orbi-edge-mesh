# ORBI Edge Mesh — Adaptive Scheduling v0.1

## Goal

Use local historical evidence to improve routing decisions without weakening safety constraints.

## Inputs

Current adaptive score uses:

- success rate
- average successful latency
- average observed temperature
- number of historical samples

## Important ordering

Adaptive history is **not** the first gate.

The routing flow remains:

```text
service/model locality
        ↓
runtime health
        ↓
thermal/power eligibility
        ↓
historical performance
        ↓
failure count
        ↓
current temperature
```

Therefore:

```text
historically fastest node + critical temperature
→ excluded
```

## Cold-start handling

A node with no history receives a neutral-but-nonzero penalty.

This prevents:

```text
no data = perfect score
```

Low sample counts also receive a temporary penalty so one lucky request does not dominate the scheduler.

## Phase 0 scoring

The Phase 0 score is intentionally simple:

```text
reliability penalty
+ latency penalty
+ historical thermal penalty
+ low-sample penalty
```

The exact weights are experimental and must be calibrated with real Node-01/02/03 data.

## Non-goals

Adaptive Scheduling v0.1 does not use:
- machine learning
- reinforcement learning
- cloud analytics
- prompt content
- user profiling

It is deterministic, local and inspectable.

## Future evolution

Later versions may score per:

```text
node
+ model
+ quantization
+ context size
+ workload class
```

and include:
- TTFT
- generation tokens/s
- RAM pressure
- battery drain/token
- thermal slope
- queue delay
- network RTT
