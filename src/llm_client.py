from __future__ import annotations

from typing import Any, Literal

import requests


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
    base_url: str = "http://localhost:11434",
    timeout_seconds: int = 120,
) -> str:
    """
    Generate a response using a local Ollama model.

    Args:
        messages: Chat-style messages.
        model_name: Name of the Ollama model to use.
        base_url: Base URL for the local Ollama server.
        timeout_seconds: Request timeout in seconds.

    Returns:
        Model response text.

    Raises:
        LLMClientError: If Ollama is unavailable or returns an invalid response.
    """
    url = f"{base_url}/api/chat"

    payload: dict[str, Any] = {
        "model": model_name,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 220,
        },
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise LLMClientError(
            "Could not generate response from Ollama. "
            "Make sure Ollama is running and the requested model is available."
        ) from exc

    data = response.json()

    try:
        content = data["message"]["content"]
    except KeyError as exc:
        raise LLMClientError(
            f"Ollama returned an unexpected response format: {data}"
        ) from exc

    cleaned_content = content.strip()

    if not cleaned_content:
        raise LLMClientError("Ollama returned an empty response.")

    return cleaned_content


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