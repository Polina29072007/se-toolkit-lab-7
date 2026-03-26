# bot/bot.py
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from config import load_config
from services.backend import BackendClient, BackendError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_bot_and_backend():
    cfg = load_config()
    bot_token = cfg["BOT_TOKEN"]
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set in environment or .env.bot.secret")

    bot = Bot(token=bot_token)
    backend = BackendClient(cfg)
    return bot, backend


async def cmd_start(message: Message):
    await message.answer("Привет! Я бот для работы с лабораторными.")


async def cmd_health(message: Message, backend: BackendClient):
    try:
        items = backend.get_items()
        await message.answer(f"Backend доступен, получено элементов: {len(items)}")
    except BackendError as e:
        await message.answer(f"Backend error: {e}")


async def cmd_labs(message: Message, backend: BackendClient):
    try:
        items = backend.get_items()
        if not items:
            await message.answer("Пока нет доступных лабораторных.")
            return

        lines = [f"- {item['id']}: {item['title']}" for item in items]
        await message.answer("Доступные лабораторные:\n" + "\n".join(lines))
    except BackendError as e:
        await message.answer(f"Backend error: {e}")


async def cmd_scores(message: Message, backend: BackendClient):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /scores <lab-id>, например: /scores lab-04")
        return

    lab_id = parts[1].strip()
    try:
        stats = backend.get_pass_rates(lab_id)
        if not stats:
            await message.answer(f"Нет данных по лабе {lab_id}.")
            return

        lines = [f"{row['group']}: {row['pass_rate']}%" for row in stats]
        await message.answer(f"Статистика по {lab_id}:\n" + "\n".join(lines))
    except BackendError as e:
        await message.answer(f"Backend error: {e}")


def setup_handlers(dp: Dispatcher, backend: BackendClient):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(lambda m: cmd_health(m, backend), Command("health"))
    dp.message.register(lambda m: cmd_labs(m, backend), Command("labs"))
    dp.message.register(lambda m: cmd_scores(m, backend), Command("scores"))


async def main():
    bot, backend = create_bot_and_backend()
    dp = Dispatcher()
    setup_handlers(dp, backend)
    await dp.start_polling(bot)


async def main_test_start():
    bot, backend = create_bot_and_backend()
    dp = Dispatcher()
    setup_handlers(dp, backend)
    print("Bot test /start: OK (handler is wired).")


if __name__ == "__main__":
    asyncio.run(main())