from __future__ import annotations

from typing import Any


def generate_mock_npc_response(
    interview_context: dict[str, Any],
) -> str:
    """
    Generate a mock NPC response for testing the interview flow.

    This function does not call an LLM. It uses the evidence reaction guidance
    from the interview context when available, then falls back to a generic
    in-character response.

    Args:
        interview_context: Structured interview context from game_engine.py.

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
    mode: str = "mock",
) -> str:
    """
    Generate an NPC response.

    Args:
        interview_context: Structured interview context from game_engine.py.
        mode: Response generation mode. Currently only 'mock' is supported.

    Returns:
        NPC response string.

    Raises:
        ValueError: If an unsupported mode is provided.
    """
    if mode == "mock":
        return generate_mock_npc_response(interview_context)

    raise ValueError(f"Unsupported NPC response mode: {mode}")