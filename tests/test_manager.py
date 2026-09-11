import unittest

from manager.orbi_manager import Node, choose_node


def make_node(node_id, status="ready", temp=35.0, service="llm"):
    return Node(
        base_url=f"http://{node_id}",
        capability={
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
        },
    )


class ManagerRoutingTests(unittest.TestCase):
    def test_ready_beats_busy(self):
        ready = make_node("node-ready", status="ready", temp=45.0)
        busy = make_node("node-busy", status="busy", temp=30.0)
        self.assertEqual(choose_node([busy, ready], "llm").node_id, "node-ready")

    def test_cooler_ready_node_wins(self):
        hot = make_node("node-hot", temp=43.0)
        cool = make_node("node-cool", temp=34.0)
        self.assertEqual(choose_node([hot, cool], "llm").node_id, "node-cool")

    def test_service_filtering(self):
        llm = make_node("node-llm", service="llm")
        stt = make_node("node-stt", service="speech_to_text")
        self.assertEqual(
            choose_node([llm, stt], "speech_to_text").node_id,
            "node-stt",
        )

    def test_no_route(self):
        llm = make_node("node-llm", service="llm")
        self.assertIsNone(choose_node([llm], "text_to_speech"))


if __name__ == "__main__":
    unittest.main()
