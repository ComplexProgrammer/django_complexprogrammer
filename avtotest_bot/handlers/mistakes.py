# avtotest_bot/handlers/mistakes.py
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..database import db
from ..texts import get_text
from .quiz import start_quiz_session

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("mistakes"))
@router.message(F.text.in_(["❌ Xatolar ustida ishlash", "❌ Работа над ошибками"]))
async def cmd_mistakes(message: Message, bot: Bot):
    """Foydalanuvchi oldin xato qilgan savollari bo'yicha mashq boshlash."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    lang = await db.get_user_lang(user_id)

    mistake_q_ids = await db.get_user_mistake_question_ids(user_id, count=20)
    if not mistake_q_ids:
        text = get_text("no_mistakes", lang)
        await message.answer(text, parse_mode="HTML")
        return

    title = "❌ Xatolar ustida ishlash" if lang == "uz" else "❌ Работа над ошибками"
    await start_quiz_session(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        mode="mistakes",
        title=title,
        question_ids=mistake_q_ids
    )

@router.callback_query(F.data == "practice_mistakes")
async def cb_practice_mistakes(callback: CallbackQuery, bot: Bot):
    """Natija sahifasidagi 'Xatolarni tahlil qilish' tugmasi bosilganda."""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    lang = await db.get_user_lang(user_id)

    mistake_q_ids = await db.get_user_mistake_question_ids(user_id, count=20)
    if not mistake_q_ids:
        text = get_text("no_mistakes", lang)
        await callback.message.answer(text, parse_mode="HTML")
        await callback.answer()
        return

    try:
        await callback.message.delete()
    except Exception:
        pass

    title = "❌ Xatolar ustida ishlash" if lang == "uz" else "❌ Работа над ошибками"
    await start_quiz_session(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        mode="mistakes",
        title=title,
        question_ids=mistake_q_ids
    )
    await callback.answer()
