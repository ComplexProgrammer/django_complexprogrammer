# avtotest_bot/handlers/start.py
import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from ..database import db
from ..texts import get_text
from ..keyboards import get_main_reply_keyboard, get_language_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name or "Foydalanuvchi"

    user = await db.get_or_create_user(user_id, username, full_name)
    lang = user.get("lang", "uz")

    welcome_text = get_text("welcome", lang, name=full_name)
    await message.answer(
        welcome_text,
        reply_markup=get_main_reply_keyboard(lang),
        parse_mode="HTML"
    )

@router.message(Command("lang"))
@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык"]))
async def cmd_select_language(message: Message):
    user_id = message.from_user.id
    lang = await db.get_user_lang(user_id)
    text = get_text("select_lang", lang)
    await message.answer(text, reply_markup=get_language_keyboard(), parse_mode="HTML")

@router.callback_query(F.data.startswith("set_lang:"))
async def cb_set_language(callback: CallbackQuery):
    lang_code = callback.data.split(":")[1]
    if lang_code not in ["uz", "ru"]:
        lang_code = "uz"

    user_id = callback.from_user.id
    await db.update_user_lang(user_id, lang_code)

    confirm_text = get_text("lang_chosen", lang_code)
    await callback.message.delete()
    await callback.message.answer(
        confirm_text,
        reply_markup=get_main_reply_keyboard(lang_code),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "to_main_menu")
async def cb_to_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await db.get_user_lang(user_id)
    name = callback.from_user.full_name or "Foydalanuvchi"

    await db.cancel_session(user_id)
    try:
        await callback.message.delete()
    except Exception:
        pass

    welcome_text = get_text("welcome", lang, name=name)
    await callback.message.answer(
        welcome_text,
        reply_markup=get_main_reply_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()
