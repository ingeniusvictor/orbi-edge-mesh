#!/usr/bin/env python3
"""Experimental history-aware score modifiers."""

from __future__ import annotations

from typing import Any


def history_penalty(
    node_id: str,
    summary: dict[str, dict[str, Any]],
) -> tuple[int, float]:
    """Return failure and latency penalties.

    Lower is better.
    This is deliberately simple and remains experimental.
    """
    row = summary.get(node_id)
    if not row:
        return (0, 0.0)

    failures = int(row.get("failures") or 0)
    latency = row.get("avg_success_latency_s")
    latency_penalty = float(latency) if isinstance(latency, (int, float)) else 0.0

    return (failures, latency_penalty)
