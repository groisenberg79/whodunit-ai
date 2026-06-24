# Whodunit AI

Whodunit AI is a GenAI capstone prototype focused on stateful LLM interaction, evidence-aware dialogue, and natural-language reasoning over structured application data.

Although the project uses a mystery-game setting, the main goal is not game design. The mystery format provides a controlled environment for testing technical problems common in LLM applications: maintaining conversation state, grounding generated responses in structured data, reacting to user-provided context, validating model outputs, and converting free-form user input into structured decisions.

The player investigates a fictional murder case by exploring locations, discovering clues, interviewing suspects, confronting them with evidence, and submitting a final accusation in natural language. Behind the interface, the application combines JSON-based domain data, game state tracking, retrieval-augmented context, prompt construction, response validation, and LLM-based accusation parsing.

## Technical Focus

This project is primarily an experiment in building a reliable LLM-powered interaction system. The core technical goals are:

- Maintain persistent game state across location exploration, clue discovery, suspect interviews, and accusations.
- Generate NPC responses constrained by character profiles, known facts, discovered evidence, prior dialogue, and hidden solution boundaries.
- Support evidence-aware conversations where suspects react differently depending on which clues the player presents.
- Track which evidence has already been shown to each suspect, so repeated confrontations can produce different responses.
- Limit evidence confrontations to a small number of clues, keeping the prompt focused and the interaction interpretable.
- Use retrieval to provide relevant context to the LLM without exposing hidden solution data.
- Validate generated NPC responses to reduce hallucinations, contradictions, accidental confessions, and unsupported plot claims.
- Parse free-form final accusations into structured culprit, motive, method, and evidence fields.
- Score accusations partially, allowing incomplete or imperfect answers instead of requiring exact wording.

## Why a Mystery Scenario?

The mystery format is useful because it creates a compact but challenging test case for LLM behavior. A suspect interview system requires the model to balance several competing constraints: answer naturally, stay in character, acknowledge evidence, avoid revealing hidden information too early, remember previous interactions, and respond differently as the player discovers more.

In other words, the mystery is a practical sandbox for testing stateful, constrained, context-aware LLM interactions. The project is not intended as a polished commercial game or a full mystery-writing exercise.

## Current Features

- Streamlit interface for exploring locations, inspecting areas, interviewing suspects, and submitting accusations.
- Structured JSON data for characters, clues, locations, and the hidden solution.
- Persistent `GameState` object tracking discovered clues, revealed evidence, interviewed suspects, dialogue history, improvised facts, and accusation attempts.
- LLM-powered suspect interviews using prompt context assembled from character data, evidence metadata, game state, and retrieved context.
- Evidence confrontations with support for one to three clues at a time.
- Combo-evidence reactions that let suspects respond differently to meaningful clue combinations.
- Repeated-evidence tracking so suspects can react differently when shown the same clues again.
- RAG-style retrieval with FAISS and sentence embeddings for relevant context injection.
- Response validation and fallback handling to reduce unsupported or solution-breaking NPC responses.
- Free-form final accusation parsing, where an LLM maps the player's written explanation to structured motive, method, and evidence IDs.
- Partial accusation scoring, so the player can be partly correct without solving every part of the case.
- Generated visual assets for suspects and locations.

## How to Run

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and add your OpenRouter API key if using the hosted LLM mode.
5. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

The app can also be tested in mock or local modes depending on the configuration in `src/llm_client.py`.

## Tech Stack

- Python
- Streamlit
- JSON-based domain data
- OpenRouter-compatible LLM API
- Optional local/mock LLM modes
- FAISS
- Sentence embeddings
- LangGraph-style interview flow
- Pydantic/dataclass-style state modeling

## Project Status

The project is a working prototype. The focus is on the technical architecture of stateful LLM interaction rather than on producing a fully polished detective game. Some narrative details and mystery-design elements are intentionally compact, because the main goal is to demonstrate how structured data, retrieval, prompting, validation, and state tracking can work together in an interactive GenAI application.