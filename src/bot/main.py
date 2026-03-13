import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from src.core.config import settings
from src.core.logger import setup_logger
from src.database.init_db import init_db
from src.database.session import async_session_maker
from src.bot.handlers.add_service import router as add_service_router

logger = setup_logger(__name__)


async def on_startup(bot: Bot):
    logger.info(f"Bot started! Bot ID: {bot.id}")


async def on_shutdown(bot: Bot):
    logger.info("Bot stopped!")
    await bot.session.close()


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # ✅ Создаем таблицы БД при старте
    await init_db()
    
    # ✅ Регистрируем роутеры
    dp.include_router(add_service_router)
    
    # Команда /start
    @dp.message(Command("start"))
    async def start_cmd(message: types.Message):
        await message.answer(
            "🚀 <b>Balance Hub</b> запущен!\n\n"
            "Доступные команды:\n"
            "/add — добавить сервис\n"
            "/status — проверить балансы\n"
            "/help — помощь\n"
            "/cancel — отменить операцию"
        )
    
    # Команда /help
    @dp.message(Command("help"))
    async def help_cmd(message: types.Message):
        await message.answer(
            "📚 <b>Справка</b>\n\n"
            "Этот бот помогает отслеживать баланс и сроки оплаты сервисов.\n\n"
            "<b>Команды:</b>\n"
            "/add — добавить новый сервис\n"
            "/status — проверить баланс всех сервисов\n"
            "/cancel — отменить текущую операцию"
        )
    
    # Команда /status (заглушка)
    @dp.message(Command("status"))
    async def status_cmd(message: types.Message):
        await message.answer("📊 Статус сервисов в разработке...")
    
    # Хендлер на любое сообщение (заглушка)
    @dp.message()
    async def echo(message: types.Message):
        await message.answer(
            f"👋 Используйте /add для добавления сервиса\n"
            f"Или /help для справки"
        )
    
    logger.info("Starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")