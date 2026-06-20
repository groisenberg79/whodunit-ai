from __future__ import annotations

from src.game_engine import inspect_location_area
from src.data_loader import get_clue_by_id, load_game_data
from src.game_state import GameState
from src.interview_graph import build_interview_graph
from src.rag_index import load_embedding_model, load_rag_index
import streamlit as st

def initialize_session_state() -> None:
    """
    Initialize Streamlit session state for the game.
    """
    if "game_data" not in st.session_state:
        st.session_state.game_data = load_game_data()

    if "game_state" not in st.session_state:
        st.session_state.game_state = GameState.from_case_data(
            st.session_state.game_data["case"]
        )

    if "embedding_model" not in st.session_state:
        st.session_state.embedding_model = load_embedding_model()

    if "rag_index" not in st.session_state:
        rag_index, rag_documents = load_rag_index()
        st.session_state.rag_index = rag_index
        st.session_state.rag_documents = rag_documents

    if "interview_graph" not in st.session_state:
        st.session_state.interview_graph = build_interview_graph()

def reset_game() -> None:
    """
    Reset the game state while keeping the loaded game data.
    """
    st.session_state.game_state = GameState.from_case_data(
        st.session_state.game_data["case"]
    )

def get_discovered_clue_details() -> list[dict]:
    """
    Return full clue dictionaries for clues discovered by the player.
    """
    game_data = st.session_state.game_data
    game_state = st.session_state.game_state

    discovered_clues = []

    for clue_id in game_state.discovered_clues:
        clue = get_clue_by_id(
            game_data=game_data,
            clue_id=clue_id,
        )
        discovered_clues.append(clue)

    return discovered_clues

def main() -> None:
    """
    Run the Whodunit AI Streamlit app.
    """
    st.set_page_config(
        page_title="Whodunit AI",
        page_icon="🕵️",
        layout="wide",
    )

    initialize_session_state()

    if st.button("Reset game"):
        reset_game()
        st.session_state.just_reset = True
        st.rerun()

    if st.session_state.get("just_reset", False):
        st.success("Game reset.")
        st.session_state.just_reset = False

    st.title("🕵️ Whodunit AI")
    st.subheader("An LLM-powered mystery game prototype")

    st.write(
        "Welcome to Blackwood Manor. A murder has taken place, "
        "and it is your job to uncover the truth."
    )

    game_data = st.session_state.game_data
    game_state = st.session_state.game_state

    case_data = game_data["case"]

    st.divider()

    st.header(case_data["title"])
    st.write(case_data["premise"])

    st.subheader("Current game state")
    st.write(f"Game status: `{game_state.game_status}`")
    st.write(f"Discovered clues: `{len(game_state.discovered_clues)}`")
    st.write(f"Visited locations: `{len(game_state.visited_locations)}`")

    st.divider()

    st.header("Case notes")

    discovered_clue_details = get_discovered_clue_details()

    if not discovered_clue_details:
        st.info("No clues discovered yet.")
    else:
        for clue in discovered_clue_details:
            with st.expander(clue["name"]):
                st.write(clue["description"])

    st.divider()

    st.header("Suspects")

    suspects = game_data["characters"]["characters"]

    for suspect in suspects:
        with st.expander(suspect["name"]):
            st.write(suspect["player_description"])

            st.markdown(f"**Role:** {suspect['role']}")
    
    st.subheader("Interview a suspect")

    suspect_options = {
        suspect["name"]: suspect["id"]
        for suspect in suspects
    }

    selected_suspect_name = st.selectbox(
        "Choose a suspect to interview",
        options=list(suspect_options.keys()),
    )

    selected_suspect_id = suspect_options[selected_suspect_name]

    player_question = st.text_area(
        "Ask a question",
        placeholder="Example: Where were you when Edward was killed?",
    )

    response_mode = st.selectbox(
        "Response mode",
        options=["mock", "ollama", "openrouter"],
        help="Use mock for fast testing, Ollama for local generation, or OpenRouter for the live demo.",
    )

    model_names = {
        "mock": "mock",
        "ollama": "llama3.1:8b",
        "openrouter": "openai/gpt-4o-mini",
    }

    selected_model_name = model_names[response_mode]

    discovered_clues_for_options = get_discovered_clue_details()

    clue_options = {"No evidence": None}

    for clue in discovered_clues_for_options:
        clue_options[clue["name"]] = clue["id"]

    selected_clue_name = st.selectbox(
        "Optional: confront with evidence",
        options=list(clue_options.keys()),
    )

    confronted_clue_id = clue_options[selected_clue_name]

    if st.button("Ask suspect"):
        if not player_question.strip():
            st.warning("Please enter a question before interviewing the suspect.")
        else:
            initial_graph_state = {
                "game_data": game_data,
                "game_state": game_state,
                "suspect_id": selected_suspect_id,
                "player_question": player_question,
                "confronted_clue_id": confronted_clue_id,
                "rag_index": st.session_state.rag_index,
                "rag_documents": st.session_state.rag_documents,
                "embedding_model": st.session_state.embedding_model,
                "raw_rag_results": [],
                "filtered_rag_results": [],
                "retrieved_context": "",
                "interview_context": {},
                "messages": [],
                "llm_mode": response_mode,
                "model_name": selected_model_name,
                "npc_response": "",
                "validation_result": None,
            }

            with st.spinner("Interviewing suspect..."):
                updated_graph_state = st.session_state.interview_graph.invoke(
                    initial_graph_state
                )

            st.session_state.last_interview_result = updated_graph_state
            st.rerun()

    if "last_interview_result" in st.session_state:
        interview_result = st.session_state.last_interview_result

        st.subheader("Latest response")
        st.write(interview_result["npc_response"])

        st.subheader("Dialogue history with this suspect")

        selected_history = [
            entry
            for entry in game_state.dialogue_history
            if entry.suspect_id == interview_result["suspect_id"]
        ]

        for entry in selected_history:
            with st.container(border=True):
                st.markdown(f"**You:** {entry.player_question}")
                st.markdown(f"**{selected_suspect_name}:** {entry.npc_response}")
    
    st.divider()

    st.header("Investigate locations")

    locations = game_data["locations"]["locations"]

    location_options = {
        location["name"]: location
        for location in locations
        if location.get("available_from_start", False)
    }

    selected_location_name = st.selectbox(
        "Choose a location to investigate",
        options=list(location_options.keys()),
    )

    selected_location = location_options[selected_location_name]

    st.subheader(selected_location["name"])
    st.write(selected_location["description"])

    area_options = {
        area["label"]: area["id"]
        for area in selected_location["inspectable_areas"]
    }

    selected_area_label = st.selectbox(
        "Choose an area to inspect",
        options=list(area_options.keys()),
    )

    if st.button("Inspect area"):
        result = inspect_location_area(
            state=game_state,
            location=selected_location,
            area_id=area_options[selected_area_label],
        )

        st.session_state.last_inspection_result = result
        st.rerun()

    if "last_inspection_result" in st.session_state:
        result = st.session_state.last_inspection_result

        st.subheader("Inspection result")
        st.write(result["result_text"])

        if result["has_clue"]:
            clue = get_clue_by_id(
                game_data=game_data,
                clue_id=result["clue_id"],
            )
            clue_name = clue["name"]

            if result["newly_discovered"]:
                st.success(f"New clue discovered: **{clue_name}**")
            else:
                st.info(f"You already discovered this clue: **{clue_name}**")


if __name__ == "__main__":
    main()