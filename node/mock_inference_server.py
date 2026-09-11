#!/usr/bin/env python3
"""Mock OpenAI-compatible inference server for fallback tests."""

from __future__ import annotations

import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class Handler(BaseHTTPRequestHandler):
    server_version = "ORBI-MockInference/0.1"

    def _json(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/chat/completions":
            self._json(404, {"error": "not_found"})
            return

        mode = self.server.mode  # type: ignore[attr-defined]
        delay = self.server.delay  # type: ignore[attr-defined]
        node_id = self.server.node_id  # type: ignore[attr-defined]

        if delay > 0:
            time.sleep(delay)

        if mode == "error":
            self._json(500, {"error": {"message": f"mock failure on {node_id}"}})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._json(400, {"error": "invalid_json"})
            return

        model = payload.get("model", "mock-model")
        self._json(
            200,
            {
                "id": f"mock-{node_id}",
                "object": "chat.completion",
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": f"Respuesta local simulada desde {node_id}.",
                        },
                        "finish_reason": "stop",
                    }
                ],
            },
        )

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[mock-inference] {self.address_string()} - {fmt % args}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--node-id", default="node-01")
    parser.add_argument("--mode", choices=["ok", "error"], default="ok")
    parser.add_argument("--delay", type=float, default=0.0)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    server.node_id = args.node_id  # type: ignore[attr-defined]
    server.mode = args.mode  # type: ignore[attr-defined]
    server.delay = args.delay  # type: ignore[attr-defined]

    print(
        f"Mock inference server {args.node_id} "
        f"mode={args.mode} -> http://{args.host}:{args.port}"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
