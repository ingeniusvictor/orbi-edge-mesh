import json
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ecc_orbi_edge_context_budget.py"


def report():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stderr)
    return json.loads(completed.stdout)


class EdgeContextBudgetTests(unittest.TestCase):
    def test_reports_layered_loading_model(self):
        value = report()
        self.assertEqual(value["schemaVersion"], "orbi.edge.context-budget.v1")
        self.assertEqual(value["loadingModel"]["alwaysInstructions"], "persistent")
        self.assertEqual(value["loadingModel"]["discoverableSkills"], "conditional")
        self.assertEqual(value["loadingModel"]["configReferences"], "on-demand")
        self.assertEqual(
            len([x for x in value["files"] if x["kind"] == "discoverable-skill"]),
            4,
        )
        self.assertGreater(value["totals"]["persistentEstimateTokens"], 0)
        self.assertGreater(value["totals"]["discoverableIfAllLoadedTokens"], 0)
        self.assertGreater(value["totals"]["configIfAllLoadedTokens"], 0)

    def test_project_skills_are_never_persistent(self):
        value = report()
        skill_rows = [x for x in value["files"] if "/skills/" in x["path"]]
        self.assertEqual(len(skill_rows), 4)
        for row in skill_rows:
            self.assertEqual(row["kind"], "discoverable-skill")

    def test_only_agents_is_persistent(self):
        value = report()
        persistent = [x for x in value["files"] if x["kind"] == "always-instructions"]
        self.assertEqual([x["path"] for x in persistent], ["AGENTS.md"])

    def test_protected_edge_invariants_remain_present(self):
        value = report()
        self.assertTrue(value["protectedInvariants"])
        self.assertTrue(all(value["protectedInvariants"].values()))


if __name__ == "__main__":
    unittest.main()
