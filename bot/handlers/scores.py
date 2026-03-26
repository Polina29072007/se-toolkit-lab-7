from typing import Any, Dict
from services.backend import BackendClient, BackendError


def handle_scores(text: str, context: Dict[str, Any]) -> str:
    parts = text.strip().split(maxsplit=1)
    if len(parts) == 1:
        return "Usage: /scores <lab-id>, e.g. /scores lab-04"

    lab = parts[1].strip()
    config = context["config"]
    client = BackendClient(config)

    try:
        data = client.get_pass_rates(lab)
    except BackendError as e:
        return f"Backend error: {e}"

    if not data:
        return f"No scores found for {lab}."

    lines = [f"Pass rates for {lab}:"]
    for task in data:
        name = task.get("task_name") or task.get("name") or "Task"
        rate = task.get("pass_rate") or task.get("passRate")
        attempts = task.get("attempts") or task.get("total_attempts")
        if rate is None or attempts is None:
            continue
        lines.append(f"- {name}: {rate:.1f}% ({attempts} attempts)")
    return "\n".join(lines)