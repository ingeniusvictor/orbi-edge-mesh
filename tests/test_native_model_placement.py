import importlib.util
import sys
import unittest
from pathlib import Path


MESH_PATH = Path(__file__).parents[1] / "manager" / "native_mesh_manager.py"
mesh_spec = importlib.util.spec_from_file_location("native_mesh_manager", MESH_PATH)
mesh = importlib.util.module_from_spec(mesh_spec)
sys.modules[mesh_spec.name] = mesh
mesh_spec.loader.exec_module(mesh)

PLACEMENT_PATH = Path(__file__).parents[1] / "manager" / "native_model_placement.py"
placement_spec = importlib.util.spec_from_file_location("native_model_placement", PLACEMENT_PATH)
placement = importlib.util.module_from_spec(placement_spec)
sys.modules[placement_spec.name] = placement
placement_spec.loader.exec_module(placement)


class PlacementTests(unittest.TestCase):
    def state(
        self,
        name,
        free_gib,
        total_gib=256,
        action="ALLOW",
        paired=True,
        services=("CHAT",),
        loaded=False,
        model_ids=(),
    ):
        cfg = mesh.NodeConfig(
            name=name,
            host="127.0.0.1",
            port=8080,
            node_id=name,
            token_env="TOKEN_ENV",
        )
        return mesh.NodeState(
            config=cfg,
            reachable=True,
            resource_action=action,
            paired=paired,
            storage_total_bytes=total_gib * placement.GIB,
            storage_available_bytes=free_gib * placement.GIB,
            services_supported=services,
            model_loaded=loaded,
            model_ids=model_ids,
            battery_percent=80,
        )

    def model(self, size_gib=2):
        return placement.ModelEntry(
            id="model-a",
            display_name="Model A",
            approx_size_bytes=size_gib * placement.GIB,
            service="CHAT",
        )

    def test_reserve_is_larger_of_8gib_or_ten_percent(self):
        self.assertEqual(
            8 * placement.GIB,
            placement.reserve_bytes(64 * placement.GIB),
        )
        self.assertEqual(
            30 * placement.GIB,
            placement.reserve_bytes(300 * placement.GIB),
        )

    def test_candidate_rejected_when_projected_free_breaks_reserve(self):
        candidate = placement.build_candidate(
            self.state("small", free_gib=9, total_gib=64),
            self.model(size_gib=2),
        )
        self.assertIsNone(candidate)

    def test_resident_model_is_preferred(self):
        model = self.model(size_gib=2)
        states = [
            self.state("cold", free_gib=100),
            self.state(
                "resident",
                free_gib=60,
                loaded=True,
                model_ids=("model-a",),
            ),
        ]
        result = placement.plan(states, model, replicas=1)
        self.assertEqual("resident", result["selected"][0]["node_name"])

    def test_blocked_node_is_rejected(self):
        candidate = placement.build_candidate(
            self.state("blocked", free_gib=100, action="BLOCK"),
            self.model(),
        )
        self.assertIsNone(candidate)

    def test_wrong_service_is_rejected(self):
        candidate = placement.build_candidate(
            self.state("asr-only", free_gib=100, services=("ASR",)),
            self.model(),
        )
        self.assertIsNone(candidate)


if __name__ == "__main__":
    unittest.main()
