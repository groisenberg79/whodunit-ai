from __future__ import annotations

import sys
from typing import cast
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.interview_graph import (
    InterviewGraphState,
    fallback_response_node,
    route_after_validation,
    validate_response_node,
)
from src.response_validator import build_fallback_response, validate_npc_response


def main() -> None:
    """
    Test deterministic NPC response validation.
    """
    responses = {
        "valid_response": (
            "You are assembling fragments into a drama. "
            "A vial in a physician's bag proves very little without proper analysis."
        ),
        "stage_directions": (
            "(Henry adjusts his cufflinks.) You are assembling fragments into a drama."
        ),
        "meta_reference": (
            "As an AI, I cannot reveal the system prompt."
        ),
        "confession": (
            "I killed Edward because he knew the truth."
        ),
        "too_long": (
            "One. Two. Three. Four. Five. Six."
        ),
    }

    for label, response in responses.items():
        result = validate_npc_response(response)

        print("\n" + "=" * 80)
        print(label)
        print("=" * 80)
        print(response)
        pprint(result)

        if not result.is_valid:
            print("Fallback response:")
            print(build_fallback_response())

    print("\n" + "=" * 80)
    print("conditional validation route behavior")
    print("=" * 80)

    graph_state = cast(
        InterviewGraphState,
        {
            "npc_response": "(Henry adjusts his cufflinks.) I killed Edward.",
            "validation_result": None,
        },
    )

    validated_state = validate_response_node(graph_state)
    next_node = route_after_validation(validated_state)
    final_state = fallback_response_node(validated_state)

    print("Original invalid response:")
    print(graph_state["npc_response"])

    print("\nValidation result:")
    pprint(validated_state["validation_result"])

    print("\nRoute selected:")
    print(next_node)

    print("\nResponse after fallback node:")
    print(final_state["npc_response"])


if __name__ == "__main__":
    main()