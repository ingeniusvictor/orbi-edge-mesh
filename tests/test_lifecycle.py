import unittest
from node.lifecycle import decide_lifecycle

class LifecycleTests(unittest.TestCase):
    def test_healthy(self):
        d = decide_lifecycle(process_alive=True, api_reachable=True, policy_action="normal", restart_count=0, max_restarts=3)
        self.assertEqual(d.state, "healthy")
        self.assertFalse(d.restart_allowed)

    def test_process_down_requests_restart(self):
        d = decide_lifecycle(process_alive=False, api_reachable=False, policy_action="normal", restart_count=0, max_restarts=3)
        self.assertEqual(d.action, "restart_service")
        self.assertTrue(d.restart_allowed)

    def test_restart_budget_prevents_loop(self):
        d = decide_lifecycle(process_alive=False, api_reachable=False, policy_action="normal", restart_count=3, max_restarts=3)
        self.assertEqual(d.action, "quarantine")
        self.assertFalse(d.restart_allowed)

    def test_policy_pause_prevents_restart(self):
        d = decide_lifecycle(process_alive=False, api_reachable=False, policy_action="pause", restart_count=0, max_restarts=3)
        self.assertEqual(d.state, "paused_by_policy")
        self.assertFalse(d.restart_allowed)

if __name__ == "__main__":
    unittest.main()
