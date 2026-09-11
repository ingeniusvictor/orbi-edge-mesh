#!/usr/bin/env python3
"""Exit-code bridge for Android watchdog recovery authorization."""

from __future__ import annotations

import json

from node.local_telemetry import build_health_snapshot
from node.policy_gate import authorize_recovery


def main() -> int:
    health = build_health_snapshot()
    capability = {"health": health}
    authorization = authorize_recovery(capability)

    print(json.dumps({
        "allowed": authorization.allowed,
        "action": authorization.action,
        "reason": authorization.reason,
        "health": health,
    }, ensure_ascii=False))

    return 0 if authorization.allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
