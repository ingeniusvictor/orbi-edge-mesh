#!/usr/bin/env python3
"""Historical-performance scoring for ORBI Edge Mesh."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AdaptiveScore:
    reliability_penalty: float
    latency_penalty: float
    thermal_penalty: float
    sample_penalty: float

    @property
    def total(self) -> float:
        return (
            self.reliability_penalty
            + self.latency_penalty
            + self.thermal_penalty
            + self.sample_penalty
        )


def score_history(
    node_id: str,
    summary: dict[str, dict[str, Any]],
    *,
    min_samples: int = 3,
) -> AdaptiveScore:
    """Lower score is better.

    The weights are intentionally simple and conservative for Phase 0.
    A lack of history must not make a node look artificially perfect.
    """
    row = summary.get(node_id)
    if not row:
        return AdaptiveScore(
            reliability_penalty=20.0,
            latency_penalty=5.0,
            thermal_penalty=5.0,
            sample_penalty=15.0,
        )

    attempts = int(row.get("attempts") or 0)
    success_rate = row.get("success_rate")
    latency = row.get("avg_success_latency_s")
    avg_temp = row.get("avg_temperature_c")

    reliability_penalty = 20.0
    if isinstance(success_rate, (int, float)):
        reliability_penalty = max(0.0, (1.0 - float(success_rate)) * 100.0)

    latency_penalty = 5.0
    if isinstance(latency, (int, float)):
        latency_penalty = max(0.0, float(latency) * 2.0)

    thermal_penalty = 5.0
    if isinstance(avg_temp, (int, float)):
        thermal_penalty = max(0.0, float(avg_temp) - 35.0)

    sample_penalty = 0.0
    if attempts < min_samples:
        sample_penalty = float((min_samples - attempts) * 5)

    return AdaptiveScore(
        reliability_penalty=reliability_penalty,
        latency_penalty=latency_penalty,
        thermal_penalty=thermal_penalty,
        sample_penalty=sample_penalty,
    )
