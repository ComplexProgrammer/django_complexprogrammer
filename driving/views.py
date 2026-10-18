import json
import time
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import DatabaseError, connection, transaction
from django.db.models import F, Max, Sum
from django.core.cache import cache
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone, translation
from django.utils.html import strip_tags
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import Truncator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_POST

from comments.pages import page_comments
from core.context_processors import _lang_key
from core.seo import LABELS, SITE_URL, json_ld_dump, lang_url, meta_lang
from driving import telegram_auth, topics
from driving.models import ActivityDay, ExamResult, Progress, TelegramAccount
from driving.texts import texts
from projects.models import AvtoTest
from tests.models import RoadSignCategories, RoadSigns

EXAM_QUESTIONS = 20
EXAM_SECONDS = 25 * 60
EXAM_MAX_MISTAKES = 2
LETTERS = ("A", "B", "C", "D")
# Sinxronlash so'rovi chegaralari (suiiste'mol va katta yuklamadan himoya)
MAX_BODY = 256 * 1024
MAX_RESULTS = 500
MAX_MISTAKES = 3000
MAX_ANSWERED_PER_SYNC = 300
TOMBSTONE_TTL_MS = 90 * 24 * 3600 * 1000


def _lang(request):
    return _lang_key(translation.get_language())


def _sfx(lang):
    """AvtoTest maydonlari qo'shimchasi: savol / savol_ru / savol_en."""
    return {"uz": "", "ru": "_ru"}.get(lang, "_en")


def _pick(obj, field, sfx):
    return (getattr(obj, field + sfx, "") or getattr(obj, field, "") or "").strip()


def _field(lang):
    """RoadSigns va boshqa Translatable modellar maydon qo'shimchasi."""
    return {"uz": "uz_uz", "ru": "ru_ru"}.get(lang, "en_us")


def _url_lang(request):
    return getattr(request, "lang_prefix", "").strip("/") or "uz"


def _breadcrumbs(lang, url_lang, items):
    """``items`` — [(nomi, prefikssiz manzil), ...] (Bosh sahifa avtomatik qo'shiladi)."""
    crumbs = [("home", LABELS[meta_lang(lang)]["home"], "/")] + [(None, n, p) for n, p in items]
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": lang_url(path, url_lang)}
            for i, (_, name, path) in enumerate(crumbs, 1)
        ],
    }


def _seo(title, desc, graph, og_image=None):
    ctx = {"seo_title": title, "seo_description": desc, "seo_h1": "", "seo_text": [], "seo_faq": []}
    if graph:
        ctx["seo_json_ld"] = json_ld_dump(graph)
    if og_image:
        ctx["og_image"] = og_image
    return ctx


# ==================== SAVOL SAHIFASI ====================


