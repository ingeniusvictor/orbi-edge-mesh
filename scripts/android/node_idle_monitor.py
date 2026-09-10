#!/usr/bin/env python3
"""Experimental local idle-state monitor."""

from __future__ import annotations

import argparse
import json
import time

from node.power_state import decide_power_state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idle-seconds", type=float, required=True)
    parser.add_argument("--active-requests", type=int, default=0)
    parser.add_argument("--policy-action", default="normal")
    parser.add_argument("--unload-after", type=float, default=300.0)
    args = parser.parse_args()

    decision = decide_power_state(
        active_requests=args.active_requests,
        seconds_since_last_request=args.idle_seconds,
        policy_action=args.policy_action,
        idle_unload_after_s=args.unload_after,
    )

    print(json.dumps(decision.__dict__, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
