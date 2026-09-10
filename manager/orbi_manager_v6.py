#!/usr/bin/env python3
"""ORBI Edge Manager v0.6.

Adds adaptive routing from local execution history.
"""

from __future__ import annotations

import argparse
import json

from manager.heartbeat import fetch_capability
from manager.registry import NodeRegistry
from manager.routing_v4 import choose_node_adaptive
from models.inventory import find_model
from observability.metrics import summarize_by_node
from observability.store import JsonlEventStore


def build_adaptive_order(
    registry: NodeRegistry,
    *,
    service: str,
    history_summary: dict,
    model_id: str | None,
    family: str | None,
    max_attempts: int,
) -> list[str]:
    excluded: set[str] = set()
    order: list[str] = []

    for _ in range(max_attempts):
        node = choose_node_adaptive(
            registry.all(),
            service_type=service,
            history_summary=history_summary,
            model_id=model_id,
            family=family,
            excluded_node_ids=excluded,
        )
        if node is None:
            break

        model = find_model(
            node.capability,
            service_type=service,
            model_id=model_id,
            family=family,
        )
        order.append(f"{node.node_id}:{model.model_id if model else 'unknown'}")
        excluded.add(node.node_id)

    return order


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("nodes", nargs="+")
    parser.add_argument("--service", default="llm")
    parser.add_argument("--model-id")
    parser.add_argument("--family")
    parser.add_argument("--fallback-attempts", type=int, default=3)
    parser.add_argument(
        "--store",
        default="runtime/observability/execution-events.jsonl",
    )
    args = parser.parse_args()

    registry = NodeRegistry()

    for url in args.nodes:
        try:
            capability = fetch_capability(url, timeout=3.0)
            registry.upsert(url, capability)
        except Exception as exc:
            print(f"[UNAVAILABLE] {url}: {type(exc).__name__}: {exc}")

    store = JsonlEventStore(args.store)
    summary = summarize_by_node(store.read_all())

    print("[HISTORY SUMMARY]")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

    order = build_adaptive_order(
        registry,
        service=args.service,
        history_summary=summary,
        model_id=args.model_id,
        family=args.family,
        max_attempts=args.fallback_attempts,
    )

    if not order:
        print("[NO ROUTE]")
        return 2

    print("[ADAPTIVE ROUTE] " + " -> ".join(order))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