def question(request, bilet, raqam):
    q = AvtoTest.objects.filter(bilet=bilet, raqam=raqam).first()
    if q is None:
        raise Http404
    lang = _lang(request)
    t = texts(lang)
    sfx = _sfx(lang)
    url_lang = _url_lang(request)

    text = _pick(q, "savol", sfx)
    answers = []
    for letter in LETTERS:
        value = _pick(q, "javob_" + letter.lower(), sfx)
        if value:
            answers.append({"letter": letter, "text": value, "right": letter == q.javob})
    right = next((a["text"] for a in answers if a["right"]), "")
    q_topics = [
        {"slug": slug, "name": topics.topic_name(slug, lang)}
        for slug, ids in topics.topic_map().items() if q.id in ids
    ]

    siblings = list(AvtoTest.objects.filter(bilet=bilet).order_by("raqam").values("raqam", "savol" + sfx, "savol"))
    for s in siblings:
        s["text"] = Truncator(s["savol" + sfx] or s["savol"]).chars(90)
    max_bilet = AvtoTest.objects.aggregate(Max("bilet"))["bilet__max"] or bilet
    numbers = [s["raqam"] for s in siblings]
    idx = numbers.index(raqam)
    prev_url = next_url = None
    if idx > 0:
        prev_url = f"/avtotest/{bilet}/{numbers[idx - 1]}/"
    elif bilet > 1:
        last = AvtoTest.objects.filter(bilet=bilet - 1).aggregate(Max("raqam"))["raqam__max"]
        if last:
            prev_url = f"/avtotest/{bilet - 1}/{last}/"
    if idx < len(numbers) - 1:
        next_url = f"/avtotest/{bilet}/{numbers[idx + 1]}/"
    elif bilet < max_bilet:
        next_url = f"/avtotest/{bilet + 1}/1/"

    path = f"/avtotest/{bilet}/{raqam}/"
    ticket_name = t["ticket_n"].format(n=bilet)
    question_name = t["question_n"].format(n=raqam)
    image = f"{SITE_URL}/static/avtotest/{q.rasm}" if q.rasm else None
    graph = [
        _breadcrumbs(lang, url_lang, [
            ("Avtotest", "/avtotest/"), (ticket_name, f"/avtotest/{bilet}/"), (question_name, path),
        ]),
        {
            "@type": "Quiz",
            "name": f"Avtotest — {ticket_name}, {question_name}",
            "inLanguage": meta_lang(lang),
            "educationalLevel": "beginner",
            "hasPart": [{
                "@type": "Question",
                "eduQuestionType": "Multiple choice",
                "text": text,
                **({"image": image} if image else {}),
                "suggestedAnswer": [
                    {"@type": "Answer", "position": i, "text": a["text"]}
                    for i, a in enumerate(answers) if not a["right"]
                ],
                "acceptedAnswer": {"@type": "Answer", "text": right},
            }],
        },
    ]
    title = t["q_title"].format(text=Truncator(text).chars(70), b=bilet, r=raqam)
    desc = Truncator(t["q_desc"].format(b=bilet, r=raqam, answer=right)).chars(160)
    context = {
        "t": t, "q": q, "text": text, "answers": answers, "bilet": bilet, "raqam": raqam,
        "siblings": siblings, "prev_url": prev_url, "next_url": next_url,
        "ticket_name": ticket_name, "question_name": question_name, "comments": page_comments(request), "topics": q_topics,
        **_seo(title, desc, graph, image),
    }
    return render(request, "driving/question.html", context)


# ==================== IMTIHON ====================


def exam(request):
    lang = _lang(request)
    t = texts(lang)
    sfx = _sfx(lang)
    rows = AvtoTest.objects.filter(javob__in=LETTERS).exclude(savol="")
    topic = request.GET.get("mavzu")
    topic_title = ""
    if topic in topics.TOPIC_BY_SLUG:  # mavzu bo'yicha mashq (canonical baribir /avtotest/imtihon/)
        rows = rows.filter(id__in=topics.topic_map()[topic])
        topic_title = t["practice_title"].format(name=topics.topic_name(topic, lang))
    rows = rows.order_by("?")[:EXAM_QUESTIONS]
    questions = []
    for q in rows:
        options = [
            {"l": letter, "t": _pick(q, "javob_" + letter.lower(), sfx)}
            for letter in LETTERS if _pick(q, "javob_" + letter.lower(), sfx)
        ]
        questions.append({
            "id": q.id, "bilet": q.bilet, "raqam": q.raqam, "q": _pick(q, "savol", sfx),
            "img": q.rasm, "o": options, "a": q.javob,
        })
    graph = [
        _breadcrumbs(lang, _url_lang(request), [("Avtotest", "/avtotest/"), (t["exam_h1"], "/avtotest/imtihon/")]),
        {
            "@type": "WebApplication", "name": t["exam_h1"], "description": t["exam_desc"],
            "url": lang_url("/avtotest/imtihon/", _url_lang(request)), "applicationCategory": "EducationalApplication",
            "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "UZS"},
        },
    ]
    context = {
        "t": t,
        "questions_json": json.dumps(questions, ensure_ascii=False).replace("<", "\\u003c"),
        "exam_seconds": EXAM_SECONDS, "max_mistakes": EXAM_MAX_MISTAKES, "total": len(questions),
        "topic_title": topic_title,
        **_seo(t["exam_title"], t["exam_desc"], graph),
    }
    return render(request, "driving/exam.html", context)


def _score(request):
    """``?c=19&t=20`` — tekshirilgan natija yoki ``None``."""
    c, t = _int(request.GET.get("c"), -1), _int(request.GET.get("t"), -1)
    return (c, t) if 0 < t <= 50 and 0 <= c <= t else None


def exam_share(request):
    """Ulashilgan natija sahifasi: preview'da natija rasmi, sahifada "siz ham sinab ko'ring" taklifi."""
    score = _score(request)
    if score is None:
        return redirect("/avtotest/imtihon/")
    lang = _lang(request)
    t = texts(lang)
    c, total = score
    passed = total - c <= EXAM_MAX_MISTAKES
    title = t["share_title"].format(c=c, t=total)
    context = {
        "t": t, "c": c, "total": total, "passed": passed,
        **_seo(title, t["exam_desc"], None, f"{SITE_URL}/avtotest/imtihon/natija.png?c={c}&t={total}&l={lang}"),
    }
    return render(request, "driving/exam_share.html", context)


