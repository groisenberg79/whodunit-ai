from __future__ import annotations

from src.game_engine import inspect_location_area
from src.data_loader import get_clue_by_id, load_game_data
from src.game_state import GameState
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