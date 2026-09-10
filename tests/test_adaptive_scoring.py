import unittest

from manager.adaptive_scoring import score_history


class AdaptiveScoringTests(unittest.TestCase):
    def test_high_reliability_low_latency_scores_better(self):
        summary = {
            "node-a": {
                "attempts": 10,
                "success_rate": 1.0,
                "avg_success_latency_s": 1.0,
                "avg_temperature_c": 35.0,
            },
            "node-b": {
                "attempts": 10,
                "success_rate": 0.8,
                "avg_success_latency_s": 2.0,
                "avg_temperature_c": 38.0,
            },
        }
        self.assertLess(
            score_history("node-a", summary).total,
            score_history("node-b", summary).total,
        )

    def test_cold_start_has_penalty(self):
        score = score_history("missing", {})
        self.assertGreater(score.total, 0)

    def test_low_sample_count_has_penalty(self):
        summary = {
            "node-a": {
                "attempts": 1,
                "success_rate": 1.0,
                "avg_success_latency_s": 1.0,
                "avg_temperature_c": 35.0,
            }
        }
        score = score_history("node-a", summary)
        self.assertGreater(score.sample_penalty, 0)


if __name__ == "__main__":
    unittest.main()
