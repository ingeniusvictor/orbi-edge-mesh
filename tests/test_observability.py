import tempfile
import unittest

from observability.metrics import summarize_by_node
from observability.store import JsonlEventStore


class ObservabilityTests(unittest.TestCase):
    def test_jsonl_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = f"{tmp}/events.jsonl"
            store = JsonlEventStore(path)
            store.append({"node_id": "node-01", "ok": True, "elapsed_s": 1.2})
            self.assertEqual(store.read_all()[0]["node_id"], "node-01")

    def test_summary(self):
        events = [
            {
                "node_id": "node-01",
                "ok": True,
                "elapsed_s": 1.0,
                "temperature_c": 35.0,
            },
            {
                "node_id": "node-01",
                "ok": False,
                "elapsed_s": 0.0,
                "temperature_c": 37.0,
            },
            {
                "node_id": "node-02",
                "ok": True,
                "elapsed_s": 2.0,
                "temperature_c": 33.0,
            },
        ]

        summary = summarize_by_node(events)

        self.assertEqual(summary["node-01"]["attempts"], 2)
        self.assertEqual(summary["node-01"]["successes"], 1)
        self.assertEqual(summary["node-01"]["failures"], 1)
        self.assertEqual(summary["node-01"]["success_rate"], 0.5)
        self.assertEqual(summary["node-01"]["avg_success_latency_s"], 1.0)
        self.assertEqual(summary["node-01"]["avg_temperature_c"], 36.0)


if __name__ == "__main__":
    unittest.main()
