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
    confronted_clue_ids: list[str] | None = None,
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
    presented_clue_ids = set(confronted_clue_ids or [confronted_clue_id])
    combo_reactions = suspect.get("combo_evidence_reactions", [])

    for reaction in combo_reactions:
        required_clue_ids = set(reaction["required_clue_ids"])
        trigger_clue_ids = set(reaction["trigger_clue_ids"])

        if (
            required_clue_ids.issubset(presented_clue_ids)
            and trigger_clue_ids.intersection(presented_clue_ids)
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
    confronted_clue_ids: list[str] | None = None,
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
    locations = game_data.get("locations", {}).get("locations", [])
    location_names_by_id = {
        location["id"]: location["name"]
        for location in locations
    }

    suspect = None
    for character in characters:
        if character["id"] == suspect_id:
            suspect = character
            break

    if suspect is None:
        raise ValueError(f"Unknown suspect ID: {suspect_id}")

    crime_time_location_name = location_names_by_id.get(
        suspect["alibi"].get("crime_time_location_id"),
        suspect["alibi"].get("crime_time_location_id"),
    )

    suspect_last_name = suspect["name"].split()[-1]
    crime_time_location_spoken_name = crime_time_location_name

    if isinstance(crime_time_location_name, str) and (
        crime_time_location_name.startswith(suspect["name"] + "'s ")
        or crime_time_location_name.startswith(suspect_last_name + "'s ")
        or crime_time_location_name.startswith("Dr. " + suspect_last_name + "'s ")
    ):
        crime_time_location_spoken_name = "my room"

    suspect = {
        **suspect,
        "alibi": {
            **suspect["alibi"],
            "crime_time_location_name": crime_time_location_name,
            "crime_time_location_spoken_name": crime_time_location_spoken_name,
        },
    }

    confronted_clue = None
    confronted_clues = []
    evidence_reaction = None

    presented_clue_ids = confronted_clue_ids or []
    if confronted_clue_id is not None and confronted_clue_id not in presented_clue_ids:
        presented_clue_ids = [confronted_clue_id, *presented_clue_ids]

    previously_revealed_clue_ids = state.revealed_clues[suspect_id]
    repeated_confronted_clue_ids = [
        clue_id
        for clue_id in presented_clue_ids
        if clue_id in previously_revealed_clue_ids
    ]
    new_confronted_clue_ids = [
        clue_id
        for clue_id in presented_clue_ids
        if clue_id not in previously_revealed_clue_ids
    ]

    confronted_clue_is_related_to_suspect = False

    if presented_clue_ids:
        valid_clues_by_id = {
            clue["id"]: clue
            for clue in clues
        }

        for clue_id in presented_clue_ids:
            if clue_id not in state.discovered_clues:
                raise ValueError(f"Clue '{clue_id}' has not been discovered yet.")

            if clue_id not in valid_clues_by_id:
                raise ValueError(f"Unknown clue ID: {clue_id}")

            clue = valid_clues_by_id[clue_id]
            confronted_clues.append(clue)

            confrontation_targets = clue.get("confrontation_targets", [])
            if suspect_id in confrontation_targets:
                confronted_clue_is_related_to_suspect = True

        confronted_clue = confronted_clues[0]

        if confronted_clue_is_related_to_suspect:
            evidence_reaction = get_applicable_evidence_reaction(
                state=state,
                suspect=suspect,
                confronted_clue_id=confronted_clue["id"],
                confronted_clue_ids=presented_clue_ids,
            )

    return {
        "suspect": suspect,
        "player_question": player_question,
        "confronted_clue": confronted_clue,
        "confronted_clues": confronted_clues,
        "confronted_clue_ids": presented_clue_ids,
        "repeated_confronted_clue_ids": repeated_confronted_clue_ids,
        "new_confronted_clue_ids": new_confronted_clue_ids,
        "confronted_clue_is_related_to_suspect": confronted_clue_is_related_to_suspect,
        "evidence_reaction": evidence_reaction,
        "discovered_clue_ids": state.discovered_clues,
        "revealed_clue_ids_for_suspect": state.revealed_clues[suspect_id],
        "improvised_facts_for_suspect": state.improvised_facts[suspect_id],
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
    confronted_clue_ids: list[str] | None = None,
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
        valid_clue_ids = {
            clue["id"]
            for clue in game_data["clues"]["clues"]
        }

        if confronted_clue_id not in valid_clue_ids:
            raise ValueError(f"Unknown clue ID: {confronted_clue_id}")

        if confronted_clue_id not in state.discovered_clues:
            raise ValueError(
                f"Clue '{confronted_clue_id}' has not been discovered yet."
            )

    entry = state.add_dialogue_entry(
        suspect_id=suspect_id,
        player_question=player_question,
        npc_response=npc_response,
        confronted_clue_id=confronted_clue_id,
        confronted_clue_ids=confronted_clue_ids,
    )

    return entry.__dict__

def check_accusation(
    solution_data: dict[str, Any],
    culprit_id: str,
    motive_id: str,
    method_id: str,
    evidence_ids: list[str],
) -> dict[str, Any]:
    """
    Check a player's final accusation against the hidden solution.

    Args:
        solution_data: Loaded solution data from solution.json.
        culprit_id: Suspect ID selected by the player.
        motive_id: Motive ID selected by the player.
        method_id: Method ID selected by the player.
        evidence_ids: Evidence IDs selected by the player.

    Returns:
        Dictionary containing result label, score, feedback, and solved status.
    """
    correct_accusation = solution_data["correct_accusation"]
    scoring = solution_data["scoring"]
    feedback = solution_data["feedback"]

    selected_evidence = set(evidence_ids)
    required_evidence = set(correct_accusation["minimum_required_evidence_ids"])

    correct_culprit = culprit_id == correct_accusation["culprit_id"]
    correct_motive = motive_id == correct_accusation["motive_id"]
    correct_method = method_id == correct_accusation["method_id"]

    found_required_evidence = selected_evidence.intersection(required_evidence)
    has_all_required_evidence = required_evidence.issubset(selected_evidence)

    score = 0.0

    if correct_culprit:
        score += scoring["score_components"]["correct_culprit"]

    if correct_motive:
        score += scoring["score_components"]["correct_motive"]

    if correct_method:
        score += scoring["score_components"]["correct_method"]

    for clue_id in found_required_evidence:
        score += scoring["required_evidence_scoring"][clue_id]

    score = round(score, 2)

    if (
        correct_culprit
        and correct_motive
        and correct_method
        and has_all_required_evidence
    ):
        result = "correct"
        feedback_key = "correct"
        solved = True

    elif correct_culprit and not correct_motive:
        result = "partial_correct_culprit_wrong_motive"
        feedback_key = "partial_correct_culprit_wrong_motive"
        solved = False

    elif correct_culprit and not correct_method:
        result = "partial_correct_culprit_wrong_method"
        feedback_key = "partial_correct_culprit_wrong_method"
        solved = False

    elif correct_culprit and not has_all_required_evidence:
        result = "partial_correct_culprit_weak_evidence"
        feedback_key = "partial_correct_culprit_weak_evidence"
        solved = False

    elif culprit_id == "clara_vale":
        result = "wrong_clara"
        feedback_key = "wrong_clara"
        solved = False

    elif culprit_id == "beatrice_ashford":
        result = "wrong_beatrice"
        feedback_key = "wrong_beatrice"
        solved = False

    elif culprit_id == "julian_blackwood":
        result = "wrong_julian"
        feedback_key = "wrong_julian"
        solved = False

    else:
        result = "wrong_generic"
        feedback_key = "wrong_generic"
        solved = False

    selected_feedback = feedback[feedback_key]

    return {
        "result": result,
        "score": score,
        "max_score": scoring["max_score"],
        "solved": solved,
        "feedback_title": selected_feedback["title"],
        "feedback_message": selected_feedback["message"],
        "correct_parts": {
            "culprit": correct_culprit,
            "motive": correct_motive,
            "method": correct_method,
            "required_evidence": has_all_required_evidence,
        },
        "missing_required_evidence": sorted(required_evidence - selected_evidence),
        "selected_evidence": evidence_ids,
    }


def submit_accusation(
    state: GameState,
    game_data: dict[str, dict[str, Any]],
    culprit_id: str,
    motive_id: str,
    method_id: str,
    evidence_ids: list[str],
) -> dict[str, Any]:
    """
    Submit a final accusation, check it, and record the attempt in game state.

    Args:
        state: Current GameState object.
        game_data: Dictionary containing all loaded game data.
        culprit_id: Suspect ID selected by the player.
        motive_id: Motive ID selected by the player.
        method_id: Method ID selected by the player.
        evidence_ids: Evidence IDs selected by the player.

    Returns:
        Dictionary containing the accusation result and recorded attempt.

    Raises:
        ValueError: If the player tries to use evidence that has not been discovered.
    """
    undiscovered_evidence = [
        clue_id for clue_id in evidence_ids if clue_id not in state.discovered_clues
    ]

    if undiscovered_evidence:
        raise ValueError(
            f"Cannot use undiscovered evidence in accusation: {undiscovered_evidence}"
        )

    result = check_accusation(
        solution_data=game_data["solution"],
        culprit_id=culprit_id,
        motive_id=motive_id,
        method_id=method_id,
        evidence_ids=evidence_ids,
    )

    attempt = state.add_accusation_attempt(
        culprit_id=culprit_id,
        motive_id=motive_id,
        method_id=method_id,
        evidence_ids=evidence_ids,
        result=result["result"],
        score=result["score"],
        feedback=result["feedback_message"],
    )

    return {
        "result": result,
        "attempt": attempt.__dict__,
        "game_status": state.game_status,
    }