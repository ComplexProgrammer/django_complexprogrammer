"""Yo'l harakati qoidalari (VM 2022-yil 12-apreldagi 172-son qarori, 1-ilova) — lex.uz'dan olingan matn.

Matn ``driving/data/yhq_<til>.json`` da saqlanadi (``python manage.py import_yhq`` yangilaydi). Qonun hujjatlari
mualliflik huquqi obyekti emas; manba va sana sahifada ko'rsatiladi.
"""

import html
import json
import re
from functools import lru_cache
from pathlib import Path

# Rasmiy matn: özbekça (asosiy) va ruscha (lex.uz'da alohida hujjat — 5953887). /en/ sahifalari özbekça
# matnni körsatadi va canonical özbekça sahifaga.
SOURCE_URL = "https://lex.uz/uz/docs/-5953883"
SOURCE_URLS = {"uz": SOURCE_URL, "ru": "https://lex.uz/ru/docs/5953887"}
LANGS = tuple(SOURCE_URLS)
DATA_DIR = Path(__file__).resolve().parent / "data"

# Element ID: özbekça sahifada manfiy ("-7706740"), ruscha hujjatda musbat
_ELEMENT = re.compile(r'<div class="([A-Z_]+) lx_elem"[^>]*>.*?<div name="(-?\d+)" id="-?\d+">(.*?)</div>\s*</div>', re.S)
# Bob sarlavhasi: "5-bob. Nomi" (uz) yoki "Глава 5. Название" / "Глава 17¹. ..." (ru)
_CHAPTER_UZ = re.compile(r"^(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]*)[-‑]\s*bob\.?\s*(.+)$", re.I)
_CHAPTER_RU = re.compile(r"^Глава\s+(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]*)\.?\s*(.+)$", re.I)
_SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
_UNSUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
_POINT = re.compile(r"^(\d+[⁰¹²³⁴⁵⁶⁷⁸⁹]*)\.\s")
_SIGN = re.compile(r"^(\d+(?:\.\d+)+)\.?(?:,\s*\d+(?:\.\d+)+\.?)*(?:\s*[—–-]\s*\d+(?:\.\d+)+\.?)?\s*[“«\"]([^”»\"]+)[”»\"]\.?\s*(.*)$", re.S)


# Qo'shtirnoqsiz yozilgan qisqa belgi satri: "1.25.2. Pastlab uchuvchi qushlar"
_SIGN_PLAIN = re.compile(r"^(\d+(?:\.\d+)+)\.\s+([^“”«».]{3,80})\.?()$")


def _text(raw):
    raw = re.sub(r"<br\s*/?>", "\n", raw)
    # 115<sup>2</sup>. -> 115² (qo'shimcha kiritilgan bandlar, 17¹-bob)
    raw = re.sub(r"<sup>\s*(\d+)\s*</sup>", lambda m: m.group(1).translate(_SUP), raw)
    return re.sub(r"[ \t]+", " ", html.unescape(re.sub(r"<[^>]+>", "", raw))).strip()


def parse(page_html):
    """lex.uz sahifasidan boblar (bandlari bilan) va yo'l belgilari ilovasini ajratadi."""
    items = [(cls, _text(raw)) for cls, _, raw in _ELEMENT.findall(page_html)]
    chapters, signs = [], []
    section = None  # "rules" | "signs" | None
    current = point = None
    for cls, text in items:
        if section == "signs" and cls in ("TEXT_CENTER", "APPL_BANNER_LANDSCAPE_TITLE") and text:
            section = None  # belgilar ro'yxati tugadi (keyin svetoforlar, yo'l chiziqlari ilovasi)
            continue
        if not text:
            continue
        if cls == "ACT_TITLE_APPL":
            low = text.lower()
            section = "rules" if ("harakati qoidalari" in low or "правила дорожного движения" in low) and not chapters \
                else "signs" if ("belgilari" in low or "дорожные знаки" in low) and not signs else None
            current = point = None
            continue
        if section == "rules":
            if cls == "TEXT_HEADER_DEFAULT":
                m = _CHAPTER_UZ.match(text) or _CHAPTER_RU.match(text)
                if not m:
                    continue
                number, sup, title = m.group(1), m.group(2), m.group(3).strip()
                slug = number + ("-" + sup.translate(_UNSUP) if sup else "")  # 17¹-bob -> /yhq/17-1-bob/
                current = {"num": number + sup, "slug": slug, "title": title, "points": []}
                chapters.append(current)
                point = None
            elif cls == "ACT_TEXT" and current is not None:
                m = _POINT.match(text)
                if m:
                    point = {"num": m.group(1), "paragraphs": [text[m.end():].strip()]}
                    current["points"].append(point)
                elif point is not None:
                    point["paragraphs"].append(text)
                else:
                    current.setdefault("intro", []).append(text)
        elif section == "signs" and cls == "ACT_TEXT":
            m = _SIGN.match(text) or _SIGN_PLAIN.match(text)
            if m:
                signs.append({"num": m.group(1), "name": m.group(2).strip(), "text": m.group(3).strip(), "raw": text})
            elif signs:
                signs[-1]["text"] = (signs[-1]["text"] + "\n" + text).strip()
    return {"chapters": chapters, "signs": sorted(signs, key=lambda s: [int(x) for x in s["num"].split(".")])}


@lru_cache(maxsize=4)
def load(lang="uz"):
    path = DATA_DIR / f"yhq_{lang}.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"chapters": [], "signs": [], "fetched": ""}


def text_lang(lang):
    """Sahifa tilida rasmiy matn bormi: ruscha fayl bölsa "ru", qolgan hollarda özbekça matn."""
    return lang if lang in LANGS and load(lang)["chapters"] else "uz"


def chapter(slug, lang="uz"):
    return next((c for c in load(lang)["chapters"] if c["slug"] == slug), None)


def chapter_label(num, lang="uz"):
    return f"Глава {num}" if lang == "ru" else f"{num}-bob"


# Avtotest mavzulari -> tegishli boblar (savol sahifasidan qoidaga, qoidadan savollarga havola)
TOPIC_CHAPTERS = {
    "chorrahalar": ["14", "15", "16"], "quvib-otish": ["12"], "toxtash-va-turish": ["13"], "svetofor": ["7"],
    "manyovr-va-burilish": ["9", "10"], "piyodalar": ["4", "17"], "tezlik": ["11"], "temir-yol-kesishmasi": ["18"],
    "jamoat-transporti": ["17-1", "22"], "shatakka-olish": ["24"], "yoritish": ["23"],
}
