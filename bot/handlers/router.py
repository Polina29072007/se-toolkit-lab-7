# bot/handlers/router.py
from typing import Any, Dict

from .start import handle_start
from .help import handle_help
from .health import handle_health
from .labs import handle_labs
from .scores import handle_scores


def route_command(text: str, context: Dict[str, Any]) -> str:
    text = text.strip()
    if not text.startswith("/"):
        return "Unknown command. Use /help."

    if text.startswith("/start"):
        return handle_start(context)
    if text.startswith("/help"):
        return handle_help(context)
    if text.startswith("/health"):
        return handle_health(context)
    if text.startswith("/labs"):
        return handle_labs(context)
    if text.startswith("/scores"):
        return handle_scores(text, context)

    return "Unknown command. Use /help."