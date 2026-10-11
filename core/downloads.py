"""Vaqtinchalik yuklab olinadigan fayllar uchun yagona xavfsiz papka.

Foydalanuvchiga faqat shu papka ichidagi fayllar beriladi va faqat fayl nomi
(yo'lsiz) qabul qilinadi, shuning uchun ``../settings.py`` kabi yo'llar ishlamaydi.
"""

import os
import time
import uuid

from django.conf import settings

DOWNLOADS_DIR = os.path.join(settings.MEDIA_ROOT, "downloads")
# Shundan eski fayllar avtomatik o'chiriladi (soniya)
MAX_AGE_SECONDS = 60 * 60


def ensure_dir():
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    return DOWNLOADS_DIR


def new_name(original_name, ext=None):
    """Takrorlanmas va xavfsiz fayl nomi yaratadi: ``<uuid>_<asl nom>``."""
    base = os.path.basename(original_name or "file")
    stem, orig_ext = os.path.splitext(base)
    ext = ext or orig_ext
    safe_stem = "".join(c for c in stem if c.isalnum() or c in "-_ ")[:60].strip()
    return f"{uuid.uuid4().hex[:12]}_{safe_stem or 'file'}{ext.lower()}"


def resolve(name):
    """Fayl nomini DOWNLOADS_DIR ichidagi to'liq yo'lga aylantiradi.

    Nom yo'l bo'lsa, ruxsat etilmagan kengaytmada bo'lsa yoki fayl mavjud
    bo'lmasa ``None`` qaytaradi.
    """
    if not name:
        return None
    base = os.path.basename(name)
    if base != name or base.startswith("."):
        return None
    if os.path.splitext(base)[1].lower() not in settings.GET_FILE_FORMATS:
        return None
    path = os.path.realpath(os.path.join(DOWNLOADS_DIR, base))
    if os.path.dirname(path) != os.path.realpath(DOWNLOADS_DIR):
        return None
    return path if os.path.isfile(path) else None


def cleanup_old(max_age=MAX_AGE_SECONDS):
    """Eskirgan fayllarni o'chiradi (har yuklab olishda chaqiriladi)."""
    if not os.path.isdir(DOWNLOADS_DIR):
        return
    limit = time.time() - max_age
    for entry in os.scandir(DOWNLOADS_DIR):
        try:
            if entry.is_file() and entry.stat().st_mtime < limit:
                os.remove(entry.path)
        except OSError:
            pass
