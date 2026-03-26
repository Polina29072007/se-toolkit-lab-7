# bot/config.py
from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
ENV_SECRET = ROOT_DIR / ".env.bot.secret"


def load_config() -> dict:
    if ENV_SECRET.exists():
        cfg = dotenv_values(ENV_SECRET)
    else:
        cfg = {}

    return {
        "BOT_TOKEN": cfg.get("BOT_TOKEN", ""),
        "LMS_API_BASE_URL": cfg.get("LMS_API_BASE_URL", ""),
        "LMS_API_KEY": cfg.get("LMS_API_KEY", ""),
        "LLM_API_KEY": cfg.get("LLM_API_KEY", ""),
        "LLM_API_BASE_URL": cfg.get("LLM_API_BASE_URL", ""),
        "LLM_API_MODEL": cfg.get("LLM_API_MODEL", ""),
    }