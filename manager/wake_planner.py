#!/usr/bin/env python3
"""Plan whether a cold node may be woken for a request."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WakePlan:
    allowed: bool
    action: str
    reason: str


def plan_wake(
    *,
    model_status: str,
    policy_allows_work: bool,
    latency_sensitivity: str,
) -> WakePlan:
    if not policy_allows_work:
        return WakePlan(
            allowed=False,
            action="do_not_wake",
            reason="device preservation policy blocks new work",
        )

    if model_status in {"loaded", "ready"}:
        return WakePlan(
            allowed=True,
            action="use_immediately",
            reason="model is already available",
        )

    if model_status == "cold":
        if latency_sensitivity == "high":
            return WakePlan(
                allowed=True,
                action="wake_if_no_warm_candidate",
                reason="cold start may hurt interactive latency",
            )
        return WakePlan(
            allowed=True,
            action="wake_model",
            reason="cold model may be loaded for this workload",
        )

    return WakePlan(
        allowed=False,
        action="do_not_wake",
        reason=f"model status {model_status} is not executable",
    )
