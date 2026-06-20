from __future__ import annotations

import json
from typing import Any

from src.llm_client import LLMClientError, LLMMode, generate_llm_response


def _format_options(options: list[dict[str, str]]) -> str:
    """
    Format accusation options for the LLM judge.
    """
    return "\n".join(
        f"- id: {option['id']} | label: {option['label']}"
        for option in options
    )


def _format_discovered_clues(discovered_clues: list[dict[str, Any]]) -> str:
    """
    Format discovered clues for the LLM judge.
    """
    if not discovered_clues:
        return "No clues have been discovered."

    return "\n".join(
        f"- id: {clue['id']} | name: {clue['name']} | description: {clue['description']}"
        for clue in discovered_clues
    )


def evaluate_free_form_accusation(
    game_data: dict[str, Any],
    accused_culprit_id: str,
    accusation_text: str,
    discovered_clues: list[dict[str, Any]],
    mode: LLMMode = "openrouter",
    model_name: str = "openai/gpt-5.5",
) -> dict[str, Any]:
    """
    Use an LLM to convert a player's free-form accusation into structured IDs.

    The LLM does not decide whether the accusation is correct. It only extracts
    the intended culprit, motive, method, and evidence IDs. The deterministic
    game engine performs the actual scoring afterward.
    """
    solution_data = game_data["solution"]
    accusation_options = solution_data["accusation_options"]

    culprit_options = _format_options(accusation_options["culprits"])
    motive_options = _format_options(accusation_options["motives"])
    method_options = _format_options(accusation_options["methods"])
    discovered_clue_options = _format_discovered_clues(discovered_clues)

    system_message = """
You are an accusation parser for a detective mystery game.

Your task is not to solve the mystery independently.
Your task is to interpret the player's free-form accusation and convert it into structured IDs.

Rules:
- Return valid JSON only.
- Do not include markdown.
- Do not explain your reasoning outside the JSON.
- Use only the IDs provided in the option lists.
- For evidence, use only discovered clue IDs listed in the prompt.
- If the player implies a correct option using different wording, map it to the closest provided ID.
- If the player does not clearly specify motive, method, or evidence, use null or an empty list.
""".strip()

    user_message = f"""
Accused culprit selected by player:
{accused_culprit_id}

Player's written accusation:
{accusation_text}

Available culprit IDs:
{culprit_options}

Available motive IDs:
{motive_options}

Available method IDs:
{method_options}

Discovered clue IDs available as evidence:
{discovered_clue_options}

Return JSON with exactly this shape:
{{
  "culprit_id": "one culprit id",
  "motive_id": "one motive id or null",
  "method_id": "one method id or null",
  "evidence_ids": ["zero or more discovered clue ids"],
  "summary": "one short sentence explaining how you interpreted the accusation"
}}
""".strip()

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    try:
        raw_response = generate_llm_response(
            messages=messages,
            mode=mode,
            model_name=model_name,
        )
    except LLMClientError as exc:
        return {
            "culprit_id": accused_culprit_id,
            "motive_id": None,
            "method_id": None,
            "evidence_ids": [],
            "summary": f"Could not evaluate accusation with LLM: {exc}",
        }

    try:
        parsed_response = json.loads(raw_response)
    except json.JSONDecodeError:
        return {
            "culprit_id": accused_culprit_id,
            "motive_id": None,
            "method_id": None,
            "evidence_ids": [],
            "summary": "The accusation judge returned invalid JSON, so only the selected culprit was used.",
        }

    return {
        "culprit_id": parsed_response.get("culprit_id") or accused_culprit_id,
        "motive_id": parsed_response.get("motive_id"),
        "method_id": parsed_response.get("method_id"),
        "evidence_ids": parsed_response.get("evidence_ids", []),
        "summary": parsed_response.get(
            "summary",
            "The accusation was interpreted from the player's written explanation.",
        ),
    }