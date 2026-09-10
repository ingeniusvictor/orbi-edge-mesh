#!/usr/bin/env python3
"""Model inventory helpers for ORBI Edge Mesh."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelRecord:
    model_id: str
    family: str
    service_type: str
    runtime: str
    status: str
    quantization: str | None = None
    size_bytes: int | None = None
    context_max: int | None = None

    @property
    def locality_rank(self) -> int:
        return {
            "loaded": 0,
            "ready": 1,
            "cold": 2,
            "disabled": 98,
            "missing": 99,
        }.get(self.status, 97)


def parse_models(capability: dict[str, Any]) -> list[ModelRecord]:
    records: list[ModelRecord] = []

    for service in capability.get("services", []):
        model = service.get("model")
        if not model:
            continue

        records.append(
            ModelRecord(
                model_id=str(model),
                family=str(service.get("family") or model),
                service_type=str(service.get("type") or "other"),
                runtime=str(service.get("runtime") or capability.get("runtime", {}).get("kind") or "unknown"),
                status=str(service.get("model_status") or service.get("status") or "ready"),
                quantization=service.get("quantization"),
                size_bytes=service.get("size_bytes"),
                context_max=service.get("context_max"),
            )
        )

    return records


def find_model(
    capability: dict[str, Any],
    *,
    service_type: str,
    model_id: str | None = None,
    family: str | None = None,
) -> ModelRecord | None:
    candidates = [
        record
        for record in parse_models(capability)
        if record.service_type == service_type
    ]

    if model_id is not None:
        candidates = [r for r in candidates if r.model_id == model_id]

    if family is not None:
        candidates = [r for r in candidates if r.family == family]

    if not candidates:
        return None

    return min(candidates, key=lambda r: (r.locality_rank, r.model_id))
