import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from tgbot.config import load_config
from tgbot.filters.filter_log import setup_logger
from tgbot.handlers.inline.find_items import register_find_items
from tgbot.handlers.users.admin.add_item import register_add_item
from tgbot.handlers.users.admin.admin_panel import register_admin_panel
from tgbot.handlers.users.admin.advertisement import register_advertisement
from tgbot.handlers.users.authorize import register_authorize
from tgbot.handlers.users.start import register_start
from tgbot.middlewares.db import DbMiddleware
from tgbot.services.database import create_db_session
from tgbot.handlers.users.back import register_back
from tgbot.handlers.users.profile import register_profile

setup_logger(ignored=["aiogram.bot.api"])


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_start(dp)
    register_authorize(dp)
    register_admin_panel(dp)
    register_back(dp)
    register_profile(dp)
    register_add_item(dp)
    register_find_items(dp)
    register_advertisement(dp)


async def main():
    logger.info("Bot started!")

    config = load_config(".env")
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    bot['db'] = await create_db_session(config)

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
