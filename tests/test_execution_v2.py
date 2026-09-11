import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from manager.execution_v2 import execute_with_observability
from observability.store import JsonlEventStore


class OkHandler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        body = json.dumps({"choices": [{"message": {"content": "ok"}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), OkHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class ExecutionV2Tests(unittest.TestCase):
    def test_execution_writes_event(self):
        server = start_server()
        try:
            endpoint = f"http://127.0.0.1:{server.server_port}/v1/chat/completions"
            capabilities = {
                "node-01": {
                    "health": {
                        "temperature_c": 36.5,
                        "battery_percent": 77,
                        "charging": False,
                    }
                }
            }

            with tempfile.TemporaryDirectory() as tmp:
                store = JsonlEventStore(f"{tmp}/events.jsonl")
                result = execute_with_observability(
                    [("node-01", endpoint, "qwen-main")],
                    service_type="llm",
                    messages=[{"role": "user", "content": "hola"}],
                    capabilities_by_node=capabilities,
                    store=store,
                    timeout=2,
                    request_id="req-test",
                )

                self.assertTrue(result.ok)
                rows = store.read_all()
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["request_id"], "req-test")
                self.assertEqual(rows[0]["temperature_c"], 36.5)
                self.assertEqual(rows[0]["battery_percent"], 77)
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
