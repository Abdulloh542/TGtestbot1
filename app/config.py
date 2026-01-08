import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: List[int]
    database_url: str


def _parse_admin_ids(raw: str) -> List[int]:
    if not raw:
        return []
    return [int(item.strip()) for item in raw.split(",") if item.strip()]


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is required")

    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./shop.db")
    admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))

    return Config(bot_token=bot_token, admin_ids=admin_ids, database_url=database_url)
