#!/usr/bin/env python3
"""ORBI Edge Mesh observability event model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ExecutionEvent:
    schema_version: str
    timestamp: str
    request_id: str
    node_id: str
    service_type: str
    model_id: str
    ok: bool
    elapsed_s: float
    error: str | None
    temperature_c: float | None
    battery_percent: float | None
    charging: bool | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
