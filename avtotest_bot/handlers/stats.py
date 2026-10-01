# avtotest_bot/handlers/stats.py
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ..database import db
from ..texts import get_text

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("stats"))
@router.message(F.text.in_(["📊 Mening natijalarim", "📊 Моя статистика"]))
async def cmd_stats(message: Message):
    """Foydalanuvchining shaxsiy statistikasini ko'rsatish."""
    user_id = message.from_user.id
    user = await db.get_user_stats(user_id)

    if not user:
        lang = "uz"
        name = message.from_user.full_name or "Foydalanuvchi"
        registered_date = "Bugun"
        total_tests = 0
        total_questions = 0
        correct_answers = 0
        wrong_answers = 0
        accuracy = 0
    else:
        lang = user.get("lang", "uz")
        name = user.get("full_name") or message.from_user.full_name or "Foydalanuvchi"
        raw_date = user.get("created_at") or ""
        registered_date = raw_date.split("T")[0] if "T" in raw_date else raw_date[:10]
        total_tests = user.get("total_tests", 0)
        total_questions = user.get("total_questions", 0)
        correct_answers = user.get("correct_answers", 0)
        wrong_answers = user.get("wrong_answers", 0)
        accuracy = round((correct_answers / total_questions * 100) if total_questions > 0 else 0)

    stats_text = get_text(
        "stats_title",
        lang,
        name=name,
        registered_date=registered_date,
        total_tests=total_tests,
        total_questions=total_questions,
        correct_answers=correct_answers,
        wrong_answers=wrong_answers,
        accuracy=accuracy
    )

    await message.answer(stats_text, parse_mode="HTML")
