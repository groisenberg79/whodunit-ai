from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import get_location_by_id, load_game_data
from src.game_engine import inspect_location_area
from src.game_state import GameState
from src.interview_graph import InterviewGraphState, build_interview_graph
from src.rag_documents import create_all_documents
from src.rag_index import build_faiss_index, load_embedding_model


def main() -> None:
    """
    Test one full NPC interview turn through the LangGraph workflow.
    """
    game_data = load_game_data()
    game_state = GameState.from_case_data(game_data["case"])

    library = get_location_by_id(game_data, "library")
    henry_study = get_location_by_id(game_data, "henry_study")

    inspect_location_area(
        state=game_state,
        location=library,
        area_id="brandy_glass",
    )

    inspect_location_area(
        state=game_state,
        location=henry_study,
        area_id="medical_bag",
    )

    rag_documents = create_all_documents(game_data)
    embedding_model = load_embedding_model()
    rag_index = build_faiss_index(rag_documents, embedding_model)

    interview_graph = build_interview_graph()

    initial_graph_state: InterviewGraphState = {
        "game_data": game_data,
        "game_state": game_state,
        "suspect_id": "henry_ashford",
        "player_question": (
            "Doctor, I found a medical vial in your bag, and there was residue "
            "in Edward's brandy glass. How do you explain that?"
        ),
        "confronted_clue_id": "medical_vial",
        "rag_index": rag_index,
        "rag_documents": rag_documents,
        "embedding_model": embedding_model,
        "raw_rag_results": [],
        "filtered_rag_results": [],
        "retrieved_context": "",
        "interview_context": {},
        "messages": [],
        "npc_response": "",
    }

    final_graph_state = interview_graph.invoke(initial_graph_state)

    print("\n" + "=" * 80)
    print("NPC RESPONSE")
    print("=" * 80)
    print(final_graph_state["npc_response"])

    print("\n" + "=" * 80)
    print("FILTERED RAG DOCUMENT IDS")
    print("=" * 80)
    for document in final_graph_state["filtered_rag_results"]:
        print(document["id"])

    print("\n" + "=" * 80)
    print("DIALOGUE HISTORY")
    print("=" * 80)
    pprint(game_state.dialogue_history)

    print("\n" + "=" * 80)
    print("REVEALED CLUES")
    print("=" * 80)
    pprint(game_state.revealed_clues)


if __name__ == "__main__":
    main()