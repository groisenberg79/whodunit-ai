from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAG_DIR = PROJECT_ROOT / "rag_store"
INDEX_PATH = RAG_DIR / "faiss.index"
DOCUMENTS_PATH = RAG_DIR / "documents.pkl"

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class RagIndexError(Exception):
    """Raised when a RAG index operation fails."""


def load_embedding_model(
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> SentenceTransformer:
    """
    Load the sentence-transformers embedding model.

    Args:
        model_name: Hugging Face model name for embeddings.

    Returns:
        Loaded SentenceTransformer model.
    """
    return SentenceTransformer(model_name)


def embed_texts(
    texts: list[str],
    model: SentenceTransformer,
) -> np.ndarray:
    """
    Embed a list of texts into normalized vectors.

    Args:
        texts: Text strings to embed.
        model: Loaded SentenceTransformer model.

    Returns:
        NumPy array of normalized float32 embeddings.
    """
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings.astype("float32")


def build_faiss_index(
    documents: list[dict[str, Any]],
    model: SentenceTransformer,
) -> faiss.Index:
    """
    Build a FAISS index from retrievable documents.

    Args:
        documents: List of retrievable document dictionaries.
        model: Loaded embedding model.

    Returns:
        FAISS index containing document embeddings.

    Raises:
        RagIndexError: If no documents are provided.
    """
    if not documents:
        raise RagIndexError("Cannot build FAISS index with no documents.")

    texts = [document["text"] for document in documents]
    embeddings = embed_texts(texts, model)

    embedding_dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(embedding_dimension)
    index.add(embeddings)

    return index


def save_rag_index(
    index: faiss.Index,
    documents: list[dict[str, Any]],
    index_path: Path = INDEX_PATH,
    documents_path: Path = DOCUMENTS_PATH,
) -> None:
    """
    Save FAISS index and matching documents to disk.

    Args:
        index: FAISS index to save.
        documents: Documents corresponding to the index vectors.
        index_path: Path where the FAISS index should be saved.
        documents_path: Path where document metadata/text should be saved.
    """
    index_path.parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(index_path))

    with documents_path.open("wb") as file:
        pickle.dump(documents, file)


def load_rag_index(
    index_path: Path = INDEX_PATH,
    documents_path: Path = DOCUMENTS_PATH,
) -> tuple[faiss.Index, list[dict[str, Any]]]:
    """
    Load FAISS index and matching documents from disk.

    Args:
        index_path: Path to saved FAISS index.
        documents_path: Path to saved documents pickle file.

    Returns:
        Tuple containing FAISS index and document list.

    Raises:
        RagIndexError: If the index or documents file is missing.
    """
    if not index_path.exists():
        raise RagIndexError(f"FAISS index not found: {index_path}")

    if not documents_path.exists():
        raise RagIndexError(f"Documents file not found: {documents_path}")

    index = faiss.read_index(str(index_path))

    with documents_path.open("rb") as file:
        documents = pickle.load(file)

    return index, documents


def search_rag_index(
    query: str,
    index: faiss.Index,
    documents: list[dict[str, Any]],
    model: SentenceTransformer,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Search the FAISS index for documents relevant to a query.

    Args:
        query: Search query text.
        index: FAISS index.
        documents: Documents corresponding to index vectors.
        model: Loaded embedding model.
        top_k: Number of results to return.

    Returns:
        List of retrieved document dictionaries with similarity scores.
    """
    query_embedding = embed_texts([query], model)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, document_index in zip(scores[0], indices[0]):
        if document_index == -1:
            continue

        document = documents[document_index].copy()
        document["score"] = float(score)
        results.append(document)

    return results