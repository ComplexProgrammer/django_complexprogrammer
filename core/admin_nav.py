"""Unfold admin: yon menyu, belgilar (badge) va muhit yorlig'i (settings.UNFOLD dan çaqiriladi).

Har bir band faqat foydalanuvçida tegişli ``view_*`` ruxsati bölsa körinadi.
Ikonkalar: https://fonts.google.com/icons (Material Symbols).
"""
from django.conf import settings
from django.urls import NoReverseMatch, reverse

# (bölim, ikonka, [(nomi, ikonka, "app.model" yoki URL, badge callback)])
MENU = (
    ("Avtotest", None, (
        ("Savollar", "quiz", "tests.questions", "core.admin_nav.draft_explanations_badge"),
        ("Biletlar / mavzular", "view_list", "tests.topics", None),
        ("Javoblar", "checklist", "tests.answers", None),
        ("Kitoblar", "menu_book", "tests.books", None),
        ("Guruhlar", "folder", "tests.groups", None),
        ("Test turlari", "category", "tests.types", None),
        ("Kitob turlari", "library_books", "tests.booktypes", None),
        ("Yöl belgilari", "traffic", "tests.roadsigns", None),
        ("Belgi kategoriyalari", "signpost", "tests.roadsigncategories", None),
        ("AvtoTest (faqat köriş)", "visibility", "projects.avtotest", None),
    )),
    ("Kontent", None, (
        ("Blog maqolalari", "article", "blog.posts", None),
        ("Blog kategoriyalari", "sell", "blog.categories", None),
        ("Yangiliklar", "newspaper", "news.posts", None),
        ("Izohlar", "forum", "comments.comment", "core.admin_nav.pending_comments_badge"),
        ("Loyihalar", "rocket_launch", "projects.project", None),
    )),
    ("Foydalanuvçilar", None, (
        ("Foydalanuvçilar", "person", "auth.user", None),
        ("Guruhlar va ruxsatlar", "admin_panel_settings", "auth.group", None),
        ("Telegram akkauntlar", "send", "driving.telegramaccount", None),
        ("Imtihon natijalari", "workspace_premium", "driving.examresult", None),
        ("Kunlik faollik", "monitoring", "driving.activityday", None),
        ("Progress", "trending_up", "driving.progress", None),
    )),
    ("Dökon", None, (
        ("Mahsulotlar", "inventory_2", "markets.product", None),
        ("Variantlar", "style", "markets.productvariant", None),
        ("Variant rasmlari", "image", "markets.productvariantimage", None),
        ("Kategoriyalar", "sell", "markets.category", None),
        ("Marketlar", "storefront", "markets.market", None),
        ("Dökonlar", "store", "markets.store", None),
    )),
    ("Arxiv", None, (
        ("Hujjatlar", "description", "arxiv.archiveitem", None),
        ("Xonalar", "meeting_room", "arxiv.room", None),
        ("Şkaflar", "shelves", "arxiv.cabinet", None),
        ("Hujjat turlari", "label", "arxiv.archivetype", None),
        ("Holatlar", "flag", "arxiv.archivestatus", None),
    )),
    ("Tizim", None, (
        ("Turlar (core)", "tune", "core.type", None),
        ("Rasmlar (core)", "photo_library", "core.image", None),
        ("PDF fayllar", "picture_as_pdf", "pdf_tools.file", None),
    )),
)


def _changelist(model):
    app, name = model.split(".")
    try:
        return reverse(f"admin:{app}_{name}_changelist")
    except NoReverseMatch:  # model admin'da röyxatdan ötmagan
        return None


def sidebar(request):
    user = request.user
    groups = [{
        "title": "Asosiy",
        "items": [
            {"title": "Dashboard", "icon": "dashboard", "link": reverse("admin:index")},
            {"title": "Saytni oçiş", "icon": "open_in_new", "link": "/", "active": False},
        ],
    }]
    for title, _, items in MENU:
        links = []
        for name, icon, model, badge in items:
            link = _changelist(model)
            app, model_name = model.split(".")
            if link and user.has_perm(f"{app}.view_{model_name}"):
                item = {"title": name, "icon": icon, "link": link}
                if badge:
                    item["badge"] = badge
                links.append(item)
        if links:
            groups.append({"title": title, "collapsible": True, "items": links})
    return groups


def _badge(count):
    return str(count) if count else None


def pending_comments_badge(request):
    from comments.models import Comment

    return _badge(Comment.objects.filter(status=Comment.Status.PENDING).count())


def draft_explanations_badge(request):
    from tests.models import Questions

    return _badge(Questions.objects.filter(is_deleted=False, explanation_status="draft").count())


def environment(request):
    """Sarlavhadagi yorliq: lokal nusxada işlayotganingizni darhol köriş uçun."""
    return ["Lokal (DEBUG)", "warning"] if settings.DEBUG else ["Server", "success"]
