from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import get_location_by_id, load_game_data
from src.game_engine import inspect_location_area
from src.game_state import GameState
from src.rag_documents import create_all_documents
from src.rag_filter import filter_documents_for_interview, format_retrieved_context
from src.rag_index import build_faiss_index, load_embedding_model, search_rag_index


def print_section(title: str) -> None:
    """
    Print a readable section title.

    Args:
        title: Section title to display.
    """
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_doc_ids(documents: list[dict]) -> None:
    """
    Print document IDs and visibility values.

    Args:
        documents: RAG documents.
    """
    for document in documents:
        print(
            document["id"],
            "| visibility:",
            document["metadata"]["visibility"],
            "| score:",
            round(document.get("score", 0), 3),
        )


def main() -> None:
    """
    Test filtering of RAG results by game state.
    """
    game_data = load_game_data()
    state = GameState.from_case_data(game_data["case"])

    documents = create_all_documents(game_data)
    model = load_embedding_model()
    index = build_faiss_index(documents, model)

    print_section("1. Search before discovering evidence")

    results = search_rag_index(
        query="medicine in Edward's brandy glass",
        index=index,
        documents=documents,
        model=model,
        top_k=8,
    )

    print("Raw FAISS results:")
    print_doc_ids(results)

    filtered = filter_documents_for_interview(
        documents=results,
        state=state,
        suspect_id="henry_ashford",
        confronted_clue_id=None,
    )

    print("\nFiltered results for Henry before clue discovery:")
    print_doc_ids(filtered)

    print_section("2. Discover brandy glass and medical vial")

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

    print("Discovered clues:")
    pprint(state.discovered_clues)

    filtered = filter_documents_for_interview(
        documents=results,
        state=state,
        suspect_id="henry_ashford",
        confronted_clue_id=None,
    )

    print("\nFiltered results for Henry after discovery, without confrontation:")
    print_doc_ids(filtered)

    print_section("3. Confront Henry with medical vial")

    filtered = filter_documents_for_interview(
        documents=results,
        state=state,
        suspect_id="henry_ashford",
        confronted_clue_id="medical_vial",
    )

    print("Filtered results for Henry with medical_vial confrontation:")
    print_doc_ids(filtered)

    print_section("4. Formatted retrieved context")

    formatted_context = format_retrieved_context(filtered)
    print(formatted_context)


if __name__ == "__main__":
    main()