import os
from dotenv import load_dotenv
import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router

bot = Bot(token='7038404198:AAEiEmaXv-h8_5Amvt94yVNgXd_EWQ5PwxI')
dp = Dispatcher()

async def main():
    #load_dotenv()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
