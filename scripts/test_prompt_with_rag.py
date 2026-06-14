from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import get_location_by_id, load_game_data
from src.game_engine import build_interview_context, inspect_location_area
from src.game_state import GameState
from src.prompt_builder import build_npc_messages
from src.rag_documents import create_all_documents
from src.rag_filter import filter_documents_for_interview, format_retrieved_context
from src.rag_index import build_faiss_index, load_embedding_model, search_rag_index


def main() -> None:
    """
    Test prompt construction with filtered RAG context.
    """
    game_data = load_game_data()
    state = GameState.from_case_data(game_data["case"])

    library = get_location_by_id(game_data, "library")
    henry_study = get_location_by_id(game_data, "henry_study")

    inspect_location_area(
        state=state,
        location=library,
        area_id="brandy_glass",
    )

    inspect_location_area(
        state=state,
        location=henry_study,
        area_id="medical_bag",
    )

    documents = create_all_documents(game_data)
    model = load_embedding_model()
    index = build_faiss_index(documents, model)

    raw_results = search_rag_index(
        query="medicine in Edward's brandy glass",
        index=index,
        documents=documents,
        model=model,
        top_k=8,
    )

    filtered_results = filter_documents_for_interview(
        documents=raw_results,
        state=state,
        suspect_id="henry_ashford",
        confronted_clue_id="medical_vial",
    )

    retrieved_context = format_retrieved_context(filtered_results)

    interview_context = build_interview_context(
        state=state,
        game_data=game_data,
        suspect_id="henry_ashford",
        player_question=(
            "Doctor, I found a medical vial in your bag, and there was residue "
            "in Edward's brandy glass. How do you explain that?"
        ),
        confronted_clue_id="medical_vial",
    )

    interview_context["retrieved_context"] = retrieved_context

    messages = build_npc_messages(
        game_data=game_data,
        interview_context=interview_context,
    )

    print("\n" + "=" * 80)
    print("SYSTEM PROMPT")
    print("=" * 80)
    print(messages[0]["content"][:1500])

    print("\n" + "=" * 80)
    print("USER PROMPT")
    print("=" * 80)
    print(messages[1]["content"])


if __name__ == "__main__":
    main()