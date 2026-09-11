import base64
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SIGNED_PATH = Path(__file__).parents[1] / "scripts" / "pc" / "orbi_signed_chat.py"
signed_spec = importlib.util.spec_from_file_location("orbi_signed_chat", SIGNED_PATH)
signed = importlib.util.module_from_spec(signed_spec)
sys.modules[signed_spec.name] = signed
signed_spec.loader.exec_module(signed)

PROBE_PATH = Path(__file__).parents[1] / "scripts" / "pc" / "native_headless_probe.py"
probe_spec = importlib.util.spec_from_file_location("native_headless_probe", PROBE_PATH)
probe = importlib.util.module_from_spec(probe_spec)
sys.modules[probe_spec.name] = probe
probe_spec.loader.exec_module(probe)


class FakeResponse:
    def __init__(self, body, status=200):
        self._body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._body


class NativeHeadlessProbeTests(unittest.TestCase):
    def test_health_parses_ok(self):
        with patch.object(
            probe,
            "urlopen",
            return_value=FakeResponse({"status": "ok"}),
        ):
            result = probe.get_health("http://node", 1.0)

        self.assertTrue(result["ok"])

    def test_signed_chat_never_returns_secret_in_result(self):
        raw = bytes(range(32))
        token = base64.urlsafe_b64encode(raw).decode().rstrip("=")

        response = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "ORBI NATIVE HEADLESS OK",
                    }
                }
            ]
        }

        with patch.object(
            probe,
            "urlopen",
            return_value=FakeResponse(response),
        ):
            result = probe.signed_chat(
                base_url="http://node",
                node_id="node-01",
                token=token,
                model_id="model-a",
                prompt="test",
                timeout=1.0,
            )

        self.assertTrue(result["ok"])
        self.assertNotIn(token, json.dumps(result))


if __name__ == "__main__":
    unittest.main()
