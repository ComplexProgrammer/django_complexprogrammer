"""O'zbek yozuvlari orasida o'girish: kirill, lotin (1995) va yangi lotin (2026).

1995-yilgi lotin alifbosida 26 harf va sh, ch, ng birikmalari bor; gʻ va oʻ ham ikki belgidan iborat.
2026-yilgi alifboda 28 harf: sh, ch, gʻ, oʻ o'rniga ş, ç, ğ, ö; ng alohida harf hisoblanmaydi (n + g).
Tutuq belgisi (ʼ) harf emas, belgi.

``latin_to_cyrillic``: HTML teglari, ``&nbsp;`` kabi belgilar, havolalar, ``@username``, ``<code>`` ichidagi
buyruqlar va ``translate="no"`` belgilangan teg ichidagi matn (brend nomlari: ``<span translate="no">Google Play</span>``)
o'zgarmaydi. Inglizcha so'zlar ham lotincha qoladi: o'zbek lotin yozuvida yo'q ``c`` (``ch`` dan tashqari) yoki ``w``
harfi bor so'zlar (Counter-Strike, Workshop, VAC) va raqamli so'zlar (CS2, AK-47).
"""

import re

_APOS = "'‘’ʻʼ`"
# 2026-yilgi alifbo (28 harf): yangi lotin, 1995-yilgi lotin, kirill
ALPHABET_2026 = [
    ("Aa", "Aa", "Аа"), ("Bb", "Bb", "Бб"), ("Dd", "Dd", "Дд"), ("Ee", "Ee", "Ее"), ("Ff", "Ff", "Фф"),
    ("Gg", "Gg", "Гг"), ("Ğğ", "Gʻgʻ", "Ғғ"), ("Hh", "Hh", "Ҳҳ"), ("Ii", "Ii", "Ии"), ("Jj", "Jj", "Жж"),
    ("Kk", "Kk", "Кк"), ("Ll", "Ll", "Лл"), ("Mm", "Mm", "Мм"), ("Nn", "Nn", "Нн"), ("Oo", "Oo", "Оо"),
    ("Öö", "Oʻoʻ", "Ўў"), ("Pp", "Pp", "Пп"), ("Qq", "Qq", "Ққ"), ("Rr", "Rr", "Рр"), ("Ss", "Ss", "Сс"),
    ("Şş", "Shsh", "Шш"), ("Çç", "Chch", "Чч"), ("Tt", "Tt", "Тт"), ("Uu", "Uu", "Уу"), ("Vv", "Vv", "Вв"),
    ("Xx", "Xx", "Хх"), ("Yy", "Yy", "Йй"), ("Zz", "Zz", "Зз"),
]
_PAIRS = {
    "o'": "ў", "g'": "ғ", "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я", "ye": "е",
}
_SINGLE = {
    "a": "а", "b": "б", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "ҳ", "i": "и", "j": "ж", "k": "к",
    "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т", "u": "у",
    "v": "в", "x": "х", "y": "й", "z": "з",
    "ş": "ш", "ç": "ч", "ğ": "ғ", "ö": "ў",  # 2026-yilgi alifbo harflari
}
_VOWELS = set("aeiouö")
_NEW_LETTERS = set("ŞÇĞÖşçğö")
# HTML teglari, Django teglari, <code>...</code>, style/script, translate="no" teglar, &...; belgilar, havolalar va @username o'girilmaydi
_MARKUP = re.compile(
    r'({%.*?%}|{{.*?}}|<code>.*?</code>|<style.*?>.*?</style>|<script.*?>.*?</script>|<(\w+)[^>]*\btranslate="no"[^>]*>.*?</\2>|<[^>]*>|&#?\w+;|https?://\S+|@\w+)',
    re.S,
)
# Lotincha qoladigan so'z: c (ch emas) yoki w harfi yoki raqami bor
_WORD = re.compile(r"[A-Za-zŞÇĞÖşçğö0-9'‘’ʻʼ`-]+")
_FOREIGN = re.compile(r"[cC](?![hH])|[wW]|\d")
_FOREIGN_LATIN = re.compile(r"[cC](?![hH])|[wW]")

