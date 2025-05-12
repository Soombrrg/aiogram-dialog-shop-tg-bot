import asyncio
import json
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from tg_bot.config import load_config
from tg_bot.db.db_repo import Repo
from tg_bot.dialogs import setup_dialogs2
from tg_bot.handlers.user_handlers import user_router_configuration
from tg_bot.middlewares.environment import DBSessionMiddleware

logger = logging.getLogger(__name__)


# async def db_creation(engine, session_maker) -> None:
#     await drop_db(engine)
#
# await create_db(engine, session_maker)


async def on_shutdown(bot: Bot) -> None:
    logger.error("Bot stopped!")


def including_routers(dp: Dispatcher) -> None:
    dp.include_router(user_router_configuration())
    # dp.include_router(admin_router_configuration())


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # engine = create_async_engine(os.getenv('DB_LITE'), echo=True) # if using sqlite
    engine = create_async_engine(config.db.db_url, echo=True)
    session_maker = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    storage = RedisStorage() if config.tg_bot.use_redis else MemoryStorage()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    bot.admin_ids = config.tg_bot.admin_ids

    with open("tg_bot/misc/test_data.json", "r", encoding="utf-8") as f:
        repo = Repo(test_data=json.load(f))

    dp = Dispatcher(storage=storage)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DBSessionMiddleware(session_pool=session_maker, repo=repo))
    including_routers(dp)
    setup_dialogs2(dp)

    try:
        # await db_creation(engine, session_maker)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
