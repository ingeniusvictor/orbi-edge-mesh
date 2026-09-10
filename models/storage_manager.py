#!/usr/bin/env python3
"""Local model storage planning for ORBI Edge Mesh."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StoragePolicy:
    min_free_storage_mb: float = 8192.0
    reserve_fraction: float = 0.10


def projected_free_mb(
    *,
    storage_free_mb: float,
    model_size_mb: float,
) -> float:
    return storage_free_mb - model_size_mb


def can_place_model(
    capability: dict[str, Any],
    *,
    model_size_mb: float,
    policy: StoragePolicy = StoragePolicy(),
) -> bool:
    resources = capability.get("resources", {})
    total = resources.get("storage_total_mb")
    free = resources.get("storage_free_mb")

    if not isinstance(total, (int, float)) or not isinstance(free, (int, float)):
        return False

    reserve = max(
        policy.min_free_storage_mb,
        float(total) * policy.reserve_fraction,
    )

    return projected_free_mb(
        storage_free_mb=float(free),
        model_size_mb=model_size_mb,
    ) >= reserve
