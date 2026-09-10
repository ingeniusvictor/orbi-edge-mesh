#!/usr/bin/env python3
"""Minimal ORBI Edge Manager.

Phase 0 registry and routing-policy prototype.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


@dataclass
class Node:
    base_url: str
    capability: dict[str, Any]

    @property
    def node_id(self) -> str:
        return str(self.capability.get("node_id", "unknown"))

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


def fetch_node(base_url: str, timeout: float = 5.0) -> Node:
    url = base_url.rstrip("/") + "/orbi/v1/node"
    with urlopen(url, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP status: {response.status}")
        payload = json.loads(response.read().decode("utf-8"))
    return Node(base_url=base_url.rstrip("/"), capability=payload)


def score_node(node: Node, service_type: str) -> tuple[int, float, str]:
    """Lower tuple wins.

    Phase 0 policy:
    - must expose requested service
    - ready beats busy/degraded
    - cooler known temperature preferred
    - stable node_id tie-break for deterministic results
    """
    if not node.has_service(service_type):
        return (99, 999.0, node.node_id)

    status_rank = {
        "ready": 0,
        "busy": 1,
        "degraded": 2,
        "paused": 3,
        "offline": 4,
    }.get(node.status, 5)

    temp = node.temperature if node.temperature is not None else 100.0
    return (status_rank, temp, node.node_id)


def choose_node(nodes: list[Node], service_type: str) -> Node | None:
    eligible = [n for n in nodes if n.has_service(service_type)]
    if not eligible:
        return None
    return min(eligible, key=lambda n: score_node(n, service_type))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "nodes",
        nargs="+",
        help="Node base URLs, e.g. http://127.0.0.1:8787",
    )
    parser.add_argument("--service", default="llm")
    args = parser.parse_args()

    discovered: list[Node] = []

    for url in args.nodes:
        try:
            node = fetch_node(url)
            discovered.append(node)
            print(
                f"[REGISTERED] {node.node_id} "
                f"status={node.status} "
                f"temp={node.temperature}"
            )
        except (HTTPError, URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as exc:
            print(f"[UNAVAILABLE] {url}: {exc}")

    selected = choose_node(discovered, args.service)
    if selected is None:
        print(f"[NO ROUTE] No node available for service={args.service}")
        return 2

    print(
        f"[ROUTE] service={args.service} -> "
        f"{selected.node_id} ({selected.base_url})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
