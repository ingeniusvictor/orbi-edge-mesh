#!/usr/bin/env python3
"""Workload profiles for ORBI Edge Mesh."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkloadProfile:
    workload_type: str
    service_type: str
    latency_sensitivity: str
    expected_duration: str
    thermal_sensitivity: str
    preferred_model_tag: str | None
    notes: str


PROFILES: dict[str, WorkloadProfile] = {
    "chat_short": WorkloadProfile(
        workload_type="chat_short",
        service_type="llm",
        latency_sensitivity="high",
        expected_duration="short",
        thermal_sensitivity="medium",
        preferred_model_tag="fast-chat",
        notes="Short interactive assistant turn.",
    ),
    "generation_long": WorkloadProfile(
        workload_type="generation_long",
        service_type="llm",
        latency_sensitivity="medium",
        expected_duration="long",
        thermal_sensitivity="high",
        preferred_model_tag="long-generation",
        notes="Long-form generation where sustained thermals matter.",
    ),
    "embedding": WorkloadProfile(
        workload_type="embedding",
        service_type="embedding",
        latency_sensitivity="medium",
        expected_duration="short",
        thermal_sensitivity="low",
        preferred_model_tag="embedding",
        notes="Vector generation for retrieval/indexing.",
    ),
    "speech_to_text": WorkloadProfile(
        workload_type="speech_to_text",
        service_type="speech_to_text",
        latency_sensitivity="medium",
        expected_duration="medium",
        thermal_sensitivity="medium",
        preferred_model_tag="stt",
        notes="Local transcription workload.",
    ),
    "text_to_speech": WorkloadProfile(
        workload_type="text_to_speech",
        service_type="text_to_speech",
        latency_sensitivity="high",
        expected_duration="short",
        thermal_sensitivity="low",
        preferred_model_tag="tts",
        notes="Interactive local voice synthesis.",
    ),
}


def get_profile(workload_type: str) -> WorkloadProfile:
    try:
        return PROFILES[workload_type]
    except KeyError as exc:
        raise ValueError(f"Unknown workload_type: {workload_type}") from exc