@cache_control(public=True, max_age=7 * 24 * 3600)
def exam_card(request):
    from driving.cards import exam_card as draw_card

    score = _score(request)
    if score is None:
        raise Http404
    lang = request.GET.get("l") if request.GET.get("l") in ("uz", "ru", "en") else "uz"
    c, total = score
    key = f"exam_card:{c}:{total}:{lang}"
    png = cache.get(key)
    if png is None:
        png = draw_card(c, total, total - c <= EXAM_MAX_MISTAKES, lang)
        cache.set(key, png, 30 * 24 * 3600)
    return HttpResponse(png, content_type="image/png")


@require_POST
def api_exam(request):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False}, status=401)
    try:
        data = json.loads(request.body or b"{}")
        correct, total, seconds = int(data["correct"]), int(data["total"]), int(data.get("seconds", 0))
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"ok": False}, status=400)
    if not (0 < total <= 50 and 0 <= correct <= total and 0 <= seconds <= 4 * 3600):
        return JsonResponse({"ok": False}, status=400)
    today = timezone.localdate()
    if ExamResult.objects.filter(user=request.user, created_at__date=today).count() >= 50:
        return JsonResponse({"ok": False}, status=429)
    ExamResult.objects.create(
        user=request.user, correct=correct, total=total, seconds=seconds,
        passed=total - correct <= EXAM_MAX_MISTAKES,
    )
    return JsonResponse({"ok": True})


# ==================== NATIJALARNI SINXRONLASH ====================


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clean_results(raw):
    clean = {}
    if isinstance(raw, dict):
        for key, value in list(raw.items())[:MAX_RESULTS]:
            if str(key).isdigit() and isinstance(value, dict):
                clean[str(key)] = {
                    k: _int(value.get(k)) for k in ("correct", "wrong", "attempts", "best", "time", "date")
                }
    return clean


def _clean_mistakes(raw):
    clean = {}
    if isinstance(raw, dict):
        for key, value in list(raw.items())[:MAX_MISTAKES]:
            if str(key).isdigit():
                value = value if isinstance(value, dict) else {}
                clean[str(key)] = {"bilet": _int(value.get("bilet")), "t": _int(value.get("t"))}
    return clean


def merge_progress(progress, results, mistakes, removed, now_ms):
    """Brauzer holatini server nusxasi bilan birlashtirish (har bir yozuvda yangisi yutadi)."""
    merged_results = dict(progress.results or {})
    for key, value in results.items():
        if value["date"] >= merged_results.get(key, {}).get("date", -1):
            merged_results[key] = value

    tombstones = {k: v for k, v in (progress.removed or {}).items() if now_ms - v < TOMBSTONE_TTL_MS}
    for key in removed:
        tombstones[key] = now_ms

    merged_mistakes = dict(progress.mistakes or {})
    for key, value in mistakes.items():
        if value["t"] >= merged_mistakes.get(key, {}).get("t", -1):
            merged_mistakes[key] = value
    for key in list(merged_mistakes):
        if key in tombstones:
            if merged_mistakes[key]["t"] > tombstones[key]:
                del tombstones[key]  # o'chirilgandan keyin yana xato qilingan
            else:
                del merged_mistakes[key]

    progress.results = merged_results
    progress.mistakes = dict(list(merged_mistakes.items())[-MAX_MISTAKES:])
    progress.removed = tombstones
    return progress


def api_progress(request):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False}, status=401)
    if request.method == "GET":
        progress, _ = Progress.objects.get_or_create(user=request.user)
        return JsonResponse({"ok": True, "results": progress.results, "mistakes": progress.mistakes})
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)
    if len(request.body) > MAX_BODY:
        return JsonResponse({"ok": False}, status=413)
    try:
        data = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"ok": False}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({"ok": False}, status=400)

    removed = [str(k) for k in (data.get("removed") or [])[:MAX_MISTAKES] if str(k).isdigit()]
    answered = max(0, min(_int(data.get("answered")), MAX_ANSWERED_PER_SYNC))
    correct = max(0, min(_int(data.get("correct")), answered))
    with transaction.atomic():
        progress, _ = Progress.objects.select_for_update().get_or_create(user=request.user)
        merge_progress(
            progress, _clean_results(data.get("results")), _clean_mistakes(data.get("mistakes")),
            removed, int(time.time() * 1000),
        )
        progress.save()
        if answered:
            day, _ = ActivityDay.objects.get_or_create(user=request.user, date=timezone.localdate())
            ActivityDay.objects.filter(pk=day.pk).update(answered=F("answered") + answered, correct=F("correct") + correct)
    return JsonResponse({"ok": True, "results": progress.results, "mistakes": progress.mistakes})


