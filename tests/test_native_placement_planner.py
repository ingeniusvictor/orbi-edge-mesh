import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "manager" / "native_placement_planner.py"
spec = importlib.util.spec_from_file_location("native_placement_planner", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class NativePlacementPlannerTests(unittest.TestCase):
    def manifest(
        self,
        node_id,
        *,
        free_gib,
        ram_gib,
        action="ALLOW",
        models=None,
    ):
        gib = 1024 ** 3
        return {
            "node_id": node_id,
            "storage_available_bytes": int(free_gib * gib),
            "memory_total_bytes": int(ram_gib * gib),
            "resource_action": action,
            "available_model_ids": models or [],
        }

    def test_existing_model_is_kept(self):
        manifests = [
            self.manifest(
                "node-01",
                free_gib=20,
                ram_gib=12,
                models=["model-a"],
            ),
            self.manifest("node-02", free_gib=100, ram_gib=8),
        ]
        decision = mod.plan_native_model_placement(
            manifests,
            model_id="model-a",
            model_size_bytes=2 * 1024 ** 3,
            reserve_bytes=8 * 1024 ** 3,
        )
        self.assertEqual("keep_existing", decision.action)
        self.assertEqual("node-01", decision.node_id)

    def test_blocked_node_is_excluded(self):
        manifests = [
            self.manifest("blocked", free_gib=200, ram_gib=16, action="BLOCK"),
            self.manifest("allowed", free_gib=30, ram_gib=8, action="ALLOW"),
        ]
        decision = mod.plan_native_model_placement(
            manifests,
            model_id="model-a",
            model_size_bytes=2 * 1024 ** 3,
            reserve_bytes=8 * 1024 ** 3,
        )
        self.assertEqual("allowed", decision.node_id)

    def test_insufficient_storage_returns_none(self):
        manifests = [
            self.manifest("tiny", free_gib=9, ram_gib=12),
        ]
        decision = mod.plan_native_model_placement(
            manifests,
            model_id="model-a",
            model_size_bytes=2 * 1024 ** 3,
            reserve_bytes=8 * 1024 ** 3,
        )
        self.assertIsNone(decision)


if __name__ == "__main__":
    unittest.main()
