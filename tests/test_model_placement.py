import unittest

from models.placement import choose_storage_node
from models.storage_manager import StoragePolicy, can_place_model


def cap(node_id, total, free, ram):
    return {
        "node_id": node_id,
        "resources": {
            "storage_total_mb": total,
            "storage_free_mb": free,
            "physical_ram_mb": ram,
        },
        "services": [],
    }


class StoragePolicyTests(unittest.TestCase):
    def test_reserve_is_preserved(self):
        capability = cap("node-01", 100000, 30000, 12000)
        self.assertTrue(
            can_place_model(
                capability,
                model_size_mb=10000,
                policy=StoragePolicy(
                    min_free_storage_mb=8000,
                    reserve_fraction=0.10,
                ),
            )
        )

    def test_rejects_if_reserve_would_be_broken(self):
        capability = cap("node-01", 100000, 15000, 12000)
        self.assertFalse(
            can_place_model(
                capability,
                model_size_mb=10000,
                policy=StoragePolicy(
                    min_free_storage_mb=8000,
                    reserve_fraction=0.10,
                ),
            )
        )


class PlacementTests(unittest.TestCase):
    def test_prefers_more_storage_headroom(self):
        nodes = [
            cap("node-01", 500000, 200000, 12000),
            cap("node-02", 250000, 120000, 8000),
        ]
        d = choose_storage_node(
            nodes,
            model_id="new-model",
            model_size_mb=5000,
        )
        self.assertEqual(d.node_id, "node-01")

    def test_no_candidate_when_storage_too_low(self):
        nodes = [
            cap("node-01", 50000, 9000, 12000),
            cap("node-02", 50000, 7000, 8000),
        ]
        d = choose_storage_node(
            nodes,
            model_id="large-model",
            model_size_mb=5000,
            min_free_after_mb=8192,
        )
        self.assertIsNone(d)


if __name__ == "__main__":
    unittest.main()
