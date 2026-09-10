#!/usr/bin/env python3
"""Build executable request candidates from registered ORBI nodes."""

from __future__ import annotations

from manager.registry import RegisteredNode
from manager.routing_v3 import choose_node_for_request
from models.inventory import find_model


def build_candidate_order(
    nodes: list[RegisteredNode],
    *,
    service_type: str,
    model_id: str | None = None,
    family: str | None = None,
    max_attempts: int = 3,
) -> list[tuple[str, str, str]]:
    excluded: set[str] = set()
    candidates: list[tuple[str, str, str]] = []

    for _ in range(max_attempts):
        node = choose_node_for_request(
            nodes,
            service_type=service_type,
            model_id=model_id,
            family=family,
            excluded_node_ids=excluded,
        )
        if node is None:
            break

        model = find_model(
            node.capability,
            service_type=service_type,
            model_id=model_id,
            family=family,
        )
        if model is None:
            excluded.add(node.node_id)
            continue

        service = None
        for item in node.capability.get("services", []):
            if item.get("type") != service_type:
                continue
            if item.get("model") != model.model_id:
                continue
            service = item
            break

        endpoint = service.get("endpoint") if service else None
        if not endpoint:
            excluded.add(node.node_id)
            continue

        endpoint = str(endpoint).rstrip("/")
        if not endpoint.endswith("/v1/chat/completions"):
            endpoint = endpoint + "/v1/chat/completions"

        candidates.append((node.node_id, endpoint, model.model_id))
        excluded.add(node.node_id)

    return candidates
