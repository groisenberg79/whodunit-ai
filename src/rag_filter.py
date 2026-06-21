from __future__ import annotations

from typing import Any

from src.game_state import GameState


def has_discovered_all_required_clues(
    state: GameState,
    required_clue_ids: list[str],
) -> bool:
    """
    Check whether all required clues have been discovered.

    Args:
        state: Current GameState object.
        required_clue_ids: Clue IDs required for a document to be allowed.

    Returns:
        True if all required clues have been discovered, False otherwise.
    """
    return set(required_clue_ids).issubset(state.discovered_clues)


def is_document_allowed_for_interview(
    document: dict[str, Any],
    state: GameState,
    suspect_id: str,
    confronted_clue_id: str | None = None,
    confronted_clue_ids: list[str] | None = None,
) -> bool:
    """
    Check whether a retrieved RAG document is allowed in an NPC interview prompt.

    Args:
        document: Retrieved RAG document.
        state: Current GameState object.
        suspect_id: ID of the suspect currently being interviewed.
        confronted_clue_id: Optional clue ID explicitly used in confrontation.

    Returns:
        True if the document is allowed, False otherwise.
    """
    metadata = document["metadata"]
    visibility = metadata["visibility"]
    presented_clue_ids = set(confronted_clue_ids or [])
    if confronted_clue_id is not None:
        presented_clue_ids.add(confronted_clue_id)

    if visibility == "internal_only":
        return False

    if visibility == "internal_or_feedback":
        return False

    if visibility == "suspect_context":
        return False

    if visibility == "suspect_private":
        return False

    if visibility == "location_context":
        return True

    if visibility == "only_if_discovered":
        clue_id = metadata["clue_id"]
        return clue_id in state.discovered_clues

    if visibility == "only_when_confronted":
        clue_id = metadata.get("clue_id")

        return (
            metadata.get("suspect_id") == suspect_id
            and clue_id in presented_clue_ids
            and clue_id in state.discovered_clues
        )

    if visibility == "only_when_combo_applies":
        required_clue_ids = set(metadata["required_clue_ids"])
        trigger_clue_ids = set(metadata["trigger_clue_ids"])

        return (
            metadata.get("suspect_id") == suspect_id
            and required_clue_ids.issubset(presented_clue_ids)
            and trigger_clue_ids.intersection(presented_clue_ids)
            and has_discovered_all_required_clues(state, list(required_clue_ids))
        )

    return False


def filter_documents_for_interview(
    documents: list[dict[str, Any]],
    state: GameState,
    suspect_id: str,
    confronted_clue_id: str | None = None,
    confronted_clue_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Filter retrieved RAG documents for an NPC interview.

    Args:
        documents: Retrieved RAG documents.
        state: Current GameState object.
        suspect_id: ID of the suspect currently being interviewed.
        confronted_clue_id: Optional clue ID explicitly used in confrontation.

    Returns:
        List of documents allowed in the interview prompt.
    """
    return [
        document
        for document in documents
        if is_document_allowed_for_interview(
            document=document,
            state=state,
            suspect_id=suspect_id,
            confronted_clue_id=confronted_clue_id,
            confronted_clue_ids=confronted_clue_ids,
        )
    ]


def format_retrieved_context(
    documents: list[dict[str, Any]],
    max_characters_per_document: int = 1200,
) -> str:
    """
    Format allowed retrieved documents for inclusion in an LLM prompt.

    Args:
        documents: Filtered RAG documents.
        max_characters_per_document: Maximum number of characters per document.

    Returns:
        Formatted retrieved context string.
    """
    if not documents:
        return "No additional retrieved context is available."

    formatted_documents = []

    for document in documents:
        text = document["text"]

        if len(text) > max_characters_per_document:
            text = text[:max_characters_per_document].rstrip() + "..."

        formatted_documents.append(
            (
                f"[{document['id']}]\n"
                f"Document type: {document['metadata']['document_type']}\n"
                f"Retrieved text:\n{text}"
            )
        )

    return "\n\n".join(formatted_documents)