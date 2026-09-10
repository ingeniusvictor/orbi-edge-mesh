#!/usr/bin/env python3
"""Bridge node lifecycle recovery with ORBI thermal/power policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from policy.thermal_power import evaluate_node_policy


@dataclass(frozen=True)
class RecoveryAuthorization:
    allowed: bool
    action: str
    reason: str


def authorize_recovery(capability: dict[str, Any]) -> RecoveryAuthorization:
    decision = evaluate_node_policy(capability)

    if not decision.allow_new_work:
        return RecoveryAuthorization(
            allowed=False,
            action="block_restart",
            reason=(
                f"policy blocked recovery: "
                f"thermal={decision.thermal.state}/{decision.thermal.action}, "
                f"power={decision.power.state}/{decision.power.action}"
            ),
        )

    return RecoveryAuthorization(
        allowed=True,
        action="allow_restart",
        reason=(
            f"policy allows recovery: "
            f"thermal={decision.thermal.state}/{decision.thermal.action}, "
            f"power={decision.power.state}/{decision.power.action}"
        ),
    )
