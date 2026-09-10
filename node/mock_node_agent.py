#!/usr/bin/env python3
"""ORBI Edge Mesh mock Node Agent.

Phase 0 simulator for the ORBI control plane.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


class NodeState:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def get(self) -> dict[str, Any]:
        return self.data

    def set_status(self, status: str) -> None:
        self.data.setdefault("health", {})["status"] = status


class Handler(BaseHTTPRequestHandler):
    server_version = "ORBI-MockNode/0.1"

    def _json(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        state: NodeState = self.server.node_state  # type: ignore[attr-defined]

        if self.path == "/orbi/v1/node":
            self._json(200, state.get())
            return

        if self.path == "/orbi/v1/health":
            node = state.get()
            self._json(
                200,
                {
                    "schema_version": node.get("schema_version", "0.1"),
                    "node_id": node.get("node_id"),
                    "status": node.get("health", {}).get("status", "unknown"),
                },
            )
            return

        self._json(404, {"error": "not_found"})

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[mock-node] {self.address_string()} - {fmt % args}")


def load_node(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="contracts/examples/node01-capability.example.json",
        help="Node capability JSON file",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    node_state = NodeState(load_node(Path(args.config)))
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    server.node_state = node_state  # type: ignore[attr-defined]

    print(f"ORBI mock node listening on http://{args.host}:{args.port}")
    print(f"Node endpoint: http://{args.host}:{args.port}/orbi/v1/node")
    print("Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
