from __future__ import annotations

from typing import Any


def create_document(
    doc_id: str,
    text: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """
    Create a retrievable document dictionary.

    Args:
        doc_id: Unique document ID.
        text: Text content to embed and retrieve.
        metadata: Metadata used for filtering and debugging.

    Returns:
        Document dictionary.
    """
    return {
        "id": doc_id,
        "text": text.strip(),
        "metadata": metadata,
    }


def create_character_documents(characters_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Create retrievable documents from character data.

    Args:
        characters_data: Loaded data from characters.json.

    Returns:
        List of character-related retrieval documents.
    """
    documents = []

    for character in characters_data["characters"]:
        character_id = character["id"]

        profile_text = f"""
Character: {character["name"]}
Role: {character["role"]}
Relationship to victim: {character["relationship_to_victim"]}

Public description:
{character["public_description"]}

Personality:
{", ".join(character["personality"])}

Dialogue style:
{character["dialogue_style"]}

Apparent motive:
{character["apparent_motive"]["label"]}: {character["apparent_motive"]["description"]}

Real secret:
{character["real_secret"]}

Alibi:
Public claim: {character["alibi"]["public_claim"]}
Hidden truth: {character["alibi"]["hidden_truth"]}
Weakness: {character["alibi"]["weakness"]}
"""

        documents.append(
            create_document(
                doc_id=f"character_profile::{character_id}",
                text=profile_text,
                metadata={
                    "source": "characters",
                    "document_type": "character_profile",
                    "suspect_id": character_id,
                    "visibility": "suspect_context",
                },
            )
        )

        knowledge_text = f"""
Character: {character["name"]}

What this character knows:
{chr(10).join(f"- {item}" for item in character["knowledge"])}

What this character lies about:
{chr(10).join(f"- {item}" for item in character["lies"])}
"""

        documents.append(
            create_document(
                doc_id=f"character_knowledge::{character_id}",
                text=knowledge_text,
                metadata={
                    "source": "characters",
                    "document_type": "character_knowledge",
                    "suspect_id": character_id,
                    "visibility": "suspect_private",
                },
            )
        )

        for clue_id, reaction in character["evidence_reactions"].items():
            reaction_text = f"""
Character: {character["name"]}
Evidence reaction for clue: {clue_id}

Reaction type:
{reaction["reaction_type"]}

Response guidance:
{reaction["response_guidance"]}

May reveal:
{chr(10).join(f"- {item}" for item in reaction.get("may_reveal", []))}

Sample response:
{reaction.get("sample_response", "None")}
"""

            documents.append(
                create_document(
                    doc_id=f"evidence_reaction::{character_id}::{clue_id}",
                    text=reaction_text,
                    metadata={
                        "source": "characters",
                        "document_type": "evidence_reaction",
                        "suspect_id": character_id,
                        "clue_id": clue_id,
                        "visibility": "only_when_confronted",
                    },
                )
            )

        for reaction in character.get("combo_evidence_reactions", []):
            combo_text = f"""
Character: {character["name"]}
Combo evidence reaction: {reaction["id"]}

Required clues:
{chr(10).join(f"- {item}" for item in reaction["required_clue_ids"])}

Trigger clues:
{chr(10).join(f"- {item}" for item in reaction["trigger_clue_ids"])}

Reaction type:
{reaction["reaction_type"]}

Response guidance:
{reaction["response_guidance"]}

May reveal:
{chr(10).join(f"- {item}" for item in reaction.get("may_reveal", []))}

Sample response:
{reaction.get("sample_response", "None")}
"""

            documents.append(
                create_document(
                    doc_id=f"combo_reaction::{character_id}::{reaction['id']}",
                    text=combo_text,
                    metadata={
                        "source": "characters",
                        "document_type": "combo_evidence_reaction",
                        "suspect_id": character_id,
                        "required_clue_ids": reaction["required_clue_ids"],
                        "trigger_clue_ids": reaction["trigger_clue_ids"],
                        "visibility": "only_when_combo_applies",
                    },
                )
            )

    return documents


def create_clue_documents(clues_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Create retrievable documents from clue data.

    Each clue is split into two documents:
    - a player-facing clue document that can be retrieved during interviews
      once the clue has been discovered,
    - an internal interpretation document that should not be used in ordinary
      NPC interviews.

    Args:
        clues_data: Loaded data from clues.json.

    Returns:
        List of clue-related retrieval documents.
    """
    documents = []

    for clue in clues_data["clues"]:
        public_clue_text = f"""
Clue: {clue["name"]}
Clue ID: {clue["id"]}
Location ID: {clue["location_id"]}
Type: {clue["type"]}
Category: {clue["category"]}
Solution critical: {clue["is_solution_critical"]}

Description:
{clue["description"]}

Discovery text:
{clue["discovery_text"]}

What it suggests:
{clue["what_it_suggests"]}

Related suspects:
{", ".join(clue["related_suspect_ids"])}

Confrontation targets:
{", ".join(clue["confrontation_targets"])}
"""

        documents.append(
            create_document(
                doc_id=f"clue_public::{clue['id']}",
                text=public_clue_text,
                metadata={
                    "source": "clues",
                    "document_type": "clue_public",
                    "clue_id": clue["id"],
                    "location_id": clue["location_id"],
                    "related_suspect_ids": clue["related_suspect_ids"],
                    "confrontation_targets": clue["confrontation_targets"],
                    "visibility": "only_if_discovered",
                    "is_solution_critical": clue["is_solution_critical"],
                },
            )
        )

        internal_clue_text = f"""
Internal interpretation for clue: {clue["name"]}
Clue ID: {clue["id"]}

What it actually means:
{clue["what_it_actually_means"]}

Solution critical:
{clue["is_solution_critical"]}

Category:
{clue["category"]}

Related suspects:
{", ".join(clue["related_suspect_ids"])}
"""

        documents.append(
            create_document(
                doc_id=f"clue_internal::{clue['id']}",
                text=internal_clue_text,
                metadata={
                    "source": "clues",
                    "document_type": "clue_internal",
                    "clue_id": clue["id"],
                    "location_id": clue["location_id"],
                    "related_suspect_ids": clue["related_suspect_ids"],
                    "visibility": "internal_or_feedback",
                    "is_solution_critical": clue["is_solution_critical"],
                },
            )
        )

    return documents


def create_location_documents(locations_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Create retrievable documents from location data.

    Args:
        locations_data: Loaded data from locations.json.

    Returns:
        List of location-related retrieval documents.
    """
    documents = []

    for location in locations_data["locations"]:
        areas_text = "\n".join(
            (
                f"- {area['label']} ({area['id']}): "
                f"{area['description']} Result: {area['result_text']}"
            )
            for area in location["inspectable_areas"]
        )

        location_text = f"""
Location: {location["name"]}
Location ID: {location["id"]}

Short description:
{location["short_description"]}

Description:
{location["description"]}

Function in mystery:
{location["function_in_mystery"]}

Clues found here:
{", ".join(location["clue_ids"])}

Inspectable areas:
{areas_text}
"""

        documents.append(
            create_document(
                doc_id=f"location::{location['id']}",
                text=location_text,
                metadata={
                    "source": "locations",
                    "document_type": "location",
                    "location_id": location["id"],
                    "clue_ids": location["clue_ids"],
                    "visibility": "location_context",
                },
            )
        )

    return documents


def create_solution_documents(solution_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Create retrievable documents from solution data.

    These documents are highly sensitive and should not be freely retrieved during
    ordinary NPC interviews. They are mainly useful for final accusation feedback,
    consistency checks, or internal validation.

    Args:
        solution_data: Loaded data from solution.json.

    Returns:
        List of solution-related retrieval documents.
    """
    documents = []

    solution_text = f"""
Hidden solution for case: {solution_data["case_id"]}

Culprit:
{solution_data["culprit"]["name"]} ({solution_data["culprit"]["suspect_id"]})

True motive:
{solution_data["true_motive"]["label"]}: {solution_data["true_motive"]["description"]}

Method:
{solution_data["method"]["label"]}: {solution_data["method"]["description"]}

Opportunity:
{solution_data["opportunity"]["description"]}

Required evidence:
{chr(10).join(f"- {item}" for item in solution_data["required_evidence_ids"])}

Supporting evidence:
{chr(10).join(f"- {item}" for item in solution_data["supporting_evidence_ids"])}
"""

    documents.append(
        create_document(
            doc_id="solution::hidden_solution",
            text=solution_text,
            metadata={
                "source": "solution",
                "document_type": "hidden_solution",
                "visibility": "internal_only",
            },
        )
    )

    for false_motive in solution_data["false_motives"]:
        motive_text = f"""
False motive:
{false_motive["label"]}

Points to:
{false_motive["points_to"]}

Description:
{false_motive["description"]}
"""

        documents.append(
            create_document(
                doc_id=f"solution_false_motive::{false_motive['id']}",
                text=motive_text,
                metadata={
                    "source": "solution",
                    "document_type": "false_motive",
                    "motive_id": false_motive["id"],
                    "points_to": false_motive["points_to"],
                    "visibility": "internal_or_feedback",
                },
            )
        )

    return documents


def create_all_documents(game_data: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Create all retrievable documents from loaded game data.

    Args:
        game_data: Dictionary containing all loaded game data.

    Returns:
        List of retrievable document dictionaries.
    """
    documents = []

    documents.extend(create_character_documents(game_data["characters"]))
    documents.extend(create_clue_documents(game_data["clues"]))
    documents.extend(create_location_documents(game_data["locations"]))
    documents.extend(create_solution_documents(game_data["solution"]))

    return documents