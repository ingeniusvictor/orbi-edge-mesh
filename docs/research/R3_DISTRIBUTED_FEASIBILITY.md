# R3 Cross-Phone Distributed Inference Feasibility Gate

## Purpose

R3 does not assume that splitting a model across phones is useful.

It creates a quantitative stop/go gate before ORBI invests in distributed experts, pipeline stages or tensor/shard execution.

## Principle

A technically possible cross-phone split is not automatically a useful one.

Wi-Fi transfer, RTT, jitter, serialization, orchestration and thermal/energy cost can erase the compute benefit.

## Harness inputs

For every candidate split ORBI must measure or estimate:

- single-node compute time;
- remote-stage compute time;
- bytes transferred in each direction;
- Wi-Fi RTT;
- throughput;
- jitter;
- orchestration overhead.

## Decision

The initial research gate rejects a scenario when:

- distributed execution is slower than the single-node baseline;
- estimated speedup is below 1.10x; or
- network/orchestration overhead is more than 35% of distributed latency.

These thresholds are research defaults and may be revised with real measurements.

## Critical rule

A `NO-GO` result is a successful research outcome.

ORBI must document negative results rather than forcing distributed sharding into the architecture.

## Example

```powershell
python research/distributed_feasibility.py `
  --scenarios research/distributed-scenarios.example.json `
  --rtt-ms 3.5 `
  --throughput-mbps 600 `
  --jitter-ms 1.0
```

## Synthetic scenario warning

The example scenario numbers are deliberately synthetic and exist only to verify the harness.

They are not measurements or performance claims for the POCO, Xiaomi 11T Pro or Mi 10T Lite.

## Physical research sequence

Only after N10/R1/R2 are stable:

1. measure LAN RTT/jitter between the real nodes;
2. measure effective transfer throughput;
3. profile candidate compute stages locally;
4. feed measured values into this harness;
5. pursue only scenarios marked `PHYSICAL-EXPERIMENT-CANDIDATE`;
6. compare the real experiment against the predicted result.
