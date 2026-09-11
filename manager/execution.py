#!/usr/bin/env python3
"""ORBI Edge Mesh request execution with ordered fallback."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class ExecutionAttempt:
    node_id: str
    endpoint: str
    ok: bool
    elapsed_s: float
    error: str | None
    response: dict[str, Any] | None


@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    selected_node_id: str | None
    attempts: list[ExecutionAttempt]
    response: dict[str, Any] | None


def post_chat_completion(
    endpoint: str,
    *,
    model: str,
    messages: list[dict[str, str]],
    timeout: float,
    temperature: float = 0.2,
) -> tuple[dict[str, Any], float]:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
    }
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        endpoint,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    started = time.perf_counter()
    with urlopen(req, timeout=timeout) as response:
        raw = response.read()
        elapsed = time.perf_counter() - started
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"unexpected HTTP status {response.status}")
        return json.loads(raw.decode("utf-8")), elapsed


def execute_with_fallback(
    candidates: list[tuple[str, str, str]],
    *,
    messages: list[dict[str, str]],
    timeout: float = 60.0,
    temperature: float = 0.2,
) -> ExecutionResult:
    """Try candidates in order.

    Each candidate is:
      (node_id, chat_completions_endpoint, model_id)
    """
    attempts: list[ExecutionAttempt] = []

    for node_id, endpoint, model_id in candidates:
        try:
            response, elapsed = post_chat_completion(
                endpoint,
                model=model_id,
                messages=messages,
                timeout=timeout,
                temperature=temperature,
            )
            attempts.append(
                ExecutionAttempt(
                    node_id=node_id,
                    endpoint=endpoint,
                    ok=True,
                    elapsed_s=elapsed,
                    error=None,
                    response=response,
                )
            )
            return ExecutionResult(
                ok=True,
                selected_node_id=node_id,
                attempts=attempts,
                response=response,
            )
        except (HTTPError, URLError, TimeoutError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
            attempts.append(
                ExecutionAttempt(
                    node_id=node_id,
                    endpoint=endpoint,
                    ok=False,
                    elapsed_s=0.0,
                    error=f"{type(exc).__name__}: {exc}",
                    response=None,
                )
            )

    return ExecutionResult(
        ok=False,
        selected_node_id=None,
        attempts=attempts,
        response=None,
    )
