#!/usr/bin/env python3
"""Simple deterministic workload classifier.

Phase 0 deliberately avoids ML-based classification.
"""

from __future__ import annotations


def classify_workload(
    *,
    service_type: str,
    requested_output_tokens: int | None = None,
) -> str:
    if service_type == "embedding":
        return "embedding"
    if service_type == "speech_to_text":
        return "speech_to_text"
    if service_type == "text_to_speech":
        return "text_to_speech"
    if service_type == "llm":
        if requested_output_tokens is not None and requested_output_tokens > 512:
            return "generation_long"
        return "chat_short"
    return service_type
