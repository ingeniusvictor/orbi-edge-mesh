import unittest

from manager.registry import NodeRegistry
from manager.routing_v5 import choose_node_for_workload
from workloads.profiles import get_profile


def cap(node_id, *, temp, tags):
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
                "model": "qwen-main",
                "family": "qwen",
                "model_status": "loaded",
                "endpoint": f"http://{node_id}:8080",
                "tags": tags,
            }
        ],
    }


class WorkloadRoutingTests(unittest.TestCase):
    def test_fast_chat_tag_can_influence_short_chat(self):
        reg = NodeRegistry()
        tagged = reg.upsert(
            "http://tagged",
            cap("tagged", temp=36.0, tags=["fast-chat"]),
        )
        untagged = reg.upsert(
            "http://untagged",
            cap("untagged", temp=36.0, tags=[]),
        )

        selected = choose_node_for_workload(
            [untagged, tagged],
            profile=get_profile("chat_short"),
            history_summary={},
            model_id="qwen-main",
        )
        self.assertEqual(selected.node_id, "tagged")

    def test_long_generation_penalizes_hotter_node_more(self):
        reg = NodeRegistry()
        cool = reg.upsert(
            "http://cool",
            cap("cool", temp=36.0, tags=["long-generation"]),
        )
        warm = reg.upsert(
            "http://warm",
            cap("warm", temp=41.0, tags=["long-generation"]),
        )

        selected = choose_node_for_workload(
            [warm, cool],
            profile=get_profile("generation_long"),
            history_summary={},
            model_id="qwen-main",
        )
        self.assertEqual(selected.node_id, "cool")


if __name__ == "__main__":
    unittest.main()
