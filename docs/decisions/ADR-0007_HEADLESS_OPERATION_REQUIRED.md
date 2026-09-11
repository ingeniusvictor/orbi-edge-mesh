# ADR-0007 — Headless Operation Is Required

Status: ACCEPTED

## Decision

Every permanent ORBI Edge node must support useful operation with the screen off.

## Rationale

A phone used as an AI/server node should not need to keep its display illuminated.

Keeping the display on would:
- waste energy;
- generate additional heat;
- reduce practical always-on viability;
- make the device behave like a demo rather than infrastructure.

## Rule

A node can be considered:

```text
EXPERIMENTAL
```

before screen-off validation.

It cannot be considered:

```text
SERVER READY
```

until it passes headless/screen-off certification.

## Safety

Screen-off operation must not bypass:
- thermal protection;
- battery protection;
- operator shutdown;
- Android preservation rules.
