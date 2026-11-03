"""Admin bosh sahifasi (dashboard) uçun ma'lumotlar — ``UNFOLD["DASHBOARD_CALLBACK"]``.

Şablon: ``templates/admin/index.html``. Har bir körsatkiç alohida hisoblanadi: bitta ilova (masalan, driving)
yöq yoki xato bersa ham dashboard oçilaveradi.
"""
import json
import logging
from datetime import timedelta

from django.db.models import Count, Q, Sum
from django.urls import reverse
from django.utils import timezone

from projects.avtotest_sync import SYNCED_BOOK_IDS

log = logging.getLogger(__name__)
DAYS = 14


def _safe(fn, default=None):
    try:
        return fn()
    except Exception:  # dashboard hech qaçon 500 bermasin
        log.exception("Dashboard körsatkiçi hisoblanmadi: %s", fn.__name__)
        return default


def _url(name, query=""):
    return reverse(f"admin:{name}") + (f"?{query}" if query else "")


def _avtotest():
    from tests.models import Questions

    qs = Questions.objects.filter(is_deleted=False, topic__book_id__in=SYNCED_BOOK_IDS, topic__is_deleted=False)
    stats = qs.aggregate(
        total=Count("id"),
        draft=Count("id", filter=Q(explanation_status="draft")),
        approved=Count("id", filter=Q(explanation_status="approved")),
    )
    return stats


def _comments():
    from comments.models import Comment

    return Comment.objects.aggregate(
        pending=Count("id", filter=Q(status=Comment.Status.PENDING)),
        week=Count("id", filter=Q(created_at__gte=timezone.now() - timedelta(days=7))),
    )


def _blog():
    from blog.models import Posts

    now = timezone.now()
    return Posts.objects.filter(is_deleted=False).aggregate(
        published=Count("id", filter=Q(publish_time__lte=now)),
        scheduled=Count("id", filter=Q(publish_time__gt=now)),
        views=Sum("view_count"),
    )


def _users():
    from django.contrib.auth.models import User

    week = timezone.now() - timedelta(days=7)
    return {"total": User.objects.count(), "week": User.objects.filter(date_joined__gte=week).count()}


def _activity():
    from driving.models import ActivityDay, ExamResult

    today = timezone.localdate()
    start = today - timedelta(days=DAYS - 1)
    per_day = dict(
        ActivityDay.objects.filter(date__gte=start).values_list("date").annotate(n=Sum("answered")).values_list("date", "n")
    )
    exams = ExamResult.objects.filter(created_at__date__gte=start)
    exams_per_day = dict(exams.values_list("created_at__date").annotate(n=Count("id")).values_list("created_at__date", "n"))
    days = [start + timedelta(days=i) for i in range(DAYS)]
    today_exams = exams.filter(created_at__date=today).aggregate(n=Count("id"), passed=Count("id", filter=Q(passed=True)))
    chart = {
        "labels": [d.strftime("%d.%m") for d in days],
        "datasets": [
            {"label": "Javob berilgan savollar", "data": [per_day.get(d, 0) for d in days],
             "backgroundColor": "#4f46e5", "borderRadius": 4},
            {"label": "Imtihonlar", "data": [exams_per_day.get(d, 0) for d in days],
             "backgroundColor": "#a5b4fc", "borderRadius": 4},
        ],
    }
    return {
        "today_answered": per_day.get(today, 0),
        "today_exams": today_exams["n"],
        "today_passed": today_exams["passed"],
        "chart": json.dumps(chart),
    }


def dashboard_callback(request, context):
    avtotest = _safe(_avtotest, {})
    comments = _safe(_comments, {})
    blog = _safe(_blog, {})
    users = _safe(_users, {})
    activity = _safe(_activity, {})

    kpis = [
        {"title": "Avtotest savollari", "value": avtotest.get("total", "—"), "icon": "quiz",
         "note": f"{avtotest.get('approved', 0)} tasida tasdiqlangan izoh bor",
         "link": _url("tests_questions_changelist", "book__id__in=" + ",".join(map(str, SYNCED_BOOK_IDS)))},
        {"title": "Tekşiriş kutayotgan izohlar", "value": avtotest.get("draft", "—"), "icon": "rate_review",
         "note": "AI qoralamalari — tasdiqlang yoki tuzating", "alert": bool(avtotest.get("draft")),
         "link": _url("tests_questions_changelist", "explanation_status__exact=draft")},
        {"title": "Moderatsiyadagi izohlar", "value": comments.get("pending", "—"), "icon": "forum",
         "note": f"Söngi 7 kunda {comments.get('week', 0)} ta yangi izoh", "alert": bool(comments.get("pending")),
         "link": _url("comments_comment_changelist", "status__exact=pending")},
        {"title": "Blog maqolalari", "value": blog.get("published", "—"), "icon": "article",
         "note": f"{blog.get('scheduled', 0)} ta rejalaştirilgan · {blog.get('views') or 0:,} köriş".replace(",", " "),
         "link": _url("blog_posts_changelist")},
        {"title": "Foydalanuvçilar", "value": users.get("total", "—"), "icon": "group",
         "note": f"Söngi 7 kunda +{users.get('week', 0)}", "link": _url("auth_user_changelist")},
        {"title": "Bugungi faollik", "value": activity.get("today_answered", "—"), "icon": "bolt",
         "note": f"javob · {activity.get('today_exams', 0)} imtihon ({activity.get('today_passed', 0)} tasi ötdi)",
         "link": _url("driving_activityday_changelist")},
    ]
    quick = [
        {"title": "Yangi savol", "icon": "add_circle", "link": _url("tests_questions_add")},
        {"title": "Yangi blog maqola", "icon": "edit_note", "link": _url("blog_posts_add")},
        {"title": "Izohlarni moderatsiya qiliş", "icon": "fact_check",
         "link": _url("comments_comment_changelist", "status__exact=pending")},
        {"title": "/avtotest/ sahifasi", "icon": "directions_car", "link": "/avtotest/", "external": True},
        {"title": "/tests/ sahifasi", "icon": "school", "link": "/tests/", "external": True},
        {"title": "Bosh sahifa", "icon": "home", "link": "/", "external": True},
    ]
    context.update({"kpis": kpis, "quick_links": quick, "activity_chart": activity.get("chart"), "chart_days": DAYS})
    return context
