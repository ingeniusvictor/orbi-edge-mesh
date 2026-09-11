import unittest

from node.local_telemetry import select_conservative_temperature


class LocalTelemetryTests(unittest.TestCase):
    def test_selects_highest_valid_temperature(self):
        rows = [
            {"temperature_c": 31.0},
            {"temperature_c": 38.5},
            {"temperature_c": 36.0},
        ]
        self.assertEqual(
            select_conservative_temperature(rows),
            38.5,
        )

    def test_ignores_implausible_values(self):
        rows = [
            {"temperature_c": 400.0},
            {"temperature_c": -100.0},
        ]
        self.assertIsNone(select_conservative_temperature(rows))


if __name__ == "__main__":
    unittest.main()
