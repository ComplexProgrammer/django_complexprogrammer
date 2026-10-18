"""Imtihon natijasi kartochkasi (1200×630 PNG) — ulashilgan havola Telegram, Facebook va boshqalarda rasm bilan ko'rinadi."""

import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = Path(__file__).resolve().parent / "fonts" / "NotoSans.ttf"
W, H = 1200, 630

TEXT = {
    "uz": {"passed": "Imtihondan o'tdim!", "failed": "Yana mashq qilaman", "sub": "Avtotest imtihon simulyatori · 20 savol, 25 daqiqa", "cta": "Siz ham sinab ko'ring »"},
    "ru": {"passed": "Экзамен сдан!", "failed": "Буду тренироваться", "sub": "Симулятор экзамена ПДД · 20 вопросов, 25 минут", "cta": "Попробуйте и вы »"},
    "en": {"passed": "I passed the exam!", "failed": "More practice needed", "sub": "Driving exam simulator · 20 questions, 25 minutes", "cta": "Try it yourself »"},
}


def _font(size, weight="Bold"):
    font = ImageFont.truetype(str(FONT), size)
    font.set_variation_by_name(weight)
    return font


def _center(draw, y, text, font, fill):
    width = draw.textlength(text, font=font)
    draw.text(((W - width) / 2, y), text, font=font, fill=fill)


def exam_card(correct, total, passed, lang="uz"):
    t = TEXT.get(lang, TEXT["en"])
    top, bottom = ((22, 163, 74), (21, 128, 61)) if passed else ((79, 70, 229), (124, 58, 237))
    img = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(img)
    for y in range(H):  # vertikal gradient
        k = y / H
        draw.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))

    white, soft = (255, 255, 255), (230, 236, 255)
    _center(draw, 60, "AVTOTEST", _font(40, "SemiBold"), soft)
    _center(draw, 120, f"{correct}/{total}", _font(210), white)
    _center(draw, 375, t["passed"] if passed else t["failed"], _font(64), white)
    _center(draw, 470, t["sub"], _font(32, "Regular"), soft)
    _center(draw, 540, f"complexprogrammer.uz  ·  {t['cta']}", _font(34, "SemiBold"), white)

    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()
