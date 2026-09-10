# ORBI Edge Mesh — Request Execution & Fallback v0.1

## Goal

Move from route planning to actual request execution.

## Flow

```text
User / LUMI request
      ↓
Capability + model filtering
      ↓
Thermal/power eligibility
      ↓
Ordered candidate list
      ↓
HTTP request to candidate 1
      ↓
SUCCESS → return response

or

FAIL / TIMEOUT
      ↓
candidate 2
      ↓
SUCCESS → return response
```

## Current transport

Phase 0 LLM execution uses the OpenAI-compatible:

```text
POST /v1/chat/completions
```

provided by llama-server or the mock equivalent.

## Executable candidate

A node is only added to the execution list when:

- it is policy-eligible;
- it exposes the requested service/model;
- the service has a concrete endpoint.

This is stricter than merely being discoverable.

## Failure classes handled

Current prototype treats these as fallback-triggering failures:

- HTTP error
- URL/network error
- timeout
- invalid JSON
- unexpected runtime error

## Current limitation

The executor retries complete requests from the beginning.

It does not yet support:
- stream resumption;
- token-level migration;
- partial-generation continuation;
- distributed decoding;
- cross-node KV cache transfer.

Those are significantly harder problems and are explicitly outside Phase 0.

## Safety rule

Fallback never overrides thermal/power exclusion.

An unhealthy candidate is not put back into the list merely because the first execution attempt failed.
