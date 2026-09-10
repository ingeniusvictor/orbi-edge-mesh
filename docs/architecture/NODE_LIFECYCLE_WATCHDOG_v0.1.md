# ORBI Edge Mesh — Node Lifecycle & Watchdog v0.1

## Goal

Keep a headless node useful when the display is off without creating an uncontrolled restart loop.

## Fault model

- process up + API up → healthy
- process up + API down → hung / starting
- process down → service down
- repeated restart failures → quarantine
- thermal/power hard pause → do not restart

## Bounded recovery

Automatic recovery has a finite restart budget. Phase 0 default: `MAX_RESTARTS=3`.

After the budget is exhausted, the node must enter quarantine and require operator inspection.

This avoids an infinite crash → restart → crash loop that wastes battery and creates heat.

## Safety ordering

Automatic restart must never override a hard ORBI preservation decision.

`policy = PAUSE → do not restart inference`

## Phase 0 implementation

The Android watchdog prototype checks `llama-server` process presence and local `/v1/models` reachability, then uses a bounded restart count.

## Current limitation

The shell watchdog does not yet consume the Python thermal/power control plane directly. Until real Node-01 telemetry is integrated, operator testing must stop the watchdog manually if thermal/power safety is in doubt.
