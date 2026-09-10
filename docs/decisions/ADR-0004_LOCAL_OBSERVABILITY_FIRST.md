# ADR-0004 — Local Observability First

Status: ACCEPTED

## Decision

ORBI Edge Mesh stores operational telemetry locally before considering any remote analytics.

## Reason

The system is explicitly local-first and privacy-first.

Performance tuning requires evidence, but evidence does not require cloud telemetry.

## Initial format

Append-only JSONL.

Advantages:
- human-readable;
- trivial to inspect;
- easy to process with Python;
- no database dependency;
- easy to replace later.

## Rule

Do not record full prompt or response content in the default operational event stream.

Operational telemetry should capture behavior, not conversation content.
