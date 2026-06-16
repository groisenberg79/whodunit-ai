from __future__ import annotations

from typing import Literal


LLMMode = Literal["mock", "ollama"]


class LLMClientError(Exception):
    """Raised when an LLM response cannot be generated."""


def generate_mock_response(messages: list[dict[str, str]]) -> str:
    """
    Generate a placeholder response for testing.

    Args:
        messages: Chat-style messages.

    Returns:
        Mock response string.
    """
    return (
        "I will answer that carefully, though I suspect you have already formed "
        "your theory."
    )


def generate_ollama_response(
    messages: list[dict[str, str]],
    model_name: str = "llama3.1:8b",
) -> str:
    """
    Generate a response using a local Ollama model.

    Args:
        messages: Chat-style messages.
        model_name: Name of the Ollama model to use.

    Returns:
        Model response text.

    Raises:
        LLMClientError: If Ollama is unavailable or returns an invalid response.
    """
    raise NotImplementedError(
        "Ollama integration will be added after the adapter is connected."
    )


def generate_llm_response(
    messages: list[dict[str, str]],
    mode: LLMMode = "mock",
    model_name: str = "llama3.1:8b",
) -> str:
    """
    Generate an NPC response from chat messages.

    Args:
        messages: Chat-style system/user messages.
        mode: LLM backend mode.
        model_name: Model name for local or hosted providers.

    Returns:
        NPC response string.
    """
    if mode == "mock":
        return generate_mock_response(messages)

    if mode == "ollama":
        return generate_ollama_response(
            messages=messages,
            model_name=model_name,
        )

    raise LLMClientError(f"Unsupported LLM mode: {mode}")