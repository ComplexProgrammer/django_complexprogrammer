"""Barcha shablonlarga umumiy ma'lumot: UI matnlari (4 tilda), SEO meta va canonical URL."""

from django.conf import settings
from django.utils import translation

SITE_URL = "https://complexprogrammer.uz"

UI = {
    "uz": {
        "markets": "Bozorlar", "archive": "Arxiv", "popular_tools": "Mashhur vositalar",
        "all_tools": "Barcha loyihalar", "translate": "Tarjimon", "password": "Parol generatori",
        "pdf": "PDF konvertor", "rates": "Valyuta kurslari", "latin": "Lotin ↔ Kirill",
        "ip": "IP manzil", "imagecompare": "Rasm solishtirish", "sitemap": "Sitemap generator",
        "coins": "Kripto narxlar", "youtube": "YouTube yuklovchi",
        "blog_desc": "Maqolalar va darsliklar", "projects_desc": "Onlayn vositalar va o'yinlar",
        "markets_desc": "Do'konlar va mahsulotlar", "tests_desc": "Mavzular bo'yicha testlar",
        "avtotest_desc": "YHQ imtihon biletlari", "archive_desc": "Hujjatlar arxivi",
        "home": "Bosh sahifa", "blog": "Blog", "projects": "Loyihalar", "tests": "Testlar",
        "avtotest": "Avtotest", "news": "Yangiliklar", "search": "Qidiruv",
        "search_placeholder": "Sayt bo'yicha qidirish...", "theme": "Mavzu", "language": "Til",
        "menu": "Menyu",
    },
    "ru": {
        "markets": "Маркеты", "archive": "Архив", "popular_tools": "Популярные инструменты",
        "all_tools": "Все проекты", "translate": "Переводчик", "password": "Генератор паролей",
        "pdf": "PDF конвертер", "rates": "Курсы валют", "latin": "Латиница ↔ Кириллица",
        "ip": "IP адрес", "imagecompare": "Сравнение картинок", "sitemap": "Генератор sitemap",
        "coins": "Курсы криптовалют", "youtube": "Загрузчик YouTube",
        "blog_desc": "Статьи и уроки", "projects_desc": "Онлайн-инструменты и игры",
        "markets_desc": "Магазины и товары", "tests_desc": "Тесты по темам",
        "avtotest_desc": "Экзаменационные билеты ПДД", "archive_desc": "Архив документов",
        "home": "Главная", "blog": "Блог", "projects": "Проекты", "tests": "Тесты",
        "avtotest": "Автотест", "news": "Новости", "search": "Поиск",
        "search_placeholder": "Поиск по сайту...", "theme": "Тема", "language": "Язык",
        "menu": "Меню",
    },
    "en": {
        "markets": "Markets", "archive": "Archive", "popular_tools": "Popular tools",
        "all_tools": "All projects", "translate": "Translator", "password": "Password generator",
        "pdf": "PDF converter", "rates": "Exchange rates", "latin": "Latin ↔ Cyrillic",
        "ip": "IP lookup", "imagecompare": "Image compare", "sitemap": "Sitemap generator",
        "coins": "Crypto prices", "youtube": "YouTube downloader",
        "blog_desc": "Articles and tutorials", "projects_desc": "Online tools and games",
        "markets_desc": "Stores and products", "tests_desc": "Tests by topic",
        "avtotest_desc": "Driving exam tickets", "archive_desc": "Document archive",
        "home": "Home", "blog": "Blog", "projects": "Projects", "tests": "Tests",
        "avtotest": "Driving test", "news": "News", "search": "Search",
        "search_placeholder": "Search the site...", "theme": "Theme", "language": "Language",
        "menu": "Menu",
    },
    "tr": {
        "markets": "Pazarlar", "archive": "Arşiv", "popular_tools": "Popüler araçlar",
        "all_tools": "Tüm projeler", "translate": "Çevirmen", "password": "Şifre oluşturucu",
        "pdf": "PDF dönüştürücü", "rates": "Döviz kurları", "latin": "Latin ↔ Kiril",
        "ip": "IP sorgulama", "imagecompare": "Resim karşılaştırma", "sitemap": "Sitemap oluşturucu",
        "coins": "Kripto fiyatları", "youtube": "YouTube indirici",
        "blog_desc": "Makaleler ve dersler", "projects_desc": "Çevrimiçi araçlar ve oyunlar",
        "markets_desc": "Mağazalar ve ürünler", "tests_desc": "Konulara göre testler",
        "avtotest_desc": "Ehliyet sınav biletleri", "archive_desc": "Belge arşivi",
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
