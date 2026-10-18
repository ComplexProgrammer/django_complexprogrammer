# avtotest_bot/handlers/reminder.py
import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Router
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import Command
from aiogram.types import Message

from ..database import db
from ..texts import get_text

logger = logging.getLogger(__name__)
router = Router()

# Eslatma yuboriladigan soat (server vaqti bo'yicha) va tekshiruv oralig'i
REMIND_HOUR = 19
CHECK_INTERVAL = 10 * 60


@router.message(Command("eslatma", "remind"))
async def cmd_remind(message: Message):
    """Kunlik eslatmani yoqish / o'chirish."""
    user_id = message.from_user.id
    await db.get_or_create_user(user_id, message.from_user.username, message.from_user.full_name or "")
    enabled = await db.toggle_remind(user_id)
    lang = await db.get_user_lang(user_id)
    await message.answer(get_text("remind_on" if enabled else "remind_off", lang), parse_mode="HTML")


async def enable_from_deeplink(message: Message):
    """Saytdagi "Botni ochish" havolasi (/start eslatma) orqali kelganlar uchun."""
    await db.toggle_remind(message.from_user.id, enable=True)
    lang = await db.get_user_lang(message.from_user.id)
    await message.answer(get_text("remind_on", lang), parse_mode="HTML")


async def reminder_loop(bot: Bot):
    """Har kuni REMIND_HOUR dan keyin, o'sha kuni faol bo'lmagan obunachilarga bitta eslatma yuboradi."""
    while True:
        try:
            now = datetime.now()
            if now.hour >= REMIND_HOUR:
                today = now.date().isoformat()
                for user in await db.get_users_to_remind(today):
                    disable = False
                    try:
                        await bot.send_message(
                            user["user_id"], get_text("remind_daily", user.get("lang") or "uz"),
                            parse_mode="HTML", disable_web_page_preview=True,
                        )
                    except TelegramRetryAfter as e:
                        await asyncio.sleep(e.retry_after)
                        continue  # keyingi tekshiruvda qayta urinamiz
                    except TelegramForbiddenError:
                        disable = True  # foydalanuvchi botni bloklagan
                    except Exception as e:
                        logger.warning(f"Eslatma yuborilmadi ({user['user_id']}): {e}")
                    await db.mark_reminded(user["user_id"], today, disable=disable)
                    await asyncio.sleep(0.05)  # Telegram cheklovi: ~30 xabar/soniya
        except Exception as e:
            logger.exception(f"Eslatma siklida xatolik: {e}")
        await asyncio.sleep(CHECK_INTERVAL)


@router.message(Command("taklif", "invite"))
async def cmd_invite(message: Message):
    """Shaxsiy taklif havolasi va taklif qilinganlar soni."""
    user_id = message.from_user.id
    await db.get_or_create_user(user_id, message.from_user.username, message.from_user.full_name or "")
    lang = await db.get_user_lang(user_id)
    me = await message.bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{user_id}"
    count = await db.count_referrals(user_id)
    await message.answer(
        get_text("ref_info", lang, link=link, count=count), parse_mode="HTML", disable_web_page_preview=True
    )
