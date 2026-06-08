from __future__ import annotations

from typing import Any

from src.game_state import GameState


class GameEngineError(Exception):
    """Raised when a game engine operation fails."""


def get_inspectable_area(
    location: dict[str, Any],
    area_id: str,
) -> dict[str, Any]:
    """
    Return an inspectable area from a location by area ID.

    Args:
        location: Location dictionary from locations.json.
        area_id: ID of the inspectable area.

    Returns:
        Inspectable area dictionary matching the given ID.

    Raises:
        KeyError: If no inspectable area with the given ID is found.
    """
    for area in location["inspectable_areas"]:
        if area["id"] == area_id:
            return area

    raise KeyError(f"Inspectable area not found: {area_id}")


def inspect_location_area(
    state: GameState,
    location: dict[str, Any],
    area_id: str,
) -> dict[str, Any]:
    """
    Inspect an area inside a location and update the game state if a clue is found.

    Args:
        state: Current GameState object.
        location: Location dictionary from locations.json.
        area_id: ID of the inspectable area selected by the player.

    Returns:
        Dictionary describing the result of the inspection.

    Raises:
        KeyError: If the inspectable area does not exist.
    """
    state.mark_location_visited(location["id"])

    area = get_inspectable_area(location, area_id)

    result = {
        "location_id": location["id"],
        "area_id": area["id"],
        "area_label": area["label"],
        "result_text": area["result_text"],
        "has_clue": area["has_clue"],
        "clue_id": area["clue_id"],
        "newly_discovered": False,
    }

    if area["has_clue"]:
        clue_id = area["clue_id"]

        if clue_id is None:
            raise GameEngineError(
                f"Area '{area_id}' in location '{location['id']}' has_clue=True but clue_id=None."
            )

        newly_discovered = state.mark_clue_discovered(clue_id)
        result["newly_discovered"] = newly_discovered

    return result


