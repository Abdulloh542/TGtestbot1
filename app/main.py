import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import load_config
from db.base import Base
from db.seed import seed_demo_data
from db.session import create_engine, create_session_factory
from handlers import admin, cart, checkout, orders, products, start, support
from utils.db_middleware import DbSessionMiddleware


async def on_startup(dispatcher: Dispatcher, session_factory):
    async with session_factory() as session:
        async with session.bind.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await seed_demo_data(session)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    config = load_config()
    engine = create_engine(config)
    session_factory = create_session_factory(engine)

    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()
    dispatcher["config"] = config
    dispatcher.message.middleware(DbSessionMiddleware(session_factory))
    dispatcher.callback_query.middleware(DbSessionMiddleware(session_factory))

    dispatcher.include_router(start.router)
    dispatcher.include_router(products.router)
    dispatcher.include_router(cart.router)
    dispatcher.include_router(checkout.router)
    dispatcher.include_router(orders.router)
    dispatcher.include_router(support.router)
    dispatcher.include_router(admin.router)

    await on_startup(dispatcher, session_factory)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
