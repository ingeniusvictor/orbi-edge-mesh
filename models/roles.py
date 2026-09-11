#!/usr/bin/env python3
"""Model role assignments across ORBI Edge nodes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRole:
    model_id: str
    role: str
    preferred_node_id: str | None
    residency: str


VALID_ROLES = {
    "primary",
    "fallback",
    "specialized",
    "replica",
}

VALID_RESIDENCY = {
    "hot",
    "warm",
    "cold",
}


def validate_role(role: ModelRole) -> None:
    if role.role not in VALID_ROLES:
        raise ValueError(f"invalid model role: {role.role}")
    if role.residency not in VALID_RESIDENCY:
        raise ValueError(f"invalid residency: {role.residency}")
