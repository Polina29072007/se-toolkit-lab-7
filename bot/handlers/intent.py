from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

from services.llm_client import LlmClient
from services.backend import BackendClient
from services.tools import TOOLS, call_tool


SYSTEM_PROMPT = (
    "You are an assistant for a Learning Management System.\n"
    "You MUST use the provided tools to answer questions about labs, scores, "
    "groups, learners, and analytics. Do not make up data.\n"
    "When the user asks about labs, scores, pass rates, groups, or learners, "
    "first call an appropriate tool, then answer using ONLY tool results.\n"
)


def _build_initial_messages(user_text: str) -> List[Dict[str, Any]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text},
    ]


async def run_llm_router(
    text: str,
    backend: BackendClient,
    llm: LlmClient,
) -> str:
    # Если LLM не настроен — мягкий фоллбек
    if not llm.is_configured():
        return (
            "LLM is not configured. For now, use commands like /labs or /scores lab-04."
        )

    messages: List[Dict[str, Any]] = _build_initial_messages(text)

    # Первое обращение к LLM — он должен вернуть tool_calls
    try:
        msg = await llm.chat(messages, tools=TOOLS)
    except Exception as e:
        return f"LLM error: {e}"

    # Если модель сразу вернула текст без tools — просто отдадим его
    tool_calls = msg.get("tool_calls") or []
    if not tool_calls:
        content = msg.get("content") or ""
        if not content:
            return (
                "I didn't understand that. You can ask about labs, scores, groups, and more."
            )
        return content

    # Логирование на stderr, как в задании
    for tc in tool_calls:
        name = tc["function"]["name"]
        args_str = tc["function"].get("arguments", "{}")
        print(f"[tool] LLM called: {name}({args_str})", file=sys.stderr)

    # Выполняем каждый tool_call
    tool_results: List[Dict[str, Any]] = []
    for tc in tool_calls:
        name = tc["function"]["name"]
        raw_args = tc["function"].get("arguments") or "{}"
        try:
            args = json.loads(raw_args)
        except json.JSONDecodeError:
            args = {}

        result = call_tool(name, args, backend)
        tool_results.append(
            {
                "tool_call_id": tc.get("id", ""),
                "name": name,
                "content": result,
            }
        )

    # Добавляем сообщения role=tool и просим LLM сделать финальное резюме
    messages.append(msg)
    for tr in tool_results:
        print(f"[tool] Result: {type(tr['content'])}", file=sys.stderr)
        messages.append(
            {
                "role": "tool",
                "name": tr["name"],
                "tool_call_id": tr["tool_call_id"],
                "content": json.dumps(tr["content"]),
            }
        )

    print(
        f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM",
        file=sys.stderr,
    )

    try:
        final_msg = await llm.chat(messages, tools=None)
    except Exception as e:
        return f"LLM error during summary: {e}"

    content = final_msg.get("content") or ""
    if not content:
        return (
            "I called the backend tools but could not generate a helpful answer."
        )
    return content


def handle_intent(text: str, context: Dict[str, Any]) -> str:
    """
    Синхронная обёртка для использования из bot.py / тестового режима.
    """
    backend: BackendClient = context["backend"]
    llm: LlmClient = context["llm"]

    # В тестовом режиме main_test() не использует asyncio-цикл, поэтому
    # вызываем run_llm_router через asyncio.run, но только здесь.
    import asyncio

    try:
        return asyncio.run(run_llm_router(text, backend, llm))
    except RuntimeError:
        # Если уже есть running loop (в Telegram-режиме), используем его
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(run_llm_router(text, backend, llm))