import argparse
import sys
from typing import Any, Dict

from config import load_config
from handlers.router import route_command


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SE Toolkit LMS Bot")
    parser.add_argument(
        "--test",
        metavar="TEXT",
        help="Run in test mode with given command or message text",
    )
    return parser.parse_args(argv)


def run_test_mode(text: str) -> int:
    config = load_config()
    context: Dict[str, Any] = {
        "config": config,
        # позже сюда можно добавить клиентов к LMS/LLM
    }
    response = route_command(text, context)
    print(response)
    return 0


def run_telegram_mode() -> int:
    # Реальный Telegram режим будет реализован позже (Task 2+).
    print("Telegram mode not implemented yet. Use --test.", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.test:
        return run_test_mode(args.test)
    return run_telegram_mode()


if __name__ == "__main__":
    raise SystemExit(main())cd ~/se-toolkit-lab-7
