"""Avtotest savollarini mavzularga ajratiş (özbekça matndagi kalit sözlar böyiça).

Bazada mavzu maydoni yöq, şuning uçun mavzu savol va javob matnidan aniqlanadi; bitta savol bir nechta mavzuga
tushishi mumkin. Odamlar "chorraha savollari", "quvib o'tish avtotest" kabi so'rovlar bilan qidiradi —
har bir mavzu alohida sahifa (/avtotest/mavzu/<slug>/).
"""

import re

from django.core.cache import cache

from projects.models import AvtoTest

# (slug, kalit so'zlar regex'i, {til: nomi})
TOPICS = [
    ("chorrahalar", r"chorraha|çorraha", {"uz": "Çorrahalardan ötiş", "ru": "Проезд перекрёстков", "en": "Intersections"}),
    ("quvib-otish", r"quvib o'?t|quvib ket|quvishni", {"uz": "Quvib ötiş", "ru": "Обгон", "en": "Overtaking"}),
    ("toxtash-va-turish", r"t[oö][\'ʻʼ]?xta[şs]h?|t[oö][\'ʻʼ]?xtab tur", {"uz": "Töxtaş va töxtab turiş", "ru": "Остановка и стоянка", "en": "Stopping and parking"}),
    ("svetofor", r"svetofor|tartibga soluvchi|tartibga solin", {"uz": "Svetofor va tartibga soluvçi işoralari", "ru": "Светофор и сигналы регулировщика", "en": "Traffic lights and controller signals"}),
    ("yol-belgilari", r"belgi(si|lar|ning|ga|dan|ni)?\b|belgisi", {"uz": "Yöl belgilari", "ru": "Дорожные знаки", "en": "Road signs"}),
    ("yol-chiziqlari", r"chiziq|çiziq", {"uz": "Yöl çiziqlari (razmetka)", "ru": "Дорожная разметка", "en": "Road markings"}),
    ("manyovr-va-burilish", r"burili[şs]h?|qayrili[şs]h?|orqaga|manyovr|çhapga|chapga|[oö][\'ʻʼ]?ngga", {"uz": "Manyovr, buriliş va qayriliş", "ru": "Манёвры, повороты и разворот", "en": "Manoeuvres, turns and U-turns"}),
    ("piyodalar", r"piyoda", {"uz": "Piyodalar va piyodalar ötiş joylari", "ru": "Пешеходы и пешеходные переходы", "en": "Pedestrians and crossings"}),
    ("tezlik", r"tezlik|km/soat|km/s", {"uz": "Harakat tezligi", "ru": "Скорость движения", "en": "Speed limits"}),
    ("temir-yol-kesishmasi", r"temir y[oö][\'ʻʼ]?l|pereezd", {"uz": "Temir yöl kesişmalari", "ru": "Железнодорожные переезды", "en": "Railway crossings"}),
    ("jamoat-transporti", r"avtobus|tramvay|trolleybus|marshrut", {"uz": "Jamoat transporti va tramvay", "ru": "Общественный транспорт и трамвай", "en": "Public transport and trams"}),
    ("shatakka-olish", r"[şs]h?atak", {"uz": "Şatakka oliş", "ru": "Буксировка", "en": "Towing"}),
    ("tibbiy-yordam", r"tibbiy|jarohat|[şs]h?ikast|qon ket|bint|nafas|yurak|hu[şs]h?idan|kuyi[şs]h?|suyak", {"uz": "Birinçi tibbiy yordam", "ru": "Первая медицинская помощь", "en": "First aid"}),
    ("texnik-holat", r"tormoz|\b[şs]h?ina|nosoz|\brul\b|texnik holat|dvigatel|akkumulyator", {"uz": "Texnik holat va nosozliklar", "ru": "Техническое состояние и неисправности", "en": "Vehicle condition and faults"}),
    ("yoritish", r"chiroq|çiroq|\bfara|yoriti[şs]h?|keçasi|kechasi|tungi|k[oö][\'ʻʼ]?rini[şs]h? yetarli", {"uz": "Taşqi yoritiş va köriniş", "ru": "Внешние световые приборы и видимость", "en": "Lights and visibility"}),
]
TOPIC_BY_SLUG = {slug: (slug, pattern, names) for slug, pattern, names in TOPICS}
_COMPILED = [(slug, re.compile(pattern)) for slug, pattern, _ in TOPICS]
_APOSTROPHES = re.compile(r"[`ʻʼ‘’´]")
CACHE_KEY = "avtotest_topics_v2"


def normalize(text):
    return _APOSTROPHES.sub("'", (text or "").lower())


def topics_for_text(text):
    text = normalize(text)
    return [slug for slug, rx in _COMPILED if rx.search(text)]


def topic_map():
    """{slug: [savol_id, ...]} — 6 soatga keshlanadi (savollar kam özgaradi)."""
    data = cache.get(CACHE_KEY)
    if data is None:
        data = {slug: [] for slug, _, _ in TOPICS}
        for q in AvtoTest.objects.order_by("bilet", "raqam").values("id", "savol", "javob_a", "javob_b", "javob_c", "javob_d"):
            text = " ".join([q["savol"], q["javob_a"], q["javob_b"], q["javob_c"], q["javob_d"]])
            for slug in topics_for_text(text):
                data[slug].append(q["id"])
        cache.set(CACHE_KEY, data, 6 * 3600)
    return data


def topic_name(slug, lang):
    names = TOPIC_BY_SLUG[slug][2]
    return names.get(lang) or names["en"]
