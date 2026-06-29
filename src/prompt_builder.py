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


def format_confronted_clues(
    confronted_clues: list[dict[str, Any]],
    suspect_id: str,
) -> str:
    """
    Format all clues explicitly presented in the current confrontation.

    Args:
        confronted_clues: List of clue dictionaries selected by the player.
        suspect_id: Current suspect ID.

    Returns:
        Human-readable evidence summary.
    """
    if not confronted_clues:
        return "No evidence was presented."

    lines = []
    for index, clue in enumerate(confronted_clues, start=1):
        confrontation_targets = clue.get("confrontation_targets", [])
        relation = (
            "directly related to this suspect"
            if suspect_id in confrontation_targets
            else "not directly related to this suspect"
        )

        lines.append(
            f"{index}. {clue['name']}\n"
            f"   Relevance: {relation}\n"
            f"   Description: {clue['description']}\n"
            f"   What it suggests: {clue['what_it_suggests']}\n"
            f"   Dialogue effect: {clue['dialogue_effects']['default']}"
        )

    return "\n\n".join(lines)



def format_evidence_acknowledgement_checklist(
    confronted_clues: list[dict[str, Any]],
) -> str:
    """
    Build a mandatory checklist forcing the NPC to acknowledge each presented clue.
    """
    if not confronted_clues:
        return "No evidence acknowledgement is required because no evidence was presented."

    lines = [
        "The response must explicitly acknowledge each of the following evidence items:"
    ]

    for clue in confronted_clues:
        lines.append(f"- {clue['name']}")

    lines.append(
        "Do not give only a general denial, emotional reaction, or philosophical objection. "
        "Each listed item must be mentioned directly or by an unmistakable paraphrase."
    )

    return "\n".join(lines)


# --- Inserted helper: format_repeated_evidence_context ---
def format_repeated_evidence_context(
    repeated_clue_ids: list[str],
    new_clue_ids: list[str],
    confronted_clues: list[dict[str, Any]],
) -> str:
    """
    Format whether presented evidence has already been shown to this suspect.

    Args:
        repeated_clue_ids: Presented clue IDs already revealed to this suspect.
        new_clue_ids: Presented clue IDs not yet revealed to this suspect.
        confronted_clues: Full clue dictionaries presented in this confrontation.

    Returns:
        Repeated-evidence guidance for the NPC prompt.
    """
    if not confronted_clues:
        return "No evidence was presented."

    clue_names_by_id = {
        clue["id"]: clue["name"]
        for clue in confronted_clues
    }

    repeated_names = [
        clue_names_by_id[clue_id]
        for clue_id in repeated_clue_ids
        if clue_id in clue_names_by_id
    ]
    new_names = [
        clue_names_by_id[clue_id]
        for clue_id in new_clue_ids
        if clue_id in clue_names_by_id
    ]

    repeated_text = format_list(repeated_names)
    new_text = format_list(new_names)

    if repeated_names and not new_names:
        repeated_guidance = (
            "All evidence presented in this question has already been shown to this suspect. "
            "The suspect must make this repetition noticeable in the response. "
            "They should explicitly indicate that the detective has already raised these same items before, "
            "then restate or sharpen their previous position in character. "
            "They should sound more impatient, weary, colder, more defensive, or more emotionally strained than before."
        )
    elif repeated_names:
        repeated_guidance = (
            "Some evidence presented in this question has already been shown to this suspect. "
            "The suspect should distinguish repeated evidence from newly presented evidence. "
            "They should not act newly surprised by repeated items, and should briefly refer back to having addressed them before."
        )
    else:
        repeated_guidance = (
            "All evidence presented in this question is new to this suspect. "
            "The suspect may react as though encountering these items for the first time."
        )

    return f"""Repeated evidence already shown to this suspect:
{repeated_text}

Newly presented evidence for this suspect:
{new_text}

Repeated-evidence behavior requirement:
{repeated_guidance}"""


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
    must_show = evidence_reaction.get("must_show", [])
    must_not_reveal = evidence_reaction.get("must_not_reveal", [])

    return (
        f"Reaction type: {evidence_reaction['reaction_type']}\n"
        f"Response guidance: {evidence_reaction['response_guidance']}\n"
        f"May reveal:\n{format_list(may_reveal)}\n"
        f"Must show in this response:\n{format_list(must_show)}\n"
        f"Must not reveal:\n{format_list(must_not_reveal)}\n"
        "Do not copy sample responses from the data verbatim. Generate a fresh response that obeys the presented-evidence checklist."
    )
