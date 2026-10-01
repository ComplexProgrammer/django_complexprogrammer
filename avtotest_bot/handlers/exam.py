# avtotest_bot/handlers/exam.py
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from ..config import EXAM_QUESTIONS_COUNT, UZB_AVTOTEST_BOOK_ID
from ..database import db
from .quiz import start_quiz_session

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("exam"))
@router.message(F.text.in_(["🎲 Imtihon (20 savol)", "🎲 Экзамен (20 вопросов)"]))
async def cmd_exam(message: Message, bot: Bot):
    """20 ta tasodifiy savoldan iborat rasmiy imtihon rejimini boshlash."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    lang = await db.get_user_lang(user_id)

    question_ids = await db.get_random_exam_question_ids(
        book_id=UZB_AVTOTEST_BOOK_ID,
        count=EXAM_QUESTIONS_COUNT
    )

    if not question_ids:
        await message.answer("Imtihon savollari topilmadi.")
        return

    title = "🎲 Imtihon (20 ta savol)" if lang == "uz" else "🎲 Экзамен (20 вопросов)"

    await start_quiz_session(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        mode="exam",
        title=title,
        question_ids=question_ids
    )