# ==================== PROFIL VA REYTING ====================


def streak_for(user):
    days = set(ActivityDay.objects.filter(user=user, answered__gt=0).values_list("date", flat=True)[:400])
    day = timezone.localdate()
    if day not in days:
        day -= timedelta(days=1)  # bugun hali mashq qilmagan bo'lsa, kechagidan sanaymiz
    count = 0
    while day in days:
        count += 1
        day -= timedelta(days=1)
    return count


def profile(request):
    lang = _lang(request)
    t = texts(lang)
    context = {"t": t, **_seo(t["profile_title"], t["login_text"], None)}
    if request.user.is_authenticated:
        progress, _ = Progress.objects.get_or_create(user=request.user)
        results = progress.results or {}
        total_bilets = AvtoTest.objects.values("bilet").distinct().count() or 1
        passed = sum(1 for r in results.values() if r.get("wrong", 0) <= EXAM_MAX_MISTAKES)
        correct = sum(r.get("correct", 0) for r in results.values())
        answered = correct + sum(r.get("wrong", 0) for r in results.values())
        exams = list(request.user.exam_results.all()[:10])
        for e in exams:
            e.duration = f"{e.seconds // 60:02d}:{e.seconds % 60:02d}"
        readiness = passed / total_bilets
        if exams:
            recent = exams[:5]
            readiness = 0.6 * readiness + 0.4 * sum(e.correct / e.total for e in recent) / len(recent)
        weak = sorted(
            ((int(b), r) for b, r in results.items() if r.get("wrong", 0) > EXAM_MAX_MISTAKES),
            key=lambda item: -item[1].get("wrong", 0),
        )[:12]
        context.update({
            "account": getattr(request.user, "telegram", None),
            "solved": len(results), "total_bilets": total_bilets, "passed": passed,
            "accuracy": round(correct / answered * 100) if answered else None,
            "mistakes_count": len(progress.mistakes or {}), "streak": streak_for(request.user),
            "exams": exams, "exam_count": request.user.exam_results.count(),
            "exams_passed": request.user.exam_results.filter(passed=True).count(),
            "readiness": round(readiness * 100), "weak": weak,
        })
    else:
        context.update(_login_context(request, "/profil/"))
    return render(request, "driving/profile.html", context)


def leaderboard(request):
    lang = _lang(request)
    t = texts(lang)
    since = timezone.localdate() - timedelta(days=6)
    rows = list(
        ActivityDay.objects.filter(date__gte=since, user__telegram__isnull=False)
        .values("user_id")
        .annotate(correct_sum=Sum("correct"), answered_sum=Sum("answered"))
        .filter(answered_sum__gt=0)
        .order_by("-correct_sum", "-answered_sum")[:50]
    )
    names = {a.user_id: a for a in TelegramAccount.objects.filter(user_id__in=[r["user_id"] for r in rows])}
    for i, row in enumerate(rows, 1):
        row["place"] = i
        row["account"] = names.get(row["user_id"])
        row["me"] = request.user.is_authenticated and row["user_id"] == request.user.id
    graph = [_breadcrumbs(lang, _url_lang(request), [("Avtotest", "/avtotest/"), (t["lb_h1"], "/avtotest/reyting/")])]
    context = {"t": t, "rows": rows, **_seo(t["lb_title"], t["lb_desc"], graph)}
    if not request.user.is_authenticated:
        context.update(_login_context(request, "/avtotest/reyting/"))
    return render(request, "driving/leaderboard.html", context)


# ==================== TELEGRAM ORQALI KIRISH ====================


def _login_context(request, next_path):
    return {
        "tg_bot_username": settings.TELEGRAM_LOGIN_BOT_USERNAME if settings.TELEGRAM_LOGIN_BOT_TOKEN else "",
        "tg_auth_url": f"/auth/telegram/?next={next_path}",
    }


