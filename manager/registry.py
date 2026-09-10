#!/usr/bin/env python3
"""ORBI Edge Mesh in-memory node registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class RegisteredNode:
    node_id: str
    base_url: str
    capability: dict[str, Any]
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    consecutive_failures: int = 0

    @property
    def status(self) -> str:
        return str(self.capability.get("health", {}).get("status", "offline"))

    @property
    def temperature(self) -> float | None:
        value = self.capability.get("health", {}).get("temperature_c")
        return float(value) if isinstance(value, (int, float)) else None

    def has_service(self, service_type: str) -> bool:
        for service in self.capability.get("services", []):
            if (
                service.get("type") == service_type
                and service.get("status") == "ready"
            ):
                return True
        return False


class NodeRegistry:
    def __init__(self) -> None:
        self._nodes: dict[str, RegisteredNode] = {}

    def upsert(self, base_url: str, capability: dict[str, Any]) -> RegisteredNode:
        node_id = str(capability["node_id"])
        now = datetime.now(timezone.utc)

        if node_id in self._nodes:
            node = self._nodes[node_id]
            node.base_url = base_url
            node.capability = capability
            node.last_seen = now
            node.consecutive_failures = 0
            return node

        node = RegisteredNode(
            node_id=node_id,
            base_url=base_url,
            capability=capability,
            last_seen=now,
        )
        self._nodes[node_id] = node
        return node

    def mark_failure(self, node_id: str) -> None:
        if node_id in self._nodes:
            self._nodes[node_id].consecutive_failures += 1

    def remove(self, node_id: str) -> None:
        self._nodes.pop(node_id, None)

    def get(self, node_id: str) -> RegisteredNode | None:
        return self._nodes.get(node_id)

    def all(self) -> list[RegisteredNode]:
        return list(self._nodes.values())
