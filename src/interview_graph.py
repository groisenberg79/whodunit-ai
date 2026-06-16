from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from src.llm_client import LLMMode

from src.game_engine import build_interview_context, record_interview_exchange
from src.npc_engine import generate_npc_response
from src.prompt_builder import build_npc_messages
from src.rag_filter import filter_documents_for_interview, format_retrieved_context
from src.rag_index import search_rag_index

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

    return {
        **state,
        "npc_response": npc_response,
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
    )

    return state

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
    graph.add_node("record_dialogue", record_dialogue_node)

    graph.add_edge(START, "build_context")

    graph.add_edge("build_context", "retrieve_rag")
    graph.add_edge("retrieve_rag", "filter_rag")
    graph.add_edge("filter_rag", "build_prompt")
    graph.add_edge("build_prompt", "generate_response")
    graph.add_edge("generate_response", "record_dialogue")
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