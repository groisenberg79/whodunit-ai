from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import get_location_by_id, load_game_data
from src.game_engine import (
    build_interview_context,
    inspect_location_area,
    record_interview_exchange,
)
from src.game_state import GameState
from src.npc_engine import generate_npc_response
from src.prompt_builder import build_npc_messages


def print_section(title: str) -> None:
    """
    Print a readable section title.

    Args:
        title: Section title to display.
    """
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    """
    Test the mock NPC response layer.
    """
    game_data = load_game_data()
    state = GameState.from_case_data(game_data["case"])

    print_section("1. Discover Beatrice's letters")

    beatrice_room = get_location_by_id(game_data, "beatrice_room")

    inspect_result = inspect_location_area(
        state=state,
        location=beatrice_room,
        area_id="writing_box",
    )

    pprint(inspect_result)

    print_section("2. Build interview context")

    interview_context = build_interview_context(
        state=state,
        game_data=game_data,
        suspect_id="beatrice_ashford",
        player_question=(
            "I found your letters to Edward. "
            "You were furious after he ended the affair. Did you kill him?"
        ),
        confronted_clue_id="beatrice_letters",
    )

    print("Evidence reaction:")
    pprint(interview_context["evidence_reaction"])

    print_section("3. Build prompt messages")

    messages = build_npc_messages(
        game_data=game_data,
        interview_context=interview_context,
    )

    print("System prompt preview:")
    print(messages[0]["content"][:800])

    print("\nUser prompt preview:")
    print(messages[1]["content"][:800])

    print_section("4. Generate mock NPC response")

    npc_response = generate_npc_response(
        interview_context=interview_context,
        mode="mock",
    )

    print(npc_response)

    print_section("5. Record interview exchange")

    dialogue_entry = record_interview_exchange(
        state=state,
        game_data=game_data,
        suspect_id="beatrice_ashford",
        player_question=interview_context["player_question"],
        npc_response=npc_response,
        confronted_clue_id="beatrice_letters",
    )

    pprint(dialogue_entry)

    print_section("6. Final state")

    pprint(state.to_dict())


if __name__ == "__main__":
    main()