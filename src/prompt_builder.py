from __future__ import annotations

from typing import Any


def format_list(items: list[str]) -> str:
    """
    Format a list of strings as Markdown bullet points.

    Args:
        items: List of strings to format.

    Returns:
        Bullet-point string representation of the list.
    """
    if not items:
        return "- None"

    return "\n".join(f"- {item}" for item in items)


def format_dialogue_history(dialogue_history: list[dict[str, Any]]) -> str:
    """
    Format previous dialogue exchanges for prompt context.

    Args:
        dialogue_history: List of dialogue entry dictionaries.

    Returns:
        Formatted dialogue history.
    """
    if not dialogue_history:
        return "No previous dialogue with this suspect."

    formatted_entries = []

    for index, entry in enumerate(dialogue_history, start=1):
        confronted_clue_id = entry["confronted_clue_id"]

        clue_line = ""
        if confronted_clue_id is not None:
            clue_line = f"\nConfronted evidence: {confronted_clue_id}"

        formatted_entries.append(
            (
                f"Exchange {index}:\n"
                f"Player: {entry['player_question']}"
                f"{clue_line}\n"
                f"Suspect: {entry['npc_response']}"
            )
        )

    return "\n\n".join(formatted_entries)

def format_improvised_facts(improvised_facts: list[str]) -> str:
    """
    Format established improvised facts for prompt context.

    These are harmless personal details previously established by the NPC
    during dialogue. They are included so the NPC remains consistent.

    Args:
        improvised_facts: List of improvised facts for the current suspect.

    Returns:
        Formatted improvised facts.
    """
    if not improvised_facts:
        return "No improvised personal facts have been established yet."

    return format_list(improvised_facts)


def format_confronted_clue(confronted_clue: dict[str, Any] | None) -> str:
    """
    Format confronted clue information for prompt context.

    Args:
        confronted_clue: Clue dictionary selected for confrontation, if any.

    Returns:
        Formatted clue information.
    """
    if confronted_clue is None:
        return "No evidence was explicitly presented in this question."

    return (
        f"Clue ID: {confronted_clue['id']}\n"
        f"Clue name: {confronted_clue['name']}\n"
        f"Description: {confronted_clue['description']}\n"
        f"What it suggests: {confronted_clue['what_it_suggests']}\n"
        f"Dialogue effect: {confronted_clue['dialogue_effects']['default']}"
    )


def format_evidence_reaction(
    evidence_reaction: dict[str, Any] | None,
    confronted_clue: dict[str, Any] | None,
    clue_is_related_to_suspect: bool,
) -> str:
    """
    Format evidence reaction guidance for prompt context.

    Args:
        evidence_reaction: Evidence reaction dictionary, if any.
        confronted_clue: Clue dictionary selected for confrontation, if any.
        clue_is_related_to_suspect: Whether the clue directly targets this suspect.

    Returns:
        Formatted evidence reaction guidance.
    """
    if confronted_clue is None:
        return "No evidence was presented, so no special evidence reaction applies."

    if not clue_is_related_to_suspect:
        return (
            "The presented evidence is not specifically connected to this suspect. "
            "The NPC should still answer naturally from their own knowledge and personality. "
            "They may deny knowledge, express surprise, dismiss its relevance, or redirect suspicion, "
            "but they must not invent new plot facts, new alibis, new witnesses, new documents, "
            "or hidden knowledge about the clue."
        )

    if evidence_reaction is None:
        return (
            "This evidence is connected to the suspect, but no special reaction is defined. "
            "The NPC should respond cautiously using only established character knowledge and the clue text."
        )

    may_reveal = evidence_reaction.get("may_reveal", [])

    return (
        f"Reaction type: {evidence_reaction['reaction_type']}\n"
        f"Response guidance: {evidence_reaction['response_guidance']}\n"
        f"May reveal:\n{format_list(may_reveal)}\n"
        f"Sample response tone/content: {evidence_reaction.get('sample_response', 'None')}"
    )


def build_npc_system_prompt(
    global_npc_rules: list[str],
    suspect: dict[str, Any],
) -> str:
    """
    Build the system prompt for an NPC.

    Args:
        global_npc_rules: Global behavior rules for all NPCs.
        suspect: Suspect dictionary from characters.json.

    Returns:
        System prompt string.
    """
    personality = format_list(suspect["personality"])
    knowledge = format_list(suspect["knowledge"])
    lies = format_list(suspect["lies"])
    forbidden_behavior = format_list(suspect["forbidden_behavior"])
    crime_time_location_id = suspect["alibi"].get(
        "crime_time_location_id",
        "No specific crime-time location is provided.",
    )

    return f"""
You are roleplaying as a suspect in an interactive detective mystery game.

You must follow these global NPC rules:

{format_list(global_npc_rules)}

Character profile:

Name: {suspect['name']}
Role: {suspect['role']}
Relationship to victim: {suspect['relationship_to_victim']}

Public description:
{suspect['public_description']}

Personality:
{personality}

Dialogue style:
{suspect['dialogue_style']}

Apparent motive:
{suspect['apparent_motive']['label']} — {suspect['apparent_motive']['description']}

Real secret:
{suspect['real_secret']}

Alibi:
Public claim: {suspect['alibi']['public_claim']}
Crime-time location ID: {crime_time_location_id}
Hidden truth: {suspect['alibi']['hidden_truth']}
Weakness: {suspect['alibi']['weakness']}

What this character knows:
{knowledge}

What this character lies about:
{lies}

Forbidden behavior:
{forbidden_behavior}

Important instruction:
Answer as {suspect['name']} only. Do not narrate as the game system. Do not reveal hidden plot information unless the current evidence reaction guidance allows it. You may improvise harmless personal details only when they do not affect the mystery or contradict established facts.

Grounding rule:
Treat the character profile, evidence reaction guidance, retrieved context, and previous dialogue as the only source of mystery-relevant factual information. Do not invent specific rooms, locations, alibis, activities, habits, substances, documents, relationships, or explanations that are not explicitly provided in the prompt.

Harmless improvisation rule:
You may improvise minor personal opinions, manners, and atmospheric reactions when they do not create new facts about the murder, evidence, timeline, locations, suspects, motives, relationships, or alibis.
""".strip()


