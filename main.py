import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from app.database.models import async_session
from app.middleware.db import DataBaseSession
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from app.handlers import router
from app.database.models import async_main

allowed_updates=['message', 'edited_message', 'callback_query']

async def main():
    await async_main()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher(storage=storage)
    dp.update.middleware(DataBaseSession(session_pool=async_session))
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=allowed_updates)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    asyncio.run(main())
