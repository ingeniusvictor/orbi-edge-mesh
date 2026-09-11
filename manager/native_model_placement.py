#!/usr/bin/env python3
"""Advisory storage-aware model placement planner for ORBI native nodes."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from native_mesh_manager import inspect_node, load_config


GIB = 1024 ** 3


@dataclass(frozen=True)
class ModelEntry:
    id: str
    display_name: str
    approx_size_bytes: int
    service: str


@dataclass(frozen=True)
class PlacementCandidate:
    node_name: str
    host: str
    resource_action: str
    battery_percent: int | None
    storage_total_bytes: int
    storage_available_bytes: int
    reserve_bytes: int
    projected_free_bytes: int
    model_already_loaded: bool
    score: tuple[int, int, int, str]


def load_catalog(path: Path) -> dict[str, ModelEntry]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    models = raw.get("models")
    if not isinstance(models, list):
        raise ValueError("catalog must contain models[]")

    result: dict[str, ModelEntry] = {}
    for item in models:
        model = ModelEntry(
            id=str(item["id"]),
            display_name=str(item.get("display_name", item["id"])),
            approx_size_bytes=int(item["approx_size_bytes"]),
            service=str(item.get("service", "CHAT")).upper(),
        )
        if model.approx_size_bytes <= 0:
            raise ValueError(f"model {model.id} has invalid approx_size_bytes")
        result[model.id] = model

    return result


def reserve_bytes(total_bytes: int) -> int:
    """Provisional research reserve: max(8 GiB, 10% of total capacity)."""
    return max(8 * GIB, math.ceil(total_bytes * 0.10))


def build_candidate(state, model: ModelEntry) -> PlacementCandidate | None:
    if not state.reachable or not state.paired:
        return None

    if state.resource_action == "BLOCK":
        return None

    if model.service not in state.services_supported:
        return None

    total = state.storage_total_bytes
    available = state.storage_available_bytes

    if not isinstance(total, int) or total <= 0:
        return None
    if not isinstance(available, int) or available < 0:
        return None

    already_loaded = model.id in state.model_ids and state.model_loaded
    required = 0 if already_loaded else model.approx_size_bytes
    projected = available - required
    reserve = reserve_bytes(total)

    if projected < reserve:
        return None

    action_rank = {
        "ALLOW": 0,
        "DEGRADE": 1,
    }.get(state.resource_action, 5)

    battery = state.battery_percent
    battery_penalty = 100 - battery if isinstance(battery, int) else 101

    # Prefer already resident models, then safer resource state, then more free space.
    score = (
        0 if already_loaded else 1,
        action_rank,
        -projected,
        state.config.name,
    )

    return PlacementCandidate(
        node_name=state.config.name,
        host=state.config.host,
        resource_action=state.resource_action,
        battery_percent=battery,
        storage_total_bytes=total,
        storage_available_bytes=available,
        reserve_bytes=reserve,
        projected_free_bytes=projected,
        model_already_loaded=already_loaded,
        score=score,
    )


def plan(states, model: ModelEntry, replicas: int) -> dict:
    if replicas < 1:
        raise ValueError("replicas must be >= 1")

    candidates = [
        candidate
        for state in states
        if (candidate := build_candidate(state, model)) is not None
    ]
    candidates.sort(key=lambda item: item.score)

    selected = candidates[:replicas]
    return {
        "model": asdict(model),
        "requested_replicas": replicas,
        "selected": [
            {
                key: value
                for key, value in asdict(candidate).items()
                if key != "score"
            }
            for candidate in selected
        ],
        "unfulfilled_replicas": max(0, replicas - len(selected)),
        "policy": {
            "mode": "advisory_only",
            "automatic_delete": False,
            "automatic_transfer": False,
            "reserve_rule": "max(8 GiB, 10% of total storage) must remain free after placement",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--replicas", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    try:
        configs = load_config(args.config)
        catalog = load_catalog(args.catalog)
        model = catalog[args.model_id]
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2

    states = [
        inspect_node(config, args.timeout)
        for config in configs
    ]

    try:
        result = plan(states, model, args.replicas)
    except ValueError as exc:
        print(f"PLAN ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if result["unfulfilled_replicas"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
