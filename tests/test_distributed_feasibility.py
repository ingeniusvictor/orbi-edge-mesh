import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "research" / "distributed_feasibility.py"
spec = importlib.util.spec_from_file_location("distributed_feasibility", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class DistributedFeasibilityTests(unittest.TestCase):
    def test_transfer_time(self):
        # 1 MB decimal-equivalent payload at 8 Mbps = ~1 second.
        ms = mod.transfer_time_ms(1_000_000, 8.0)
        self.assertAlmostEqual(1000.0, ms, places=6)

    def test_slow_distributed_path_is_no_go(self):
        scenario = mod.Scenario(
            name="slow",
            payload_bytes_each_direction=1024,
            local_compute_ms=100.0,
            remote_compute_ms=120.0,
        )
        network = mod.NetworkProfile(
            rtt_ms=5.0,
            throughput_mbps=100.0,
            jitter_ms=1.0,
        )
        result = mod.evaluate(scenario, network)
        self.assertEqual("NO-GO", result.decision)

    def test_fast_remote_can_be_candidate(self):
        scenario = mod.Scenario(
            name="candidate",
            payload_bytes_each_direction=1024,
            local_compute_ms=1000.0,
            remote_compute_ms=400.0,
            orchestration_overhead_ms=5.0,
        )
        network = mod.NetworkProfile(
            rtt_ms=3.0,
            throughput_mbps=500.0,
            jitter_ms=1.0,
        )
        result = mod.evaluate(scenario, network)
        self.assertEqual("PHYSICAL-EXPERIMENT-CANDIDATE", result.decision)

    def test_network_bound_case_is_no_go(self):
        scenario = mod.Scenario(
            name="network-bound",
            payload_bytes_each_direction=32 * 1024 * 1024,
            local_compute_ms=1000.0,
            remote_compute_ms=300.0,
        )
        network = mod.NetworkProfile(
            rtt_ms=5.0,
            throughput_mbps=50.0,
            jitter_ms=2.0,
        )
        result = mod.evaluate(scenario, network)
        self.assertEqual("NO-GO", result.decision)


if __name__ == "__main__":
    unittest.main()
