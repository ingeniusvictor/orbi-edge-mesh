# ORBI Edge Discovery

## Phase 0

Discovery begins with a static JSON source.

This is deliberate.

Before adding mDNS, UDP broadcast or another automatic mechanism, ORBI first freezes the interface between:

```text
Discovery source
      ↓
Node URLs
      ↓
Heartbeat
      ↓
Registry
      ↓
Scheduler
```

## Why not mDNS immediately?

Automatic LAN discovery introduces additional variables:

- Android multicast behavior
- Wi-Fi isolation
- power-management effects
- hostname collisions
- library/runtime dependencies
- router-specific behavior

Static discovery lets us validate the rest of the system first.

## Planned evolution

Phase 0:
- static JSON

Later:
- mDNS/Bonjour candidate
- UDP broadcast candidate
- optional QR/manual pairing
- persisted trusted-node registry

Any automatic method must remain local-first and must not require cloud discovery.
