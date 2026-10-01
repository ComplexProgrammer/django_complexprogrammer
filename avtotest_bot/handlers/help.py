# avtotest_bot/handlers/help.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ..database import db
from ..texts import get_text

router = Router()

@router.message(Command("help"))
@router.message(F.text.in_(["ℹ️ Bot haqida", "ℹ️ О боте"]))
async def cmd_help(message: Message):
    """Bot haqida ma'lumot va yordam."""
    user_id = message.from_user.id
    lang = await db.get_user_lang(user_id)
    text = get_text("help_text", lang)
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=False)
