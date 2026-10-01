# avtotest_bot/keyboards.py
from typing import List, Dict, Any, Optional
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from .texts import get_text

def get_main_reply_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi (pastdagi panel)."""
    kb = [
        [
            KeyboardButton(text=get_text("btn_bilets", lang)),
            KeyboardButton(text=get_text("btn_exam", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_mistakes", lang)),
            KeyboardButton(text=get_text("btn_stats", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_cdl", lang)),
            KeyboardButton(text=get_text("btn_lang", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_help", lang))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Tilni tanlash tugmalari."""
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_bilet_list_keyboard(
    topics: List[Dict[str, Any]],
    current_page: int = 1,
    per_page: int = 15,
    lang: str = "uz"
) -> InlineKeyboardMarkup:
    """108 ta bilet uchun sahifalangan (pagination) inline tugmalar."""
    total_items = len(topics)
    total_pages = max(1, (total_items + per_page - 1) // per_page)
    current_page = max(1, min(current_page, total_pages))

    start_idx = (current_page - 1) * per_page
    end_idx = start_idx + per_page
    page_topics = topics[start_idx:end_idx]

    keyboard = []
    row = []

    for topic in page_topics:
        number = topic["number"]
        name = topic["name_uz_uz"] if lang == "uz" else topic["name_ru_ru"]
        if not name:
            name = f"{number}-bilet"
        btn_text = f"🚗 {number}-bilet" if lang == "uz" else f"🚗 {number}-й билет"
        row.append(InlineKeyboardButton(text=btn_text, callback_data=f"bilet:{topic['id']}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Navigatsiya qatori
    nav_row = []
    if current_page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"bilet_page:{current_page - 1}"))
    
    nav_row.append(InlineKeyboardButton(
        text=f"📄 {current_page}/{total_pages}",
        callback_data="noop"
    ))

    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"bilet_page:{current_page + 1}"))

    keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="to_main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_question_keyboard(
    answers: List[Dict[str, Any]],
    selected_answer_id: Optional[int] = None,
    is_answered: bool = False,
    is_last: bool = False,
    lang: str = "uz"
) -> InlineKeyboardMarkup:
    """Savol javob variantlari uchun inline tugmalar."""
    keyboard = []
    options_row = []

    for idx, ans in enumerate(answers):
        num = ans["number"] or (idx + 1)
        btn_text = f"{num}"

        if is_answered:
            if ans.get("right") == 1:
                btn_text = f"✅ {num}"
            elif ans["id"] == selected_answer_id:
                btn_text = f"❌ {num}"
            callback_data = "noop"
        else:
            callback_data = f"ans:{ans['id']}"

        options_row.append(InlineKeyboardButton(text=btn_text, callback_data=callback_data))

    if options_row:
        keyboard.append(options_row)

    # Javob berilgandan so'ng "Keyingi savol" tugmasi
    if is_answered:
        next_text = get_text("btn_finish_quiz" if is_last else "btn_next_question", lang)
        keyboard.append([InlineKeyboardButton(text=next_text, callback_data="next_q")])

    # Bekor qilish tugmasi
    keyboard.append([InlineKeyboardButton(text=get_text("btn_cancel_quiz", lang), callback_data="cancel_quiz")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_finish_keyboard(
    has_next_bilet: bool = False,
    next_topic_id: Optional[int] = None,
    next_bilet_num: Optional[int] = None,
    has_mistakes: bool = False,
    lang: str = "uz"
) -> InlineKeyboardMarkup:
    """Test yakunlanganidagi tugmalar."""
    keyboard = []

    # Qayta topshirish
    keyboard.append([InlineKeyboardButton(text=get_text("btn_retry", lang), callback_data="retry_quiz")])

    # Keyingi bilet
    if has_next_bilet and next_topic_id:
        keyboard.append([InlineKeyboardButton(
            text=get_text("btn_next_bilet", lang, next_bilet=next_bilet_num),
            callback_data=f"bilet:{next_topic_id}"
        )])

    # Xatolar ustida ishlash
    if has_mistakes:
        keyboard.append([InlineKeyboardButton(
            text=get_text("btn_review_mistakes", lang),
            callback_data="practice_mistakes"
        )])

    # Bosh menyu
    keyboard.append([InlineKeyboardButton(text=get_text("btn_home", lang), callback_data="to_main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Admin panel boshqaruv tugmalari."""
    keyboard = [
        [InlineKeyboardButton(text="📊 Bot statistikasi", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Xabar tarqatish (Broadcast)", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
