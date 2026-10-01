# avtotest_bot/handlers/cdl.py
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from ..database import db
from .quiz import start_quiz_session

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("cdl"))
@router.message(F.text.in_(["🇺🇸 AQSh CDL testi", "🇺🇸 Тест США CDL"]))
async def cmd_cdl(message: Message, bot: Bot):
    """AQSh CDL tayyorgarlik testini boshlash."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    lang = await db.get_user_lang(user_id)

    question_ids = await db.get_cdl_question_ids(count=20)
    if not question_ids:
        await message.answer("AQSh CDL test savollari topilmadi.")
        return

    title = "🇺🇸 AQSh CDL haydovchilik testi" if lang == "uz" else "🇺🇸 Тест США CDL (водительское)"

    await start_quiz_session(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        mode="cdl",
        title=title,
        question_ids=question_ids
    )
