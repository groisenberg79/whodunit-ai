from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.response_validator import validate_npc_response


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


if __name__ == "__main__":
    main()