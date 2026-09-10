import unittest

from manager.registry import NodeRegistry
from manager.request_planner import build_candidate_order


def cap(node_id, model, endpoint, temp=35.0):
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
                "endpoint": endpoint,
            }
        ],
    }


class RequestPlannerTests(unittest.TestCase):
    def test_builds_ordered_executable_candidates(self):
        reg = NodeRegistry()
        reg.upsert("http://n1", cap("node-01", "qwen-main", "http://10.0.0.1:8080", 35.0))
        reg.upsert("http://n2", cap("node-02", "qwen-main", "http://10.0.0.2:8080", 37.0))

        candidates = build_candidate_order(
            reg.all(),
            service_type="llm",
            model_id="qwen-main",
            max_attempts=2,
        )

        self.assertEqual(candidates[0][0], "node-01")
        self.assertEqual(candidates[1][0], "node-02")
        self.assertTrue(candidates[0][1].endswith("/v1/chat/completions"))

    def test_missing_endpoint_is_not_executable(self):
        reg = NodeRegistry()
        reg.upsert("http://n1", cap("node-01", "qwen-main", None))

        candidates = build_candidate_order(
            reg.all(),
            service_type="llm",
            model_id="qwen-main",
        )

        self.assertEqual(candidates, [])


if __name__ == "__main__":
    unittest.main()
