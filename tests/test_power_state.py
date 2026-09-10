import unittest

from node.power_state import decide_power_state


class PowerStateTests(unittest.TestCase):
    def test_active_keeps_model_loaded(self):
        d = decide_power_state(
            active_requests=1,
            seconds_since_last_request=0,
            policy_action="normal",
            idle_unload_after_s=300,
        )
        self.assertEqual(d.state, "active")
        self.assertTrue(d.keep_model_loaded)

    def test_recent_idle_keeps_model_warm(self):
        d = decide_power_state(
            active_requests=0,
            seconds_since_last_request=120,
            policy_action="normal",
            idle_unload_after_s=300,
        )
        self.assertEqual(d.state, "idle_warm")
        self.assertTrue(d.keep_model_loaded)

    def test_long_idle_can_unload_model(self):
        d = decide_power_state(
            active_requests=0,
            seconds_since_last_request=600,
            policy_action="normal",
            idle_unload_after_s=300,
        )
        self.assertEqual(d.state, "idle_cold")
        self.assertFalse(d.keep_model_loaded)
        self.assertTrue(d.keep_api_alive)

    def test_policy_pause_forces_model_unload(self):
        d = decide_power_state(
            active_requests=0,
            seconds_since_last_request=0,
            policy_action="pause",
            idle_unload_after_s=300,
        )
        self.assertEqual(d.state, "protected_pause")
        self.assertFalse(d.keep_model_loaded)
        self.assertFalse(d.allow_wake)


if __name__ == "__main__":
    unittest.main()
