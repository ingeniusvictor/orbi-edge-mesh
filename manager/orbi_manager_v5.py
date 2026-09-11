#!/usr/bin/env python3
"""ORBI Edge Manager v0.5.

Adds real HTTP request execution with ordered fallback.
"""

from __future__ import annotations

import argparse
import json

from manager.execution import execute_with_fallback
from manager.heartbeat import fetch_capability
from manager.registry import NodeRegistry
from manager.request_planner import build_candidate_order


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("nodes", nargs="+", help="ORBI node base URLs")
    parser.add_argument("--service", default="llm")
    parser.add_argument("--model-id")
    parser.add_argument("--family")
    parser.add_argument(
        "--prompt",
        default="Responde en una frase: ¿qué es ORBI Edge Mesh?",
    )
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--fallback-attempts", type=int, default=3)
    args = parser.parse_args()

    registry = NodeRegistry()

    for url in args.nodes:
        try:
            capability = fetch_capability(url, timeout=3.0)
            node = registry.upsert(url, capability)
            print(f"[REGISTERED] {node.node_id}")
        except Exception as exc:
            print(f"[UNAVAILABLE] {url}: {type(exc).__name__}: {exc}")

    candidates = build_candidate_order(
        registry.all(),
        service_type=args.service,
        model_id=args.model_id,
        family=args.family,
        max_attempts=args.fallback_attempts,
    )

    if not candidates:
        print("[NO ROUTE] No executable candidate")
        return 2

    print("[CANDIDATES]")
    for idx, (node_id, endpoint, model) in enumerate(candidates, start=1):
        print(f"  {idx}. {node_id} model={model} endpoint={endpoint}")

    result = execute_with_fallback(
        candidates,
        messages=[{"role": "user", "content": args.prompt}],
        timeout=args.timeout,
    )

    for attempt in result.attempts:
        state = "PASS" if attempt.ok else "FAIL"
        print(
            f"[ATTEMPT {state}] node={attempt.node_id} "
            f"elapsed={attempt.elapsed_s:.3f}s "
            f"error={attempt.error}"
        )

    if not result.ok:
        print("[EXECUTION FAILED] All candidates failed")
        return 3

    print(f"[EXECUTION PASS] node={result.selected_node_id}")
    print(json.dumps(result.response, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
