#!/usr/bin/env python3
"""Placement planning for native ORBI Edge Node capability manifests.

This module does not transfer model binaries. It only produces a deterministic
placement recommendation using currently observable node resources.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from models.placement import PlacementDecision, choose_storage_node


MIB = 1024 * 1024


@dataclass(frozen=True)
class NativePlacementInput:
    node_id: str
    manifest: dict[str, Any]


def manifest_to_phase0_capability(
    manifest: dict[str, Any],
) -> dict[str, Any]:
    storage_free = manifest.get("storage_available_bytes")
    ram_total = manifest.get("memory_total_bytes")
    available_models = manifest.get("available_model_ids", [])

    services = []
    if isinstance(available_models, list):
        for model_id in available_models:
            if isinstance(model_id, str):
                services.append({"model": model_id})

    return {
        "node_id": str(manifest.get("node_id", "unknown")),
        "resources": {
            "storage_free_mb": (
                float(storage_free) / MIB
                if isinstance(storage_free, (int, float))
                else None
            ),
            "physical_ram_mb": (
                float(ram_total) / MIB
                if isinstance(ram_total, (int, float))
                else None
            ),
        },
        "services": services,
    }


def policy_eligible(manifest: dict[str, Any]) -> bool:
    action = str(manifest.get("resource_action", "UNKNOWN")).upper()
    return action in {"ALLOW", "DEGRADE"}


def plan_native_model_placement(
    manifests: list[dict[str, Any]],
    *,
    model_id: str,
    model_size_bytes: int,
    reserve_bytes: int,
) -> PlacementDecision | None:
    if model_size_bytes <= 0:
        raise ValueError("model_size_bytes must be > 0")
    if reserve_bytes < 0:
        raise ValueError("reserve_bytes must be >= 0")

    candidates = [
        manifest_to_phase0_capability(manifest)
        for manifest in manifests
        if policy_eligible(manifest)
    ]

    return choose_storage_node(
        candidates,
        model_id=model_id,
        model_size_mb=model_size_bytes / MIB,
        min_free_after_mb=reserve_bytes / MIB,
    )


def load_manifests(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    manifests = raw.get("manifests")
    if not isinstance(manifests, list) or not manifests:
        raise ValueError("input must contain a non-empty manifests[] list")
    return [
        manifest
        for manifest in manifests
        if isinstance(manifest, dict)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--model-size-bytes", required=True, type=int)
    parser.add_argument(
        "--reserve-bytes",
        type=int,
        default=8 * 1024 * 1024 * 1024,
        help="Projected free-space reserve after placement. Default: 8 GiB.",
    )
    args = parser.parse_args()

    try:
        manifests = load_manifests(args.input)
        decision = plan_native_model_placement(
            manifests,
            model_id=args.model_id,
            model_size_bytes=args.model_size_bytes,
            reserve_bytes=args.reserve_bytes,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PLACEMENT INPUT ERROR: {exc}", file=sys.stderr)
        return 2

    if decision is None:
        print(json.dumps({
            "result": "NO_PLACEMENT",
            "model_id": args.model_id,
            "reason": "No resource-eligible node satisfies storage reserve policy.",
            "binary_transfer_performed": False,
        }, indent=2))
        return 1

    payload = {
        "result": "PLACEMENT_PLAN",
        "decision": asdict(decision),
        "binary_transfer_performed": False,
        "unified_ram_assumed": False,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
