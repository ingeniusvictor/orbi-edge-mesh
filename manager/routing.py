#!/usr/bin/env python3
"""ORBI Edge Mesh routing policy."""

from __future__ import annotations

from .registry import RegisteredNode


STATUS_RANK = {
    "ready": 0,
    "busy": 1,
    "degraded": 2,
    "paused": 3,
    "offline": 4,
}


def score_node(node: RegisteredNode, service_type: str) -> tuple[int, int, float, str]:
    """Lower tuple wins.

    Ordering:
    1. requested service must be available;
    2. healthier state wins;
    3. fewer consecutive failures wins;
    4. lower known temperature wins;
    5. node_id breaks ties deterministically.
    """
    if not node.has_service(service_type):
        return (99, 99, 999.0, node.node_id)

    status_rank = STATUS_RANK.get(node.status, 5)
    temp = node.temperature if node.temperature is not None else 100.0
    return (
        status_rank,
        node.consecutive_failures,
        temp,
        node.node_id,
    )


def choose_node(
    nodes: list[RegisteredNode],
    service_type: str,
    excluded_node_ids: set[str] | None = None,
) -> RegisteredNode | None:
    excluded = excluded_node_ids or set()
    eligible = [
        node
        for node in nodes
        if node.node_id not in excluded and node.has_service(service_type)
    ]
    if not eligible:
        return None
    return min(eligible, key=lambda n: score_node(n, service_type))
