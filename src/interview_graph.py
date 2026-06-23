from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from src.llm_client import LLMMode

from src.response_validator import (
    ValidationResult,
    build_fallback_response,
    validate_npc_response,
)
from src.game_engine import build_interview_context, record_interview_exchange
from src.npc_engine import generate_npc_response
from src.prompt_builder import build_npc_messages
from src.rag_filter import filter_documents_for_interview, format_retrieved_context
from src.rag_index import search_rag_index


def clean_npc_response_formatting(response: str) -> str:
    """
    Remove formatting artifacts from an NPC response without changing its content.

    This is mainly used to remove quotation marks that the LLM may add because it
    understands the response as spoken dialogue.
    """
    cleaned_paragraphs = []

    for paragraph in response.strip().split("\n\n"):
        cleaned = paragraph.strip()

        quote_pairs = [
            ('"', '"'),
            ("'", "'"),
            ("“", "”"),
            ("‘", "’"),
        ]

        for opening_quote, closing_quote in quote_pairs:
            if cleaned.startswith(opening_quote) and cleaned.endswith(closing_quote):
                cleaned = cleaned[1:-1].strip()
                break

        cleaned_paragraphs.append(cleaned)

    return "\n\n".join(
        paragraph
        for paragraph in cleaned_paragraphs
        if paragraph
    )


def build_context_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Build deterministic interview context for the current NPC interaction.
    """
    interview_context = build_interview_context(
        state=state["game_state"],
        game_data=state["game_data"],
        suspect_id=state["suspect_id"],
        player_question=state["player_question"],
        confronted_clue_id=state["confronted_clue_id"],
        confronted_clue_ids=state.get("confronted_clue_ids", []),
    )

    return {
        **state,
        "interview_context": interview_context,
    }


def retrieve_rag_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Retrieve semantically relevant RAG documents for the player's question.
    """
    raw_rag_results = search_rag_index(
        query=state["player_question"],
        index=state["rag_index"],
        documents=state["rag_documents"],
        model=state["embedding_model"],
        top_k=8,
    )

    return {
        **state,
        "raw_rag_results": raw_rag_results,
    }


def filter_rag_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Filter retrieved RAG documents according to game state and confrontation.
    """
    filtered_rag_results = filter_documents_for_interview(
        documents=state["raw_rag_results"],
        state=state["game_state"],
        suspect_id=state["suspect_id"],
        confronted_clue_id=state["confronted_clue_id"],
        confronted_clue_ids=state.get("confronted_clue_ids", []),
    )

    retrieved_context = format_retrieved_context(filtered_rag_results)

    return {
        **state,
        "filtered_rag_results": filtered_rag_results,
        "retrieved_context": retrieved_context,
    }


def build_prompt_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Build LLM-ready prompt messages using interview context and filtered RAG.
    """
    interview_context = {
        **state["interview_context"],
        "retrieved_context": state["retrieved_context"],
    }

    messages = build_npc_messages(
        game_data=state["game_data"],
        interview_context=interview_context,
    )

    return {
        **state,
        "interview_context": interview_context,
        "messages": messages,
    }


def generate_response_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Generate the NPC response.

    For now this can use mock mode. Later it can call a real LLM backend.
    """
    npc_response = generate_npc_response(
        interview_context=state["interview_context"],
        messages=state["messages"],
        mode=state["llm_mode"],
        model_name=state["model_name"],
    )

    npc_response = clean_npc_response_formatting(npc_response)

    return {
        **state,
        "npc_response": npc_response,
    }


def validate_response_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Validate the generated NPC response before recording it.
    """
    validation_result = validate_npc_response(state["npc_response"])

    return {
        **state,
        "validation_result": validation_result,
    }


def record_dialogue_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Record the completed interview exchange in GameState.
    """
    record_interview_exchange(
        state=state["game_state"],
        game_data=state["game_data"],
        suspect_id=state["suspect_id"],
        player_question=state["player_question"],
        npc_response=state["npc_response"],
        confronted_clue_id=state["confronted_clue_id"],
        confronted_clue_ids=state["confronted_clue_ids"],
    )

    return state


def fallback_response_node(state: InterviewGraphState) -> InterviewGraphState:
    """
    Replace an invalid NPC response with a safe fallback response.
    """
    fallback_response = build_fallback_response()

    return {
        **state,
        "npc_response": fallback_response,
    }


def route_after_validation(state: InterviewGraphState) -> str:
    """
    Decide whether to record the response or replace it with a fallback first.
    """
    validation_result = state["validation_result"]

    if validation_result is None:
        raise ValueError("Missing validation_result after validation node.")

    if validation_result.is_valid:
        return "record_dialogue"

    return "fallback_response"


def build_interview_graph():
    """
    Build and compile the LangGraph interview workflow.

    Returns:
        A compiled LangGraph app that can process one NPC interview turn.
    """
    graph = StateGraph(InterviewGraphState)

    graph.add_node("build_context", build_context_node)
    graph.add_node("retrieve_rag", retrieve_rag_node)
    graph.add_node("filter_rag", filter_rag_node)
    graph.add_node("build_prompt", build_prompt_node)
    graph.add_node("generate_response", generate_response_node)
    graph.add_node("validate_response", validate_response_node)
    graph.add_node("fallback_response", fallback_response_node)
    graph.add_node("record_dialogue", record_dialogue_node)

    graph.add_edge(START, "build_context")

    graph.add_edge("build_context", "retrieve_rag")
    graph.add_edge("retrieve_rag", "filter_rag")
    graph.add_edge("filter_rag", "build_prompt")
    graph.add_edge("build_prompt", "generate_response")
    graph.add_edge("generate_response", "validate_response")
    graph.add_conditional_edges(
        "validate_response",
        route_after_validation,
        {
            "record_dialogue": "record_dialogue",
            "fallback_response": "fallback_response",
        },
    )
    graph.add_edge("fallback_response", "record_dialogue")
    graph.add_edge("record_dialogue", END)
    return graph.compile()


class InterviewGraphState(TypedDict):
    """
    State passed through the LangGraph interview workflow.

    This state combines:
    - player input,
    - current game data,
    - mutable game state,
    - RAG components,
    - intermediate prompt-building data,
    - final NPC response.
    """

    game_data: dict[str, Any]
    game_state: Any

    suspect_id: str
    player_question: str
    confronted_clue_id: str | None
    confronted_clue_ids: list[str]

    rag_index: Any
    rag_documents: list[dict[str, Any]]
    embedding_model: Any

    raw_rag_results: list[dict[str, Any]]
    filtered_rag_results: list[dict[str, Any]]
    retrieved_context: str

    interview_context: dict[str, Any]
    messages: list[dict[str, str]]
    llm_mode: LLMMode
    model_name: str
    npc_response: str
    validation_result: ValidationResult | None