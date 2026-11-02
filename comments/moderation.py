"""Izohlar moderatsiyasi: spamni aniqlaş va şaxsiy ma'lumotlarni (telefon, pasport, JŞŞIR, karta) yaşiriş.

Bazadagi izohlarda köp uçraydigan muammolar:
* reklama va havolali spam (kazino, SEO, "GSA SER Project");
* bir xil matn bir necha marta;
* foydalanuvçilar öz pasport, JŞŞIR va telefon raqamini oçiq yozgan (uy-joy navbati haqidagi savollarda).
"""

import re

LINK_RE = re.compile(
    r"https?://|www\.|\[url|<a\s|href\s*=|\b[\w-]+\.(?:com|net|org|ru|info|biz|xyz|top|site|online|shop|io|me|it|de|br)\b",
    re.I,
)
# "bet" (sahifa) va "sex" (ustaxona) özbekça sözlar — şuning uçun röyxatda yöq
SPAM_WORDS_RE = re.compile(
    r"\b(?:casino|kazino|казино|betting|slot|poker|porn|xxx|escort|viagra|cialis|loan|backlinks?|seo\s+services?|"
    r"gsa\s+ser|web\s*design\s+services?|erotik\w*|эротик\w*|ставк\w*|букмекер\w*|займ\w*|crypto\s+recovery|"
    r"seo|продвиж\w*|раскрутк\w*|посещаемост\w*|веб-дизайн\w*)\b",
    re.I,
)

# Şaxsiy ma'lumotlar: raqamlar orasida böşliq, çiziqça yoki nuqta bölişi mumkin
_SEP = r"[\s\-.()]*"
PHONE_RE = re.compile(r"(?<!\d)(?:\+?998" + _SEP + r")?\(?\d{2}\)?" + _SEP + r"\d{3}" + _SEP + r"\d{2}" + _SEP + r"\d{2}(?!\d)")
JSHSHIR_RE = re.compile(r"(?<!\d)\d{14}(?!\d)")
CARD_RE = re.compile(r"(?<!\d)(?:\d{4}" + _SEP + r"){3}\d{4}(?!\d)")
PASSPORT_RE = re.compile(r"\b[A-Za-zА-Яа-я]{2}" + r"\s?\d{7}\b")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
MASK = "•••"


# Saytning öz manzillari (ilova, Telegram bot, kanal) havola hisoblanmaydi
ALLOWED_LINK_RE = re.compile(
    r"(?:https?://)?(?:www\.)?(?:complexprogrammer\.uz\S*|t\.me/AvtoTestUzbBot\S*|"
    r"play\.google\.com/store/apps/details\?id=uzbavtotest\.complexprogrammer\.uz\S*|my\.gov\.uz\S*)",
    re.I,
)


def spam_reason(text, username=""):
    """Izoh spamga öxşasa sababini qaytaradi (moderatsiyaga tuşadi), aks holda böş qator."""
    # Email manzil (köpinça ism örniga yozilgan) havola hisoblanmaydi
    sample = EMAIL_RE.sub(" ", ALLOWED_LINK_RE.sub(" ", f"{username} {text}"))
    if LINK_RE.search(sample):
        return "havola"
    if SPAM_WORDS_RE.search(sample):
        return "reklama sözlari"
    return ""


def mask_pii(text):
    """Izohdagi email, telefon, karta, JŞŞIR va pasport raqamlarini ••• bilan yaşiradi (bazadagi asl matn özgarmaydi)."""
    if not text:
        return text
    text = EMAIL_RE.sub(lambda m: m.group(0)[:2] + MASK, text)
    if not any(ch.isdigit() for ch in text):
        return text
    for pattern in (CARD_RE, JSHSHIR_RE, PHONE_RE, PASSPORT_RE):
        text = pattern.sub(MASK, text)
    return text
