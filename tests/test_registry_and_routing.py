import unittest

from manager.registry import NodeRegistry
from manager.routing import choose_node


def capability(node_id, status="ready", temp=35.0, service="llm"):
    return {
        "node_id": node_id,
        "health": {
            "status": status,
            "temperature_c": temp,
        },
        "services": [
            {
                "type": service,
                "status": "ready",
            }
        ],
    }


class RegistryTests(unittest.TestCase):
    def test_upsert(self):
        reg = NodeRegistry()
        reg.upsert("http://a", capability("node-a"))
        self.assertEqual(len(reg.all()), 1)

        reg.upsert("http://a2", capability("node-a", temp=33.0))
        self.assertEqual(len(reg.all()), 1)
        self.assertEqual(reg.get("node-a").base_url, "http://a2")
        self.assertEqual(reg.get("node-a").temperature, 33.0)

    def test_failure_counter_resets_on_success(self):
        reg = NodeRegistry()
        reg.upsert("http://a", capability("node-a"))
        reg.mark_failure("node-a")
        self.assertEqual(reg.get("node-a").consecutive_failures, 1)

        reg.upsert("http://a", capability("node-a"))
        self.assertEqual(reg.get("node-a").consecutive_failures, 0)


class RoutingTests(unittest.TestCase):
    def test_lower_failure_count_wins_before_temperature(self):
        reg = NodeRegistry()
        a = reg.upsert("http://a", capability("node-a", temp=30.0))
        b = reg.upsert("http://b", capability("node-b", temp=40.0))
        reg.mark_failure("node-a")

        selected = choose_node([a, b], "llm")
        self.assertEqual(selected.node_id, "node-b")

    def test_exclusion_enables_fallback(self):
        reg = NodeRegistry()
        a = reg.upsert("http://a", capability("node-a", temp=30.0))
        b = reg.upsert("http://b", capability("node-b", temp=35.0))

        first = choose_node([a, b], "llm")
        second = choose_node([a, b], "llm", {first.node_id})

        self.assertEqual(first.node_id, "node-a")
        self.assertEqual(second.node_id, "node-b")


if __name__ == "__main__":
    unittest.main()
