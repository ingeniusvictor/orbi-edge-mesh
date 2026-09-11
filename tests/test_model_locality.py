import unittest

from manager.registry import NodeRegistry
from manager.routing_v3 import choose_node_for_request
from models.inventory import find_model


def capability(node_id, temp, services):
    return {
        "node_id": node_id,
        "health": {
            "status": "ready",
            "temperature_c": temp,
            "battery_percent": 80,
            "charging": False,
        },
        "services": services,
    }


class ModelInventoryTests(unittest.TestCase):
    def test_find_exact_model(self):
        cap = capability(
            "node-01",
            35.0,
            [
                {
                    "type": "llm",
                    "status": "ready",
                    "model": "qwen-main",
                    "family": "qwen",
                    "model_status": "loaded",
                }
            ],
        )
        model = find_model(cap, service_type="llm", model_id="qwen-main")
        self.assertIsNotNone(model)
        self.assertEqual(model.model_id, "qwen-main")


class LocalityRoutingTests(unittest.TestCase):
    def test_exact_model_beats_cooler_wrong_model(self):
        reg = NodeRegistry()
        a = reg.upsert(
            "http://a",
            capability(
                "node-a",
                38.0,
                [{
                    "type": "llm",
                    "status": "ready",
                    "model": "qwen-main",
                    "family": "qwen",
                    "model_status": "loaded",
                }],
            ),
        )
        b = reg.upsert(
            "http://b",
            capability(
                "node-b",
                30.0,
                [{
                    "type": "llm",
                    "status": "ready",
                    "model": "qwen-light",
                    "family": "qwen",
                    "model_status": "loaded",
                }],
            ),
        )

        selected = choose_node_for_request(
            [a, b],
            service_type="llm",
            model_id="qwen-main",
        )
        self.assertEqual(selected.node_id, "node-a")

    def test_loaded_model_beats_cold_model(self):
        reg = NodeRegistry()
        loaded = reg.upsert(
            "http://loaded",
            capability(
                "loaded",
                37.0,
                [{
                    "type": "llm",
                    "status": "ready",
                    "model": "qwen-main",
                    "family": "qwen",
                    "model_status": "loaded",
                }],
            ),
        )
        cold = reg.upsert(
            "http://cold",
            capability(
                "cold",
                32.0,
                [{
                    "type": "llm",
                    "status": "ready",
                    "model": "qwen-main",
                    "family": "qwen",
                    "model_status": "cold",
                }],
            ),
        )

        selected = choose_node_for_request(
            [loaded, cold],
            service_type="llm",
            model_id="qwen-main",
        )
        self.assertEqual(selected.node_id, "loaded")

    def test_whisper_routes_to_specialized_node(self):
        reg = NodeRegistry()
        llm = reg.upsert(
            "http://llm",
            capability(
                "llm",
                33.0,
                [{
                    "type": "llm",
                    "status": "ready",
                    "model": "qwen-main",
                    "family": "qwen",
                    "model_status": "loaded",
                }],
            ),
        )
        voice = reg.upsert(
            "http://voice",
            capability(
                "voice",
                35.0,
                [{
                    "type": "speech_to_text",
                    "status": "ready",
                    "model": "whisper-small",
                    "family": "whisper",
                    "model_status": "loaded",
                }],
            ),
        )

        selected = choose_node_for_request(
            [llm, voice],
            service_type="speech_to_text",
            family="whisper",
        )
        self.assertEqual(selected.node_id, "voice")


if __name__ == "__main__":
    unittest.main()
