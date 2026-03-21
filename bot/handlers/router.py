from typing import Any, Dict
from . import base


def route_command(raw: str, context: Dict[str, Any] | None = None) -> str:
    text = raw.strip()
    if not text:
        return base.handle_fallback(text, context)

    if text.startswith("/start"):
        return base.handle_start(context)
    if text.startswith("/help"):
        return base.handle_help(context)
    if text.startswith("/health"):
        return base.handle_health(context)
    if text.startswith("/labs"):
        return base.handle_labs(context)
    if text.startswith("/scores"):
        parts = text.split(maxsplit=1)
        arg = parts[1] if len(parts) > 1 else None
        return base.handle_scores(arg, context)

    # сюда попадёт свободный текст и неизвестные команды
    return base.handle_fallback(text, context)