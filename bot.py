import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import register_handlers

bot = Bot(token=TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def main():
    print("Bot running")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