def get_discovered_clues(
    state: GameState,
    clues_data: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Return full clue dictionaries for all clues discovered by the player.

    Args:
        state: Current GameState object.
        clues_data: Loaded clues data from clues.json.

    Returns:
        List of clue dictionaries discovered by the player.
    """
    discovered = []

    for clue in clues_data["clues"]:
        if clue["id"] in state.discovered_clues:
            discovered.append(clue)

    return discovered


def get_available_evidence_for_interview(
    state: GameState,
    clues_data: dict[str, Any],
    suspect_id: str,
) -> list[dict[str, Any]]:
    """
    Return discovered clues that can be used to confront a specific suspect.

    Args:
        state: Current GameState object.
        clues_data: Loaded clues data from clues.json.
        suspect_id: ID of the suspect being interviewed.

    Returns:
        List of discovered clue dictionaries that can confront the selected suspect.
    """
    available_evidence = []

    for clue in clues_data["clues"]:
        if (
            clue["id"] in state.discovered_clues
            and suspect_id in clue["confrontation_targets"]
        ):
            available_evidence.append(clue)

    return available_evidence

def can_confront_suspect_with_clue(
    state: GameState,
    clues_data: dict[str, Any],
    suspect_id: str,
    clue_id: str,
) -> bool:
    """
    Check whether a discovered clue can be used to confront a specific suspect.

    Args:
        state: Current GameState object.
        clues_data: Loaded clues data from clues.json.
        suspect_id: ID of the suspect being interviewed.
        clue_id: ID of the clue selected as confronted evidence.

    Returns:
        True if the clue has been discovered and can be used to confront the suspect,
        False otherwise.
    """
    if clue_id not in state.discovered_clues:
        return False

    for clue in clues_data["clues"]:
        if clue["id"] == clue_id:
            return suspect_id in clue["confrontation_targets"]

    return False


def get_applicable_evidence_reaction(
    state: GameState,
    suspect: dict[str, Any],
    confronted_clue_id: str,
) -> dict[str, Any] | None:
    """
    Return the best evidence reaction for a suspect and confronted clue.

    Combo evidence reactions are checked first. If no combo reaction applies,
    the function falls back to the suspect's single-clue evidence reaction.

    Args:
        state: Current GameState object.
        suspect: Suspect dictionary from characters.json.
        confronted_clue_id: ID of the clue selected as confronted evidence.

    Returns:
        Evidence reaction dictionary if one applies, otherwise None.
    """
    combo_reactions = suspect.get("combo_evidence_reactions", [])

    for reaction in combo_reactions:
        required_clue_ids = set(reaction["required_clue_ids"])
        trigger_clue_ids = set(reaction["trigger_clue_ids"])

        if (
            confronted_clue_id in trigger_clue_ids
            and required_clue_ids.issubset(state.discovered_clues)
        ):
            return reaction

    return suspect.get("evidence_reactions", {}).get(confronted_clue_id)


def build_interview_context(
    state: GameState,
    game_data: dict[str, dict[str, Any]],
    suspect_id: str,
    player_question: str,
    confronted_clue_id: str | None = None,
) -> dict[str, Any]:
    """
    Build structured context for a suspect interview.

    This function does not call the LLM. It prepares the information that will later
    be passed to the prompt builder and NPC engine.

    Args:
        state: Current GameState object.
        game_data: Dictionary containing all loaded game data.
        suspect_id: ID of the suspect being interviewed.
        player_question: Free-form question asked by the player.
        confronted_clue_id: Optional clue ID used to confront the suspect.

    Returns:
        Dictionary containing interview context.

    Raises:
        ValueError: If the suspect does not exist, or if the confronted clue has not
            been discovered or cannot be used to confront the selected suspect.
    """
    characters = game_data["characters"]["characters"]
    clues = game_data["clues"]["clues"]

    suspect = None
    for character in characters:
        if character["id"] == suspect_id:
            suspect = character
            break

    if suspect is None:
        raise ValueError(f"Unknown suspect ID: {suspect_id}")

    confronted_clue = None
    evidence_reaction = None

    if confronted_clue_id is not None:
        can_confront = can_confront_suspect_with_clue(
            state=state,
            clues_data=game_data["clues"],
            suspect_id=suspect_id,
            clue_id=confronted_clue_id,
        )

        if not can_confront:
            raise ValueError(
                f"Clue '{confronted_clue_id}' cannot be used to confront suspect '{suspect_id}'."
            )

        for clue in clues:
            if clue["id"] == confronted_clue_id:
                confronted_clue = clue
                break

        evidence_reaction = get_applicable_evidence_reaction(
            state=state,
            suspect=suspect,
            confronted_clue_id=confronted_clue_id,
        )

    return {
        "suspect": suspect,
        "player_question": player_question,
        "confronted_clue": confronted_clue,
        "evidence_reaction": evidence_reaction,
        "discovered_clue_ids": state.discovered_clues,
        "revealed_clue_ids_for_suspect": state.revealed_clues[suspect_id],
        "dialogue_history": [
            entry.__dict__
            for entry in state.dialogue_history
            if entry.suspect_id == suspect_id
        ],
    }


def record_interview_exchange(
    state: GameState,
    game_data: dict[str, dict[str, Any]],
    suspect_id: str,
    player_question: str,
    npc_response: str,
    confronted_clue_id: str | None = None,
) -> dict[str, Any]:
    """
    Record an interview exchange and update evidence confrontation state.

    Args:
        state: Current GameState object.
        game_data: Dictionary containing all loaded game data.
        suspect_id: ID of the suspect being interviewed.
        player_question: Free-form question asked by the player.
        npc_response: Response given by the NPC.
        confronted_clue_id: Optional clue ID used to confront the suspect.

    Returns:
        Dictionary version of the created dialogue entry.

    Raises:
        ValueError: If the confronted clue is invalid for the selected suspect.
    """
    if confronted_clue_id is not None:
        can_confront = can_confront_suspect_with_clue(
            state=state,
            clues_data=game_data["clues"],
            suspect_id=suspect_id,
            clue_id=confronted_clue_id,
        )

        if not can_confront:
            raise ValueError(
                f"Clue '{confronted_clue_id}' cannot be used to confront suspect '{suspect_id}'."
            )

    entry = state.add_dialogue_entry(
        suspect_id=suspect_id,
        player_question=player_question,
        npc_response=npc_response,
        confronted_clue_id=confronted_clue_id,
    )

    return entry.__dict__