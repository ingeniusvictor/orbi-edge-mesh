import unittest

from manager.wake_planner import plan_wake


class WakePlannerTests(unittest.TestCase):
    def test_loaded_model_uses_immediately(self):
        d = plan_wake(
            model_status="loaded",
            policy_allows_work=True,
            latency_sensitivity="high",
        )
        self.assertEqual(d.action, "use_immediately")

    def test_cold_interactive_model_is_not_first_choice(self):
        d = plan_wake(
            model_status="cold",
            policy_allows_work=True,
            latency_sensitivity="high",
        )
        self.assertEqual(d.action, "wake_if_no_warm_candidate")

    def test_policy_block_prevents_wake(self):
        d = plan_wake(
            model_status="cold",
            policy_allows_work=False,
            latency_sensitivity="low",
        )
        self.assertFalse(d.allowed)


if __name__ == "__main__":
    unittest.main()
