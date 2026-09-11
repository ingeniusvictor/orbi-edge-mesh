# ORBI Edge Node API Contract v0.1

Status: **PROVISIONAL / PHASE 0**

## Purpose

Define the minimum interface ORBI expects from a local LLM node before the multi-node manager exists.

## Inference baseline

Phase 0 reuses the OpenAI-compatible HTTP routes provided by `llama-server`.

Required verification routes:

```text
GET  /v1/models
POST /v1/chat/completions
```

The exact implementation is delegated to llama.cpp during Phase 0. ORBI does not fork or redefine the inference protocol yet.

## ORBI control-plane contract

Future ORBI Node Agent implementations will expose node capability/health data separately from the inference runtime.

Conceptual local endpoint:

```text
GET /orbi/v1/node
```

Example response is versioned by:

```text
contracts/node-capability.schema.json
```

Phase 0 does **not** require this endpoint to be implemented. The schema is frozen early so later Node Agent work has a stable target.

## Required separation

The architecture intentionally separates:

```text
Inference plane
  llama-server / OpenAI-compatible API

Control plane
  ORBI node identity / telemetry / health / capabilities
```

This prevents ORBI scheduling logic from becoming tightly coupled to one model runtime.

## Network policy

During Phase 0:
- bind only for trusted LAN experiments;
- no router port forwarding;
- no public reverse proxy;
- no Internet-facing listener;
- no assumption of authentication because the endpoint is not permitted outside the trusted test LAN.

Authentication becomes mandatory before any broader network exposure is considered.
