from typing import Any, Dict
from services.backend import BackendClient, BackendError


def handle_labs(context: Dict[str, Any]) -> str:
    config = context["config"]
    client = BackendClient(config)
    try:
        items = client.get_items()
    except BackendError as e:
        return f"Backend error: {e}"

    labs = [i for i in items if i.get("type") == "lab"]
    if not labs:
        return "No labs found in backend."

    lines = ["Available labs:"]
    for lab in labs:
        name = lab.get("name") or lab.get("title") or "Lab"
        lines.append(f"- {name}")
    return "\n".join(lines)