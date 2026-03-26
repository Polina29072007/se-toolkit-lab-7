# bot/handlers/help.py
from typing import Any, Dict


def handle_help(context: Dict[str, Any]) -> str:
    return (
        "Available commands:\n"
        "/start - welcome message\n"
        "/help - list available commands\n"
        "/health - check backend status\n"
        "/labs - list available labs\n"
        "/scores <lab-id> - show pass rates for a lab"
    )