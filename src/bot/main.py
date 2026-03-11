import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from src.core.config import settings
from src.core.logger import setup_logger

logger = setup_logger(__name__)


# ✅ Исправлено: принимаем bot, а не dp
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
    
    # Регистрируем хендлеры старта/остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Хендлер на любое сообщение
    @dp.message()
    async def echo(message: types.Message):
        await message.answer(
            f"👋 Привет! Я пока в разработке.\n"
            f"Ваш баланс-хаб скоро будет готов.\n"
            f"<b>Ваш ID:</b> <code>{message.from_user.id}</code>"
        )
    
    # Команда /start
    @dp.message(lambda msg: msg.text == "/start")
    async def start_cmd(message: types.Message):
        await message.answer(
            "🚀 <b>Balance Hub</b> запущен!\n\n"
            "Доступные команды:\n"
            "/status — проверить балансы\n"
            "/add — добавить сервис\n"
            "/help — помощь"
        )
    
    # Команда /help
    @dp.message(lambda msg: msg.text == "/help")
    async def help_cmd(message: types.Message):
        await message.answer(
            "📚 <b>Справка</b>\n\n"
            "Этот бот помогает отслеживать баланс и сроки оплаты сервисов.\n"
            "Поддерживаемые сервисы: DigitalOcean, AWS, Hetzner (в разработке)."
        )
    
    logger.info("Starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")