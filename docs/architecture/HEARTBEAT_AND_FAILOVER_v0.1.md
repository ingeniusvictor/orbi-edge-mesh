# Heartbeat and Failover v0.1

## Goal

ORBI Edge Mesh must assume phones can disappear at any time.

Reasons include:
- Android background restrictions;
- Wi-Fi roaming;
- battery depletion;
- thermal throttling or shutdown;
- manual app closure;
- device reboot.

## Heartbeat model

The manager periodically refreshes:

```text
GET /orbi/v1/node
```

A successful response:
- updates capability data;
- refreshes last_seen;
- resets consecutive failure count.

A failed response:
- increments failure count for a previously known node.

## Stale eviction

A node whose last successful heartbeat exceeds the configured TTL is evicted from the active registry.

Phase 0 defaults are experimental:
- heartbeat interval: 5 s
- TTL: 15 s
- request timeout: 3 s

These are not production defaults.

## Fallback routing

The scheduler generates a deterministic ordered list of eligible nodes.

Example:

```text
LLM request
   ↓
Node-01
   ↓ failure
Node-02
   ↓ failure
No route
```

The Phase 0 prototype only computes the fallback order. Actual inference retry execution is deferred until real inference adapters are connected.

## Ranking inputs in v0.1

1. service availability
2. health status
3. consecutive failures
4. temperature
5. node_id deterministic tie-break

Future additions:
- model locality
- queue depth
- RAM pressure
- recent throughput
- time to first token
- battery reserve
- charging state
- network RTT
