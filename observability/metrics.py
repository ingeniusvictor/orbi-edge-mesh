#!/usr/bin/env python3
"""Derive simple scheduler-facing metrics from execution history."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any


def summarize_by_node(events: list[dict[str, Any]]) -> dict[str, dict[str, float | int | None]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[str(event.get("node_id", "unknown"))].append(event)

    summary: dict[str, dict[str, float | int | None]] = {}

    for node_id, rows in grouped.items():
        attempts = len(rows)
        successes = sum(1 for row in rows if row.get("ok") is True)
        failures = attempts - successes

        latencies = [
            float(row["elapsed_s"])
            for row in rows
            if row.get("ok") is True and isinstance(row.get("elapsed_s"), (int, float))
        ]

        temps = [
            float(row["temperature_c"])
            for row in rows
            if isinstance(row.get("temperature_c"), (int, float))
        ]

        summary[node_id] = {
            "attempts": attempts,
            "successes": successes,
            "failures": failures,
            "success_rate": successes / attempts if attempts else None,
            "avg_success_latency_s": mean(latencies) if latencies else None,
            "avg_temperature_c": mean(temps) if temps else None,
        }

    return summary
