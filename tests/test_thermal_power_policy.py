import unittest

from policy.thermal_power import (
    classify_power,
    classify_thermal,
    evaluate_node_policy,
)


class ThermalPolicyTests(unittest.TestCase):
    def test_normal(self):
        d = classify_thermal(35.0)
        self.assertTrue(d.allow_new_work)
        self.assertEqual(d.action, "normal")

    def test_warm_degrades(self):
        d = classify_thermal(41.0)
        self.assertTrue(d.allow_new_work)
        self.assertEqual(d.action, "degrade")

    def test_hot_avoids(self):
        d = classify_thermal(44.0)
        self.assertFalse(d.allow_new_work)
        self.assertEqual(d.action, "avoid")

    def test_critical_pauses(self):
        d = classify_thermal(49.0)
        self.assertFalse(d.allow_new_work)
        self.assertEqual(d.action, "pause")


class PowerPolicyTests(unittest.TestCase):
    def test_low_battery_not_charging_avoids(self):
        d = classify_power(18.0, False)
        self.assertFalse(d.allow_new_work)
        self.assertEqual(d.action, "avoid")

    def test_charging_low_battery_allowed(self):
        d = classify_power(18.0, True)
        self.assertTrue(d.allow_new_work)

    def test_critical_battery_pauses(self):
        d = classify_power(8.0, False)
        self.assertFalse(d.allow_new_work)
        self.assertEqual(d.action, "pause")


class CombinedPolicyTests(unittest.TestCase):
    def test_hot_node_blocks_even_with_good_battery(self):
        capability = {
            "health": {
                "temperature_c": 44.0,
                "battery_percent": 90,
                "charging": False,
            }
        }
        d = evaluate_node_policy(capability)
        self.assertFalse(d.allow_new_work)
        self.assertEqual(d.action, "avoid")


if __name__ == "__main__":
    unittest.main()
