# avtotest_bot/handlers/quiz.py
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.exceptions import TelegramBadRequest

from ..config import MEDIA_DIR, PASSING_PERCENTAGE
from ..database import db
from ..texts import get_text
from ..keyboards import get_question_keyboard, get_finish_keyboard, get_main_reply_keyboard

logger = logging.getLogger(__name__)
router = Router()

async def start_quiz_session(
    bot: Bot,
    chat_id: int,
    user_id: int,
    mode: str,
    title: str,
    question_ids: List[int],
    topic_id: Optional[int] = None
):
    """Yangi test sessiyasini boshlash."""
    if not question_ids:
        lang = await db.get_user_lang(user_id)
        await bot.send_message(chat_id, "Savollar topilmadi.", reply_markup=get_main_reply_keyboard(lang))
        return

    await db.create_session(
        user_id=user_id,
        mode=mode,
        title=title,
        question_ids=question_ids,
        topic_id=topic_id
    )

    session = await db.get_session(user_id)
    await render_question(bot, chat_id, user_id, session)

async def render_question(
    bot: Bot,
    chat_id: int,
    user_id: int,
    session: Dict[str, Any],
    old_message_id: Optional[int] = None
):
    """Joriy savolni ekranga chiqarish (rasm va matn bilan)."""
    lang = await db.get_user_lang(user_id)
    current_idx = session["current_index"]
    question_ids = session["question_ids"]

    if current_idx >= len(question_ids):
        await finish_quiz(bot, chat_id, user_id)
        return

    q_id = question_ids[current_idx]
    question = await db.get_question(q_id)
    if not question:
        # Savol topilmasa, keyingisiga o'tamiz
        await db.advance_session_index(user_id)
        session = await db.get_session(user_id)
        await render_question(bot, chat_id, user_id, session, old_message_id)
        return

    answers = await db.get_answers(q_id)

    # Savol matnini tayyorlash
    q_name = question["name_uz_uz"] if lang == "uz" else question["name_ru_ru"]
    if not q_name:
        q_name = question["name_uz_uz"] or "Savol matni mavjud emas"

    header = get_text(
        "question_header",
        lang,
        title=session["title"],
        current=current_idx + 1,
        total=len(question_ids)
    )

    caption_lines = [header, f"<b>{q_name}</b>\n"]
    for idx, ans in enumerate(answers):
        num = ans["number"] or (idx + 1)
        a_name = ans["name_uz_uz"] if lang == "uz" else ans["name_ru_ru"]
        if not a_name:
            a_name = ans["name_uz_uz"] or ""
        caption_lines.append(f"<b>{num})</b> {a_name}")

    full_text = "\n".join(caption_lines)

    # Rasm mavjudligini tekshirish
    img_rel_path = question.get("image")
    image_file = None
    if img_rel_path and img_rel_path.strip():
        img_full_path = MEDIA_DIR / img_rel_path.strip()
        if img_full_path.exists() and img_full_path.is_file():
            image_file = FSInputFile(str(img_full_path))

    is_last = (current_idx == len(question_ids) - 1)
    reply_markup = get_question_keyboard(answers, is_answered=False, is_last=is_last, lang=lang)

    # Eski xabarni o'chirish (tozalik uchun)
    if old_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=old_message_id)
        except Exception:
            pass

    sent_msg = None
    try:
        if image_file:
            # Agar matn 1024 belgidan oshsa, captionni qisqartirib alohida matn yuborish mumkin
            if len(full_text) > 1020:
                short_caption = f"{header}\n<b>{q_name[:300]}...</b>"
                sent_msg = await bot.send_photo(
                    chat_id=chat_id,
                    photo=image_file,
                    caption=short_caption,
                    parse_mode="HTML"
                )
                sent_msg = await bot.send_message(
                    chat_id=chat_id,
                    text=full_text,
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
            else:
                sent_msg = await bot.send_photo(
                    chat_id=chat_id,
                    photo=image_file,
                    caption=full_text,
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
        else:
            sent_msg = await bot.send_message(
                chat_id=chat_id,
                text=full_text,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error(f"Savol yuborishda xatolik: {e}")
        sent_msg = await bot.send_message(
            chat_id=chat_id,
            text=full_text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

    if sent_msg:
        await db.update_last_message_id(user_id, sent_msg.message_id)

@router.callback_query(F.data.startswith("ans:"))
async def cb_answer_chosen(callback: CallbackQuery, bot: Bot):
    """Foydalanuvchi variant tanlaganida."""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    session = await db.get_session(user_id)

    if not session:
        await callback.answer("Sessiya topilmadi!", show_alert=True)
        return

    current_idx = session["current_index"]
    question_ids = session["question_ids"]

    if current_idx >= len(question_ids):
        await callback.answer()
        await finish_quiz(bot, chat_id, user_id)
        return

    q_id = question_ids[current_idx]
    history = session.get("answers_history", {})

    # Bir savolga ikki marta bosishni oldini olish
    if str(q_id) in history:
        await callback.answer("Siz bu savolga allaqachon javob bergansiz!")
        return

    selected_ans_id = int(callback.data.split(":")[1])
    answers = await db.get_answers(q_id)
    lang = await db.get_user_lang(user_id)

    selected_ans = next((a for a in answers if a["id"] == selected_ans_id), None)
    is_correct = bool(selected_ans and selected_ans.get("right") == 1)

    # To'g'ri javob matnini aniqlash
    correct_ans = next((a for a in answers if a.get("right") == 1), None)
    correct_text = ""
    if correct_ans:
        num = correct_ans["number"]
        name = correct_ans["name_uz_uz"] if lang == "uz" else correct_ans["name_ru_ru"]
        correct_text = f"{num}) {name or ''}"

    # Sessiyani yangilash
    await db.update_session_answer(user_id, q_id, selected_ans_id, is_correct)

    # Javob natijasi matni
    if is_correct:
        feedback = get_text("correct_answer_feedback", lang)
    else:
        feedback = get_text("wrong_answer_feedback", lang, correct_text=correct_text)

    is_last = (current_idx == len(question_ids) - 1)
    new_kb = get_question_keyboard(
        answers,
        selected_answer_id=selected_ans_id,
        is_answered=True,
        is_last=is_last,
        lang=lang
    )

    # Xabarga javob natijasini qo'shamiz
    orig_text = callback.message.caption or callback.message.text or ""
    separator = "\n\n────────────────\n"
    
    if callback.message.photo:
        # Telegram photo caption limiti 1024 belgi
        max_orig_len = 1020 - len(separator) - len(feedback)
        if len(orig_text) > max_orig_len and max_orig_len > 50:
            orig_text = orig_text[:max_orig_len] + "..."
    
    updated_text = f"{orig_text}{separator}{feedback}"

    try:
        if callback.message.photo:
            await callback.message.edit_caption(
                caption=updated_text,
                reply_markup=new_kb,
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                text=updated_text,
                reply_markup=new_kb,
                parse_mode="HTML"
            )
    except TelegramBadRequest as e:
        logger.warning(f"Xabarni tahrirlashda ogohlantirish: {e}")

    await callback.answer("✅ To'g'ri!" if is_correct else "❌ Noto'g'ri!")

@router.callback_query(F.data == "next_q")
async def cb_next_question(callback: CallbackQuery, bot: Bot):
    """Keyingi savolga o'tish."""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    new_index = await db.advance_session_index(user_id)
    session = await db.get_session(user_id)

    if not session or new_index >= len(session["question_ids"]):
        await finish_quiz(bot, chat_id, user_id, callback.message.message_id)
        await callback.answer()
        return

    old_msg_id = callback.message.message_id
    await render_question(bot, chat_id, user_id, session, old_message_id=old_msg_id)
    await callback.answer()

@router.callback_query(F.data == "cancel_quiz")
async def cb_cancel_quiz(callback: CallbackQuery, bot: Bot):
    """Testni to'xtatish."""
    user_id = callback.from_user.id
    lang = await db.get_user_lang(user_id)

    await db.cancel_session(user_id)
    try:
        await callback.message.delete()
    except Exception:
        pass

    text = get_text("quiz_cancelled", lang)
    await callback.message.answer(
        text,
        reply_markup=get_main_reply_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()

async def finish_quiz(bot: Bot, chat_id: int, user_id: int, old_msg_id: Optional[int] = None):
    """Testni yakunlash va natijalarni ko'rsatish."""
    session = await db.finish_session(user_id)
    if not session:
        return

    lang = await db.get_user_lang(user_id)
    total = len(session["question_ids"])
    score = session["score"]
    mistakes = session["mistakes"]
    percentage = round((score / total * 100) if total > 0 else 0)

    header = get_text("result_header", lang)
    info = get_text(
        "result_info",
        lang,
        title=session["title"],
        total=total,
        score=score,
        mistakes=mistakes,
        percentage=percentage
    )

    passed = (percentage >= PASSING_PERCENTAGE)
    status_text = get_text("result_passed" if passed else "result_failed", lang)
    final_text = f"{header}{info}{status_text}"

    # Keyingi bilet mavjudligini tekshirish (agar bilet rejimi bo'lsa)
    has_next_bilet = False
    next_topic_id = None
    next_bilet_num = None

    if session["mode"] == "bilet" and session.get("topic_id"):
        topic = await db.get_topic_by_id(session["topic_id"])
        if topic and topic.get("number"):
            next_topic = await db.get_next_topic(topic["number"], topic.get("book_id", 49))
            if next_topic:
                has_next_bilet = True
                next_topic_id = next_topic["id"]
                next_bilet_num = next_topic["number"]

    has_mistakes = (mistakes > 0)
    finish_kb = get_finish_keyboard(
        has_next_bilet=has_next_bilet,
        next_topic_id=next_topic_id,
        next_bilet_num=next_bilet_num,
        has_mistakes=has_mistakes,
        lang=lang
    )

    if old_msg_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except Exception:
            pass

    await bot.send_message(
        chat_id=chat_id,
        text=final_text,
        reply_markup=finish_kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "retry_quiz")
async def cb_retry_quiz(callback: CallbackQuery, bot: Bot):
    """Xuddi shu testni qaytadan boshlash."""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    # Oxirgi o'ynagan biletni topamiz yoki 1-biletni yuklaymiz
    user = await db.get_user_stats(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    # Default sifatida 1-biletni qayta boshlaymiz
    topics = await db.get_topics()
    if topics:
        first_topic = topics[0]
        q_ids = await db.get_bilet_question_ids(first_topic["id"])
        title = first_topic["name_uz_uz"] if lang == "uz" else first_topic["name_ru_ru"]
        await callback.message.delete()
        await start_quiz_session(bot, chat_id, user_id, "bilet", title, q_ids, topic_id=first_topic["id"])
    await callback.answer()
