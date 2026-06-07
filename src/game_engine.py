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