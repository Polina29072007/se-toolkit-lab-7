# bot/handlers/labs.py
from typing import Any, Dict
from services.backend import BackendClient, BackendError


def handle_labs(context: Dict[str, Any]) -> str:
    backend: BackendClient = context["backend"]

    try:
        items = backend.get_items()
        # фильтрация только лаб, если в items есть тип/категория — подстрой под свой формат
        labs = [item for item in items if item.get("type") == "lab"] or items

        if not labs:
            return "No labs available yet."

        lines = [f"- {lab['title']}" for lab in labs]
        return "Available labs:\n" + "\n".join(lines)
    except BackendError as e:
        return f"Backend error: {e}"