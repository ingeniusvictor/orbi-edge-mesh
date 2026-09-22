#!/usr/bin/env python3
import argparse
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

FILES = (
    ("always-instructions", "AGENTS.md"),
    ("discoverable-skill", ".agents/skills/orbi-edge-physical-evidence-review/SKILL.md"),
    ("discoverable-skill", ".agents/skills/orbi-edge-node-trust-review/SKILL.md"),
    ("discoverable-skill", ".agents/skills/orbi-edge-agent-harness/SKILL.md"),
    ("discoverable-skill", ".agents/skills/orbi-edge-context-budget/SKILL.md"),
    ("config-reference", ".orbi/ecc-profile.json"),
    ("config-reference", ".orbi/repository-adapter.json"),
    ("config-reference", ".orbi/orbi-edge-agent-observation-v1.schema.json"),
)

PROTECTED_INVARIANTS = (
    "CI GREEN != PHYSICAL NODE CERTIFIED",
    "SIGNED REQUEST AUTHENTICATED != TRANSPORT ENCRYPTED",
    "LAN API READY != SAFE FOR PUBLIC INTERNET EXPOSURE",
    "NODE DISCOVERED != NODE TRUSTED / ELIGIBLE",
    "WHOLE-WORKLOAD ROUTING != UNIFIED RAM / DISTRIBUTED MODEL EXECUTION",
    "Do not bypass BLOCK/DEGRADE policy",
)


def estimate(text: str) -> int:
    words = len(text.split())
    return math.ceil(max(len(text) / 4, words * 1.3))


def build_report() -> dict:
    rows = []
    totals = {
        "persistentEstimateTokens": 0,
        "discoverableIfAllLoadedTokens": 0,
        "configIfAllLoadedTokens": 0,
    }

    for kind, relative in FILES:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"CONTEXT_BUDGET_FILE_MISSING:{relative}")
        text = path.read_text(encoding="utf-8")
        tokens = estimate(text)
        rows.append(
            {
                "kind": kind,
                "path": relative,
                "lines": len(text.splitlines()),
                "estimatedTokens": tokens,
            }
        )
        if kind == "always-instructions":
            totals["persistentEstimateTokens"] += tokens
        elif kind == "discoverable-skill":
            totals["discoverableIfAllLoadedTokens"] += tokens
        elif kind == "config-reference":
            totals["configIfAllLoadedTokens"] += tokens

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    protected = {
        invariant: invariant in agents
        for invariant in PROTECTED_INVARIANTS
    }
    missing = [name for name, present in protected.items() if not present]
    if missing:
        raise RuntimeError("CONTEXT_BUDGET_PROTECTED_INVARIANT_MISSING:" + "|".join(missing))

    return {
        "schemaVersion": "orbi.edge.context-budget.v1",
        "loadingModel": {
            "alwaysInstructions": "persistent",
            "discoverableSkills": "conditional",
            "configReferences": "on-demand",
        },
        "totals": totals,
        "protectedInvariants": protected,
        "files": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        report = build_report()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    for row in report["files"]:
        print(
            f'{row["kind"]}\t{row["lines"]} lines\t'
            f'~{row["estimatedTokens"]} tokens\t{row["path"]}'
        )
    print(f'persistent_estimate\t~{report["totals"]["persistentEstimateTokens"]}')
    print(
        "discoverable_if_all_loaded\t~"
        f'{report["totals"]["discoverableIfAllLoadedTokens"]}'
    )
    print(f'config_if_all_loaded\t~{report["totals"]["configIfAllLoadedTokens"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
