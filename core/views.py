from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_control

from blog.models import Posts as BlogPost
from core.context_processors import SITE_URL, UI, _lang_key, news_active
from core.seo import SEO_LANGS, alternates, lang_url, page_meta
from django.utils import translation
from news.models import Posts as NewsPost
from projects.models import AvtoTest, Project
from tests.models import Books, RoadSigns
from tests.views import DUPLICATE_BOOKS

MAX_RESULTS = 20

# Qidiruvda ko'rinadigan vositalar: (url, UI kaliti, qo'shimcha kalit so'zlar)
TOOLS = [
    ("/avtotest/", "avtotest", "yhq imtihon bilet prava haydovchilik пдд экзамен driving"),
    ("/avtotest/imtihon/", "exam", "imtihon simulyator sinov экзамен симулятор exam simulator"),
    ("/yol-belgilari/", "signs", "yo'l belgilari belgi знаки дорожные road signs"),
    ("/avtotest/reyting/", "leaderboard", "reyting top рейтинг leaderboard"),
    ("/tests/", "tests", "test savol maktab тест"),
    ("/translate/", "translate", "tarjima перевод translate"),
    ("/changetext/", "latin", "lotin kirill krill латиница кириллица"),
    ("/pdf_tools/", "pdf", "pdf word excel docx rasm"),
    ("/password_generator/", "password", "parol пароль password"),
    ("/exchangerates/", "rates", "valyuta kurs dollar rubl курс валют"),
    ("/coins/", "coins", "kripto bitcoin btc крипто"),
    ("/ip/", "ip", "ip manzil адрес"),
    ("/imagecompare/", "imagecompare", "rasm solishtirish картинка сравнение"),
    ("/sitemap/", "sitemap", "sitemap xml sayt xaritasi карта сайта"),
    ("/youtube_downloader/", "youtube", "youtube video yuklab скачать"),
    ("/blog/", "blog", "maqola статья"),
    ("/news/", "news", "yangilik новости"),
    ("/projects/", "projects", "o'yin игры games snake tetris"),
]


def _title_field(lang):
    return {"ru": "title_ru_ru", "en": "title_en_us"}.get(lang, "title_uz_uz")


def search(request):
    q = (request.GET.get("q") or "").strip()[:100]
    lang = _lang_key(translation.get_language())
    ui = UI[lang]
    results = {"tools": [], "avtotest": [], "blog": [], "news": [], "projects": []}

    if len(q) >= 2:
        ql = q.lower()
        for url, key, keywords in TOOLS:
            title = ui.get(key, key)
            desc = (page_meta(url, lang) or {}).get("desc", "") or ui.get(key + "_desc", "")
            haystack = " ".join([title, desc, keywords] + [u.get(key, "") for u in UI.values()]).lower()
            if ql in haystack:
                results["tools"].append({"url": url, "title": title, "desc": desc})

        savol_field = {"ru": "savol_ru", "en": "savol_en"}.get(lang, "savol")
        for item in AvtoTest.objects.filter(
            Q(savol__icontains=q) | Q(savol_ru__icontains=q) | Q(savol_en__icontains=q)
        ).values("bilet", "raqam", "savol", savol_field)[:MAX_RESULTS]:
            results["avtotest"].append({
                "url": f"/avtotest/{item['bilet']}/{item['raqam']}/",
                "title": strip_tags(item[savol_field] or item["savol"])[:160],
                "desc": f"{item['bilet']}-bilet, {item['raqam']}-savol",
            })

        tf = _title_field(lang)
        title_q = Q(title_uz_uz__icontains=q) | Q(title_ru_ru__icontains=q) | Q(title_en_us__icontains=q) | Q(title_uz_crl__icontains=q)
        nf = tf.replace("title_", "name_")
        name_q = Q(name_uz_uz__icontains=q) | Q(name_ru_ru__icontains=q) | Q(name_en_us__icontains=q)
        for post in BlogPost.published().filter(title_q | name_q).values("slug", nf, "name_uz_uz", tf, "title_uz_uz")[:MAX_RESULTS]:
            results["blog"].append({
                "url": f"/blog/{post['slug']}/",
                "title": post[nf] or post["name_uz_uz"],
                "desc": strip_tags(post[tf] or post["title_uz_uz"])[:160],
            })
        for post in NewsPost.objects.filter(title_q, is_deleted=False).values("id", tf, "title_uz_uz")[:MAX_RESULTS]:
            results["news"].append({"url": f"/news/?id={post['id']}", "title": post[tf] or post["title_uz_uz"], "desc": ""})

        for p in Project.actives.filter(Q(title__icontains=q) | Q(sub_title__icontains=q) | Q(category__icontains=q))[:MAX_RESULTS]:
            results["projects"].append({"url": p.url or f"/project/{p.id}/", "title": p.title, "desc": p.sub_title})

    sections = [
        (ui["popular_tools"] if key == "tools" else ui.get(key, key), items)
        for key, items in results.items()
        if items
    ]
    context = {"q": q, "sections": sections, "total": sum(len(v) for v in results.values())}
    return render(request, "search.html", context)


