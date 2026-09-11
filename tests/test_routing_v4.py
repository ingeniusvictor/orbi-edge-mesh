import unittest

from manager.registry import NodeRegistry
from manager.routing_v4 import choose_node_adaptive


def capability(node_id, *, temp=35.0, model="qwen-main"):
    return {
        "node_id": node_id,
        "health": {
            "status": "ready",
            "temperature_c": temp,
            "battery_percent": 80,
            "charging": False,
        },
        "services": [
            {
                "type": "llm",
                "status": "ready",
                "model": model,
                "family": "qwen",
                "model_status": "loaded",
                "endpoint": f"http://{node_id}:8080",
            }
        ],
    }


class AdaptiveRoutingTests(unittest.TestCase):
    def test_history_can_prefer_more_reliable_node(self):
        reg = NodeRegistry()
        a = reg.upsert("http://a", capability("node-a", temp=35.0))
        b = reg.upsert("http://b", capability("node-b", temp=34.0))

        history = {
            "node-a": {
                "attempts": 10,
                "success_rate": 1.0,
                "avg_success_latency_s": 1.0,
                "avg_temperature_c": 35.0,
            },
            "node-b": {
                "attempts": 10,
                "success_rate": 0.6,
                "avg_success_latency_s": 0.8,
                "avg_temperature_c": 34.0,
            },
        }

        selected = choose_node_adaptive(
            [a, b],
            service_type="llm",
            history_summary=history,
            model_id="qwen-main",
        )
        self.assertEqual(selected.node_id, "node-a")

    def test_policy_block_still_wins_over_good_history(self):
        reg = NodeRegistry()
        hot = reg.upsert("http://hot", capability("hot", temp=49.0))
        safe = reg.upsert("http://safe", capability("safe", temp=36.0))

        history = {
            "hot": {
                "attempts": 100,
                "success_rate": 1.0,
                "avg_success_latency_s": 0.5,
                "avg_temperature_c": 38.0,
            },
            "safe": {
                "attempts": 3,
                "success_rate": 0.9,
                "avg_success_latency_s": 1.5,
                "avg_temperature_c": 36.0,
            },
        }

        selected = choose_node_adaptive(
            [hot, safe],
            service_type="llm",
            history_summary=history,
            model_id="qwen-main",
        )
        self.assertEqual(selected.node_id, "safe")


if __name__ == "__main__":
    unittest.main()
