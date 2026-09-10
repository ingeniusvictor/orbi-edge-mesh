#!/usr/bin/env python3
"""Unified ORBI Edge Mesh Phase 0 manager.

This entrypoint composes the current Phase 0 building blocks:
- heartbeat / registry
- thermal + power policy
- model locality
- workload classification
- adaptive history
- executable candidate planning
- request execution with fallback
- local observability
"""

from __future__ import annotations

import argparse
import json

from manager.execution_v2 import execute_with_observability
from manager.heartbeat import fetch_capability
from manager.registry import NodeRegistry
from manager.routing_v5 import choose_node_for_workload
from models.inventory import find_model
from observability.metrics import summarize_by_node
from observability.store import JsonlEventStore
from workloads.classifier import classify_workload
from workloads.profiles import get_profile


def build_candidate_order(
    registry: NodeRegistry,
    *,
    profile,
    history_summary: dict,
    model_id: str | None,
    family: str | None,
    max_attempts: int,
) -> list[tuple[str, str, str]]:
    excluded: set[str] = set()
    candidates: list[tuple[str, str, str]] = []

    for _ in range(max_attempts):
        node = choose_node_for_workload(
            registry.all(),
            profile=profile,
            history_summary=history_summary,
            model_id=model_id,
            family=family,
            excluded_node_ids=excluded,
        )
        if node is None:
            break

        model = find_model(
            node.capability,
            service_type=profile.service_type,
            model_id=model_id,
            family=family,
        )
        if model is None:
            excluded.add(node.node_id)
            continue

        service = next((
            s for s in node.capability.get("services", [])
            if s.get("type") == profile.service_type
            and s.get("model") == model.model_id
        ), None)

        endpoint = service.get("endpoint") if service else None
        if not endpoint:
            excluded.add(node.node_id)
            continue

        endpoint = str(endpoint).rstrip("/")
        if profile.service_type == "llm" and not endpoint.endswith("/v1/chat/completions"):
            endpoint += "/v1/chat/completions"

        candidates.append((node.node_id, endpoint, model.model_id))
        excluded.add(node.node_id)

    return candidates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("nodes", nargs="+", help="ORBI node base URLs")
    parser.add_argument("--service", default="llm")
    parser.add_argument("--model-id")
    parser.add_argument("--family")
    parser.add_argument("--requested-output-tokens", type=int, default=128)
    parser.add_argument("--prompt", default="Responde brevemente: ¿qué es ORBI Edge Mesh?")
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--fallback-attempts", type=int, default=3)
    parser.add_argument("--store", default="runtime/observability/execution-events.jsonl")
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
            node = registry.upsert(url, capability)
            print(f"[REGISTERED] {node.node_id}")
        except Exception as exc:
            print(f"[UNAVAILABLE] {url}: {type(exc).__name__}: {exc}")

    store = JsonlEventStore(args.store)
    history_summary = summarize_by_node(store.read_all())

    candidates = build_candidate_order(
        registry,
        profile=profile,
        history_summary=history_summary,
        model_id=args.model_id,
        family=args.family,
        max_attempts=args.fallback_attempts,
    )

    print("[WORKLOAD]")
    print(json.dumps(profile.__dict__, ensure_ascii=False, indent=2))

    if not candidates:
        print("[NO ROUTE] no executable candidate")
        return 2

    print("[CANDIDATES]")
    for i, (node_id, endpoint, model) in enumerate(candidates, start=1):
        print(f"  {i}. {node_id} model={model} endpoint={endpoint}")

    if profile.service_type != "llm":
        print("[NOT EXECUTED] Phase 0 unified executor currently executes LLM requests only")
        return 0

    capabilities_by_node = {
        node.node_id: node.capability
        for node in registry.all()
    }

    result = execute_with_observability(
        candidates,
        service_type=profile.service_type,
        messages=[{"role": "user", "content": args.prompt}],
        capabilities_by_node=capabilities_by_node,
        store=store,
        timeout=args.timeout,
    )

    for attempt in result.attempts:
        state = "PASS" if attempt.ok else "FAIL"
        print(f"[ATTEMPT {state}] node={attempt.node_id} error={attempt.error}")

    if not result.ok:
        print("[EXECUTION FAILED] all candidates failed")
        return 3

    print(f"[EXECUTION PASS] node={result.selected_node_id}")
    print(json.dumps(result.response, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
