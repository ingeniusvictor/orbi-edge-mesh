#!/usr/bin/env python3
"""ORBI Native Mesh Manager — whole-workload routing research prototype."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class NodeConfig:
    name: str
    host: str
    port: int
    node_id: str
    token_env: str

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


@dataclass
class NodeState:
    config: NodeConfig
    reachable: bool
    resource_action: str = "UNKNOWN"
    resource_reason: str = ""
    model_loaded: bool = False
    paired: bool = False
    battery_percent: int | None = None
    thermal_status: str | None = None
    memory_total_bytes: int | None = None
    memory_available_bytes: int | None = None
    storage_total_bytes: int | None = None
    storage_available_bytes: int | None = None
    reported_node_id: str | None = None
    services_supported: tuple[str, ...] = ()
    model_ids: tuple[str, ...] = ()
    error: str | None = None


def get_json(url: str, timeout: float) -> dict[str, Any]:
    with urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def load_config(path: Path) -> list[NodeConfig]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    nodes = raw.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("config must contain a non-empty nodes[] list")

    return [
        NodeConfig(
            name=str(item["name"]),
            host=str(item["host"]),
            port=int(item.get("port", 8080)),
            node_id=str(item["node_id"]),
            token_env=str(item["token_env"]),
        )
        for item in nodes
    ]


def inspect_node(config: NodeConfig, timeout: float) -> NodeState:
    try:
        node = get_json(config.base_url + "/node", timeout)
        models = get_json(config.base_url + "/v1/models", timeout)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return NodeState(config=config, reachable=False, error=f"{type(exc).__name__}: {exc}")

    reported_node_id = node.get("node_id")
    if reported_node_id and reported_node_id != config.node_id:
        return NodeState(
            config=config,
            reachable=False,
            reported_node_id=str(reported_node_id),
            error="NODE_ID_MISMATCH",
        )

    data = models.get("data")
    model_ids = tuple(
        str(item.get("id"))
        for item in data
        if isinstance(item, dict) and item.get("id")
    ) if isinstance(data, list) else ()
    has_model = len(model_ids) > 0

    services_raw = node.get("services_supported")
    services_supported = tuple(
        str(item).upper()
        for item in services_raw
        if isinstance(item, str)
    ) if isinstance(services_raw, list) else ()

    return NodeState(
        config=config,
        reachable=True,
        resource_action=str(node.get("resource_action", "UNKNOWN")).upper(),
        resource_reason=str(node.get("resource_reason", "")),
        model_loaded=bool(node.get("model_loaded", False)) and has_model,
        paired=bool(node.get("paired", False)),
        battery_percent=node.get("battery_percent"),
        thermal_status=node.get("thermal_status"),
        memory_total_bytes=node.get("memory_total_bytes"),
        memory_available_bytes=node.get("memory_available_bytes"),
        storage_total_bytes=node.get("storage_total_bytes"),
        storage_available_bytes=node.get("storage_available_bytes"),
        reported_node_id=reported_node_id,
        services_supported=services_supported,
        model_ids=model_ids,
    )


def candidate_rank(state: NodeState) -> tuple[int, int, str]:
    if not state.reachable:
        return (9, 999, state.config.name)
    if not state.model_loaded:
        return (8, 999, state.config.name)
    if not state.paired:
        return (7, 999, state.config.name)

    action_rank = {
        "ALLOW": 0,
        "DEGRADE": 1,
        "UNKNOWN": 5,
        "BLOCK": 9,
    }.get(state.resource_action, 5)

    battery = state.battery_percent
    battery_penalty = 100 - battery if isinstance(battery, int) else 101
    return (action_rank, battery_penalty, state.config.name)


def eligible(
    state: NodeState,
    service: str = "CHAT",
    model_id: str | None = None,
) -> bool:
    requested_service = service.upper()
    if requested_service not in state.services_supported:
        return False
    if model_id is not None and model_id not in state.model_ids:
        return False

    return (
        state.reachable
        and state.model_loaded
        and state.paired
        and state.resource_action in {"ALLOW", "DEGRADE"}
    )


def decode_token(token: str) -> bytes:
    padding = "=" * (-len(token) % 4)
    secret = base64.urlsafe_b64decode(token + padding)
    if len(secret) != 32:
        raise ValueError(f"pairing token decoded to {len(secret)} bytes; expected 32")
    return secret


def sign_headers(config: NodeConfig, method: str, path: str, body: bytes) -> dict[str, str]:
    token = os.environ.get(config.token_env)
    if not token:
        raise RuntimeError(f"missing token environment variable {config.token_env} for {config.name}")

    secret = decode_token(token)
    timestamp_ms = int(time.time() * 1000)
    nonce = secrets.token_hex(16)
    digest = hashlib.sha256(body).hexdigest()

    canonical = "\n".join([
        "ORBI-AUTH-V1",
        config.node_id,
        method.upper(),
        path,
        str(timestamp_ms),
        nonce,
        digest,
    ])

    signature = hmac.new(secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()

    return {
        "Content-Type": "application/json; charset=utf-8",
        "X-ORBI-Node-ID": config.node_id,
        "X-ORBI-Timestamp": str(timestamp_ms),
        "X-ORBI-Nonce": nonce,
        "X-ORBI-Signature": signature,
    }


def execute_chat(state: NodeState, prompt: str, max_tokens: int, timeout: float, model_id: str) -> dict[str, Any]:
    path = "/v1/chat/completions"
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max(1, min(max_tokens, 256)),
        "stream": False,
    }
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    headers = sign_headers(state.config, "POST", path, body)
    request = Request(state.config.base_url + path, data=body, method="POST", headers=headers)

    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def states_for_json(states: list[NodeState]) -> list[dict[str, Any]]:
    result = []
    for state in states:
        item = asdict(state)
        item["config"].pop("token_env", None)
        result.append(item)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument(
        "--prompt",
        default="Responde en español y en una sola frase: ¿qué es ORBI Edge Mesh?",
    )
    parser.add_argument("--max-tokens", type=int, default=96)
    parser.add_argument("--service", default="CHAT")
    parser.add_argument("--model-id", default="qwen3-1.7b-q4_k_m-node01")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--status-only", action="store_true")
    args = parser.parse_args()

    try:
        configs = load_config(args.config)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2

    states = [inspect_node(config, args.timeout) for config in configs]
    print(json.dumps({"nodes": states_for_json(states)}, ensure_ascii=False, indent=2))

    if args.status_only:
        return 0

    candidates = sorted(
        (
            state
            for state in states
            if eligible(state, service=args.service, model_id=args.model_id)
        ),
        key=candidate_rank,
    )
    if not candidates:
        print("NO ELIGIBLE NATIVE ORBI NODE", file=sys.stderr)
        return 1

    failures = []
    for state in candidates:
        try:
            completion = execute_chat(
                state,
                args.prompt,
                args.max_tokens,
                max(args.timeout, 90.0),
                args.model_id,
            )
            print(json.dumps({
                "selected_node": state.config.name,
                "selected_host": state.config.host,
                "completion": completion,
            }, ensure_ascii=False, indent=2))
            return 0
        except (
            HTTPError,
            URLError,
            TimeoutError,
            OSError,
            RuntimeError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
            failures.append({
                "node": state.config.name,
                "error": f"{type(exc).__name__}: {exc}",
            })

    print(json.dumps({"routing_failures": failures}, ensure_ascii=False, indent=2), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
