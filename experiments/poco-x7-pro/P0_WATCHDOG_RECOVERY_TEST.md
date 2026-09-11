# P0 — Node-01 Watchdog Recovery Test

Status: NOT STARTED

## Objective

Verify that Node-01 can recover from a stopped/hung inference service while operating headless.

## Test A — Process termination

1. Start the headless server.
2. Start the watchdog.
3. Start the PC fault probe.
4. Manually terminate `llama-server`.
5. Observe temporary failure, watchdog detection, bounded restart and API recovery.

PASS if the API becomes reachable again without turning the display on.

## Test B — Restart budget

1. Configure an intentionally invalid server startup.
2. Start watchdog with `MAX_RESTARTS=3`.
3. Confirm retries are bounded.
4. Confirm watchdog stops/quarantines instead of looping forever.

## Evidence

- initial/final battery
- initial/max/final temperature
- failure detection time
- API recovery time
- restart count
- watchdog logs
- PC probe logs

Do not run deliberate fault tests if the device is already thermally stressed.
