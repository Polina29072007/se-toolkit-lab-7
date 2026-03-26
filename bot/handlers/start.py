# bot/handlers/start.py
from typing import Any, Dict


def handle_start(context: Dict[str, Any]) -> str:
    return "Welcome to SE Toolkit Bot! Use /help to see available commands."