@cache_control(max_age=0, no_cache=True)
def service_worker(request):
    """/sw.js — butun saytni boshqara olishi uchun ildizdan beriladi."""
    with open(settings.BASE_DIR / "static" / "sw.js", "rb") as fh:
        return HttpResponse(fh.read(), content_type="application/javascript")


def offline(request):
    return render(request, "offline.html")


# Sitemap'dagi doimiy sahifalar bo'limlar bo'yicha: (bo'lim nomi, [(manzil, changefreq, priority), ...])
STATIC_SITEMAP_SECTIONS = [
    ("Asosiy sahifalar", [
        ("/", "daily", "1.0"), ("/avtotest/", "weekly", "0.9"), ("/avtotest/imtihon/", "weekly", "0.9"),
        ("/avtotest/reyting/", "daily", "0.5"), ("/avtotest/kun-savoli/", "daily", "0.7"), ("/tests/", "weekly", "0.8"),
        ("/blog/", "daily", "0.8"), ("/projects/", "weekly", "0.7"),
    ]),
    ("Onlayn vositalar", [
        ("/translate/", "monthly", "0.7"), ("/changetext/", "monthly", "0.7"), ("/pdf_tools/", "monthly", "0.7"),
        ("/password_generator/", "monthly", "0.6"), ("/exchangerates/", "daily", "0.6"), ("/coins/", "daily", "0.5"),
        ("/ip/", "monthly", "0.5"), ("/imagecompare/", "monthly", "0.5"), ("/sitemap/", "monthly", "0.5"),
        ("/youtube_downloader/", "monthly", "0.4"),
    ]),
    ("Boshqa bo'limlar", [
        ("/markets/", "weekly", "0.4"), ("/arxiv/", "weekly", "0.4"), ("/cryptomarket/", "daily", "0.4"),
    ]),
    ("O'yinlar", [
        ("/snake/", "yearly", "0.3"), ("/snake2/", "yearly", "0.3"), ("/tetris/", "yearly", "0.3"),
        ("/tictactoe/", "yearly", "0.3"), ("/pingpong/", "yearly", "0.3"), ("/car/", "yearly", "0.3"),
        ("/duckhunt/", "yearly", "0.3"), ("/motorcycle/", "yearly", "0.3"), ("/bubbleshooter/", "yearly", "0.3"),
    ]),
    ("Huquqiy sahifalar", [
        ("/terms/", "yearly", "0.1"), ("/privacy/", "yearly", "0.1"),
    ]),
]