COMMON_FOREIGN_WORDS = {
    "chrome", "google", "microsoft", "windows", "telegram", "instagram", "facebook",
    "youtube", "android", "ios", "python", "django", "chat", "chatgpt", "miniapp",
    "channel", "captcha", "javascript", "exchange", "exchangerates", "download",
    "downloader", "calculator", "sitemap", "word", "excel", "pdf", "search", "post",
    "posts", "git", "bash", "linux", "cloudlinux", "passenger", "bootstrap", "css",
    "html", "json", "api", "id", "url", "qr", "dark", "light", "mode", "theme"
}


# sh/ch bilan yoziladigan inglizça sözlar (va inglizça yozilişdagi nomlar): 2026-yilgi alifboga ögirilmaydi.
# Ro'yxat bazadagi haqiqiy buzilişlardan (Sçool, Şooter, toothaçe...) yig'ilgan; özbekça sözlar ataylab
# kiritilmagan (chap, choy, tosh, bosh, kishi, ish, uch, shu, chin, sher, osh...).
ENGLISH_SH_CH_WORDS = frozenset("""
she should shouldn shall shan school schools scholarship scholz children child childhood change changed changes
changing exchange exchanging shooter shooting shoot shot short shorter shorts shop shops shopping shoppers
bookshop bookshops photoshop each much such which rich reach teach teacher teachers teaching approach speech
english french turkish polish spanish finish finished finishing fish fishing fisherman fishermen match matches
matching unmatched chess cheese cheap cheat cheats cheater cheers chef chemist chemistry charge charm charters
chair chairs chapter purchase kitchen lunch brunch launch touch touched stretch brush brushes brushing push
pushed pushing rubbish hardship hardships share shared shares sharing shape shark shelf shelton shift shifted
shine shines shining shone shoe shoes shoulder shirt shirts show shows showed shown shower flash crash cash
wash washing watch catch fresh dish notch beech birch ranch march inch technology technologies tech techs
fintech mechanism machine machines machinery headache toothache earache research searching search achievement
achievements anchor anchors orchestra orchestras champion champions championship challenge challenges chance
choose chose chosen choice check checked cherry chicken chocolate church chair cheek chest chaplin
publish published publisher publishing fashion fashioned chauffeur chauffeurs tashkent shakespeare
richard charles christie chester manchester chevrolet blanchard aeschylus synchronized
breach breaches charity charities sponsorship channel channels attachment attachments interchangeable dashboard
schedule scheduled schema sketch switch fetch batch patch watchers worship relationship ownership membership
leadership partnership friendship workshop bishop crash brushed shell shellcode bash flush hash refresh push
""".split())


