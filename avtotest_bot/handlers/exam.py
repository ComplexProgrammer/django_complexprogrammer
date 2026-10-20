# avtotest_bot/handlers/exam.py
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from ..config import EXAM_QUESTIONS_COUNT, QUICK_QUESTIONS_COUNT, UZB_AVTOTEST_BOOK_ID
from ..database import db
from ..texts import TEXTS, get_text
from .quiz import start_quiz_session

logger = logging.getLogger(__name__)
router = Router()


async def start_random_mode(bot: Bot, chat_id: int, user_id: int, mode: str) -> bool:
    """Tasodifiy savollardan iborat rejim: "exam" (20 savol), "quick" (5 savol) yoki "cdl"."""
    lang = await db.get_user_lang(user_id)
    if mode == "cdl":
        question_ids = await db.get_cdl_question_ids(count=20)
        title = "🇺🇸 AQSh CDL haydovchilik testi" if lang == "uz" else "🇺🇸 Тест США CDL (водительское)"
    elif mode == "quick":
        question_ids = await db.get_random_exam_question_ids(
            book_id=UZB_AVTOTEST_BOOK_ID, count=QUICK_QUESTIONS_COUNT
        )
        title = get_text("quick_title", lang)
    else:
        question_ids = await db.get_random_exam_question_ids(
            book_id=UZB_AVTOTEST_BOOK_ID, count=EXAM_QUESTIONS_COUNT
        )
        title = "🎲 Imtihon (20 ta savol)" if lang == "uz" else "🎲 Экзамен (20 вопросов)"

    if not question_ids:
        return False
    await start_quiz_session(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        mode=mode,
        title=title,
        question_ids=question_ids,
    )
    return True


@router.message(Command("exam"))
@router.message(F.text.in_(["🎲 Imtihon (20 savol)", "🎲 Экзамен (20 вопросов)"]))
async def cmd_exam(message: Message, bot: Bot):
    """20 ta tasodifiy savoldan iborat rasmiy imtihon rejimini boshlash."""
    if not await start_random_mode(bot, message.chat.id, message.from_user.id, "exam"):
        await message.answer("Imtihon savollari topilmadi.")


@router.message(Command("tezkor", "quick"))
@router.message(F.text.in_([TEXTS["uz"]["btn_quick"], TEXTS["ru"]["btn_quick"]]))
async def cmd_quick(message: Message, bot: Bot):
    """5 savollik tezkor mashq: ko'pchilik 10–20 savollik testni 3-savolda tashlab ketardi."""
    if not await start_random_mode(bot, message.chat.id, message.from_user.id, "quick"):
        await message.answer("Savollar topilmadi.")


@router.callback_query(F.data.startswith("retry:"))
async def cb_retry_mode(callback: CallbackQuery, bot: Bot):
    """Natija ostidagi "Qaytadan ishlash": xuddi shu rejimni yangi savollar bilan boshlaydi."""
    mode = callback.data.split(":", 1)[1]
    if mode not in ("exam", "quick", "cdl"):
        await callback.answer()
        return
    try:
        await callback.message.delete()
    except Exception:
        pass
    await start_random_mode(bot, callback.message.chat.id, callback.from_user.id, mode)
    await callback.answer()
