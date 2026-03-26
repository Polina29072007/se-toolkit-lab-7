# bot/handlers/health.py
from typing import Any, Dict
from services.backend import BackendClient, BackendError


def handle_health(context: Dict[str, Any]) -> str:
    backend: BackendClient = context["backend"]

    try:
        items = backend.get_items()
        return f"Backend is healthy. {len(items)} items available."
    except BackendError as e:
        # важно: включить текст ошибки (connection refused / HTTP 502 и т.п.)
        return f"Backend error: {e}"