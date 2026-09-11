#!/usr/bin/env python3
"""Thermal/power-aware ORBI Edge routing policy."""

from __future__ import annotations

from manager.registry import RegisteredNode
from policy.thermal_power import evaluate_node_policy


STATUS_RANK = {
    "ready": 0,
    "busy": 1,
    "degraded": 2,
    "paused": 3,
    "offline": 4,
}


def score_node(
    node: RegisteredNode,
    service_type: str,
) -> tuple[int, int, int, float, str]:
    if not node.has_service(service_type):
        return (99, 99, 99, 999.0, node.node_id)

    policy = evaluate_node_policy(node.capability)
    if not policy.allow_new_work:
        return (98, 98, 98, 998.0, node.node_id)

    status_rank = STATUS_RANK.get(node.status, 5)
    action_rank = {
        "normal": 0,
        "degrade": 1,
        "avoid": 2,
        "pause": 3,
    }.get(policy.action, 4)
    temp = node.temperature if node.temperature is not None else 100.0

    return (
        status_rank,
        action_rank,
        node.consecutive_failures,
        temp,
        node.node_id,
    )


def choose_node_policy_aware(
    nodes: list[RegisteredNode],
    service_type: str,
    excluded_node_ids: set[str] | None = None,
) -> RegisteredNode | None:
    excluded = excluded_node_ids or set()
    eligible = []

    for node in nodes:
        if node.node_id in excluded:
            continue
        if not node.has_service(service_type):
            continue
        decision = evaluate_node_policy(node.capability)
        if not decision.allow_new_work:
            continue
        eligible.append(node)

    if not eligible:
        return None

    return min(eligible, key=lambda n: score_node(n, service_type))
