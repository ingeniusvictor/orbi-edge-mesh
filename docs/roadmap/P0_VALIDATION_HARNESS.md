# P0 — Validation Harness

Status: IMPLEMENTED / REAL NODE PENDING

## Goal

Convert Node-01 bring-up from an ad-hoc manual test into a reproducible PASS/FAIL workflow.

## Output

The harness produces a local JSON result containing:

- target node
- requested model
- check names
- PASS/FAIL state
- elapsed time
- diagnostic detail
- UTC timestamp

## Design rule

Validation evidence must be reproducible and machine-readable.

Human screenshots may supplement evidence, but they should not be the only proof.
