#!/usr/bin/env python3
"""Adaptive, locality-aware, policy-aware ORBI routing."""

from __future__ import annotations

from typing import Any

from manager.adaptive_scoring import score_history
from manager.registry import RegisteredNode
from models.inventory import find_model
from policy.thermal_power import evaluate_node_policy


STATUS_RANK = {
    "ready": 0,
    "busy": 1,
    "degraded": 2,
    "paused": 3,
    "offline": 4,
}


def score_node_adaptive(
    node: RegisteredNode,
    *,
    service_type: str,
    history_summary: dict[str, dict[str, Any]],
    model_id: str | None = None,
    family: str | None = None,
) -> tuple[int, int, float, float, int, float, str]:
    model = find_model(
        node.capability,
        service_type=service_type,
        model_id=model_id,
        family=family,
    )
    if model is None:
        return (99, 99, 9999.0, 9999.0, 99, 999.0, node.node_id)

    policy = evaluate_node_policy(node.capability)
    if not policy.allow_new_work:
        return (98, 98, 9998.0, 9998.0, 98, 998.0, node.node_id)

    status_rank = STATUS_RANK.get(node.status, 5)
    policy_rank = {
        "normal": 0,
        "degrade": 1,
        "avoid": 2,
        "pause": 3,
    }.get(policy.action, 4)

    adaptive = score_history(node.node_id, history_summary)
    temp = node.temperature if node.temperature is not None else 100.0

    return (
        model.locality_rank,
        status_rank,
        float(policy_rank),
        adaptive.total,
        node.consecutive_failures,
        temp,
        node.node_id,
    )


def choose_node_adaptive(
    nodes: list[RegisteredNode],
    *,
    service_type: str,
    history_summary: dict[str, dict[str, Any]],
    model_id: str | None = None,
    family: str | None = None,
    excluded_node_ids: set[str] | None = None,
) -> RegisteredNode | None:
    excluded = excluded_node_ids or set()
    eligible: list[RegisteredNode] = []

    for node in nodes:
        if node.node_id in excluded:
            continue

        model = find_model(
            node.capability,
            service_type=service_type,
            model_id=model_id,
            family=family,
        )
        if model is None or model.locality_rank >= 98:
            continue

        policy = evaluate_node_policy(node.capability)
        if not policy.allow_new_work:
            continue

        eligible.append(node)

    if not eligible:
        return None

    return min(
        eligible,
        key=lambda node: score_node_adaptive(
            node,
            service_type=service_type,
            history_summary=history_summary,
            model_id=model_id,
            family=family,
        ),
    )
