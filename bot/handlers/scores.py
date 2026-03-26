import httpx

def handle_scores(text: str, context: dict) -> str:
    parts = text.split(maxsplit=1)
    if len(parts) != 2:
        return "Usage: /scores <lab-id>"

    lab_id = parts[1]
    backend_url = context["backend_url"]  # вот так достаём из dict

    try:
        resp = httpx.get(
            f"{backend_url}/analytics/pass-rates",
            params={"lab": lab_id},
            timeout=5.0,
        )
    except httpx.RequestError:
        return "Backend is unavailable. Please try again later."

    if resp.status_code != 200:
        return f"Failed to fetch scores for {lab_id}: {resp.text}"

    data = resp.json()

    # если бэкенд вернул ошибку в JSON
    if isinstance(data, dict) and "detail" in data:
        return f"Failed to fetch scores for {lab_id}: {data['detail']}"

    # ожидаем список с полями task, pass_rate, attempts (подставь реальные ключи, если в условии они другие)
    lines = [f"Pass rates for {lab_id}:"]
    for row in data:
        task = row.get("task", "unknown task")
        # если бэкенд всё-таки присылает поле в другом формате — пока выводим как есть
        pass_rate = row.get("pass_rate") or row.get("passRate") or "n/a"
        attempts = row.get("attempts", "n/a")
        lines.append(f"- {task}: {pass_rate}% ({attempts} attempts)")

    return "\n".join(lines)