from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data_loader import get_location_by_id, load_game_data
from src.game_engine import (
    build_interview_context,
    get_available_evidence_for_interview,
    inspect_location_area,
    record_interview_exchange,
    submit_accusation,
)
from src.game_state import GameState


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
    Run a terminal-based smoke test of the core game engine.

    This test checks:
    - loading JSON game data,
    - initializing GameState,
    - visiting locations,
    - discovering clues,
    - checking available confrontation evidence,
    - building interview context,
    - recording dialogue,
    - submitting a final accusation.
    """
    print_section("1. Load game data")

    game_data = load_game_data()
    print("Loaded data files:")
    print(game_data.keys())

    print_section("2. Initialize game state")

    state = GameState.from_case_data(game_data["case"])
    pprint(state.to_dict())

    print_section("3. Inspect Beatrice's room and discover letters")

    beatrice_room = get_location_by_id(game_data, "beatrice_room")

    result = inspect_location_area(
        state=state,
        location=beatrice_room,
        area_id="writing_box",
    )

    pprint(result)
    print("Discovered clues:", state.discovered_clues)

    print_section("4. Check evidence available when interviewing Beatrice")

    available_evidence = get_available_evidence_for_interview(
        state=state,
        clues_data=game_data["clues"],
        suspect_id="beatrice_ashford",
    )

    print([clue["id"] for clue in available_evidence])

    print_section("5. Build interview context for Beatrice")

    context = build_interview_context(
        state=state,
        game_data=game_data,
        suspect_id="beatrice_ashford",
        player_question="I found your letters to Edward. You were furious.",
        confronted_clue_id="beatrice_letters",
    )

    print("Suspect:", context["suspect"]["name"])
    print("Confronted clue:", context["confronted_clue"]["name"])
    print("Evidence reaction:")
    pprint(context["evidence_reaction"])

    print_section("6. Record interview exchange")

    dialogue_entry = record_interview_exchange(
        state=state,
        game_data=game_data,
        suspect_id="beatrice_ashford",
        player_question="I found your letters to Edward. You were furious.",
        npc_response="I wrote them, yes. But I did not kill him.",
        confronted_clue_id="beatrice_letters",
    )

    pprint(dialogue_entry)
    print("Revealed clues:")
    pprint(state.revealed_clues)

    print_section("7. Discover Henry solution clues")

    library = get_location_by_id(game_data, "library")
    henry_room = get_location_by_id(game_data, "henry_room")

    inspect_location_area(
        state=state,
        location=library,
        area_id="brandy_glass",
    )

    inspect_location_area(
        state=state,
        location=henry_room,
        area_id="medical_bag",
    )

    inspect_location_area(
        state=state,
        location=henry_room,
        area_id="henry_locked_drawer",
    )

    print("Discovered clues:")
    pprint(state.discovered_clues)

    print_section("8. Build combo evidence context for Henry")

    henry_context = build_interview_context(
        state=state,
        game_data=game_data,
        suspect_id="henry_ashford",
        player_question="The vial and the brandy residue seem connected.",
        confronted_clue_id="medical_vial",
    )

    print("Suspect:", henry_context["suspect"]["name"])
    print("Confronted clue:", henry_context["confronted_clue"]["name"])
    print("Evidence reaction:")
    pprint(henry_context["evidence_reaction"])

    print_section("9. Submit correct accusation")

    accusation_result = submit_accusation(
        state=state,
        game_data=game_data,
        culprit_id="henry_ashford",
        motive_id="exposure_hidden_medical_crime",
        method_id="drugged_brandy_and_staged_stabbing",
        evidence_ids=[
            "medical_vial",
            "brandy_glass_residue",
            "altered_death_certificate",
        ],
    )

    pprint(accusation_result)
    print("Final game status:", state.game_status)

    print_section("10. Final state")

    pprint(state.to_dict())


if __name__ == "__main__":
    main()