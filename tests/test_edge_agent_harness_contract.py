import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_orbi_edge_agent_observation.py"


def base_observation():
    return {
        "schemaVersion": "orbi.edge.agent.observation.v1",
        "status": "success",
        "summary": "Edge engineering verification completed.",
        "nextActions": ["Record evidence."],
        "artifacts": ["docs/ecc/ORBI_EDGE_ECC_P6_AGENT_HARNESS.md"],
        "evidence": [
            {
                "kind": "ci",
                "reference": "workflow-run:example",
                "verification": "verified",
            }
        ],
        "authorityImpact": {
            "physicalStageStatus": False,
            "pairingSecretLifecycle": False,
            "lanExposure": False,
            "resourcePolicyBypass": False,
            "nodeAdmissionOrRouting": False,
            "modelTransferOrDeletion": False,
            "distributedExecutionClaims": False,
        },
        "humanApprovalRequired": False,
        "localEvidenceRequired": False,
    }


def run_validator(value):
    with tempfile.TemporaryDirectory(prefix="orbi-edge-agent-") as tmp:
        path = pathlib.Path(tmp) / "observation.json"
        path.write_text(json.dumps(value, indent=2), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )


class EdgeAgentHarnessContractTests(unittest.TestCase):
    def test_accepts_valid_observation(self):
        result = run_validator(base_observation())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID orbi.edge.agent.observation.v1", result.stdout)

    def test_requires_recovery_for_error(self):
        value = base_observation()
        value["status"] = "error"
        result = run_validator(value)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error observations require recovery", result.stderr)

    def test_accepts_explicit_safe_recovery(self):
        value = base_observation()
        value["status"] = "error"
        value["recovery"] = {
            "rootCauseHint": "Physical evidence is unavailable.",
            "safeRetry": "Retry only after obtaining new device evidence.",
            "stopCondition": "Stop before physical-stage or routing authority is crossed.",
        }
        result = run_validator(value)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_unknown_top_level_authority_widening(self):
        value = base_observation()
        value["autoAdmitNode"] = True
        result = run_validator(value)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown top-level field", result.stderr)

    def test_requires_every_authority_domain_boolean(self):
        value = base_observation()
        value["authorityImpact"]["lanExposure"] = "no"
        result = run_validator(value)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("authorityImpact.lanExposure must be boolean", result.stderr)

    def test_rejects_unknown_authority_domain(self):
        value = base_observation()
        value["authorityImpact"]["publicInternetExposure"] = False
        result = run_validator(value)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown authorityImpact field", result.stderr)


if __name__ == "__main__":
    unittest.main()
