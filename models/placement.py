#!/usr/bin/env python3
"""Model placement helpers for ORBI Edge Mesh."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlacementDecision:
    node_id: str
    model_id: str
    action: str
    reason: str


def free_storage_mb(capability: dict[str, Any]) -> float | None:
    resources = capability.get("resources", {})
    value = resources.get("storage_free_mb")
    return float(value) if isinstance(value, (int, float)) else None


def physical_ram_mb(capability: dict[str, Any]) -> float | None:
    resources = capability.get("resources", {})
    value = resources.get("physical_ram_mb")
    return float(value) if isinstance(value, (int, float)) else None


def node_has_model(capability: dict[str, Any], model_id: str) -> bool:
    return any(
        service.get("model") == model_id
        for service in capability.get("services", [])
    )


def choose_storage_node(
    nodes: list[dict[str, Any]],
    *,
    model_id: str,
    model_size_mb: float,
    min_free_after_mb: float = 8192.0,
) -> PlacementDecision | None:
    candidates = []

    for capability in nodes:
        node_id = str(capability.get("node_id", "unknown"))
        free_mb = free_storage_mb(capability)

        if free_mb is None:
            continue

        if node_has_model(capability, model_id):
            return PlacementDecision(
                node_id=node_id,
                model_id=model_id,
                action="keep_existing",
                reason="model already present on node",
            )

        free_after = free_mb - model_size_mb
        if free_after < min_free_after_mb:
            continue

        ram_mb = physical_ram_mb(capability) or 0.0
        candidates.append((free_after, ram_mb, node_id, capability))

    if not candidates:
        return None

    free_after, ram_mb, node_id, _ = max(candidates)
    return PlacementDecision(
        node_id=node_id,
        model_id=model_id,
        action="place",
        reason=(
            f"best storage headroom; projected free={free_after:.0f} MB, "
            f"physical RAM={ram_mb:.0f} MB"
        ),
    )
