#!/usr/bin/env python3
"""Estimate whether a cross-phone inference split is worth a physical experiment."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    name: str
    payload_bytes_each_direction: int
    local_compute_ms: float
    remote_compute_ms: float
    orchestration_overhead_ms: float = 0.0


@dataclass(frozen=True)
class NetworkProfile:
    rtt_ms: float
    throughput_mbps: float
    jitter_ms: float = 0.0


@dataclass(frozen=True)
class FeasibilityResult:
    scenario: str
    single_node_ms: float
    distributed_ms: float
    transfer_ms: float
    network_penalty_ms: float
    speedup: float
    overhead_fraction: float
    decision: str
    reason: str


def transfer_time_ms(payload_bytes: int, throughput_mbps: float) -> float:
    if payload_bytes < 0:
        raise ValueError("payload_bytes must be >= 0")
    if throughput_mbps <= 0:
        raise ValueError("throughput_mbps must be > 0")

    bits = payload_bytes * 8.0
    bits_per_second = throughput_mbps * 1_000_000.0
    return (bits / bits_per_second) * 1000.0


def evaluate(
    scenario: Scenario,
    network: NetworkProfile,
    min_speedup: float = 1.10,
    max_overhead_fraction: float = 0.35,
) -> FeasibilityResult:
    if scenario.local_compute_ms <= 0:
        raise ValueError("local_compute_ms must be > 0")
    if scenario.remote_compute_ms < 0:
        raise ValueError("remote_compute_ms must be >= 0")
    if network.rtt_ms < 0 or network.jitter_ms < 0:
        raise ValueError("network latency values must be >= 0")

    upload_ms = transfer_time_ms(
        scenario.payload_bytes_each_direction,
        network.throughput_mbps,
    )
    download_ms = transfer_time_ms(
        scenario.payload_bytes_each_direction,
        network.throughput_mbps,
    )
    transfer_ms = upload_ms + download_ms

    # Conservative network penalty:
    # one full RTT for request/coordination plus one jitter allowance.
    network_penalty_ms = (
        network.rtt_ms
        + network.jitter_ms
        + transfer_ms
        + scenario.orchestration_overhead_ms
    )

    single_node_ms = scenario.local_compute_ms
    distributed_ms = scenario.remote_compute_ms + network_penalty_ms

    if distributed_ms <= 0:
        speedup = math.inf
    else:
        speedup = single_node_ms / distributed_ms

    overhead_fraction = (
        network_penalty_ms / distributed_ms
        if distributed_ms > 0
        else 0.0
    )

    if speedup < 1.0:
        decision = "NO-GO"
        reason = "Distributed path is slower than the single-node baseline."
    elif speedup < min_speedup:
        decision = "NO-GO"
        reason = (
            f"Speedup {speedup:.2f}x is below the research threshold "
            f"{min_speedup:.2f}x."
        )
    elif overhead_fraction > max_overhead_fraction:
        decision = "NO-GO"
        reason = (
            f"Network/orchestration overhead {overhead_fraction:.1%} exceeds "
            f"the threshold {max_overhead_fraction:.1%}."
        )
    else:
        decision = "PHYSICAL-EXPERIMENT-CANDIDATE"
        reason = (
            f"Estimated speedup {speedup:.2f}x with "
            f"{overhead_fraction:.1%} network/orchestration overhead."
        )

    return FeasibilityResult(
        scenario=scenario.name,
        single_node_ms=single_node_ms,
        distributed_ms=distributed_ms,
        transfer_ms=transfer_ms,
        network_penalty_ms=network_penalty_ms,
        speedup=speedup,
        overhead_fraction=overhead_fraction,
        decision=decision,
        reason=reason,
    )


def load_scenarios(path: Path) -> list[Scenario]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    scenarios = raw.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenario file must contain a non-empty scenarios[] list")

    result = []
    for item in scenarios:
        result.append(
            Scenario(
                name=str(item["name"]),
                payload_bytes_each_direction=int(
                    item["payload_bytes_each_direction"]
                ),
                local_compute_ms=float(item["local_compute_ms"]),
                remote_compute_ms=float(item["remote_compute_ms"]),
                orchestration_overhead_ms=float(
                    item.get("orchestration_overhead_ms", 0.0)
                ),
            )
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", type=Path, required=True)
    parser.add_argument("--rtt-ms", type=float, required=True)
    parser.add_argument("--throughput-mbps", type=float, required=True)
    parser.add_argument("--jitter-ms", type=float, default=0.0)
    parser.add_argument("--min-speedup", type=float, default=1.10)
    parser.add_argument("--max-overhead-fraction", type=float, default=0.35)
    args = parser.parse_args()

    try:
        scenarios = load_scenarios(args.scenarios)
        network = NetworkProfile(
            rtt_ms=args.rtt_ms,
            throughput_mbps=args.throughput_mbps,
            jitter_ms=args.jitter_ms,
        )
        results = [
            evaluate(
                scenario,
                network,
                min_speedup=args.min_speedup,
                max_overhead_fraction=args.max_overhead_fraction,
            )
            for scenario in scenarios
        ]
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        return 2

    print(
        json.dumps(
            {
                "network": asdict(network),
                "thresholds": {
                    "min_speedup": args.min_speedup,
                    "max_overhead_fraction": args.max_overhead_fraction,
                },
                "results": [asdict(item) for item in results],
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    # A NO-GO is a valid research result, not a process failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
