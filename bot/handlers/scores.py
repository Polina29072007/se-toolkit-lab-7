# bot/handlers/scores.py
from typing import Any, Dict
from services.backend import BackendClient, BackendError


def handle_scores(text: str, context: Dict[str, Any]) -> str:
    parts = text.split(maxsplit=1)
    if len(parts) != 2:
        return "Usage: /scores <lab-id>"

    lab_id = parts[1]
    backend: BackendClient = context["backend"]

    try:
        # предполагаем, что в BackendClient есть метод для pass-rates
        scores = backend.get_pass_rates(lab_id)
    except BackendError as e:
        return f"Backend error: {e}"

    if not scores:
        return f"No scores available for {lab_id}."

    lines = [f"Pass rates for {lab_id}:"]
    for row in scores:
        task = row.get("task", "unknown task")
        pass_rate = row.get("pass_rate") or row.get("passRate") or "n/a"
        attempts = row.get("attempts", "n/a")
        lines.append(f"- {task}: {pass_rate}% ({attempts} attempts)")

    return "\n".join(lines)