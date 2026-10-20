# avtotest_bot/handlers/channel_post.py
"""Kanalga kuniga bir necha marta tasodifiy avtotest savolini viktorina (quiz poll) ko'rinishida joylash."""
import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from ..config import BASE_DIR, POST_CHANNEL, POST_TIMES
from ..database import db
from .admin import is_admin

logger = logging.getLogger(__name__)
router = Router()

SITE_URL = "https://complexprogrammer.uz"
# Telegram ichki brauzeri referrer bermaydi — UTM bo'lmasa Metrika/GA'da "to'g'ridan-to'g'ri" bo'lib ko'rinadi
UTM = "?utm_source=telegram&utm_medium=channel&utm_campaign=kun_savoli"
CHECK_INTERVAL = 60
# Bot shu vaqtdan ko'proq o'chiq turgan bo'lsa, o'tib ketgan joylash qilinmaydi (kechasi ertalabki savol chiqmasin)
MAX_DELAY = timedelta(hours=2)
LETTERS = ("A", "B", "C", "D")
# Telegram cheklovlari
POLL_QUESTION_MAX = 300
POLL_OPTION_MAX = 100


def _poll_parts(q):
    """Telegram cheklovlariga sig'adigan savol bo'lsa (savol, variantlar, to'g'ri javob indeksi), aks holda None."""
    text = (q.get("savol") or "").strip()
    options, correct = [], None
    for letter in LETTERS:
        option = (q.get("javob_" + letter.lower()) or "").strip()
        if not option:
            continue
        if letter == q["javob"]:
            correct = len(options)
        options.append(option)
    if correct is None or len(options) < 2 or not text or len(text) > POLL_QUESTION_MAX:
        return None
    if any(len(o) > POLL_OPTION_MAX for o in options):
        return None  # qisqartirsak ma'nosi buzilishi mumkin — boshqa savol tanlanadi
    return text, options, correct


async def post_random_question(bot: Bot, chat_id: str):
    """Bitta tasodifiy savolni joylaydi. Joylangan savol ID sini qaytaradi."""
    for q in await db.get_random_channel_questions():
        parts = _poll_parts(q)
        if parts is None:
            continue
        text, options, correct = parts
        url = f"{SITE_URL}/avtotest/{q['bilet']}/{q['raqam']}/{UTM}"
        header = f"🚗 <b>Kun savoli</b> · {q['bilet']}-bilet, {q['raqam']}-savol"

        image = BASE_DIR / "static" / "avtotest" / (q.get("rasm") or "")
        if q.get("rasm") and image.is_file():
            await bot.send_photo(chat_id, FSInputFile(str(image)), caption=header, parse_mode="HTML")
        else:
            await bot.send_message(chat_id, header, parse_mode="HTML")

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📖 Javob va izoh saytda", url=url)],
            [InlineKeyboardButton(text="🎯 20 savollik imtihon", url=f"{SITE_URL}/avtotest/imtihon/{UTM}")],
        ])
        await bot.send_poll(
            chat_id,
            question=text,
            options=options,
            type="quiz",
            correct_option_id=correct,
            is_anonymous=True,
            explanation=f"To'g'ri javob: {q['javob']}. Barcha biletlar: complexprogrammer.uz/avtotest",
            reply_markup=keyboard,
        )
        return q["id"]
    logger.warning("Kanalga joylash uchun mos savol topilmadi.")
    return None


async def channel_post_loop(bot: Bot):
    """POST_TIMES dagi har bir vaqtda kuniga bir martadan savol joylaydi."""
    if not POST_CHANNEL or not POST_TIMES:
        logger.info("Kanalga savol joylash o'chirilgan (AVTOTEST_POST_CHANNEL / AVTOTEST_POST_TIMES).")
        return
    logger.info(f"Kanalga savol joylash yoqildi: {POST_CHANNEL}, vaqtlar: {', '.join(POST_TIMES)}")
    # Bazadagi belgi yetarli emas: db.sqlite3 git orqali eski nusxaga almashsa, yozuv yo'qoladi va bitta vaqt uchun
    # savol qayta-qayta joylanadi (2026-10-20: 13:00 va 15:00 slotlari 4–5 martadan). Jarayon ichida ham eslab qolamiz.
    posted = set()
    while True:
        try:
            now = datetime.now()
            for hhmm in POST_TIMES:
                try:
                    hour, minute = (int(x) for x in hhmm.split(":"))
                except ValueError:
                    continue
                planned = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                slot = planned.strftime("%Y-%m-%d %H:%M")
                if slot in posted or not planned <= now < planned + MAX_DELAY:
                    continue
                if await db.is_slot_posted(slot):
                    posted.add(slot)
                    continue
                # Avval belgilaymiz: xatolikda ham shu vaqt uchun qayta-qayta urinib kanalni to'ldirib yubormaslik uchun
                posted.add(slot)
                await db.mark_slot_posted(slot, None)
                question_id = await post_random_question(bot, POST_CHANNEL)
                await db.mark_slot_posted(slot, question_id)
        except Exception as e:
            logger.exception(f"Kanalga joylashda xatolik: {e}")
        await asyncio.sleep(CHECK_INTERVAL)


@router.message(Command("post_now"))
async def cmd_post_now(message: Message, bot: Bot):
    """Admin: hozirning o'zida kanalga bitta savol joylash (sinab ko'rish uchun)."""
    if not is_admin(message.from_user.id):
        return
    try:
        question_id = await post_random_question(bot, POST_CHANNEL)
    except Exception as e:
        await message.answer(f"❌ Joylanmadi: {e}\n\nBot {POST_CHANNEL} kanalida admin ekanini tekshiring.")
        return
    await db.mark_slot_posted("manual " + datetime.now().isoformat(timespec="seconds"), question_id)
    await message.answer(f"✅ {POST_CHANNEL} kanaliga savol joylandi (id={question_id}).")
