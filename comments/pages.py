"""Izoh qaysi sahifaga tegishli ekanini aniqlash.

Bir sahifa turli manzillar bilan ochilishi mumkin (``/ru/`` prefiksi, http/https,
``?page=2``, ``?utm_...``, ``?ysclid=...``). Izohlar hammasida bir xil ko'rinishi
uchun manzil bitta ko'rinishga keltiriladi.
"""

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django.conf import settings

# Sahifani aniqlaydigan (kontentni o'zgartiradigan) parametrlar — qolganlari tashlanadi
MEANINGFUL_PARAMS = ("id", "categorie_id", "type_id", "group_id", "book_id")
LANG_PREFIXES = {code.split("-")[0] for code, _ in settings.LANGUAGES}


def normalize_page_url(url):
    parts = urlsplit(url or "")
    path = parts.path or "/"
    segments = path.split("/")
    # "/ru/blog/" -> "/blog/"
    if len(segments) > 2 and segments[1] in LANG_PREFIXES:
        path = "/" + "/".join(segments[2:])
    query = urlencode(
        sorted((k, v) for k, v in parse_qsl(parts.query) if k in MEANINGFUL_PARAMS)
    )
    netloc = parts.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return urlunsplit(("https", netloc, path, query, ""))


def page_url_for(request):
    return normalize_page_url(request.build_absolute_uri())


def page_comments(request):
    """Joriy sahifaning yuqori darajadagi izohlari (javoblari bilan)."""
    from comments.models import Comment

    return (
        Comment.objects.filter(page_url=page_url_for(request), parent=None)
        .prefetch_related("replies", "replies__replies", "replies__replies__replies")
        .order_by("-created_at")
    )
