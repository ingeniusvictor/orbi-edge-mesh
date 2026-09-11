# ADR-0012 — Explicit Local Trust

Status: ACCEPTED

## Decision

Network proximity is not sufficient for ORBI node trust.

Every privileged ORBI node relationship must be explicitly paired.

## Rationale

Consumer LANs commonly contain unrelated or untrusted devices.

## Rule

`same Wi-Fi != trusted node`

## Consequence

The control plane must distinguish unpaired, trusted and revoked nodes before privileged actions are allowed.
