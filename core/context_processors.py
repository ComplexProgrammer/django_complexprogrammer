"""Barcha shablonlarga umumiy ma'lumot: UI matnlari (4 tilda), SEO meta va canonical URL."""

from django.conf import settings
from django.utils import translation

SITE_URL = "https://complexprogrammer.uz"

UI = {
    "uz": {
        "home": "Bosh sahifa", "blog": "Blog", "projects": "Loyihalar", "tests": "Testlar",
        "avtotest": "Avtotest", "news": "Yangiliklar", "search": "Qidiruv",
        "search_placeholder": "Sayt bo'yicha qidirish...", "theme": "Mavzu", "language": "Til",
        "menu": "Menyu",
    },
    "ru": {
        "home": "Главная", "blog": "Блог", "projects": "Проекты", "tests": "Тесты",
        "avtotest": "Автотест", "news": "Новости", "search": "Поиск",
        "search_placeholder": "Поиск по сайту...", "theme": "Тема", "language": "Язык",
        "menu": "Меню",
    },
    "en": {
        "home": "Home", "blog": "Blog", "projects": "Projects", "tests": "Tests",
        "avtotest": "Driving test", "news": "News", "search": "Search",
        "search_placeholder": "Search the site...", "theme": "Theme", "language": "Language",
        "menu": "Menu",
    },
    "tr": {
        "home": "Ana sayfa", "blog": "Blog", "projects": "Projeler", "tests": "Testler",
        "avtotest": "Ehliyet testi", "news": "Haberler", "search": "Ara",
        "search_placeholder": "Sitede ara...", "theme": "Tema", "language": "Dil",
        "menu": "Menü",
    },
}

# Sahifa bo'yicha SEO sarlavha va tavsif: (uz, ru, en)
PAGE_META = {
    "/": (
        "Complex Programmer — onlayn vositalar, testlar va o'yinlar",
        "Бесплатные онлайн-инструменты, тесты ПДД и игры",
        "Free online tools, driving tests and games",
    ),
    "/avtotest/": (
        "Avtotest 2026 — YHQ imtihon biletlari onlayn",
        "Автотест — экзаменационные билеты ПДД Узбекистана онлайн",
        "Uzbekistan driving test tickets online",
    ),
    "/tests/": (
        "Onlayn testlar — avtotest, mavzular bo'yicha savollar",
        "Онлайн тесты по темам ПДД",
        "Online tests by topic",
    ),
    "/translate/": (
        "Onlayn tarjimon — o'zbek, rus, ingliz va 20+ til",
        "Онлайн переводчик — узбекский, русский, английский",
        "Free online translator — Uzbek, Russian, English and 20+ languages",
    ),
    "/password_generator/": (
        "Kuchli parol generatori — xavfsiz parol yaratish",
        "Генератор надёжных паролей",
        "Strong password generator",
    ),
    "/changetext/": (
        "Lotin-kirill o'girgich — o'zbek matnini lotin/kirillga o'tkazish",
        "Конвертер узбекского текста латиница — кириллица",
        "Uzbek Latin–Cyrillic text converter",
    ),
    "/exchangerates/": (
        "Valyuta kurslari — O'zbekiston Markaziy banki",
        "Курсы валют ЦБ Узбекистана",
        "Central Bank of Uzbekistan exchange rates",
    ),
    "/coins/": (
        "Kriptovalyuta narxlari onlayn",
        "Курсы криптовалют онлайн",
        "Cryptocurrency prices",
    ),
    "/ip/": ("IP manzilni aniqlash", "Узнать IP адрес", "IP address lookup"),
    "/sitemap/": (
        "Sitemap generator — sayt xaritasini yaratish",
        "Генератор карты сайта (sitemap.xml)",
        "XML sitemap generator",
    ),
    "/pdf_tools/": (
        "PDF ni Word, Excel va rasmga o'tkazish",
        "Конвертер PDF в Word, Excel и изображения",
        "Convert PDF to Word, Excel and images",
    ),
    "/imagecompare/": (
        "Ikki rasmni solishtirish — farqlarni topish",
        "Сравнение двух изображений",
        "Compare two images and find differences",
    ),
    "/youtube_downloader/": (
        "YouTube video yuklab olish",
        "Скачать видео с YouTube",
        "YouTube video downloader",
    ),
    "/blog/": ("Blog — dasturlash bo'yicha maqolalar", "Блог о программировании", "Programming blog"),
    "/projects/": ("Loyihalar va o'yinlar", "Проекты и игры", "Projects and games"),
}


def _lang_key(code):
    code = (code or "uz").split("-")[0]
    return code if code in UI else "en"


def site(request):
    lang = _lang_key(translation.get_language())
    meta = PAGE_META.get(request.path)
    idx = {"uz": 0, "ru": 1}.get(lang, 2)
    return {
        "ui": UI[lang],
        "ui_lang": lang,
        "site_url": SITE_URL,
        # canonical: query parametrlarsiz, faqat sahifani aniqlovchi ?id= saqlanadi
        "canonical_url": SITE_URL + request.path + (
            f"?id={request.GET['id']}" if request.GET.get("id") else ""
        ),
        "seo_description": meta[idx] if meta else PAGE_META["/"][idx],
        "available_languages": settings.LANGUAGES,
    }
