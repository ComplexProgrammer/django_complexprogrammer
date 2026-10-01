# avtotest_bot/handlers/bilet.py
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..database import db
from ..texts import get_text
from ..keyboards import get_bilet_list_keyboard
from .quiz import start_quiz_session

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("bilets"))
@router.message(F.text.in_(["🚗 Biletlar (1-108)", "🚗 Билеты (1-108)"]))
async def cmd_bilets(message: Message):
    """Biletlar ro'yxatini chiqarish."""
    user_id = message.from_user.id
    lang = await db.get_user_lang(user_id)
    topics = await db.get_topics()

    if not topics:
        await message.answer("Biletlar topilmadi.")
        return

    text = get_text("bilet_title", lang)
    kb = get_bilet_list_keyboard(topics, current_page=1, per_page=15, lang=lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("bilet_page:"))
async def cb_bilet_page(callback: CallbackQuery):
    """Biletlar sahifasini almashtirish (Pagination)."""
    user_id = callback.from_user.id
    lang = await db.get_user_lang(user_id)
    page = int(callback.data.split(":")[1])

    topics = await db.get_topics()
    text = get_text("bilet_title", lang)
    kb = get_bilet_list_keyboard(topics, current_page=page, per_page=15, lang=lang)

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer()

@router.callback_query(F.data.startswith("bilet:"))
async def cb_select_bilet(callback: CallbackQuery, bot: Bot):
    """Foydalanuvchi ma'lum bir biletni tanlaganida."""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    lang = await db.get_user_lang(user_id)
    topic_id = int(callback.data.split(":")[1])

    topic = await db.get_topic_by_id(topic_id)
    if not topic:
        await callback.answer("Bilet topilmadi!", show_alert=True)
        return

    question_ids = await db.get_bilet_question_ids(topic_id)
    if not question_ids:
        await callback.answer("Ushbu biletda savollar topilmadi!", show_alert=True)
        return

    title = topic["name_uz_uz"] if lang == "uz" else topic["name_ru_ru"]
    if not title:
        title = f"{topic['number']}-bilet"

    try:
        await callback.message.delete()
    except Exception:
        pass

    await start_quiz_session(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        mode="bilet",
        title=title,
        question_ids=question_ids,
        topic_id=topic_id
    )
    await callback.answer()
