# ORBI Edge Mesh — Headless / Screen-Off Operation v0.1

## Requirement

An ORBI Edge node must be able to provide local AI/server services with the display turned off.

This is a first-class requirement because the display can represent a significant avoidable power draw on a phone used as infrastructure.

## Important distinction

Screen off must NOT mean:

- CPU suspended
- Wi-Fi disconnected
- Termux/runtime killed
- llama-server stopped
- heartbeat unavailable

The desired state is:

```text
DISPLAY OFF
    +
CPU/runtime alive
    +
Wi-Fi alive
    +
local API reachable
    +
thermal/power monitoring alive
```

## Android constraints

Android and vendor power-management layers may:

- enter Doze
- restrict background execution
- kill long-running processes
- restrict Wi-Fi/network activity
- suspend apps considered idle

Therefore screen-off operation requires explicit validation per device.

## Phase 0 strategy

For Termux-based Node-01:

1. run the service in Termux;
2. acquire a partial wake lock while the node is serving;
3. configure Android battery optimization so the Termux process is not aggressively killed;
4. lock/turn off the display;
5. verify API reachability from the PC;
6. run a sustained test;
7. measure battery/temperature impact.

## Wake lock

Termux provides:

```bash
termux-wake-lock
```

to request that the CPU remain awake while the display can be off.

Release it with:

```bash
termux-wake-unlock
```

Wake locks must not be held unnecessarily.

## Certification requirement

Node-01 is not considered server-ready until it passes a screen-off test:

- screen off for at least 30 minutes;
- local API remains reachable;
- heartbeat remains available;
- model inference still works;
- process is not killed by Android;
- no unsafe thermal behavior;
- battery consumption is recorded.

## Device-specific validation

POCO/Xiaomi battery-management settings must be checked manually because behavior may vary by HyperOS/Android version.

No assumption should be made that a configuration proven on Node-01 automatically works on Node-02 or Node-03.
