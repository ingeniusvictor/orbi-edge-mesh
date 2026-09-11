#!/usr/bin/env python3
"""Lifecycle state model for ORBI Edge nodes."""

from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LifecycleDecision:
    state: str
    action: str
    restart_allowed: bool
    reason: str

def decide_lifecycle(*, process_alive: bool, api_reachable: bool, policy_action: str, restart_count: int, max_restarts: int) -> LifecycleDecision:
    if policy_action == "pause":
        return LifecycleDecision("paused_by_policy", "do_not_restart", False, "hard thermal/power policy pause")
    if process_alive and api_reachable:
        return LifecycleDecision("healthy", "none", False, "process and API are healthy")
    if restart_count >= max_restarts:
        return LifecycleDecision("restart_budget_exhausted", "quarantine", False, "automatic restart budget exhausted")
    if process_alive and not api_reachable:
        return LifecycleDecision("hung_or_starting", "restart_service", True, "process exists but API is unreachable")
    if not process_alive:
        return LifecycleDecision("service_down", "restart_service", True, "service process is not running")
    return LifecycleDecision("unknown", "inspect", False, "unclassified lifecycle state")
