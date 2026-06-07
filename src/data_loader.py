from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


class DataLoadError(Exception):
    """Raised when a game data file cannot be loaded or parsed."""


def load_json_file(file_path: Path) -> dict[str, Any]:
    """
    Load a JSON file and return its contents as a dictionary.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Parsed JSON data as a dictionary.

    Raises:
        DataLoadError: If the file does not exist or contains invalid JSON.
    """
    if not file_path.exists():
        raise DataLoadError(f"File not found: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise DataLoadError(f"Invalid JSON in {file_path}: {error}") from error

    if not isinstance(data, dict):
        raise DataLoadError(f"Expected JSON object in {file_path}, got {type(data).__name__}")

    return data


def load_game_data(data_dir: Path = DATA_DIR) -> dict[str, dict[str, Any]]:
    """
    Load all structured game data files.

    Args:
        data_dir: Directory containing the JSON data files.

    Returns:
        Dictionary containing all loaded game data.
    """
    files = {
        "case": "mystery_case.json",
        "characters": "characters.json",
        "clues": "clues.json",
        "locations": "locations.json",
        "solution": "solution.json",
    }

    game_data: dict[str, dict[str, Any]] = {}

    for key, filename in files.items():
        file_path = data_dir / filename
        game_data[key] = load_json_file(file_path)

    return game_data


def get_character_by_id(game_data: dict[str, dict[str, Any]], character_id: str) -> dict[str, Any]:
    """
    Return a character dictionary by ID.

    Args:
        game_data: Dictionary containing all loaded game data.
        character_id: ID of the character to retrieve.

    Returns:
        Character dictionary matching the given ID.

    Raises:
        KeyError: If no character with the given ID is found.
    """
    characters = game_data["characters"].get("characters", [])

    for character in characters:
        if character.get("id") == character_id:
            return character

    raise KeyError(f"Character not found: {character_id}")


def get_clue_by_id(game_data: dict[str, dict[str, Any]], clue_id: str) -> dict[str, Any]:
    """
    Return a clue dictionary by ID.

    Args:
        game_data: Dictionary containing all loaded game data.
        clue_id: ID of the clue to retrieve.

    Returns:
        Clue dictionary matching the given ID.

    Raises:
        KeyError: If no clue with the given ID is found.
    """
    clues = game_data["clues"].get("clues", [])

    for clue in clues:
        if clue.get("id") == clue_id:
            return clue

    raise KeyError(f"Clue not found: {clue_id}")


def get_location_by_id(game_data: dict[str, dict[str, Any]], location_id: str) -> dict[str, Any]:
    """
    Return a location dictionary by ID.

    Args:
        game_data: Dictionary containing all loaded game data.
        location_id: ID of the location to retrieve.

    Returns:
        Location dictionary matching the given ID.

    Raises:
        KeyError: If no location with the given ID is found.
    """
    locations = game_data["locations"].get("locations", [])

    for location in locations:
        if location.get("id") == location_id:
            return location

    raise KeyError(f"Location not found: {location_id}")