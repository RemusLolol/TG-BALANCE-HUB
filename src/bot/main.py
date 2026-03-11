import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.core.config import settings
from src.core.logger import setup_logger

logger = setup_logger(__name__)


async def on_startup(dp: Dispatcher):
    logger.info("Bot started!")


async def on_shutdown(dp: Dispatcher):
    logger.info("Bot stopped!")


async def main():
    bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Заглушка хендлера
    @dp.message()
    async def echo(message):
        await message.answer(f"👋 Привет! Я пока в разработке.\nВаш баланс-хаб скоро будет готов.")
    
    logger.info("Starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
