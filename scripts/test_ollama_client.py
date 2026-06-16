from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.llm_client import generate_llm_response


def main() -> None:
    """
    Test direct Ollama response generation.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are Dr. Henry Ashford, a controlled and evasive suspect "
                "in a 1930s detective mystery. Stay in character."
            ),
        },
        {
            "role": "user",
            "content": (
                "Doctor, I found a medical vial in your bag. "
                "How do you explain that?"
            ),
        },
    ]

    response = generate_llm_response(
        messages=messages,
        mode="ollama",
        model_name="llama3.1:8b",
    )

    print("\n" + "=" * 80)
    print("OLLAMA RESPONSE")
    print("=" * 80)
    print(response)


if __name__ == "__main__":
    main()