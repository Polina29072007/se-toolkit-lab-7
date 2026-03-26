import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import load_config
from services.backend import BackendClient
from handlers.router import route_command

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


async def on_message(message: Message, backend: BackendClient):
    context = {"backend": backend}
    reply = route_command(message.text or "", context)
    await message.answer(reply)


def setup_handlers(dp: Dispatcher, backend: BackendClient):
    dp.message.register(lambda m: on_message(m, backend))


async def main():
    bot, backend = create_bot_and_backend()
    dp = Dispatcher()
    setup_handlers(dp, backend)
    await dp.start_polling(bot)


# ===== Тестовый режим =====

async def main_test():
    if len(sys.argv) < 3:
        raise RuntimeError('Usage: uv run bot.py --test "/command"')

    command = sys.argv[2]
    cfg = load_config()
    backend = BackendClient(cfg)

    context = {"backend": backend}
    reply = route_command(command, context)
    print(reply)


async def main_test_start():
    await main_test()


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--test":
        asyncio.run(main_test_start())
    else:
        asyncio.run(main())