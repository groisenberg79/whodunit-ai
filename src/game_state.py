from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class DialogueEntry:
    """
    Store one dialogue exchange between the player and a suspect.

    Args:
        suspect_id: ID of the suspect being interviewed.
        player_question: Free-form question asked by the player.
        npc_response: Response generated for the suspect.
        confronted_clue_id: Optional clue ID used to confront the suspect.
        timestamp: UTC timestamp for the dialogue entry.
    """

    suspect_id: str
    player_question: str
    npc_response: str
    confronted_clue_id: str | None = None
    confronted_clue_ids: list[str] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class AccusationAttempt:
    """
    Store one final accusation attempt.

    Args:
        culprit_id: Suspect accused by the player.
        motive_id: Motive interpreted from the player's accusation, or None.
        method_id: Method interpreted from the player's accusation, or None.
        evidence_ids: Evidence IDs selected by the player.
        result: Result label returned by the accusation checker.
        score: Numeric score returned by the accusation checker.
        feedback: Feedback message shown to the player.
        timestamp: UTC timestamp for the accusation attempt.
    """

    culprit_id: str
    motive_id: str | None
    method_id: str | None
    evidence_ids: list[str]
    result: str
    score: float
    feedback: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class GameState:
    """
    Track the current state of a Whodunit AI game session.

    Args:
        suspect_ids: List of suspect IDs in the case.
        discovered_clues: Clue IDs discovered by the player.
        revealed_clues: Mapping from suspect ID to clue IDs revealed to that suspect.
        improvised_facts: Mapping from suspect ID to harmless improvised facts established during dialogue.
        visited_locations: Location IDs visited by the player.
        interviewed_suspects: Suspect IDs interviewed by the player.
        dialogue_history: Dialogue entries from suspect interviews.
        accusation_attempts: Final accusation attempts made by the player.
        game_status: Current game status.
    """

    suspect_ids: list[str]
    discovered_clues: list[str] = field(default_factory=list)
    revealed_clues: dict[str, list[str]] = field(default_factory=dict)
    improvised_facts: dict[str, list[str]] = field(default_factory=dict)
    visited_locations: list[str] = field(default_factory=list)
    interviewed_suspects: list[str] = field(default_factory=list)
    dialogue_history: list[DialogueEntry] = field(default_factory=list)
    accusation_attempts: list[AccusationAttempt] = field(default_factory=list)
    game_status: str = "in_progress"

    def __post_init__(self) -> None:
        """
        Initialize per-suspect tracking dictionaries.

        This ensures each suspect has:
        - a list of clues explicitly revealed during interviews,
        - a list of harmless improvised facts established during dialogue.
        """
        for suspect_id in self.suspect_ids:
            self.revealed_clues.setdefault(suspect_id, [])
            self.improvised_facts.setdefault(suspect_id, [])

    @classmethod
    def from_case_data(cls, case_data: dict[str, Any]) -> GameState:
        """
        Create a GameState object from mystery case data.

        Args:
            case_data: Loaded mystery case data from mystery_case.json.

        Returns:
            Initialized GameState object.
        """
        suspect_ids = case_data["suspect_ids"]
        initial_state = case_data["initial_state"]

        return cls(
            suspect_ids=suspect_ids,
            discovered_clues=initial_state["discovered_clues"].copy(),
            revealed_clues={
                suspect_id: clues.copy()
                for suspect_id, clues in initial_state["revealed_clues"].items()
            },
            visited_locations=initial_state["visited_locations"].copy(),
            interviewed_suspects=initial_state["interviewed_suspects"].copy(),
            game_status=initial_state["game_status"],
        )

    def mark_clue_discovered(self, clue_id: str) -> bool:
        """
        Mark a clue as discovered by the player.

        Args:
            clue_id: ID of the clue to mark as discovered.

        Returns:
            True if the clue was newly discovered, False if it was already known.
        """
        if clue_id in self.discovered_clues:
            return False

        self.discovered_clues.append(clue_id)
        return True

    def mark_location_visited(self, location_id: str) -> bool:
        """
        Mark a location as visited.

        Args:
            location_id: ID of the visited location.

        Returns:
            True if the location was newly visited, False if it was already visited.
        """
        if location_id in self.visited_locations:
            return False

        self.visited_locations.append(location_id)
        return True

    def mark_clue_revealed_to_suspect(self, suspect_id: str, clue_id: str) -> bool:
        """
        Mark a discovered clue as revealed to a suspect.

        Args:
            suspect_id: ID of the suspect being confronted.
            clue_id: ID of the clue revealed to the suspect.

        Returns:
            True if the clue was newly revealed to the suspect, False otherwise.

        Raises:
            ValueError: If the clue has not been discovered by the player.
            KeyError: If the suspect ID is not tracked by the game state.
        """
        if clue_id not in self.discovered_clues:
            raise ValueError(
                f"Cannot reveal clue '{clue_id}' because it has not been discovered."
            )

        if suspect_id not in self.revealed_clues:
            raise KeyError(f"Unknown suspect ID: {suspect_id}")

        if clue_id in self.revealed_clues[suspect_id]:
            return False

        self.revealed_clues[suspect_id].append(clue_id)
        return True

    def mark_suspect_interviewed(self, suspect_id: str) -> bool:
        """
        Mark a suspect as interviewed.

        Args:
            suspect_id: ID of the suspect interviewed by the player.

        Returns:
            True if the suspect was newly marked as interviewed, False otherwise.
        """
        if suspect_id in self.interviewed_suspects:
            return False

        self.interviewed_suspects.append(suspect_id)
        return True

    def add_improvised_fact(self, suspect_id: str, fact: str) -> bool:
        """
        Store a harmless improvised fact for a suspect.

        Args:
            suspect_id: ID of the suspect.
            fact: Harmless improvised fact to store.

        Returns:
            True if the fact was newly added, False if it was already stored.

        Raises:
            KeyError: If the suspect ID is not tracked by the game state.
            ValueError: If the fact is empty.
        """
        cleaned_fact = fact.strip()

        if not cleaned_fact:
            raise ValueError("Improvised fact cannot be empty.")

        if suspect_id not in self.improvised_facts:
            raise KeyError(f"Unknown suspect ID: {suspect_id}")

        if cleaned_fact in self.improvised_facts[suspect_id]:
            return False

        self.improvised_facts[suspect_id].append(cleaned_fact)
        return True

    def add_dialogue_entry(
        self,
        suspect_id: str,
        player_question: str,
        npc_response: str,
        confronted_clue_id: str | None = None,
        confronted_clue_ids: list[str] | None = None,
    ) -> DialogueEntry:
        """
        Add a dialogue exchange to the game state.

        Args:
            suspect_id: ID of the suspect being interviewed.
            player_question: Free-form question asked by the player.
            npc_response: Response generated for the suspect.
            confronted_clue_id: Optional primary clue ID used in the confrontation.
            confronted_clue_ids: Optional list of all clue IDs used in the confrontation.

        Returns:
            The created DialogueEntry.
        """
        self.mark_suspect_interviewed(suspect_id)

        all_confronted_clue_ids = list(confronted_clue_ids or [])

        if (
            confronted_clue_id is not None
            and confronted_clue_id not in all_confronted_clue_ids
        ):
            all_confronted_clue_ids.insert(0, confronted_clue_id)

        for clue_id in all_confronted_clue_ids:
            self.mark_clue_revealed_to_suspect(suspect_id, clue_id)

        entry = DialogueEntry(
            suspect_id=suspect_id,
            player_question=player_question,
            npc_response=npc_response,
            confronted_clue_id=confronted_clue_id,
            confronted_clue_ids=all_confronted_clue_ids,
        )

        self.dialogue_history.append(entry)
        return entry

    def add_accusation_attempt(
        self,
        culprit_id: str,
        motive_id: str | None,
        method_id: str | None,
        evidence_ids: list[str],
        result: str,
        score: float,
        feedback: str,
    ) -> AccusationAttempt:
        """
        Add a final accusation attempt to the game state.

        Args:
            culprit_id: Suspect accused by the player.
            motive_id: Motive interpreted from the player's accusation, or None.
            method_id: Method interpreted from the player's accusation, or None.
            evidence_ids: Evidence selected by the player.
            result: Result label returned by the accusation checker.
            score: Numeric score returned by the accusation checker.
            feedback: Feedback message shown to the player.

        Returns:
            The created AccusationAttempt.
        """
        attempt = AccusationAttempt(
            culprit_id=culprit_id,
            motive_id=motive_id,
            method_id=method_id,
            evidence_ids=evidence_ids,
            result=result,
            score=score,
            feedback=feedback,
        )

        self.accusation_attempts.append(attempt)

        if result == "correct":
            self.game_status = "solved"

        return attempt

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the current game state into a serializable dictionary.

        Returns:
            Dictionary representation of the game state.
        """
        return {
            "discovered_clues": self.discovered_clues,
            "revealed_clues": self.revealed_clues,
            "improvised_facts": self.improvised_facts,
            "visited_locations": self.visited_locations,
            "interviewed_suspects": self.interviewed_suspects,
            "dialogue_history": [
                entry.__dict__ for entry in self.dialogue_history
            ],
            "accusation_attempts": [
                attempt.__dict__ for attempt in self.accusation_attempts
            ],
            "game_status": self.game_status,
        }