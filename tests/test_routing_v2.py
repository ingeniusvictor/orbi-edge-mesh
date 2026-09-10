import unittest

from manager.registry import NodeRegistry
from manager.routing_v2 import choose_node_policy_aware


def capability(
    node_id,
    temp=35.0,
    battery=80,
    charging=False,
    service="llm",
):
    return {
        "node_id": node_id,
        "health": {
            "status": "ready",
            "temperature_c": temp,
            "battery_percent": battery,
            "charging": charging,
        },
        "services": [
            {
                "type": service,
                "status": "ready",
            }
        ],
    }


class RoutingV2Tests(unittest.TestCase):
    def test_hot_node_is_skipped(self):
        reg = NodeRegistry()
        hot = reg.upsert("http://hot", capability("hot", temp=44.0))
        cool = reg.upsert("http://cool", capability("cool", temp=36.0))
        selected = choose_node_policy_aware([hot, cool], "llm")
        self.assertEqual(selected.node_id, "cool")

    def test_low_battery_node_is_skipped(self):
        reg = NodeRegistry()
        low = reg.upsert("http://low", capability("low", battery=15))
        ok = reg.upsert("http://ok", capability("ok", battery=70))
        selected = choose_node_policy_aware([low, ok], "llm")
        self.assertEqual(selected.node_id, "ok")

    def test_no_route_if_all_blocked(self):
        reg = NodeRegistry()
        hot = reg.upsert("http://hot", capability("hot", temp=49.0))
        low = reg.upsert("http://low", capability("low", battery=8))
        self.assertIsNone(choose_node_policy_aware([hot, low], "llm"))


if __name__ == "__main__":
    unittest.main()
