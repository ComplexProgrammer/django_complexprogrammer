from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_control

from blog.models import Posts as BlogPost
from core.context_processors import PAGE_META, SITE_URL, UI, _lang_key
from django.utils import translation
from news.models import Posts as NewsPost
from projects.models import AvtoTest, Project
from tests.models import Books

MAX_RESULTS = 20

# Qidiruvda ko'rinadigan vositalar: (url, UI kaliti, qo'shimcha kalit so'zlar)
TOOLS = [
    ("/avtotest/", "avtotest", "yhq imtihon bilet prava haydovchilik пдд экзамен driving"),
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
        idx = {"uz": 0, "ru": 1}.get(lang, 2)
        for url, key, keywords in TOOLS:
            title = ui.get(key, key)
            desc = PAGE_META.get(url, ("", "", ""))[idx]
            haystack = " ".join([title, desc, keywords] + [u.get(key, "") for u in UI.values()]).lower()
            if ql in haystack:
                results["tools"].append({"url": url, "title": title, "desc": desc})

        savol_field = {"ru": "savol_ru", "en": "savol_en"}.get(lang, "savol")
        for item in AvtoTest.objects.filter(
            Q(savol__icontains=q) | Q(savol_ru__icontains=q) | Q(savol_en__icontains=q)
        ).values("bilet", "raqam", "savol", savol_field)[:MAX_RESULTS]:
            results["avtotest"].append({
                "url": f"/avtotest/{item['bilet']}/",
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


STATIC_SITEMAP_PATHS = [
    ("/", "daily", "1.0"), ("/avtotest/", "weekly", "0.9"), ("/tests/", "weekly", "0.8"),
    ("/blog/", "daily", "0.8"), ("/news/", "daily", "0.7"), ("/projects/", "weekly", "0.7"),
    ("/translate/", "monthly", "0.7"), ("/changetext/", "monthly", "0.7"), ("/pdf_tools/", "monthly", "0.7"),
    ("/password_generator/", "monthly", "0.6"), ("/exchangerates/", "daily", "0.6"), ("/coins/", "daily", "0.5"),
    ("/ip/", "monthly", "0.5"), ("/imagecompare/", "monthly", "0.5"), ("/sitemap/", "monthly", "0.5"),
    ("/youtube_downloader/", "monthly", "0.4"), ("/snake/", "yearly", "0.3"), ("/tetris/", "yearly", "0.3"),
    ("/tictactoe/", "yearly", "0.3"), ("/pingpong/", "yearly", "0.3"), ("/terms/", "yearly", "0.1"),
    ("/privacy/", "yearly", "0.1"), ("/snake2/", "yearly", "0.3"), ("/car/", "yearly", "0.3"),
    ("/duckhunt/", "yearly", "0.3"), ("/motorcycle/", "yearly", "0.3"), ("/bubbleshooter/", "yearly", "0.3"),
    ("/markets/", "weekly", "0.4"), ("/arxiv/", "weekly", "0.4"), ("/cryptomarket/", "daily", "0.4"),
]


def sitemap_xml(request):
    """Avtomatik sitemap: yangi blog/yangilik/bilet qo'shilsa, o'zi paydo bo'ladi."""
    from xml.sax.saxutils import escape

    from django.db.models import Max

    base = SITE_URL
    rows = [(base + path, None, freq, prio) for path, freq, prio in STATIC_SITEMAP_PATHS]
    max_bilet = AvtoTest.objects.aggregate(Max("bilet"))["bilet__max"] or 0
    rows += [(f"{base}/avtotest/{i}/", None, "monthly", "0.6") for i in range(1, max_bilet + 1)]
    for post in BlogPost.published().values("slug", "updated_at"):
        rows.append((f"{base}/blog/{post['slug']}/", post["updated_at"], "monthly", "0.7"))
    for post in NewsPost.objects.filter(is_deleted=False).values("id", "updated_at"):
        rows.append((f"{base}/news/?id={post['id']}", post["updated_at"], "monthly", "0.5"))
    for book in Books.objects.filter(is_deleted=False).values("id", "updated_at"):
        rows.append((f"{base}/tests/?book_id={book['id']}", book["updated_at"], "monthly", "0.6"))
    for project in Project.actives.values("id", "updated_time"):
        rows.append((f"{base}/project/{project['id']}/", project["updated_time"], "monthly", "0.4"))

    items = []
    for loc, lastmod, freq, prio in rows:
        lm = f"<lastmod>{lastmod.date().isoformat()}</lastmod>" if lastmod else ""
        items.append(f"<url><loc>{escape(loc)}</loc>{lm}<changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(items) + "\n</urlset>\n"
    )
    return HttpResponse(xml, content_type="application/xml")


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
