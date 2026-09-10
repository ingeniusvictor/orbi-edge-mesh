#!/usr/bin/env python3
"""ORBI Edge Manager v0.4.

Adds model-locality-aware routing to heartbeat, registry,
thermal/power policy and fallback.
"""

from __future__ import annotations

import argparse

from manager.orbi_manager_v3 import (
    evict_stale,
    print_policy_snapshot,
    refresh_registry,
)
from manager.registry import NodeRegistry
from manager.routing_v3 import choose_node_for_request
from models.inventory import find_model


def route_order(
    registry: NodeRegistry,
    *,
    service: str,
    model_id: str | None,
    family: str | None,
    max_attempts: int,
) -> list[str]:
    attempted: set[str] = set()
    order: list[str] = []

    for _ in range(max_attempts):
        node = choose_node_for_request(
            registry.all(),
            service_type=service,
            model_id=model_id,
            family=family,
            excluded_node_ids=attempted,
        )
        if node is None:
            break

        model = find_model(
            node.capability,
            service_type=service,
            model_id=model_id,
            family=family,
        )
        model_label = model.model_id if model else "unknown"
        order.append(f"{node.node_id}:{model_label}")
        attempted.add(node.node_id)

    return order


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("nodes", nargs="+", help="Known node base URLs")
    parser.add_argument("--service", default="llm")
    parser.add_argument("--model-id")
    parser.add_argument("--family")
    parser.add_argument("--heartbeat-seconds", type=float, default=5.0)
    parser.add_argument("--ttl-seconds", type=float, default=15.0)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--cycles", type=int, default=1)
    parser.add_argument("--fallback-attempts", type=int, default=3)
    args = parser.parse_args()

    registry = NodeRegistry()

    for cycle in range(1, args.cycles + 1):
        print(f"\n=== Cycle {cycle}/{args.cycles} ===")
        refresh_registry(registry, args.nodes, args.timeout)
        evict_stale(registry, args.ttl_seconds)
        print_policy_snapshot(registry)

        order = route_order(
            registry,
            service=args.service,
            model_id=args.model_id,
            family=args.family,
            max_attempts=args.fallback_attempts,
        )

        request_desc = f"service={args.service}"
        if args.model_id:
            request_desc += f" model={args.model_id}"
        if args.family:
            request_desc += f" family={args.family}"

        if order:
            print(f"[ROUTE ORDER] {request_desc} -> " + " -> ".join(order))
        else:
            print(f"[NO ROUTE] {request_desc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
