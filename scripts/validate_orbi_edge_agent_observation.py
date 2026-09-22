#!/usr/bin/env python3
import json
import pathlib
import sys

ALLOWED_TOP = {
    "schemaVersion", "status", "summary", "nextActions", "artifacts",
    "evidence", "authorityImpact", "humanApprovalRequired",
    "localEvidenceRequired", "recovery",
}
STATUSES = {"success", "warning", "error"}
EVIDENCE_KINDS = {"git", "test", "ci", "file", "artifact", "runtime", "external"}
VERIFICATION = {"verified", "observed", "unverified"}
AUTHORITY_KEYS = (
    "physicalStageStatus",
    "pairingSecretLifecycle",
    "lanExposure",
    "resourcePolicyBypass",
    "nodeAdmissionOrRouting",
    "modelTransferOrDeletion",
    "distributedExecutionClaims",
)
RECOVERY_KEYS = {"rootCauseHint", "safeRetry", "stopCondition"}


def fail(message: str) -> int:
    print(f"INVALID: {message}", file=sys.stderr)
    return 1


def non_empty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(value) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["top-level value must be an object"]

    for key in value:
        if key not in ALLOWED_TOP:
            errors.append(f"unknown top-level field: {key}")

    if value.get("schemaVersion") != "orbi.edge.agent.observation.v1":
        errors.append("schemaVersion must be orbi.edge.agent.observation.v1")
    if value.get("status") not in STATUSES:
        errors.append("invalid status")
    if not non_empty(value.get("summary")):
        errors.append("summary must be non-empty")

    for key in ("nextActions", "artifacts", "evidence"):
        if not isinstance(value.get(key), list):
            errors.append(f"{key} must be an array")

    if isinstance(value.get("nextActions"), list):
        if any(not non_empty(item) for item in value["nextActions"]):
            errors.append("nextActions entries must be non-empty strings")
    if isinstance(value.get("artifacts"), list):
        if any(not non_empty(item) for item in value["artifacts"]):
            errors.append("artifacts entries must be non-empty strings")

    if isinstance(value.get("evidence"), list):
        for item in value["evidence"]:
            if not isinstance(item, dict):
                errors.append("evidence entries must be objects")
                continue
            for key in item:
                if key not in {"kind", "reference", "verification"}:
                    errors.append(f"unknown evidence field: {key}")
            if item.get("kind") not in EVIDENCE_KINDS:
                errors.append("invalid evidence.kind")
            if not non_empty(item.get("reference")):
                errors.append("evidence.reference must be non-empty")
            if item.get("verification") not in VERIFICATION:
                errors.append("invalid evidence.verification")

    authority = value.get("authorityImpact")
    if not isinstance(authority, dict):
        errors.append("authorityImpact must be an object")
    else:
        for key in authority:
            if key not in AUTHORITY_KEYS:
                errors.append(f"unknown authorityImpact field: {key}")
        for key in AUTHORITY_KEYS:
            if type(authority.get(key)) is not bool:
                errors.append(f"authorityImpact.{key} must be boolean")

    for key in ("humanApprovalRequired", "localEvidenceRequired"):
        if key in value and type(value[key]) is not bool:
            errors.append(f"{key} must be boolean")

    if value.get("status") == "error":
        recovery = value.get("recovery")
        if not isinstance(recovery, dict):
            errors.append("error observations require recovery")
        else:
            for key in recovery:
                if key not in RECOVERY_KEYS:
                    errors.append(f"unknown recovery field: {key}")
            for key in ("rootCauseHint", "safeRetry", "stopCondition"):
                if not non_empty(recovery.get(key)):
                    errors.append(f"recovery.{key} must be non-empty")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        return fail("usage: python scripts/validate_orbi_edge_agent_observation.py <observation.json>")

    path = pathlib.Path(sys.argv[1])
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot parse JSON: {exc}")

    errors = validate(value)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    print("VALID orbi.edge.agent.observation.v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
