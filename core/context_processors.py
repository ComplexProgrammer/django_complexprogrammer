"""Barcha shablonlarga umumiy ma'lumot: UI matnlari (4 tilda), SEO meta, canonical va hreflang.

Sahifalar SEO matnlari — ``core/seo_pages.py``da.
"""

from django.conf import settings
from django.utils import translation

from core import seo

SITE_URL = seo.SITE_URL

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
        "menu": "Menyu", "exam": "Imtihon", "signs": "Yo'l belgilari", "profile": "Profil",
        "leaderboard": "Reyting", "exam_desc": "20 savol, 25 daqiqa — haqiqiy imtihon kabi",
        "hero_title": "Avtotest 2026 — haydovchilik imtihoniga bepul tayyorlaning",
        "hero_lead": "YHXBB biletlari, imtihon simulyatori, xatolar ustida ishlash va yo'l belgilari. Natijalaringiz Telegram orqali saqlanadi.",
        "hero_tickets": "Biletlarni yechish",
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
        "menu": "Меню", "exam": "Экзамен", "signs": "Дорожные знаки", "profile": "Профиль",
        "leaderboard": "Рейтинг", "exam_desc": "20 вопросов, 25 минут — как на настоящем экзамене",
        "hero_title": "Автотест 2026 — бесплатная подготовка к экзамену на права",
        "hero_lead": "Билеты ГУБДД, симулятор экзамена, работа над ошибками и дорожные знаки. Результаты сохраняются через Telegram.",
        "hero_tickets": "Решать билеты",
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
        "menu": "Menu", "exam": "Exam", "signs": "Road signs", "profile": "Profile",
        "leaderboard": "Leaderboard", "exam_desc": "20 questions, 25 minutes — just like the real exam",
        "hero_title": "Driving test 2026 — prepare for the licence exam for free",
        "hero_lead": "Official exam tickets, an exam simulator, mistake review and road signs. Your progress is saved via Telegram.",
        "hero_tickets": "Solve tickets",
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
        "menu": "Menü", "exam": "Sınav", "signs": "Trafik işaretleri", "profile": "Profil",
        "leaderboard": "Sıralama", "exam_desc": "20 soru, 25 dakika — gerçek sınav gibi",
        "hero_title": "Ehliyet testi 2026 — sınava ücretsiz hazırlanın",
        "hero_lead": "Sınav biletleri, sınav simülatörü, hata çalışması ve trafik işaretleri. İlerlemeniz Telegram ile kaydedilir.",
        "hero_tickets": "Biletleri çöz",
    },
}

def _lang_key(code):
    code = (code or "uz").split("-")[0]
    return code if code in UI else "en"


def site(request):
    lang = _lang_key(translation.get_language())
    path = request.path_info  # /ru/ prefiksisiz
    prefix = getattr(request, "lang_prefix", "")
    url_lang = prefix.strip("/") or seo.DEFAULT_LANG
    query = seo.canonical_query(request.GET)
    canonical = SITE_URL + prefix + path + query
    meta = seo.page_meta(path, lang) or {}
    noindex = path in seo.NOINDEX_PATHS
    return {
        "ui": UI[lang],
        "ui_lang": lang,
        "site_url": SITE_URL,
        # canonical: query parametrlarsiz, faqat sahifani aniqlovchi (?id=, ?book_id=) saqlanadi
        "canonical_url": canonical,
        "seo_title": meta.get("title", ""),
        "seo_description": meta.get("desc") or seo.page_meta("/", lang)["desc"],
        "seo_h1": meta.get("h1", ""),
        "seo_lead": meta.get("lead", ""),
        "seo_text": meta.get("text", []),
        "seo_faq": meta.get("faq", []),
        "seo_labels": seo.LABELS[seo.meta_lang(lang)],
        "seo_json_ld": seo.json_ld(lang, meta, canonical, url_lang) if meta and not noindex else "",
        "hreflang_links": [] if noindex else seo.alternates(path + query),
        "og_locale": seo.OG_LOCALES.get(lang, "uz_UZ"),
        "noindex": noindex,
        "lang_prefix": prefix,
        "available_languages": settings.LANGUAGES,
    }
