import unittest

from node.policy_gate import authorize_recovery


class PolicyGateTests(unittest.TestCase):
    def test_safe_node_allows_restart(self):
        d = authorize_recovery({
            "health": {
                "temperature_c": 35.0,
                "battery_percent": 80,
                "charging": False,
            }
        })
        self.assertTrue(d.allowed)

    def test_hot_node_blocks_restart(self):
        d = authorize_recovery({
            "health": {
                "temperature_c": 49.0,
                "battery_percent": 80,
                "charging": False,
            }
        })
        self.assertFalse(d.allowed)

    def test_critical_battery_blocks_restart(self):
        d = authorize_recovery({
            "health": {
                "temperature_c": 35.0,
                "battery_percent": 8,
                "charging": False,
            }
        })
        self.assertFalse(d.allowed)


if __name__ == "__main__":
    unittest.main()
