"""O'zbek lotin yozuvidan kirill yozuviga o'girish (``*_uz_crl`` maydonlari uchun).

HTML teglari, ``&nbsp;`` kabi belgilar, havolalar va ``@username`` o'zgarmaydi — faqat matn qismi o'giriladi.
"""

import re

_APOS = "'‘’ʻʼ`"
_PAIRS = {
    "o'": "ў", "g'": "ғ", "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я", "ye": "е",
}
_SINGLE = {
    "a": "а", "b": "б", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "ҳ", "i": "и", "j": "ж", "k": "к",
    "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т", "u": "у",
    "v": "в", "x": "х", "y": "й", "z": "з",
}
_VOWELS = set("aeiou")
# HTML teglari, &...; belgilar, havolalar va @username o'girilmaydi
_MARKUP = re.compile(r"(<[^>]*>|&#?\w+;|https?://\S+|@\w+)")


def _convert(text):
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        low = ch.lower()
        nxt = text[i + 1].lower() if i + 1 < n else ""
        if nxt and nxt in _APOS:
            nxt = "'"
        prev = text[i - 1] if i else ""
        word_start = not prev.isalpha() and not (prev and prev in _APOS)
        pair = low + nxt
        after = text[i + 2] if i + 2 < n else ""
        if pair == "yo" and after and after in _APOS:
            pair = ""  # yo'l -> йўл (y + o'), ё emas
        if pair in _PAIRS:
            cyr = _PAIRS[pair]
            out.append(cyr.upper() if ch.isupper() else cyr)
            i += 2
            continue
        if low == "e" and word_start:
            out.append("Э" if ch.isupper() else "э")
        elif ch in _APOS:
            # tutuq belgisi (ma'no, san'at) — ъ; boshqa joyda (qo'shtirnoq) o'zgarmaydi
            out.append("ъ" if prev.lower() in _VOWELS | set("ln") and i + 1 < n and text[i + 1].isalpha() else ch)
        elif low in _SINGLE:
            cyr = _SINGLE[low]
            out.append(cyr.upper() if ch.isupper() else cyr)
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def latin_to_cyrillic(text):
    if not text:
        return text
    return "".join(part if _MARKUP.fullmatch(part) else _convert(part) for part in _MARKUP.split(text))
