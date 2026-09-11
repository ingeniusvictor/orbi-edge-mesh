#!/usr/bin/env python3
"""ORBI Edge node power-state model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PowerStateDecision:
    state: str
    keep_api_alive: bool
    keep_model_loaded: bool
    allow_wake: bool
    reason: str


def decide_power_state(
    *,
    active_requests: int,
    seconds_since_last_request: float,
    policy_action: str,
    idle_unload_after_s: float = 300.0,
) -> PowerStateDecision:
    if policy_action == "pause":
        return PowerStateDecision(
            state="protected_pause",
            keep_api_alive=True,
            keep_model_loaded=False,
            allow_wake=False,
            reason="thermal/power policy requires pause",
        )

    if active_requests > 0:
        return PowerStateDecision(
            state="active",
            keep_api_alive=True,
            keep_model_loaded=True,
            allow_wake=True,
            reason="request currently executing",
        )

    if seconds_since_last_request >= idle_unload_after_s:
        return PowerStateDecision(
            state="idle_cold",
            keep_api_alive=True,
            keep_model_loaded=False,
            allow_wake=True,
            reason="idle timeout reached; model may unload",
        )

    return PowerStateDecision(
        state="idle_warm",
        keep_api_alive=True,
        keep_model_loaded=True,
        allow_wake=True,
        reason="recent activity; keep model warm",
    )