def _convert(text, new=False):
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
        if new and pair in ("sh", "ch"):
            pair = ""  # 2026-yilgi yozuvda sh = с + ҳ (Ishoq -> Исҳоқ)
        if pair in _PAIRS:
            cyr = _PAIRS[pair]
            out.append(cyr.upper() if ch.isupper() else cyr)
            i += 2
            continue
        if low == "e" and word_start:
            out.append("Э" if ch.isupper() else "э")
        elif ch in _APOS:
            if prev.lower() in "sc" and nxt == "h":
                pass  # Is'hoq -> Исҳоқ: ajratuvchi belgi tushib qoladi
            # tutuq belgisi (ma'no, san'at) — ъ; boshqa joyda (qo'shtirnoq) o'zgarmaydi
            elif prev.lower() in _VOWELS | set("ln") and i + 1 < n and text[i + 1].isalpha():
                out.append("ъ")
            else:
                out.append(ch)
        elif low in _SINGLE:
            cyr = _SINGLE[low]
            out.append(cyr.upper() if ch.isupper() else cyr)
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def _outside_markup(text, fn):
    """``fn`` ni faqat belgilashdan (teg, havola, @username) tashqaridagi matnga qo'llaydi."""
    parts = []
    pos = 0
    for m in _MARKUP.finditer(text):
        parts.append(fn(text[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(fn(text[pos:]))
    return "".join(parts)


def latin_to_cyrillic(text):
    """Lotin (1995 yoki 2026) -> kirill. 2026-yilgi harflar (ş, ç, ğ, ö) bo'lsa, sh/ch birikma emas."""
    if not text:
        return text
    new = any(c in _NEW_LETTERS for c in text)

    def words(part):
        return _WORD.sub(lambda m: m.group(0) if _FOREIGN.search(m.group(0)) else _convert(m.group(0), new), part)

    return _outside_markup(text, words)


_CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
    "х": "x", "ҳ": "h", "қ": "q", "э": "e", "ё": "yo", "ю": "yu", "я": "ya", "ъ": "ʼ", "ь": "", "ы": "i",
    "щ": "sh", "ш": "sh", "ч": "ch", "ў": "oʻ", "ғ": "gʻ",
}
_CYR_2026 = {"ш": "ş", "щ": "ş", "ч": "ç", "ў": "ö", "ғ": "ğ"}
_CYR_VOWELS = set("аеёиоуўэюяыъь")


def _case(lat, ch, prev, nxt):
    if not ch.isupper():
        return lat
    # SHAXAR (hammasi katta) -> SH, Shahar -> Sh
    if len(lat) > 1 and (nxt.isupper() or (not nxt.isalpha() and prev.isupper())):
        return lat.upper()
    return lat[:1].upper() + lat[1:]


def cyrillic_to_latin(text, alphabet="1995"):
    """Kirill -> lotin. ``alphabet``: "1995" (sh, ch, oʻ, gʻ) yoki "2026" (ş, ç, ö, ğ)."""
    if not text:
        return text
    table = dict(_CYR, **_CYR_2026) if alphabet == "2026" else _CYR
    out = []
    n = len(text)
    for i, ch in enumerate(text):
        low = ch.lower()
        prev = text[i - 1] if i else ""
        nxt = text[i + 1] if i + 1 < n else ""
        word_start = not prev.isalpha()
        if low == "е":
            lat = "ye" if word_start or prev.lower() in _CYR_VOWELS else "e"
        elif low == "ц":
            lat = "ts" if not word_start and prev.lower() in _CYR_VOWELS else "s"
        elif low == "ҳ" and alphabet != "2026" and prev.lower() in "сц":
            lat = "ʼh"  # Исҳоқ -> Isʼhoq (sh birikmasi bilan adashmaslik uchun)
        elif low in table:
            lat = table[low]
        else:
            out.append(ch)
            continue
        out.append(_case(lat, ch, prev, nxt))
    return "".join(out)


_OLD_PAIR = re.compile(r"([sScC])([hH])|([oOgG])[" + _APOS + r"]|([sS])[" + _APOS + r"]([hH])")
_NEW_OF = {"s": "ş", "c": "ç", "o": "ö", "g": "ğ"}
_OLD_OF = {"ş": "sh", "ç": "ch", "ö": "oʻ", "ğ": "gʻ"}


def latin1995_to_2026(text):
    """sh, ch, gʻ, oʻ -> ş, ç, ğ, ö; sʼh (Isʼhoq) -> sh."""
    if not text:
        return text

    def pair(m):
        if m.group(4):
            return m.group(4) + m.group(5)
        letter = m.group(1) or m.group(3)
        new = _NEW_OF[letter.lower()]
        return new.upper() if letter.isupper() else new

    def words(part):
        def _convert_word(m):
            w = m.group(0)
            if w.lower() in COMMON_FOREIGN_WORDS or is_english_word(w):
                return w
            if "-" in w and not any(c.isdigit() for c in w):
                return "-".join(s if is_english_word(s) else _OLD_PAIR.sub(pair, s) for s in w.split("-"))
            if any(c.isdigit() for c in w) and "-" in w:
                subs = w.split("-")
                res = []
                for s in subs:
                    if s.lower() in COMMON_FOREIGN_WORDS or _FOREIGN_LATIN.search(s) or s.isdigit():
                        res.append(s)
                    else:
                        res.append(_OLD_PAIR.sub(pair, s))
                return "-".join(res)
            if _FOREIGN_LATIN.search(w):
                return w
            return _OLD_PAIR.sub(pair, w)

        return _WORD.sub(_convert_word, part)

    return _outside_markup(text, words)


_EN_SUFFIX = ("", "s", "t", "ll", "re", "ve", "d", "m")  # children's, shouldn't, she'll
_APOS_SPLIT = re.compile(r"^([^" + _APOS + r"]*)[" + _APOS + r"](.*)$")


def is_english_word(word):
    """``word`` (1995 lotin yoki 2026 yozuvida) — ``ENGLISH_SH_CH_WORDS`` dagi inglizça sözmi.

    ``şe’r`` (she + r) özbekça: tutuq belgisidan keyingi qism inglizça qisqartma bölgandagina inglizça hisoblanadi.
    """
    if not word:
        return False
    low = word.lower().replace("ş", "sh").replace("ç", "ch")
    m = _APOS_SPLIT.match(low)
    base, suffix = (m.group(1), m.group(2)) if m else (low, "")
    return base in ENGLISH_SH_CH_WORDS and suffix in _EN_SUFFIX


def _restore_case(word):
    upper = word.isupper() and len(word) > 1
    return word.replace("Ş", "SH" if upper else "Sh").replace("Ç", "CH" if upper else "Ch").replace(
        "ş", "sh").replace("ç", "ch")


def restore_english_2026(text):
    """2026-yilgi alifboga xato ögirilgan inglizça sözlarni tiklaydi: Sçool -> School, ÇANGE -> CHANGE.

    Özbekça sözlarga tegmaydi (faqat ``ENGLISH_SH_CH_WORDS`` dagi sözlar); ö/ğ bor söz inglizça emas.
    """
    if not text or not any(c in "şçŞÇ" for c in text):
        return text

    out = []
    pos = 0
    for start, end, is_markup in _segments(text):
        if is_markup:
            continue
        for m in _WORD.finditer(text, start, end):
            w = m.group(0)
            if not any(c in "şçŞÇ" for c in w) or any(c in "öğÖĞ" for c in w):
                continue
            after = text[m.end():m.end() + 8]
            if after[:1].isalnum():
                continue  # birç᧐k: söz boşqa yozuvdagi harf bilan davom etadi
            ent = _APOS_ENTITY.match(after)
            if ent and ent.group(1).lower() not in _EN_SUFFIX:
                continue  # şe&#39;rlar — özbekça (şe’r)
            parts = w.split("-")
            if not all(is_english_word(p) for p in parts if any(c in "şçŞÇ" for c in p)):
                continue  # şop-şup — hammasi inglizça bölmasa tegmaymiz
            out.append(text[pos:m.start()])
            out.append("-".join(_restore_case(p) for p in parts))
            pos = m.end()
    out.append(text[pos:])
    return "".join(out)


_APOS_ENTITY = re.compile(r"(?:&#39;|&#x27;|&apos;|&rsquo;|&lsquo;|&#8217;|&#8216;)([A-Za-z]*)")


def _segments(text):
    """(boşlanış, tugaş, belgilaşmi) — ``_outside_markup`` bilan bir xil böliş, lekin indekslar bilan."""
    pos = 0
    for m in _MARKUP.finditer(text):
        yield pos, m.start(), False
        yield m.start(), m.end(), True
        pos = m.end()
    yield pos, len(text), False


def latin2026_to_1995(text):
    """ş, ç, ğ, ö -> sh, ch, gʻ, oʻ; s + h (Ishoq) -> sʼh."""
    if not text:
        return text

    def word(w):
        out = []
        n = len(w)
        for i, ch in enumerate(w):
            low = ch.lower()
            prev = w[i - 1] if i else ""
            nxt = w[i + 1] if i + 1 < n else ""
            if low in _OLD_OF:
                out.append(_case(_OLD_OF[low], ch, prev, nxt))
            elif low == "h" and prev.lower() == "s":
                out.append("ʼ" + ch)
            else:
                out.append(ch)
        return "".join(out)

    def words(part):
        return _WORD.sub(lambda m: m.group(0) if _FOREIGN.search(m.group(0)) else word(m.group(0)), part)

    return _outside_markup(text, words)


def detect_script(text):
    """Matn yozuvini aniqlaydi: "cyr", "lat2026" yoki "lat1995"."""
    cyr = sum(1 for c in text if "Ѐ" <= c <= "ӿ")
    lat = sum(1 for c in text if c.isascii() and c.isalpha() or c in _NEW_LETTERS)
    if cyr > lat:
        return "cyr"
    return "lat2026" if any(c in _NEW_LETTERS for c in text) else "lat1995"


def convert(text, to=None):
    """Matnni ``to`` yozuviga ("cyr", "lat1995", "lat2026") o'giradi.

    ``to`` berilmasa — avvalgidek: kirill matn lotinga (1995), lotin matn kirillga.
    """
    if not text:
        return text or ""
    source = detect_script(text)
    if to not in ("cyr", "lat1995", "lat2026"):
        to = "lat1995" if source == "cyr" else "cyr"
    if source == to:
        return text
    if source == "cyr":
        return cyrillic_to_latin(text, "2026" if to == "lat2026" else "1995")
    if to == "cyr":
        return latin_to_cyrillic(text)
    return latin1995_to_2026(text) if to == "lat2026" else latin2026_to_1995(text)


# AI yozgan özbekça matnda uçraydigan begona harflar (turkça, ruminça, grekça, kirill «körä» kabi aralaşmalar)
_STRAY = str.maketrans({
    "ä": "a", "Ä": "A", "ı": "i", "İ": "I", "ü": "u", "Ü": "U", "š": "ş", "Š": "Ş", "ș": "ş", "Ș": "Ş",
    "ţ": "t", "ț": "t", "τ": "t", "č": "ç", "Č": "Ç", "ə": "a", "Ə": "A", "ó": "ö", "ò": "ö", "ÿ": "y",
    "ñ": "n", "è": "e", "é": "e", "ĺ": "l", "ŋ": "ng", "ӧ": "ö", "Ӧ": "Ö", "\xad": "",
})
_LETTERS_RUN = re.compile(r"[^\W\d_]+")
_IS_CYR = re.compile(r"[Ѐ-ӿ]")


def clean_uz_latin(text):
    """Özbek lotin (2026) matnidagi begona belgilarni tuzatadi.

    * turkça/ruminça/grekça harflar: körä → köra, üçun → uçun, beriși → beriş, öτadi → ötadi;
    * lotin söz içiga aralaşgan kirill harflar: öрнатилган → örnatilgan, nеçа → neça;
    * alohida turgan kirill bosh harflar (А, Б, В — rasmdagi avtomobil belgilari) özgarmaydi.
    """
    if not text:
        return text
    text = text.replace('\\"', '"').translate(_STRAY)

    def fix(m):
        word = m.group(0)
        if not _IS_CYR.search(word) or (len(word) <= 2 and word.isupper()):
            return word
        return cyrillic_to_latin(word, "2026")

    return _LETTERS_RUN.sub(fix, text)
