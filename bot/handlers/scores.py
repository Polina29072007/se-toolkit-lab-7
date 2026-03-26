# bot/handlers/scores.py
from typing import Any, Dict
from services.backend import BackendClient, BackendError


def handle_scores(text: str, context: Dict[str, Any]) -> str:
    backend: BackendClient = context["backend"]

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return "Usage: /scores <lab-id>, e.g. /scores lab-04"

    lab_id = parts[1].strip()

    try:
        stats = backend.get_pass_rates(lab_id)
        if not stats:
            return f"No data for lab {lab_id}."

        # предполагаем формат: [{"task": "...", "pass_rate": 92.1, "attempts": 187}, ...]
        lines = [
            f"- {row['task']}: {row['pass_rate']}% ({row['attempts']} attempts)"
            for row in stats
        ]
        return f"Pass rates for {lab_id}:\n" + "\n".join(lines)
    except BackendError as e:
        return f"Backend error: {e}"