def build_sitemap():
    """Sitemap XML matni: yangi blog/yangilik/bilet qo'shilsa, o'zi paydo bo'ladi.

    Har bir sahifa barcha til versiyalari (uz — prefikssiz, /ru/, /en/) bilan, hreflang havolalari bilan beriladi.
    ``/sitemap.xml`` va ``manage.py write_sitemap`` (static/sitemap.xml) shu funksiyadan foydalanadi.
    """
    from xml.sax.saxutils import escape

    from django.db.models import Max

    # Bo'limlar: (sarlavha, [(manzil, lastmod, changefreq, priority), ...])
    sections = [
        (title, [(path, None, freq, prio) for path, freq, prio in paths])
        for title, paths in STATIC_SITEMAP_SECTIONS
    ]
    max_bilet = AvtoTest.objects.aggregate(Max("bilet"))["bilet__max"] or 0
    sections.append(("Avtotest biletlari", [
        (f"/avtotest/{i}/", None, "monthly", "0.6") for i in range(1, max_bilet + 1)
    ]))
    from driving.topics import TOPICS

    sections.append(("Avtotest mavzulari", [("/avtotest/mavzular/", None, "weekly", "0.8")] + [
        (f"/avtotest/mavzu/{slug}/", None, "weekly", "0.7") for slug, _, _ in TOPICS
    ]))
    sections.append(("Avtotest savollari", [
        (f"/avtotest/{q['bilet']}/{q['raqam']}/", None, "monthly", "0.5")
        for q in AvtoTest.objects.order_by("bilet", "raqam").values("bilet", "raqam")
    ]))
    # Yo'l belgilari bo'limi belgilar qo'shilgandan keyingina indekslanadi (bo'sh sahifa — noindex)
    signs = list(RoadSigns.objects.filter(is_deleted=False).order_by("category__sort_order", "sort_order").values("id", "updated_at"))
    sections.append(("Yo'l belgilari", ([("/yol-belgilari/", None, "monthly", "0.8")] if signs else []) + [
        (f"/yol-belgilari/{s['id']}/", s["updated_at"], "monthly", "0.6") for s in signs
    ]))
    sections.append(("Testlar (kitoblar bo'yicha)", [
        (f"/tests/?book_id={b['id']}", b["updated_at"], "monthly", "0.6")
        for b in Books.objects.filter(is_deleted=False, questions__is_deleted=False)  # savolsiz (bo'sh) kitoblar sitemap'ga kirmaydi
        .exclude(id__in=DUPLICATE_BOOKS).distinct().order_by("id").values("id", "updated_at")
    ]))
    sections.append(("Blog maqolalari", [
        (f"/blog/{p['slug']}/", p["updated_at"], "monthly", "0.7")
        for p in BlogPost.published().order_by("-publish_time").values("slug", "updated_at")
    ]))
    if news_active():  # eskirgan bo'lim noindex — sitemap'ga ham kirmaydi
        sections.append(("Yangiliklar", [("/news/", None, "daily", "0.7")] + [
            (f"/news/{p['slug']}/", p["updated_at"], "monthly", "0.5")
            for p in NewsPost.objects.filter(is_deleted=False).order_by("-publish_time").values("slug", "updated_at")
        ]))
    sections.append(("Loyihalar", [
        (f"/project/{p['id']}/", p["updated_time"], "monthly", "0.4")
        for p in Project.actives.order_by("id").values("id", "updated_time")
    ]))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!-- complexprogrammer.uz sitemap — avtomatik yaratiladi (core/views.py: build_sitemap). Qo'lda tahrirlamang:",
        "     static/sitemap.xml nusxasi `python manage.py write_sitemap` bilan yangilanadi.",
        "     Har bir sahifa 3 tilda: uz (prefikssiz), /ru/, /en/ — hreflang havolalari bilan. -->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for title, rows in sections:
        if not rows:
            continue
        lines += ["", f"  <!-- {title} ({len(rows)} ta sahifa × {len(SEO_LANGS)} til) -->"]
        for path, lastmod, freq, prio in rows:
            links = [
                f'    <xhtml:link rel="alternate" hreflang="{code}" href="{escape(href)}"/>'
                for code, href in alternates(path)
            ]
            for lang in SEO_LANGS:
                lines.append("  <url>")
                lines.append(f"    <loc>{escape(lang_url(path, lang))}</loc>")
                if lastmod:
                    lines.append(f"    <lastmod>{lastmod.date().isoformat()}</lastmod>")
                lines.append(f"    <changefreq>{freq}</changefreq>")
                lines.append(f"    <priority>{prio}</priority>")
                lines += links
                lines.append("  </url>")
    lines += ["", "</urlset>", ""]
    return "\n".join(lines)


def sitemap_xml(request):
    return HttpResponse(build_sitemap(), content_type="application/xml")


def indexnow_key(request, key):
    from django.http import Http404

    if key != settings.INDEXNOW_KEY:
        raise Http404
    return HttpResponse(key, content_type="text/plain")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /send_file/",
        "Disallow: /remove_file/",
        "Disallow: /search/",
        "Disallow: /media/downloads/",
        "",
        f"Sitemap: {SITE_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