def _safe_next(request, default="/profil/"):
    target = request.GET.get("next") or default
    if url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return target
    return default


def telegram_login(request):
    data = telegram_auth.verify(request.GET.dict(), settings.TELEGRAM_LOGIN_BOT_TOKEN)
    if data is None:
        return redirect("/profil/?login=failed")
    _login_telegram(request, data)
    return redirect(_safe_next(request))


@require_POST
def telegram_webapp_login(request):
    """Bot ichida ochilgan sayt (Telegram Mini App) — foydalanuvchi tugma bosmasdan avtomatik kiradi."""
    try:
        init_data = json.loads(request.body or b"{}").get("init_data", "")
    except (ValueError, AttributeError):
        return JsonResponse({"ok": False}, status=400)
    data = telegram_auth.verify_webapp(init_data, settings.TELEGRAM_LOGIN_BOT_TOKEN)
    if data is None:
        return JsonResponse({"ok": False}, status=403)
    _login_telegram(request, data)
    return JsonResponse({"ok": True})


def _login_telegram(request, data):
    telegram_id = int(data["id"])
    fields = {
        "username": data.get("username", "")[:64],
        "first_name": data.get("first_name", "")[:128],
        "last_name": data.get("last_name", "")[:128],
        "photo_url": data.get("photo_url", "")[:500] if data.get("photo_url", "").startswith("https://") else "",
    }
    with transaction.atomic():
        account = TelegramAccount.objects.select_related("user").filter(telegram_id=telegram_id).first()
        if account is None:
            user, created = User.objects.get_or_create(username=f"tg{telegram_id}")
            if created:
                user.set_unusable_password()
            user.first_name = fields["first_name"][:150]
            user.save()
            account = TelegramAccount.objects.create(user=user, telegram_id=telegram_id, **fields)
        else:
            for key, value in fields.items():
                setattr(account, key, value)
            account.save()
    login(request, account.user, backend="django.contrib.auth.backends.ModelBackend")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("/avtotest/")


# ==================== YO'L BELGILARI ====================


def signs(request):
    lang = _lang(request)
    t = texts(lang)
    f = _field(lang)
    categories = []
    for cat in RoadSignCategories.objects.filter(is_deleted=False).order_by("sort_order"):
        items = [
            {"id": s.id, "number": s.number, "name": getattr(s, "name_" + f) or s.name_uz_uz, "image": s.image}
            for s in cat.signs.filter(is_deleted=False)
        ]
        categories.append({"code": cat.code, "name": getattr(cat, "name_" + f) or cat.name_uz_uz, "signs": items})
    total = sum(len(c["signs"]) for c in categories)
    graph = [_breadcrumbs(lang, _url_lang(request), [(t["signs_h1"], "/yol-belgilari/")])]
    context = {"t": t, "categories": categories, "total": total, **_seo(t["signs_title"], t["signs_desc"], graph)}
    if not total:
        context["noindex"] = True  # bo'sh sahifa qidiruvga chiqmasin
        context["hreflang_links"] = []
    return render(request, "driving/signs.html", context)


def sign(request, pk):
    s = get_object_or_404(RoadSigns.objects.select_related("category"), pk=pk, is_deleted=False)
    lang = _lang(request)
    t = texts(lang)
    f = _field(lang)
    name = getattr(s, "name_" + f) or s.name_uz_uz
    description = getattr(s, "description_" + f) or s.description_uz_uz
    category = getattr(s.category, "name_" + f) or s.category.name_uz_uz
    others = [
        {"id": o.id, "number": o.number, "name": getattr(o, "name_" + f) or o.name_uz_uz, "image": o.image}
        for o in s.category.signs.filter(is_deleted=False).exclude(pk=s.pk)[:24]
    ]
    image = f"{SITE_URL}{s.image.url}" if s.image else None
    graph = [_breadcrumbs(lang, _url_lang(request), [
        (t["signs_h1"], "/yol-belgilari/"), (f"{s.number} {name}".strip(), f"/yol-belgilari/{s.pk}/"),
    ])]
    title = t["sign_title"].format(num=s.number, name=name).strip()
    desc = Truncator(t["sign_desc"].format(num=s.number, name=name, text=strip_tags(description))).chars(160)
    context = {
        "t": t, "sign": s, "name": name, "description": description, "category": category, "others": others,
        **_seo(title, desc, graph, image),
    }
    return render(request, "driving/sign.html", context)


