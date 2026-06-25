from __future__ import annotations

from src.game_engine import inspect_location_area, submit_accusation
from src.data_loader import get_clue_by_id, load_game_data
from src.accusation_evaluator import evaluate_free_form_accusation
from src.game_state import GameState
from src.interview_graph import build_interview_graph
from src.rag_index import load_embedding_model, load_rag_index
import streamlit as st
from pathlib import Path


MAX_EVIDENCE_PER_CONFRONTATION = 3


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

def render_multiline_text(text: str) -> None:
    """
    Render text while preserving intended line breaks in Streamlit Markdown.
    """
    st.markdown(text.replace("\n", "  \n"))


def reset_game() -> None:
    """
    Reset the game state while keeping the loaded game data.
    """
    st.session_state.game_state = GameState.from_case_data(
        st.session_state.game_data["case"]
    )

    if "last_accusation_result" in st.session_state:
        del st.session_state.last_accusation_result

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
                render_multiline_text(clue["description"])

    st.divider()

    st.header("Suspects")

    suspects = game_data["characters"]["characters"]

    for suspect in suspects:
        with st.expander(suspect["name"]):
            image_path = suspect.get("image_path")

            if image_path and Path(image_path).exists():
                st.image(image_path, width=260)

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
        "openrouter": "openai/gpt-5.5",
    }

    selected_model_name = model_names[response_mode]

    discovered_clues_for_options = get_discovered_clue_details()

    clue_options = {"No evidence": None}

    for clue in discovered_clues_for_options:
        clue_options[clue["name"]] = clue["id"]

    selected_clue_names = st.multiselect(
        "Optional: confront with evidence",
        options=[
            clue_name
            for clue_name in clue_options.keys()
            if clue_name != "No evidence"
        ],
        max_selections=MAX_EVIDENCE_PER_CONFRONTATION,
        help=(
            f"You may present up to {MAX_EVIDENCE_PER_CONFRONTATION} discovered clues. "
            "Some suspects may react differently when confronted with a combination "
            "of evidence."
        ),
    )
    st.caption(
        f"You may present up to {MAX_EVIDENCE_PER_CONFRONTATION} pieces of evidence "
        "in one confrontation."
    )

    confronted_clue_ids = [
        clue_options[clue_name]
        for clue_name in selected_clue_names
    ]

    confronted_clue_id = (
        confronted_clue_ids[0]
        if confronted_clue_ids
        else None
    )

    if st.button("Ask suspect"):
        if not player_question.strip():
            st.warning("Please enter a question before interviewing the suspect.")
        elif len(confronted_clue_ids) > MAX_EVIDENCE_PER_CONFRONTATION:
            st.warning(
                f"Please present at most {MAX_EVIDENCE_PER_CONFRONTATION} pieces "
                "of evidence in a single confrontation."
            )
        else:
            initial_graph_state = {
                "game_data": game_data,
                "game_state": game_state,
                "suspect_id": selected_suspect_id,
                "player_question": player_question,
                "confronted_clue_id": confronted_clue_id,
                "confronted_clue_ids": confronted_clue_ids,
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

    selected_history = [
        entry
        for entry in game_state.dialogue_history
        if entry.suspect_id == selected_suspect_id
    ]

    if "last_interview_result" in st.session_state:
        interview_result = st.session_state.last_interview_result

        if interview_result["suspect_id"] == selected_suspect_id:
            st.subheader("Latest response")
            st.write(interview_result["npc_response"])

    st.subheader("Dialogue history with this suspect")

    if not selected_history:
        st.caption("No dialogue with this suspect yet.")
    else:
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

    location_image_path = selected_location.get("image_path")
    if location_image_path and Path(location_image_path).exists():
        st.image(location_image_path, use_container_width=True)

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

        result_matches_current_selection = (
            result["location_id"] == selected_location["id"]
            and result["area_id"] == area_options[selected_area_label]
        )

        if result_matches_current_selection:
            st.subheader("Inspection result")
            render_multiline_text(result["result_text"])

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


    st.divider()

    st.header("Make your accusation")
    st.write(
        "When you think you understand the case, choose a suspect and explain "
        "your accusation in your own words."
    )

    solution_data = game_data["solution"]
    accusation_options = solution_data["accusation_options"]

    culprit_options = {
        option["label"]: option["id"]
        for option in accusation_options["culprits"]
    }

    selected_culprit_label = st.selectbox(
        "Who do you accuse?",
        options=list(culprit_options.keys()),
    )

    accusation_text = st.text_area(
        "Explain your accusation",
        placeholder=(
            "Example: I accuse [suspect] because [motive]. I think they committed "
            "the murder by [method]. The clues that support this are [clue 1], "
            "[clue 2], and [clue 3]."
        ),
        height=180,
    )

    st.caption(
        "Only clues you have discovered in Case notes can be counted as supporting evidence."
    )

    if st.button("Submit accusation"):
        if not accusation_text.strip():
            st.warning("Please explain your accusation before submitting it.")
        else:
            discovered_clues = get_discovered_clue_details()

            with st.spinner("Interpreting your accusation..."):
                interpreted_accusation = evaluate_free_form_accusation(
                    game_data=game_data,
                    accused_culprit_id=culprit_options[selected_culprit_label],
                    accusation_text=accusation_text,
                    discovered_clues=discovered_clues,
                )

            # Use the culprit selected from the dropdown as authoritative
            selected_culprit_id = culprit_options[selected_culprit_label]

            accusation_output = submit_accusation(
                state=game_state,
                game_data=game_data,
                culprit_id=selected_culprit_id,
                motive_id=interpreted_accusation["motive_id"],
                method_id=interpreted_accusation["method_id"],
                evidence_ids=interpreted_accusation["evidence_ids"],
            )

            st.session_state.last_accusation_result = accusation_output
            st.session_state.last_interpreted_accusation = interpreted_accusation
            st.rerun()

    if "last_accusation_result" in st.session_state:
        accusation_output = st.session_state.last_accusation_result
        interpreted_accusation = st.session_state.get(
            "last_interpreted_accusation",
            {},
        )

        result = accusation_output["result"]
        result_data = result if isinstance(result, dict) else result.__dict__

        st.subheader("Accusation interpretation")

        if interpreted_accusation.get("summary"):
            st.write(interpreted_accusation["summary"])

        with st.expander("Structured interpretation"):
            st.json(interpreted_accusation)

        st.subheader("Accusation result")

        score = result_data.get("score")
        max_score = solution_data["scoring"]["max_score"]

        if score is not None:
            st.write(f"Score: **{score} / {max_score}**")

        title = result_data.get("title")
        message = result_data.get("message")

        if accusation_output["game_status"] == "solved":
            st.success(title or "Correct accusation")
            st.subheader("Case closed")
            st.write(solution_data["ending_text"]["correct_ending"])
        else:
            st.warning(title or "Accusation incomplete")

        if message:
            st.write(message)

        feedback_key = result_data.get("feedback_key")
        if feedback_key:
            st.caption(f"Feedback category: {feedback_key}")


if __name__ == "__main__":
    main()