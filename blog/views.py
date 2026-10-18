import json
from urllib.parse import quote, urlsplit

from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import Categories, Posts
from blog.utils import UI, clean_html, excerpt, lang_key, pick, reading_minutes, split_for_ad
from comments.pages import normalize_page_url, page_comments
from core.context_processors import SITE_URL

PER_PAGE = 9
VIEW_DEDUP_SECONDS = 6 * 3600


def _card(post, lang):
    """Ro'yxat kartasi uchun maqolaning joriy tildagi qisqa ko'rinishi."""
    name, _ = pick(post, "name", lang)
    lead, _ = pick(post, "title", lang)
    body, _ = pick(post, "body", lang, min_len=50)
    cat_name = pick(post.categorie, "name", lang)[0] if post.categorie_id and post.categorie else ""
    return {
        "url": post.get_absolute_url(),
        "name": name,
        "lead": excerpt(lead, 180),
        "image": post.image.url if post.image else "",
        "date": post.publish_time,
        "minutes": reading_minutes(body),
        "views": post.view_count,
        "category": cat_name,
        "category_id": post.categorie_id,
    }


def _sidebar(lang):
    published = Posts.published()
    counts = dict(
        published.values("categorie_id").annotate(n=Count("id")).values_list("categorie_id", "n")
    )
    categories = [
        {"id": c.id, "name": pick(c, "name", lang)[0], "total": counts[c.id]}
        for c in Categories.objects.filter(id__in=counts.keys()).order_by("-sort_order", "id")
    ]
    latest = [_card(p, lang) for p in published.order_by("-publish_time")[:5]]
    popular = [_card(p, lang) for p in published.filter(view_count__gt=0).order_by("-view_count")[:5]]
    return {"categories": categories, "latest": latest, "popular": popular}


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (forwarded.split(",")[0] or request.META.get("REMOTE_ADDR", "")).strip()


def _base_context(request, lang):
    return {"t": UI[lang], "lang": lang, **_sidebar(lang)}


def index(request):
    # Eski manzillar: /blog/?id=<uuid> -> /blog/<slug>/ (Google va ulashilgan havolalar ishlashda davom etadi)
    old_id = request.GET.get("id")
    if old_id:
        try:
            post = Posts.published().filter(pk=old_id).first()
        except (ValueError, ValidationError):
            post = None
        if post is None:
            raise Http404("Maqola topilmadi")
        return redirect(getattr(request, "lang_prefix", "") + post.get_absolute_url(), permanent=True)

    lang = lang_key(translation.get_language())
    t = UI[lang]
    posts = Posts.published().order_by("-sort_order", "-publish_time")

    category = None
    categorie_id = request.GET.get("categorie_id", "")
    if categorie_id:
        if not categorie_id.isdigit():
            raise Http404()
        category = get_object_or_404(Categories, id=categorie_id)
        posts = posts.filter(categorie_id=category.id)

    q = request.GET.get("q", "").strip()[:100]
    if q:
        cond = Q()
        for field in ("name", "title", "body"):
            for sfx in ("uz_uz", "ru_ru", "en_us"):
                cond |= Q(**{f"{field}_{sfx}__icontains": q})
        posts = posts.filter(cond)

    paginator = Paginator(posts, PER_PAGE)
    page = paginator.get_page(request.GET.get("page"))
    context = _base_context(request, lang)
    category_name = pick(category, "name", lang)[0] if category else ""

    # Sahifalash havolalari joriy filtrlarni saqlashi kerak
    params = []
    if category:
        params.append(f"categorie_id={category.id}")
    if q:
        params.append(f"q={quote(q)}")
    query_prefix = "&".join(params)

    canonical = f"{SITE_URL}{getattr(request, 'lang_prefix', '')}/blog/"
    canonical_params = ([f"categorie_id={category.id}"] if category else []) + (
        [f"page={page.number}"] if page.number > 1 else []
    )
    if canonical_params:
        canonical += "?" + "&".join(canonical_params)

    title = f"{category_name} — {t['blog']}" if category else t["title"]
    if page.number > 1:
        title += f" ({page.number}-{t['page']})"

    context.update(
        {
            "page": page,
            "page_range": list(paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)),
            "ellipsis": Paginator.ELLIPSIS,
            "total": paginator.count,
            "cards": [_card(p, lang) for p in page.object_list],
            "category": category,
            "category_name": category_name,
            "q": q,
            "query_prefix": query_prefix,
            "page_title": title,
            "seo_title": f"{title} | Complex Programmer",
            "canonical_url": canonical,
            "seo_description": (
                f"{category_name}: " if category else ""
            ) + {"uz": "dasturlash, texnologiya, salomatlik va boshqa mavzulardagi maqolalar.",
                 "ru": "статьи о программировании, технологиях, здоровье и других темах.",
                 }.get(lang, "articles about programming, technology, health and more."),
            "noindex": bool(q),
            "comments": page_comments(request),
        }
    )
    return render(request, "blog/index.html", context)


