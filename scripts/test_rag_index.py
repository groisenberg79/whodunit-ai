from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_game_data
from src.rag_documents import create_all_documents
from src.rag_index import (
    build_faiss_index,
    load_embedding_model,
    save_rag_index,
    search_rag_index,
)


def print_results(results: list[dict]) -> None:
    """
    Print RAG search results in a readable format.

    Args:
        results: Retrieved document dictionaries.
    """
    for result in results:
        print("\n---")
        print(result["id"])
        print(result["metadata"])
        print("score:", result["score"])
        print(result["text"][:500])


def main() -> None:
    """
    Build and test the FAISS RAG index.
    """
    game_data = load_game_data()
    documents = create_all_documents(game_data)

    print(f"Created {len(documents)} documents.")

    print("Loading embedding model...")
    model = load_embedding_model()

    print("Building FAISS index...")
    index = build_faiss_index(
        documents=documents,
        model=model,
    )

    print(f"Index contains {index.ntotal} vectors.")

    print("Saving index...")
    save_rag_index(
        index=index,
        documents=documents,
    )

    print("\nSearch test 1: medicine in the brandy")
    results = search_rag_index(
        query="medicine in Edward's brandy glass",
        index=index,
        documents=documents,
        model=model,
        top_k=5,
    )
    print_results(results)

    print("\nSearch test 2: inheritance and Clara")
    results = search_rag_index(
        query="Clara inheritance will letter",
        index=index,
        documents=documents,
        model=model,
        top_k=5,
    )
    print_results(results)


if __name__ == "__main__":
    main()