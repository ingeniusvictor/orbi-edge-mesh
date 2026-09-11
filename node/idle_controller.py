#!/usr/bin/env python3
"""Simple idle controller for ORBI Edge Mesh."""

from __future__ import annotations

import time
from dataclasses import dataclass

from node.power_state import decide_power_state


@dataclass
class IdleController:
    idle_unload_after_s: float = 300.0
    active_requests: int = 0
    last_request_at: float = 0.0

    def __post_init__(self) -> None:
        if self.last_request_at == 0.0:
            self.last_request_at = time.monotonic()

    def mark_request_start(self) -> None:
        self.active_requests += 1
        self.last_request_at = time.monotonic()

    def mark_request_end(self) -> None:
        self.active_requests = max(0, self.active_requests - 1)
        self.last_request_at = time.monotonic()

    def current_state(self, policy_action: str = "normal"):
        return decide_power_state(
            active_requests=self.active_requests,
            seconds_since_last_request=max(
                0.0,
                time.monotonic() - self.last_request_at,
            ),
            policy_action=policy_action,
            idle_unload_after_s=self.idle_unload_after_s,
        )
