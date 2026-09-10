# Phase 0 — Control Plane Simulation

## Purpose

Validate the ORBI node contract and first routing policy before real Android telemetry is available.

This simulator is not the production Node Agent.

## Components

```text
node/mock_node_agent.py
manager/orbi_manager.py
contracts/examples/*.json
tests/test_manager.py
```

## Simulation 1 — One node

Terminal A:

```bash
python node/mock_node_agent.py \
  --config contracts/examples/node02-capability.example.json \
  --port 8787
```

Terminal B:

```bash
python manager/orbi_manager.py http://127.0.0.1:8787 --service llm
```

Expected:

```text
[REGISTERED] node-02 ...
[ROUTE] service=llm -> node-02 ...
```

## Simulation 2 — Multiple mock nodes

Launch multiple mock agents on different ports, each using a different capability document.

The manager can then receive several URLs:

```bash
python manager/orbi_manager.py \
  http://127.0.0.1:8787 \
  http://127.0.0.1:8788 \
  --service llm
```

## Phase 0 routing policy

The initial deterministic policy is intentionally simple:

1. service must be available;
2. ready nodes rank above busy/degraded/paused/offline;
3. among equal-status nodes, lower known temperature wins;
4. node ID is a deterministic final tie-break.

This is **not** the final ORBI scheduler.

Future scoring may include:
- RAM pressure
- queue depth
- recent tokens/s
- time to first token
- battery state
- charging state
- model locality
- network latency
- storage I/O pressure

## Why simulate now

It proves that:
- node telemetry has a usable shape;
- manager logic does not depend directly on Xiaomi/MediaTek/Qualcomm APIs;
- routing can be tested before Android hardware is connected;
- future hardware integration can replace mock data without redesigning the manager.
