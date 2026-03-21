from typing import Any, Dict


def handle_start(context: Dict[str, Any] | None = None) -> str:
    return "Welcome to SE Toolkit Bot! Use /help to see available commands."


def handle_help(context: Dict[str, Any] | None = None) -> str:
    return (
        "/start - welcome message\n"
        "/help - list commands\n"
        "/health - backend health status\n"
        "/scores <lab-id> - show scores\n"
        "/labs - list available labs"
    )


def handle_health(context: Dict[str, Any] | None = None) -> str:
    # пока заглушка, реальный backend будет в следующем задании
    return "Backend status: OK (placeholder)"


def handle_labs(context: Dict[str, Any] | None = None) -> str:
    return "Available labs: placeholder for now"


def handle_scores(arg: str | None, context: Dict[str, Any] | None = None) -> str:
    lab_id = (arg or "").strip() or "<lab-id>"
    return f"Scores for {lab_id}: placeholder"


def handle_fallback(text: str, context: Dict[str, Any] | None = None) -> str:
    return f"Not implemented yet for: {text!r}"