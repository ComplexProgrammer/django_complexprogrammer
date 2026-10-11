from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import translation
from comments.pages import normalize_page_url, page_comments
from core.context_processors import SITE_URL
from news.models import Posts


def index(request):
    # Eski manzillar: /news/?id=<uuid> -> /news/<slug>/ (Google va ulashilgan havolalar ishlashda davom etadi)
    old_id = request.GET.get("id")
    if old_id:
        try:
            post = Posts.objects.filter(id=old_id, is_deleted=False).first()
        except (ValueError, ValidationError):
            post = None
        if post is None:
            raise Http404("Yangilik topilmadi")
        return redirect(getattr(request, "lang_prefix", "") + post.get_absolute_url(), permanent=True)

    context = {
        "id": 0,
        "news": Posts.objects.filter(is_deleted=False).values(),
        "comments": page_comments(request),
    }
    return render(request, "news/index.html", context=context)


def detail(request, slug):
    news = Posts.objects.filter(slug=slug, is_deleted=False).first()
    if news is None:
        raise Http404("Yangilik topilmadi")

    lang = (translation.get_language() or "uz")[:2]
    suffix = {"ru": "ru_ru", "en": "en_us", "tr": "en_us"}.get(lang, "uz_uz")
    title = getattr(news, f"title_{suffix}", "") or news.title_uz_uz
    # Izohlar eski manzil (/news/?id=<uuid>) bo'yicha saqlangan — o'shanga bog'lab qo'yamiz
    comment_url = normalize_page_url(f"{SITE_URL}/news/?id={news.pk}")
    context = {
        "id": news.pk,
        "news": news,
        "comments": page_comments(request, page_url=comment_url),
        "comment_page_url": comment_url,
        "seo_title": f"{title} | Complex Programmer",
        "seo_description": title,
        "og_type": "article",
        "og_title": title,
    }
    if news.image:
        context["og_image"] = SITE_URL + news.image.url
    return render(request, "news/index.html", context=context)
