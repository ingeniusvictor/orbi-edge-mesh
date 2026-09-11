#!/usr/bin/env python3
"""Workload-aware scoring modifiers."""

from __future__ import annotations

from models.inventory import ModelRecord
from workloads.profiles import WorkloadProfile


def model_tag_penalty(
    model: ModelRecord,
    profile: WorkloadProfile,
    raw_service: dict,
) -> int:
    preferred = profile.preferred_model_tag
    if preferred is None:
        return 0

    tags = raw_service.get("tags") or []
    return 0 if preferred in tags else 5


def workload_thermal_penalty(
    current_temp: float | None,
    profile: WorkloadProfile,
) -> float:
    if current_temp is None:
        return 3.0

    base = max(0.0, current_temp - 35.0)

    multiplier = {
        "low": 0.5,
        "medium": 1.0,
        "high": 2.0,
    }.get(profile.thermal_sensitivity, 1.0)

    return base * multiplier
