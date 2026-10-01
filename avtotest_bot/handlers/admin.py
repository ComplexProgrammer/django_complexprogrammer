import asyncio
import logging
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from ..config import ADMIN_IDS
from ..database import db
from ..keyboards import get_admin_keyboard

logger = logging.getLogger(__name__)
router = Router()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Admin panelga kirish."""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Sizda admin huquqlari mavjud emas.")
        return

    stats = await db.get_total_stats()
    now_time = datetime.now().strftime("%H:%M:%S")
    text = (
        "🔐 <b>@AvtoTestUzbBot Admin Paneli</b>\n\n"
        f"👥 <b>Jami foydalanuvchilar:</b> {stats['total_users']} ta\n"
        f"🚗 <b>Ishlangan testlar:</b> {stats['total_tests']} ta\n"
        f"❓ <b>Yechilgan savollar:</b> {stats['total_questions']} ta\n\n"
        f"🕒 <i>Vaqt: {now_time}</i>\n\n"
        "Quyidagi amallardan birini tanlang 👇"
    )
    await message.answer(text, reply_markup=get_admin_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "admin_stats")
async def cb_admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    stats = await db.get_total_stats()
    now_time = datetime.now().strftime("%H:%M:%S")
    text = (
        "📊 <b>Botning umumiy ko'rsatkichlari:</b>\n\n"
        f"👥 <b>Foydalanuvchilar:</b> {stats['total_users']} ta\n"
        f"🚗 <b>Test sessiyalari:</b> {stats['total_tests']} ta\n"
        f"❓ <b>Yechilgan savollar:</b> {stats['total_questions']} ta\n\n"
        f"🕒 <i>Oxirgi yangilanish: {now_time}</i>"
    )
    try:
        await callback.message.edit_text(text, reply_markup=get_admin_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        pass
    await callback.answer("Statistika yangilandi 🔄")

@router.callback_query(F.data == "admin_broadcast")
async def cb_admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.message.answer(
        "📢 <b>Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yuboring:</b>\n\n"
        "<i>(Bekor qilish uchun /cancel deb yozing)</i>",
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(AdminStates.waiting_for_broadcast)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    if message.text and message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("Xabar yuborish bekor qilindi.")
        return

    user_ids = await db.get_all_user_ids()
    total = len(user_ids)
    success = 0
    failed = 0

    progress_msg = await message.answer(f"⏳ Xabar tarqatilmoqda... 0/{total}")

    for idx, uid in enumerate(user_ids):
        try:
            await bot.copy_message(
                chat_id=uid,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            success += 1
        except Exception:
            failed += 1

        # Har 20 ta xabarda statusni yangilaymiz
        if (idx + 1) % 20 == 0 or (idx + 1) == total:
            try:
                await progress_msg.edit_text(f"⏳ Xabar tarqatilmoqda... {idx + 1}/{total}")
            except Exception:
                pass
        await asyncio.sleep(0.05)

    await state.clear()
    await progress_msg.edit_text(
        f"✅ <b>Xabar tarqatish yakunlandi!</b>\n\n"
        f"📤 Yuborildi: {success} ta\n"
        f"❌ Yetib bormadi (bloklangan): {failed} ta",
        parse_mode="HTML"
    )
