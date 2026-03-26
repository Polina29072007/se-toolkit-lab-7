from typing import Any, Dict
from services.backend import BackendClient, BackendError


def handle_health(context: Dict[str, Any]) -> str:
    config = context["config"]
    client = BackendClient(config)
    try:
        items = client.get_items()
        return f"Backend is healthy. {len(items)} items available."
    except BackendError as e:
        return f"Backend error: {e}"