def build_npc_user_prompt(interview_context: dict[str, Any]) -> str:
    """
    Build the user prompt for an NPC interview.

    Args:
        interview_context: Structured interview context from game_engine.py.

    Returns:
        User prompt string.
    """
    confronted_clue_text = format_confronted_clue(
        interview_context["confronted_clue"]
    )
    evidence_reaction_text = format_evidence_reaction(
        evidence_reaction=interview_context["evidence_reaction"],
        confronted_clue=interview_context["confronted_clue"],
        clue_is_related_to_suspect=interview_context[
            "confronted_clue_is_related_to_suspect"
        ],
    )
    dialogue_history_text = format_dialogue_history(
        interview_context["dialogue_history"]
    )
    improvised_facts_text = format_improvised_facts(
        interview_context["improvised_facts_for_suspect"]
    )

    retrieved_context_text = interview_context.get(
        "retrieved_context",
        "No additional retrieved context is available.",
    )

    discovered_clues = format_list(interview_context["discovered_clue_ids"])
    revealed_clues = format_list(interview_context["revealed_clue_ids_for_suspect"])

    return f"""
Current interview context:

Player question:
{interview_context['player_question']}

Evidence explicitly presented in this question:
{confronted_clue_text}

Evidence reaction guidance:
{evidence_reaction_text}

Clues discovered by the player so far:
{discovered_clues}

Clues already revealed to this suspect:
{revealed_clues}

Established improvised personal facts for this suspect:
{improvised_facts_text}

Relevant retrieved context:
{retrieved_context_text}

Previous dialogue with this suspect:
{dialogue_history_text}

Respond to the player's question in character.

Constraints:
- Keep the response concise: 2 to 4 sentences.
- Reply only with spoken dialogue; do not use stage directions, parenthetical actions, or narration.
- React directly to confronted evidence if evidence was presented.
- Follow the evidence reaction guidance when it exists.
- Use retrieved context only if it is relevant and consistent with the suspect's knowledge and game state.
- Do not treat retrieved context as permission to reveal hidden solution details.
- Do not confess to the murder unless explicitly allowed by the ending logic.
- Do not reveal the final solution.
- Do not invent plot-relevant facts.
- Do not invent new clues, motives, alibis, suspects, locations, crimes, documents, relationships, habits, substances, or solution details.
- Do not invent specific alternative explanations for evidence unless they are explicitly provided in the prompt.
- If challenged about evidence and no explicit alternative explanation is provided, cast doubt on the player's interpretation without suggesting any cause, alternative source, contamination, accident, mistake, or innocent explanation.
- If asked where you were or what you were doing when the crime occurred, use only the public alibi and Crime-time location ID from the character profile. Do not invent a new room, location, errand, activity, or witness.
- If a Crime-time location ID is provided, do not replace it with a different room or a generic phrase like "my room" unless that exact phrase is in the public alibi. If no Crime-time location ID is provided, do not supply a location.
- If asked about an unprovided harmless personal opinion or atmospheric detail, answer in character without creating new mystery facts.
- Stay consistent with established improvised personal facts, but never let improvised details become evidence, alibi information, or solution logic.

Bad response patterns:
"It was probably residue from cheap liquor."
"It could be contamination."
"It may have come from some innocent source."
"There are many harmless explanations."

Good response pattern:
"Residue in a glass proves very little unless one already knows what one wishes it to prove. I would advise caution before treating such a small trace as proof."

Harmless small-talk example:
Player: "What do you think of the weather tonight?"
Good response pattern:
"This storm is dreadful, but hardly surprising for Blackwood Manor. It suits the mood of the house rather too well."
""".strip()


def build_npc_messages(
    game_data: dict[str, dict[str, Any]],
    interview_context: dict[str, Any],
) -> list[dict[str, str]]:
    """
    Build chat messages for an NPC interview.

    Args:
        game_data: Dictionary containing all loaded game data.
        interview_context: Structured interview context from game_engine.py.

    Returns:
        List of chat messages ready to send to an LLM.
    """
    global_npc_rules = game_data["characters"]["global_npc_rules"]
    suspect = interview_context["suspect"]

    system_prompt = build_npc_system_prompt(
        global_npc_rules=global_npc_rules,
        suspect=suspect,
    )

    user_prompt = build_npc_user_prompt(interview_context)

    return [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]