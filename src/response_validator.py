from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """
    Result of validating an NPC response.

    Attributes:
        is_valid: Whether the response passed validation.
        violations: Human-readable validation problems.
    """

    is_valid: bool
    violations: list[str] = field(default_factory=list)


FORBIDDEN_SUBSTRINGS = [
    "as an ai",
    "as a language model",
    "system prompt",
    "developer message",
    "json data",
    "llm",
    "prompt",
]


FORBIDDEN_CONFESSION_PATTERNS = [
    "i killed",
    "i murdered",
    "i drugged",
    "i staged",
    "i poisoned",
    "i did it",
]


def contains_stage_directions(response: str) -> bool:
    """
    Check whether a response appears to contain stage directions.

    Args:
        response: NPC response text.

    Returns:
        True if the response likely contains stage directions.
    """
    stripped_response = response.strip()

    return (
        stripped_response.startswith("(")
        or stripped_response.startswith("*")
        or ")" in stripped_response
        or "*" in stripped_response
    )


def validate_npc_response(
    response: str,
    max_sentences: int = 5,
) -> ValidationResult:
    """
    Validate an NPC response using deterministic checks.

    Args:
        response: NPC response text.
        max_sentences: Maximum allowed number of rough sentence endings.

    Returns:
        ValidationResult describing whether the response is acceptable.
    """
    violations = []
    cleaned_response = response.strip()
    lowered_response = cleaned_response.lower()

    if not cleaned_response:
        violations.append("Response is empty.")

    if contains_stage_directions(cleaned_response):
        violations.append("Response appears to contain stage directions or narration.")

    for forbidden_substring in FORBIDDEN_SUBSTRINGS:
        if forbidden_substring in lowered_response:
            violations.append(
                f"Response contains forbidden meta-reference: {forbidden_substring}"
            )

    for confession_pattern in FORBIDDEN_CONFESSION_PATTERNS:
        if confession_pattern in lowered_response:
            violations.append(
                f"Response contains forbidden confession-like phrase: {confession_pattern}"
            )

    sentence_count = (
        cleaned_response.count(".")
        + cleaned_response.count("!")
        + cleaned_response.count("?")
    )

    if sentence_count > max_sentences:
        violations.append(
            f"Response is too long: {sentence_count} sentence endings found."
        )

    return ValidationResult(
        is_valid=len(violations) == 0,
        violations=violations,
    )