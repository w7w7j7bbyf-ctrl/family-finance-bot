import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

import db
from routers import (
    start,
    transactions,
    reports,
    statistics,
    charts_handler,
    history,
    family,
    export,
    ai_assistant,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN не задан. Проверьте Secrets.")

    await db.init_db()
    logger.info("База данных инициализирована.")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Router order matters: more specific handlers first
    dp.include_router(start.router)          # /start, balance, quick-add
    dp.include_router(transactions.router)   # add income/expense FSM
    dp.include_router(reports.router)        # text reports
    dp.include_router(statistics.router)     # top-10 stats
    dp.include_router(charts_handler.router) # charts
    dp.include_router(history.router)        # history, edit, delete
    dp.include_router(family.router)         # family management
    dp.include_router(export.router)         # CSV export
    dp.include_router(ai_assistant.router)   # AI chat (last — catches remaining text)

    logger.info("🚀 Семейный Финансист запущен. Начинаю polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
