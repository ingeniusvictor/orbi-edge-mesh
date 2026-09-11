import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "manager" / "native_mesh_manager.py"
spec = importlib.util.spec_from_file_location("native_mesh_manager", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class NativeMeshRoutingTests(unittest.TestCase):
    def node(
        self,
        name,
        action="ALLOW",
        battery=80,
        loaded=True,
        paired=True,
        reachable=True,
    ):
        cfg = mod.NodeConfig(
            name=name,
            host="127.0.0.1",
            port=8080,
            node_id=name,
            token_env="TOKEN_ENV",
        )
        return mod.NodeState(
            config=cfg,
            reachable=reachable,
            resource_action=action,
            model_loaded=loaded,
            paired=paired,
            battery_percent=battery,
            services_supported=("CHAT",),
            model_ids=("qwen3-1.7b-q4_k_m-node01",),
        )

    def test_allow_beats_degrade(self):
        states = [
            self.node("degraded", action="DEGRADE", battery=100),
            self.node("allowed", action="ALLOW", battery=50),
        ]
        ordered = sorted(states, key=mod.candidate_rank)
        self.assertEqual("allowed", ordered[0].config.name)

    def test_higher_battery_breaks_allow_tie(self):
        states = [
            self.node("low", battery=40),
            self.node("high", battery=90),
        ]
        ordered = sorted(states, key=mod.candidate_rank)
        self.assertEqual("high", ordered[0].config.name)

    def test_blocked_is_not_eligible(self):
        self.assertFalse(mod.eligible(self.node("blocked", action="BLOCK")))

    def test_unpaired_is_not_eligible(self):
        self.assertFalse(mod.eligible(self.node("unpaired", paired=False)))

    def test_unloaded_is_not_eligible(self):
        self.assertFalse(mod.eligible(self.node("cold", loaded=False)))

    def test_wrong_service_is_not_eligible(self):
        state = self.node("chat-only")
        self.assertFalse(mod.eligible(state, service="ASR"))

    def test_wrong_model_is_not_eligible(self):
        state = self.node("qwen-only")
        self.assertFalse(mod.eligible(state, model_id="other-model"))

    def test_matching_service_and_model_is_eligible(self):
        state = self.node("chat-qwen")
        self.assertTrue(
            mod.eligible(
                state,
                service="CHAT",
                model_id="qwen3-1.7b-q4_k_m-node01",
            )
        )


if __name__ == "__main__":
    unittest.main()
