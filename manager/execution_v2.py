#!/usr/bin/env python3
"""Request execution with fallback and observability hooks."""

from __future__ import annotations

import uuid
from typing import Any

from manager.execution import execute_with_fallback
from observability.events import ExecutionEvent, utc_now_iso
from observability.store import JsonlEventStore


def _health_lookup(
    capabilities_by_node: dict[str, dict[str, Any]],
    node_id: str,
) -> tuple[float | None, float | None, bool | None]:
    health = capabilities_by_node.get(node_id, {}).get("health", {})

    temp = health.get("temperature_c")
    battery = health.get("battery_percent")
    charging = health.get("charging")

    return (
        float(temp) if isinstance(temp, (int, float)) else None,
        float(battery) if isinstance(battery, (int, float)) else None,
        charging if isinstance(charging, bool) else None,
    )


def execute_with_observability(
    candidates: list[tuple[str, str, str]],
    *,
    service_type: str,
    messages: list[dict[str, str]],
    capabilities_by_node: dict[str, dict[str, Any]],
    store: JsonlEventStore,
    timeout: float = 60.0,
    temperature: float = 0.2,
    request_id: str | None = None,
):
    request_id = request_id or str(uuid.uuid4())

    result = execute_with_fallback(
        candidates,
        messages=messages,
        timeout=timeout,
        temperature=temperature,
    )

    for attempt in result.attempts:
        model_id = "unknown"
        for candidate_node, _endpoint, candidate_model in candidates:
            if candidate_node == attempt.node_id:
                model_id = candidate_model
                break

        temp_c, battery, charging = _health_lookup(
            capabilities_by_node,
            attempt.node_id,
        )

        event = ExecutionEvent(
            schema_version="0.1",
            timestamp=utc_now_iso(),
            request_id=request_id,
            node_id=attempt.node_id,
            service_type=service_type,
            model_id=model_id,
            ok=attempt.ok,
            elapsed_s=attempt.elapsed_s,
            error=attempt.error,
            temperature_c=temp_c,
            battery_percent=battery,
            charging=charging,
        )
        store.append(event.to_dict())

    return result
