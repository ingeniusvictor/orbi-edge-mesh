import importlib.util
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "pc" / "node01_validation_harness.py"
spec = importlib.util.spec_from_file_location("node01_validation_harness", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/v1/models":
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps({"data": [{"id": "qwen3-1.7b-q4_k_m"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        body = json.dumps({"choices":[{"message":{"content":"ORBI"}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


class HarnessTests(unittest.TestCase):
    def test_get_and_post_helpers(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}"
            data, elapsed = mod.get_json(base + "/v1/models", 2)
            self.assertEqual(data["data"][0]["id"], "qwen3-1.7b-q4_k_m")
            self.assertGreaterEqual(elapsed, 0)

            response, elapsed = mod.post_json(
                base + "/v1/chat/completions",
                {"model":"qwen3-1.7b-q4_k_m","messages":[]},
                2,
            )
            self.assertEqual(response["choices"][0]["message"]["content"], "ORBI")
            self.assertGreaterEqual(elapsed, 0)
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