def detail(request, slug):
    post = Posts.published().filter(slug=slug).first()
    if post is None:
        raise Http404("Maqola topilmadi")

    # Ko'rishlar soni: bir IP'dan 6 soatda bir marta sanaladi (sahifani yangilash hisobga olinmaydi)
    if cache.add(f"blogview:{_client_ip(request)}:{post.pk}", 1, VIEW_DEDUP_SECONDS):
        Posts.objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)
        post.view_count += 1

    lang = lang_key(translation.get_language())
    t = UI[lang]
    name, _ = pick(post, "name", lang)
    lead, _ = pick(post, "title", lang)
    body, is_native = pick(post, "body", lang, min_len=50)
    body = clean_html(body)
    body_top, body_rest = split_for_ad(body)

    published = Posts.published()
    newer = published.filter(publish_time__gt=post.publish_time).order_by("publish_time").first()
    older = published.filter(publish_time__lt=post.publish_time).order_by("-publish_time").first()
    related = list(
        published.filter(categorie_id=post.categorie_id).exclude(pk=post.pk).order_by("-publish_time")[:3]
    )
    if len(related) < 3:
        exclude = [post.pk] + [p.pk for p in related]
        related += list(published.exclude(pk__in=exclude).order_by("-view_count")[: 3 - len(related)])

    canonical = f"{SITE_URL}{getattr(request, 'lang_prefix', '')}{post.get_absolute_url()}"
    image = f"{SITE_URL}{post.image.url}" if post.image else f"{SITE_URL}/static/img/C0mplex.png"
    description = excerpt(lead or body, 160)
    # Admin'da qidiruv uchun alohida yozilgan sarlavha/tavsif (faqat o'zbekcha sahifada)
    seo_title = f"{name} — {t['blog']} | Complex Programmer"
    if lang == "uz" and post.seo_title:
        seo_title = post.seo_title
    if lang == "uz" and post.seo_description:
        description = post.seo_description
    category_name = pick(post.categorie, "name", lang)[0] if post.categorie else ""
    json_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": name[:110],
        "description": description,
        "image": [image],
        "datePublished": post.publish_time.isoformat(),
        "dateModified": post.updated_at.isoformat(),
        "mainEntityOfPage": canonical,
        "author": {"@type": "Organization", "name": "Complex Programmer", "url": SITE_URL},
        "publisher": {
            "@type": "Organization",
            "name": "Complex Programmer",
            "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/static/img/C0mplex.png"},
        },
    }
    if category_name:
        json_ld["articleSection"] = category_name

    # Izohlar eski manzil (/blog/?id=<uuid>) bo'yicha saqlangan — o'shanga bog'lab qo'yamiz
    comment_url = normalize_page_url(f"{SITE_URL}/blog/?id={post.pk}")

    context = _base_context(request, lang)
    context.update(
        {
            "post": post,
            "name": name,
            "lead": lead,
            "body_top": body_top,
            "body_rest": body_rest,
            "is_native": is_native,
            "minutes": reading_minutes(body),
            "category_name": category_name,
            "source_host": (urlsplit(post.source_url).hostname or "").removeprefix("www."),
            "newer": _card(newer, lang) if newer else None,
            "older": _card(older, lang) if older else None,
            "related": [_card(p, lang) for p in related],
            "page_title": f"{name} — {t['blog']}",
            "seo_title": seo_title,
            "canonical_url": canonical,
            "seo_description": description,
            "og_type": "article",
            "og_title": name,
            "og_image": image,
            "json_ld": json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c"),
            "comments": page_comments(request, page_url=comment_url),
            "comment_page_url": comment_url,
        }
    )
    return render(request, "blog/post.html", context)


class LatestPostsFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "Complex Programmer — Blog"
    link = "/blog/"
    description = "Complex Programmer blogidagi yangi maqolalar"

    def items(self):
        return Posts.published().order_by("-publish_time")[:20]

    def item_title(self, item):
        return item.name_uz_uz

    def item_description(self, item):
        return excerpt(item.title_uz_uz or item.body_uz_uz, 300)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publish_time

    def item_updateddate(self, item):
        return item.updated_at

    def item_categories(self, item):
        return [item.categorie.name_uz_uz] if item.categorie else []

    def item_enclosure_url(self, item):
        return f"{SITE_URL}{item.image.url}" if item.image else None

    item_enclosure_mime_type = "image/jpeg"
    item_enclosure_length = 0
