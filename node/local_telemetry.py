#!/usr/bin/env python3
"""Minimal local telemetry reader for Android/Termux experiments."""

from __future__ import annotations

import glob
from pathlib import Path
from typing import Any


def _read_number(path: str) -> float | None:
    try:
        raw = Path(path).read_text(encoding="utf-8").strip()
        value = float(raw)
        if value > 1000:
            value = value / 1000.0
        return value
    except Exception:
        return None


def read_thermal_candidates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for zone in glob.glob("/sys/class/thermal/thermal_zone*"):
        temp = _read_number(f"{zone}/temp")
        try:
            kind = Path(f"{zone}/type").read_text(
                encoding="utf-8"
            ).strip()
        except Exception:
            kind = "unknown"

        rows.append({
            "zone": zone,
            "type": kind,
            "temperature_c": temp,
        })

    return rows


def select_conservative_temperature(
    rows: list[dict[str, Any]],
) -> float | None:
    values = [
        float(row["temperature_c"])
        for row in rows
        if isinstance(row.get("temperature_c"), (int, float))
        and -20.0 < float(row["temperature_c"]) < 120.0
    ]
    return max(values) if values else None


def read_battery_capacity() -> float | None:
    candidates = [
        "/sys/class/power_supply/battery/capacity",
        "/sys/class/power_supply/Battery/capacity",
    ]
    for path in candidates:
        value = _read_number(path)
        if value is not None:
            return value
    return None


def read_charging_state() -> bool | None:
    candidates = [
        "/sys/class/power_supply/battery/status",
        "/sys/class/power_supply/Battery/status",
    ]
    for path in candidates:
        try:
            status = Path(path).read_text(encoding="utf-8").strip().lower()
        except Exception:
            continue

        if status in {"charging", "full"}:
            return True
        if status in {"discharging", "not charging"}:
            return False

    return None


def build_health_snapshot() -> dict[str, Any]:
    thermal_rows = read_thermal_candidates()
    return {
        "status": "ready",
        "temperature_c": select_conservative_temperature(thermal_rows),
        "battery_percent": read_battery_capacity(),
        "charging": read_charging_state(),
        "thermal_sources": thermal_rows,
    }
