from __future__ import annotations

from typing import Any

from src.llm_client import LLMMode, generate_llm_response


def generate_mock_npc_response(interview_context: dict[str, Any]) -> str:
    """
    Generate a deterministic mock NPC response from interview context.

    Args:
        interview_context: Structured interview context.

    Returns:
        Mock NPC response string.
    """
    suspect = interview_context["suspect"]
    evidence_reaction = interview_context["evidence_reaction"]
    confronted_clue = interview_context["confronted_clue"]

    if evidence_reaction is not None:
        return evidence_reaction.get(
            "sample_response",
            f"{suspect['name']} reacts carefully to the evidence but reveals nothing decisive.",
        )

    if confronted_clue is not None:
        return (
            f"{suspect['name']} studies the evidence carefully, but offers no clear admission."
        )

    return (
        f"{suspect['name']} answers cautiously, revealing little beyond what is already known."
    )


def generate_npc_response(
    interview_context: dict[str, Any],
    messages: list[dict[str, str]] | None = None,
    mode: LLMMode = "mock",
    model_name: str = "llama3.1:8b",
) -> str:
    """
    Generate an NPC response.

    Args:
        interview_context: Structured interview context.
        messages: Optional chat-style messages for a real LLM.
        mode: Response generation mode.
        model_name: Model name for LLM backends.

    Returns:
        NPC response string.
    """
    if mode == "mock":
        return generate_mock_npc_response(interview_context)

    if messages is None:
        raise ValueError("messages must be provided when using a real LLM mode.")

    return generate_llm_response(
        messages=messages,
        mode=mode,
        model_name=model_name,
    )