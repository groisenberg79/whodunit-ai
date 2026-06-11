from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_game_data
from src.rag_documents import create_all_documents


def main() -> None:
    """
    Test creation of retrievable RAG documents.
    """
    game_data = load_game_data()
    documents = create_all_documents(game_data)

    print(f"Created {len(documents)} documents.")

    print("\nFirst document:")
    pprint(documents[0])

    print("\nDocument type counts:")
    counts = {}

    for document in documents:
        document_type = document["metadata"]["document_type"]
        counts[document_type] = counts.get(document_type, 0) + 1

    pprint(counts)

    print("\nSample clue document:")
    for document in documents:
        if document["id"] == "clue_public::medical_vial":
            pprint(document)
            break

    print("\nInternal clue documents:")
    for document in documents:
        if document["metadata"]["document_type"] == "clue_internal":
            print(document["id"], "| visibility:", document["metadata"]["visibility"])


if __name__ == "__main__":
    main()