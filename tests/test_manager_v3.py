import unittest

from manager.orbi_manager_v3 import route_order
from manager.registry import NodeRegistry


def capability(
    node_id,
    *,
    status="ready",
    temp=35.0,
    battery=80,
    charging=False,
    service="llm",
):
    return {
        "node_id": node_id,
        "health": {
            "status": status,
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


class ManagerV3Tests(unittest.TestCase):
    def test_hot_primary_is_removed_from_route_order(self):
        reg = NodeRegistry()
        reg.upsert("http://node-01", capability("node-01", temp=44.0))
        reg.upsert("http://node-02", capability("node-02", temp=36.0))

        self.assertEqual(
            route_order(reg, "llm", 3),
            ["node-02"],
        )

    def test_low_battery_primary_is_removed_from_route_order(self):
        reg = NodeRegistry()
        reg.upsert(
            "http://node-01",
            capability("node-01", battery=15, charging=False),
        )
        reg.upsert(
            "http://node-02",
            capability("node-02", battery=70, charging=False),
        )

        self.assertEqual(
            route_order(reg, "llm", 3),
            ["node-02"],
        )

    def test_warm_node_can_be_fallback(self):
        reg = NodeRegistry()
        reg.upsert("http://node-01", capability("node-01", temp=35.0))
        reg.upsert("http://node-02", capability("node-02", temp=41.0))

        self.assertEqual(
            route_order(reg, "llm", 3),
            ["node-01", "node-02"],
        )

    def test_all_blocked_returns_empty_route(self):
        reg = NodeRegistry()
        reg.upsert("http://node-01", capability("node-01", temp=49.0))
        reg.upsert("http://node-02", capability("node-02", battery=8))

        self.assertEqual(route_order(reg, "llm", 3), [])


if __name__ == "__main__":
    unittest.main()