# --- Inserted helper: format_repeated_evidence_context ---
def format_critical_reaction_requirement(
    evidence_reaction: dict[str, Any] | None,
) -> str:
    """
    Format high-priority reaction requirements that override default composure.
    """
    if evidence_reaction is None:
        return "No special reaction requirement."

    reaction_type = evidence_reaction.get("reaction_type")

    if reaction_type == "culprit_pressure_mask_slipping":
        return (
            "CRITICAL: Henry's composure must visibly weaken in this response. "
            "Do not make him sound calmly superior throughout the whole answer. "
            "He should show controlled emotional strain through wording, not stage directions: "
            "shorter sentences, repeated denial, sharper defensiveness, or a sudden personal warning. "
            "He may say things like 'No. That is not what it proves.' or "
            "'You are very close to making an accusation you do not understand.' "
            "He must still acknowledge all evidence, must not confess, and should recover some cold control by the end."
        )

    return "No special reaction requirement."


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
    crime_time_location_name = suspect["alibi"].get(
        "crime_time_location_name",
        "No specific crime-time location is provided.",
    )
    crime_time_location_spoken_name = suspect["alibi"].get(
        "crime_time_location_spoken_name",
        crime_time_location_name,
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
Crime-time location display name: {crime_time_location_name}
Crime-time location spoken name: {crime_time_location_spoken_name}
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
    confronted_clue_text = format_confronted_clues(
        confronted_clues=interview_context.get("confronted_clues", []),
        suspect_id=interview_context["suspect"]["id"],
    )
    evidence_reaction_text = format_evidence_reaction(
        evidence_reaction=interview_context["evidence_reaction"],
        confronted_clue=interview_context["confronted_clue"],
        clue_is_related_to_suspect=interview_context[
            "confronted_clue_is_related_to_suspect"
        ],
    )
    critical_reaction_requirement = format_critical_reaction_requirement(
        interview_context["evidence_reaction"]
    )
    evidence_acknowledgement_checklist = format_evidence_acknowledgement_checklist(
        interview_context.get("confronted_clues", [])
    )
    # Insert repeated evidence context block
    repeated_evidence_text = format_repeated_evidence_context(
        repeated_clue_ids=interview_context.get("repeated_confronted_clue_ids", []),
        new_clue_ids=interview_context.get("new_confronted_clue_ids", []),
        confronted_clues=interview_context.get("confronted_clues", []),
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

Critical reaction requirement:
{critical_reaction_requirement}

Mandatory evidence acknowledgement checklist:
{evidence_acknowledgement_checklist}

Repeated evidence context:
{repeated_evidence_text}

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
- If no evidence was presented, answer in 2 to 4 sentences.
- If one piece of evidence was presented, answer in 1 to 2 short paragraphs.
- If two or three pieces of evidence were presented, answer in 2 to 4 short paragraphs, with a more developed emotional or defensive progression.
- Reply only with spoken dialogue; do not use stage directions, parenthetical actions, or narration.
- If evidence was presented, explicitly acknowledge every presented evidence item before giving a general denial or philosophical objection.
- When acknowledging evidence, do not mechanically repeat formal clue titles if they would sound unnatural in spoken dialogue. Use natural first-person or context-aware phrasing instead. For example, Beatrice should refer to Beatrice's Letters as "my letters", "those letters", or "the letters I wrote to Edward", not as "Beatrice's Letters".
- If all presented evidence has already been shown to this suspect, explicitly say or clearly imply that the detective has already raised these same items before. Do not answer as if the repeated evidence is new.
- If some presented evidence is repeated and some is new, distinguish the repeated evidence from the new evidence in the response.
- Do not answer a confrontation with only a generic phrase such as "speculation is not proof", "you have no proof", or "I will not dignify that accusation." Those phrases may appear only after you have addressed each presented item.
- For evidence directly related to you, respond with stronger emotion, pressure, defensiveness, confession of the allowed secret, or denial according to the evidence reaction guidance.
- For evidence not directly related to you, still acknowledge it. Say whether you recognize it, deny ownership, deny expertise, or refuse its relevance, without inventing a new explanation.
- Maintain your character's distinct personality and dialogue style. Clara should sound controlled and bitter; Julian wounded and volatile; Beatrice elegant and emotionally exposed; Henry precise, cold, and clinical.
- Follow the evidence reaction guidance when it exists. If there is a Critical reaction requirement, it is mandatory and overrides the suspect's usual composure or default personality style.
- If the evidence reaction includes a "Must show in this response" checklist, every item in that checklist is mandatory. The mandatory evidence acknowledgement checklist, the Critical reaction requirement, and the "Must show" checklist all have priority over sample-like phrasing.
- Use retrieved context only if it is relevant and consistent with the suspect's knowledge and game state.
- Do not treat retrieved context as permission to reveal hidden solution details.
- Do not confess to the murder unless explicitly allowed by the ending logic.
- Do not reveal the final solution.
- Do not invent plot-relevant facts.
- Do not invent new clues, motives, alibis, suspects, locations, crimes, documents, relationships, habits, substances, or solution details.
- Do not invent specific alternative explanations for evidence unless they are explicitly provided in the prompt.
- If challenged about evidence and no explicit alternative explanation is provided, cast doubt on the player's interpretation without suggesting any cause, alternative source, contamination, accident, mistake, or innocent explanation.
- If asked where you were or what you were doing when the crime occurred, use only the public alibi and Crime-time location spoken name from the character profile. Do not invent a new room, location, errand, activity, or witness.
- Use the Crime-time location spoken name in your answer, not the display name. For example, if the spoken name is "my room", say "my room"; do not refer to yourself in the third person by saying "Dr. Ashford's Room" or "Beatrice's Room".
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