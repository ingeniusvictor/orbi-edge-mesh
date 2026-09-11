import base64
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch


MODULE_PATH = (
    Path(__file__).parents[1]
    / "scripts"
    / "pc"
    / "native_node01_certify.py"
)
spec = importlib.util.spec_from_file_location(
    "native_node01_certify",
    MODULE_PATH,
)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class FakeResponse:
    def __init__(self, status, body):
        self.status = status
        self._body = json.dumps(body).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._body


class Node01CertificationTests(unittest.TestCase):
    def test_decode_token_requires_32_bytes(self):
        raw = bytes(range(32))
        token = base64.urlsafe_b64encode(raw).decode().rstrip("=")
        self.assertEqual(raw, mod.decode_token(token))

    def test_signed_request_is_reproducible_with_fixed_nonce_and_time(self):
        secret = bytes(range(32))
        first, ts1, nonce1 = mod.signed_chat_request(
            base_url="http://node",
            node_id="node-01",
            secret=secret,
            model_id="model-a",
            prompt="hola",
            timestamp_ms=123456789,
            nonce="0123456789abcdef",
        )
        second, ts2, nonce2 = mod.signed_chat_request(
            base_url="http://node",
            node_id="node-01",
            secret=secret,
            model_id="model-a",
            prompt="hola",
            timestamp_ms=123456789,
            nonce="0123456789abcdef",
        )

        self.assertEqual(ts1, ts2)
        self.assertEqual(nonce1, nonce2)
        self.assertEqual(
            first.headers["X-orbi-signature"],
            second.headers["X-orbi-signature"],
        )

    def test_request_json_parses_success(self):
        with patch.object(
            mod,
            "urlopen",
            return_value=FakeResponse(
                200,
                {"status": "ok"},
            ),
        ):
            status, body = mod.request_json(
                "http://node/health",
                1.0,
            )

        self.assertEqual(200, status)
        self.assertEqual("ok", body["status"])


if __name__ == "__main__":
    unittest.main()
