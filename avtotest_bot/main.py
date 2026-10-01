# avtotest_bot/main.py
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from .config import BOT_TOKEN
from .database import db
from .handlers import main_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AvtoTestBot")

async def set_bot_commands(bot: Bot):
    """Telegram menyusidagi asosiy buyruqlarni o'rnatish."""
    commands = [
        BotCommand(command="start", description="Botni qayta ishga tushirish 🔄"),
        BotCommand(command="bilets", description="Biletlar ro'yxati (1-108) 🚗"),
        BotCommand(command="exam", description="Tasodifiy imtihon (20 savol) 🎲"),
        BotCommand(command="mistakes", description="Xatolar ustida ishlash ❌"),
        BotCommand(command="stats", description="Mening natijalarim 📊"),
        BotCommand(command="lang", description="Tilni o'zgartirish 🌐"),
        BotCommand(command="help", description="Yordam va ma'lumot ℹ️")
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        logger.warning(f"Bot buyruqlarini o'rnatishda xatolik: {e}")

async def start_bot():
    """Botni ishga tushirishning asosiy asinxron funksiyasi."""
    if not BOT_TOKEN:
        logger.error(
            "\n" + "=" * 60 + "\n"
            "XATOLIK: AVTOTEST_BOT_TOKEN topilmadi!\n"
            "Iltimos, .env fayliga bot tokenini kiriting:\n"
            "AVTOTEST_BOT_TOKEN=1234567890:ABCdef...\n"
            + "=" * 60
        )
        return

    logger.info("Bot ma'lumotlar bazasi tayyorlanmoqda...")
    await db.init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.include_router(main_router)

    await set_bot_commands(bot)

    bot_info = await bot.get_me()
    logger.info(f"Bot muvaffaqiyatli ishga tushdi: @{bot_info.username} ({bot_info.first_name})")

    # Eski kutilayotgan update larni tozalaymiz
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()
        logger.info("Bot to'xtatildi.")

def main():
    """Tizim orqali to'g'ridan-to'g'ri chaqirish uchun funksiya."""
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot foydalanuvchi tomonidan to'xtatildi.")

if __name__ == "__main__":
    main()
