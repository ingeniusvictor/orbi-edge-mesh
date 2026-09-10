# P0 — Request Execution & Real Fallback

Status: IMPLEMENTED IN SIMULATION

## Implemented

- ordered candidate planner
- concrete endpoint validation
- OpenAI-compatible chat request execution
- first-success return
- automatic fallback after error
- all-failed result
- structured attempt history
- mock inference server
- unit tests

## Acceptance cases

### Case A — First node works

```text
Node-01 → 200
Result → Node-01
Attempts → 1
```

### Case B — First node fails

```text
Node-01 → HTTP 500
Node-02 → 200
Result → Node-02
Attempts → 2
```

### Case C — All fail

```text
Node-01 → fail
Node-02 → fail
Result → EXECUTION FAILED
```

## Hardware validation later

Once Node-01 has real llama-server running:
- replace mock endpoint with POCO LAN IP;
- execute the same flow;
- record actual latency;
- later add Node-02 and verify true cross-phone fallback.
