# bot/handlers/intent.py
from typing import Any, Dict


def handle_intent(text: str, context: Dict[str, Any]) -> str:
    text = text.strip()
    if not text:
        return "I didn't understand that. You can ask about labs, scores, groups, and more."

    # Пока простая заглушка без LLM, чтобы всё работало стабильно.
    return (
        "I'm still learning to understand free-form questions. "
        "For now, try commands like /labs or /scores lab-04."
    )