#!/usr/bin/env python3
"""ORBI Edge Mesh thermal and power policy v0.1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ThermalDecision:
    state: str
    action: str
    allow_new_work: bool
    thread_scale: float
    reason: str


@dataclass(frozen=True)
class PowerDecision:
    state: str
    action: str
    allow_new_work: bool
    reason: str


@dataclass(frozen=True)
class NodePolicyDecision:
    thermal: ThermalDecision
    power: PowerDecision

    @property
    def allow_new_work(self) -> bool:
        return self.thermal.allow_new_work and self.power.allow_new_work

    @property
    def action(self) -> str:
        priority = {
            "pause": 4,
            "avoid": 3,
            "degrade": 2,
            "normal": 1,
        }
        candidates = [self.thermal.action, self.power.action]
        return max(candidates, key=lambda x: priority.get(x, 0))


def classify_thermal(temp_c: float | None) -> ThermalDecision:
    """Experimental Phase 0 thresholds.

    These are NOT manufacturer limits. They are deliberately conservative
    policy bands to be calibrated with real hardware measurements.
    """
    if temp_c is None:
        return ThermalDecision(
            state="unknown",
            action="degrade",
            allow_new_work=True,
            thread_scale=0.75,
            reason="temperature telemetry unavailable",
        )
    if temp_c < 40.0:
        return ThermalDecision(
            state="normal",
            action="normal",
            allow_new_work=True,
            thread_scale=1.0,
            reason="temperature below experimental warm band",
        )
    if temp_c < 43.0:
        return ThermalDecision(
            state="warm",
            action="degrade",
            allow_new_work=True,
            thread_scale=0.75,
            reason="temperature in experimental warm band",
        )
    if temp_c < 46.0:
        return ThermalDecision(
            state="hot",
            action="avoid",
            allow_new_work=False,
            thread_scale=0.5,
            reason="temperature in experimental hot band",
        )
    if temp_c < 48.0:
        return ThermalDecision(
            state="very_hot",
            action="avoid",
            allow_new_work=False,
            thread_scale=0.25,
            reason="temperature near experimental pause threshold",
        )
    return ThermalDecision(
        state="critical",
        action="pause",
        allow_new_work=False,
        thread_scale=0.0,
        reason="temperature at or above experimental pause threshold",
    )


def classify_power(
    battery_percent: float | None,
    charging: bool | None,
) -> PowerDecision:
    """Conservative Phase 0 power policy."""
    if battery_percent is None:
        return PowerDecision(
            state="unknown",
            action="degrade",
            allow_new_work=True,
            reason="battery telemetry unavailable",
        )

    if battery_percent <= 10:
        return PowerDecision(
            state="critical_battery",
            action="pause",
            allow_new_work=False,
            reason="battery at or below 10%",
        )

    if battery_percent <= 20 and not charging:
        return PowerDecision(
            state="low_battery",
            action="avoid",
            allow_new_work=False,
            reason="battery at or below 20% and not charging",
        )

    if battery_percent <= 30 and not charging:
        return PowerDecision(
            state="reserve",
            action="degrade",
            allow_new_work=True,
            reason="battery in reserve band and not charging",
        )

    return PowerDecision(
        state="normal",
        action="normal",
        allow_new_work=True,
        reason="battery state acceptable",
    )


def evaluate_node_policy(capability: dict[str, Any]) -> NodePolicyDecision:
    health = capability.get("health", {})
    temp = health.get("temperature_c")
    battery = health.get("battery_percent")
    charging = health.get("charging")

    temp_val = float(temp) if isinstance(temp, (int, float)) else None
    battery_val = float(battery) if isinstance(battery, (int, float)) else None
    charging_val = charging if isinstance(charging, bool) else None

    return NodePolicyDecision(
        thermal=classify_thermal(temp_val),
        power=classify_power(battery_val, charging_val),
    )
