#!/usr/bin/env python3
"""Workload-aware adaptive routing."""

from __future__ import annotations

from typing import Any

from manager.adaptive_scoring import score_history
from manager.registry import RegisteredNode
from manager.workload_scoring import (
    model_tag_penalty,
    workload_thermal_penalty,
)
from models.inventory import find_model
from policy.thermal_power import evaluate_node_policy
from workloads.profiles import WorkloadProfile


STATUS_RANK = {
    "ready": 0,
    "busy": 1,
    "degraded": 2,
    "paused": 3,
    "offline": 4,
}


def _service_record(node: RegisteredNode, model_id: str, service_type: str) -> dict:
    for service in node.capability.get("services", []):
        if (
            service.get("type") == service_type
            and service.get("model") == model_id
        ):
            return service
    return {}


def score_node_for_workload(
    node: RegisteredNode,
    *,
    profile: WorkloadProfile,
    history_summary: dict[str, dict[str, Any]],
    model_id: str | None = None,
    family: str | None = None,
) -> tuple[int, int, int, float, float, int, float, str]:
    model = find_model(
        node.capability,
        service_type=profile.service_type,
        model_id=model_id,
        family=family,
    )
    if model is None:
        return (99, 99, 99, 9999.0, 9999.0, 99, 999.0, node.node_id)

    policy = evaluate_node_policy(node.capability)
    if not policy.allow_new_work:
        return (98, 98, 98, 9998.0, 9998.0, 98, 998.0, node.node_id)

    service = _service_record(node, model.model_id, profile.service_type)
    tag_penalty = model_tag_penalty(model, profile, service)

    adaptive = score_history(node.node_id, history_summary)
    temp_penalty = workload_thermal_penalty(node.temperature, profile)

    status_rank = STATUS_RANK.get(node.status, 5)
    policy_rank = {
        "normal": 0,
        "degrade": 1,
        "avoid": 2,
        "pause": 3,
    }.get(policy.action, 4)

    return (
        model.locality_rank,
        status_rank,
        policy_rank,
        adaptive.total,
        temp_penalty + float(tag_penalty),
        node.consecutive_failures,
        node.temperature if node.temperature is not None else 100.0,
        node.node_id,
    )


def choose_node_for_workload(
    nodes: list[RegisteredNode],
    *,
    profile: WorkloadProfile,
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
            service_type=profile.service_type,
            model_id=model_id,
            family=family,
        )
        if model is None or model.locality_rank >= 98:
            continue

        if not evaluate_node_policy(node.capability).allow_new_work:
            continue

        eligible.append(node)

    if not eligible:
        return None

    return min(
        eligible,
        key=lambda node: score_node_for_workload(
            node,
            profile=profile,
            history_summary=history_summary,
            model_id=model_id,
            family=family,
        ),
    )
