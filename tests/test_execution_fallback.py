import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from manager.execution import execute_with_fallback


class SuccessHandler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        body = json.dumps({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "ok",
                }
            }]
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


class ErrorHandler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        self.send_response(500)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass


def start_server(handler):
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class ExecutionFallbackTests(unittest.TestCase):
    def test_first_success_stops_fallback(self):
        ok = start_server(SuccessHandler)
        try:
            endpoint = f"http://127.0.0.1:{ok.server_port}/v1/chat/completions"
            result = execute_with_fallback(
                [("node-01", endpoint, "model-a")],
                messages=[{"role": "user", "content": "hola"}],
                timeout=2,
            )
            self.assertTrue(result.ok)
            self.assertEqual(result.selected_node_id, "node-01")
            self.assertEqual(len(result.attempts), 1)
        finally:
            ok.shutdown()

    def test_error_falls_back_to_next_node(self):
        bad = start_server(ErrorHandler)
        ok = start_server(SuccessHandler)
        try:
            bad_endpoint = f"http://127.0.0.1:{bad.server_port}/v1/chat/completions"
            ok_endpoint = f"http://127.0.0.1:{ok.server_port}/v1/chat/completions"

            result = execute_with_fallback(
                [
                    ("node-01", bad_endpoint, "model-a"),
                    ("node-02", ok_endpoint, "model-a"),
                ],
                messages=[{"role": "user", "content": "hola"}],
                timeout=2,
            )

            self.assertTrue(result.ok)
            self.assertEqual(result.selected_node_id, "node-02")
            self.assertEqual(len(result.attempts), 2)
            self.assertFalse(result.attempts[0].ok)
            self.assertTrue(result.attempts[1].ok)
        finally:
            bad.shutdown()
            ok.shutdown()

    def test_all_fail(self):
        bad1 = start_server(ErrorHandler)
        bad2 = start_server(ErrorHandler)
        try:
            e1 = f"http://127.0.0.1:{bad1.server_port}/v1/chat/completions"
            e2 = f"http://127.0.0.1:{bad2.server_port}/v1/chat/completions"
            result = execute_with_fallback(
                [
                    ("node-01", e1, "model-a"),
                    ("node-02", e2, "model-a"),
                ],
                messages=[{"role": "user", "content": "hola"}],
                timeout=2,
            )
            self.assertFalse(result.ok)
            self.assertIsNone(result.selected_node_id)
            self.assertEqual(len(result.attempts), 2)
        finally:
            bad1.shutdown()
            bad2.shutdown()


if __name__ == "__main__":
    unittest.main()
