#!/usr/bin/env python3
"""ORBI Edge Manager v0.3.

Adds policy-aware routing on top of:
- heartbeat refresh
- in-memory registry
- stale eviction
- deterministic fallback

The manager never bypasses thermal/power policy blocks.
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError

from manager.heartbeat import fetch_capability
from manager.registry import NodeRegistry
from manager.routing_v2 import choose_node_policy_aware
from policy.thermal_power import evaluate_node_policy


def seconds_since(dt: datetime) -> float:
    return (datetime.now(timezone.utc) - dt).total_seconds()


def refresh_registry(
    registry: NodeRegistry,
    urls: list[str],
    timeout: float,
) -> None:
    for url in urls:
        try:
            capability = fetch_capability(url, timeout=timeout)
            node = registry.upsert(url, capability)
            decision = evaluate_node_policy(node.capability)

            print(
                f"[HEARTBEAT PASS] {node.node_id} "
                f"status={node.status} "
                f"temp={node.temperature} "
                f"policy={decision.action} "
                f"eligible={decision.allow_new_work}"
            )
        except (HTTPError, URLError, TimeoutError, RuntimeError, ValueError) as exc:
            print(f"[HEARTBEAT FAIL] {url}: {exc}")
            for node in registry.all():
                if node.base_url.rstrip("/") == url.rstrip("/"):
                    registry.mark_failure(node.node_id)


def evict_stale(registry: NodeRegistry, ttl_seconds: float) -> None:
    for node in list(registry.all()):
        age = seconds_since(node.last_seen)
        if age > ttl_seconds:
            print(f"[EVICT] {node.node_id} stale for {age:.1f}s")
            registry.remove(node.node_id)


def route_order(
    registry: NodeRegistry,
    service: str,
    max_attempts: int,
) -> list[str]:
    attempted: set[str] = set()
    order: list[str] = []

    for _ in range(max_attempts):
        node = choose_node_policy_aware(
            registry.all(),
            service,
            excluded_node_ids=attempted,
        )
        if node is None:
            break
        order.append(node.node_id)
        attempted.add(node.node_id)

    return order


def print_policy_snapshot(registry: NodeRegistry) -> None:
    if not registry.all():
        print("[POLICY] no registered nodes")
        return

    for node in sorted(registry.all(), key=lambda n: n.node_id):
        decision = evaluate_node_policy(node.capability)
        print(
            f"[POLICY] {node.node_id} "
            f"thermal={decision.thermal.state}/{decision.thermal.action} "
            f"power={decision.power.state}/{decision.power.action} "
            f"final={decision.action} "
            f"allow_new_work={decision.allow_new_work}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("nodes", nargs="+", help="Known node base URLs")
    parser.add_argument("--service", default="llm")
    parser.add_argument("--heartbeat-seconds", type=float, default=5.0)
    parser.add_argument("--ttl-seconds", type=float, default=15.0)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--cycles", type=int, default=3)
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
            args.service,
            args.fallback_attempts,
        )

        if order:
            print(
                f"[ROUTE ORDER] service={args.service} -> "
                + " -> ".join(order)
            )
        else:
            print(f"[NO ROUTE] service={args.service}")

        if cycle < args.cycles:
            time.sleep(args.heartbeat_seconds)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
