#!/usr/bin/env python3
"""ORBI Edge Manager v0.7.

Adds workload classification and service profiles.
"""

from __future__ import annotations

import argparse
import json

from manager.heartbeat import fetch_capability
from manager.registry import NodeRegistry
from manager.routing_v5 import choose_node_for_workload
from observability.metrics import summarize_by_node
from observability.store import JsonlEventStore
from workloads.classifier import classify_workload
from workloads.profiles import get_profile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("nodes", nargs="+")
    parser.add_argument("--service", default="llm")
    parser.add_argument("--model-id")
    parser.add_argument("--family")
    parser.add_argument("--requested-output-tokens", type=int)
    parser.add_argument(
        "--store",
        default="runtime/observability/execution-events.jsonl",
    )
    args = parser.parse_args()

    workload_type = classify_workload(
        service_type=args.service,
        requested_output_tokens=args.requested_output_tokens,
    )
    profile = get_profile(workload_type)

    registry = NodeRegistry()
    for url in args.nodes:
        try:
            capability = fetch_capability(url, timeout=3.0)
            registry.upsert(url, capability)
        except Exception as exc:
            print(f"[UNAVAILABLE] {url}: {type(exc).__name__}: {exc}")

    store = JsonlEventStore(args.store)
    summary = summarize_by_node(store.read_all())

    print("[WORKLOAD]")
    print(json.dumps(profile.__dict__, ensure_ascii=False, indent=2))

    selected = choose_node_for_workload(
        registry.all(),
        profile=profile,
        history_summary=summary,
        model_id=args.model_id,
        family=args.family,
    )

    if selected is None:
        print("[NO ROUTE]")
        return 2

    print(
        f"[WORKLOAD ROUTE] type={workload_type} "
        f"service={profile.service_type} -> {selected.node_id}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
