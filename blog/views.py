from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render
from django.db.models import Count
from django.db.models import F
from blog.models import Categories, Posts
from django.core.paginator import Paginator
from comments.pages import page_comments


def index(request):
    id = request.GET.get("id", 0)
    categorie_id = request.GET.get("categorie_id", 0)
    post = []
    categorie = []
    if categorie_id == 0:
        posts = Posts.objects.filter(is_deleted=False).values()
    else:
        categorie = Categories.objects.filter(id=categorie_id).values().first()
        posts = Posts.objects.filter(categorie_id=categorie_id, is_deleted=False).values()
    categories = (
        Posts.objects.filter(is_deleted=False)
        .values(
            "categorie__id",
            "categorie__name_en_us",
            "categorie__name_ru_ru",
            "categorie__name_uz_crl",
            "categorie__name_uz_uz",
            "categorie__sort_order",
        )
        .annotate(
            id=F("categorie__id"),
            name_en_us=F("categorie__name_en_us"),
            name_ru_ru=F("categorie__name_ru_ru"),
            name_uz_crl=F("categorie__name_uz_crl"),
            name_uz_uz=F("categorie__name_uz_uz"),
            sort_order=F("categorie__sort_order"),
            total=Count("categorie__id"),
        )
        .values(
            "id",
            "name_en_us",
            "name_ru_ru",
            "name_uz_crl",
            "name_uz_uz",
            "sort_order",
            "total",
        )
    )
    if id != 0:
        try:
            post = Posts.objects.filter(id=id, is_deleted=False).values().first()
        except (ValueError, ValidationError):
            post = None
        if post is None:
            raise Http404("Maqola topilmadi")
        categorie_id = post["categorie_id"]
        categorie = Categories.objects.filter(id=categorie_id).values().first()
    paginator = Paginator(posts, 3)  # Har sahifada 10 ta post ko'rsatish
    page_number = request.GET.get("page")  # URL dan sahifa raqamini olish
    posts = paginator.get_page(
        page_number
    )  # Sahifani olish    # Get comments for the current page
    comments = page_comments(request)

    context = {
        "id": id,
        "post": post,
        "posts": posts,
        "categorie": categorie,
        "categories": categories.order_by("-sort_order"),
        "comments": comments,
    }
    if post:
        # SEO: maqola sahifasi uchun o'z tavsifi (Google va Telegram preview'da ko'rinadi)
        context["seo_description"] = post.get("title_uz_uz") or post.get("title_en_us")
    return render(request, "blog/index.html", context=context)