# ==================== MAVZULAR ====================


def topics_index(request):
    lang = _lang(request)
    t = texts(lang)
    mapping = topics.topic_map()
    items = [
        {"slug": slug, "name": topics.topic_name(slug, lang), "count": len(mapping[slug])}
        for slug, _, _ in topics.TOPICS if mapping[slug]
    ]
    graph = [_breadcrumbs(lang, _url_lang(request), [("Avtotest", "/avtotest/"), (t["topics_h1"], "/avtotest/mavzular/")])]
    context = {"t": t, "items": items, **_seo(t["topics_title"], t["topics_desc"], graph)}
    return render(request, "driving/topics.html", context)


def topic(request, slug):
    if slug not in topics.TOPIC_BY_SLUG:
        raise Http404
    lang = _lang(request)
    t = texts(lang)
    sfx = _sfx(lang)
    ids = topics.topic_map()[slug]
    name = topics.topic_name(slug, lang)
    questions = [
        {"bilet": q["bilet"], "raqam": q["raqam"], "text": Truncator(q["savol" + sfx] or q["savol"]).chars(140)}
        for q in AvtoTest.objects.filter(id__in=ids).order_by("bilet", "raqam").values("bilet", "raqam", "savol", "savol" + sfx)
    ]
    others = [{"slug": s, "name": topics.topic_name(s, lang)} for s, _, _ in topics.TOPICS if s != slug]
    path = f"/avtotest/mavzu/{slug}/"
    url_lang = _url_lang(request)
    graph = [
        _breadcrumbs(lang, url_lang, [("Avtotest", "/avtotest/"), (t["topics"], "/avtotest/mavzular/"), (name, path)]),
        {
            "@type": "ItemList", "name": name, "numberOfItems": len(questions),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "url": lang_url(f"/avtotest/{q['bilet']}/{q['raqam']}/", url_lang)}
                for i, q in enumerate(questions[:100], 1)
            ],
        },
    ]
    title = t["topic_title"].format(name=name, year=timezone.localdate().year)
    desc = t["topic_desc"].format(name=name, n=len(questions))
    context = {
        "t": t, "slug": slug, "name": name, "questions": questions, "others": others,
        "h1": t["topic_h1"].format(name=name), "count": t["topic_count"].format(n=len(questions)),
        **_seo(title, desc, graph),
    }
    return render(request, "driving/topic.html", context)


# ==================== KUN SAVOLI ====================


def _channel_posted_ids(limit=30):
    """Bot kanalga joylagan savollar (yangilari birinchi). Jadvalni bot yaratadi — hali bo'lmasa bo'sh."""
    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT avtotest_id FROM avtotest_bot_channel_posts WHERE avtotest_id IS NOT NULL "
                "ORDER BY posted_at DESC LIMIT %s",
                [limit],
            )
            return [row[0] for row in cur.fetchall()]
    except DatabaseError:
        return []


def daily_question(request):
    lang = _lang(request)
    t = texts(lang)
    sfx = _sfx(lang)
    ids = list(dict.fromkeys(_channel_posted_ids()))
    if not ids:  # bot hali joylamagan bo'lsa — kun bo'yi bir xil tasodifiy savol
        pool = list(AvtoTest.objects.filter(javob__in=LETTERS).order_by("id").values_list("id", flat=True))
        ids = [pool[timezone.localdate().toordinal() % len(pool)]] if pool else []
    by_id = {q.id: q for q in AvtoTest.objects.filter(id__in=ids)}
    items = [by_id[i] for i in ids if i in by_id]
    today = items[0] if items else None
    archive = [
        {"bilet": q.bilet, "raqam": q.raqam, "text": Truncator(_pick(q, "savol", sfx)).chars(120)}
        for q in items[1:]
    ]
    context = {"t": t, "today": today, "archive": archive, **_seo(t["daily_title"], t["daily_desc"], [
        _breadcrumbs(lang, _url_lang(request), [("Avtotest", "/avtotest/"), (t["daily_h1"], "/avtotest/kun-savoli/")]),
    ])}
    if today:
        context.update({
            "today_text": _pick(today, "savol", sfx),
            "today_answers": [
                {"letter": letter, "text": _pick(today, "javob_" + letter.lower(), sfx)}
                for letter in LETTERS if _pick(today, "javob_" + letter.lower(), sfx)
            ],
        })
    return render(request, "driving/daily.html", context)
