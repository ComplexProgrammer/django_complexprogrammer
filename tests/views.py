import datetime
import json
from django.shortcuts import render
from django.utils import timezone, translation
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models.functions import Concat
from django.db.models import Count, F, Q
from tests.models import (
    Answers,
    Books,
    Groups,
    Questions,
    Topics,
    Types,
    RoadSignCategories,
    RoadSigns,
    EXPLANATION_FIELDS,
)
from comments.pages import page_comments
from core.seo import SITE_URL, alternates, json_ld_dump, lang_url

# /tests/ dagi kitob -> xuddi şu savollar asosiy joylaşgan sahifa.
# Kitob 49 = /avtotest/ ning 1–108-biletlari, kitob 50 (e-avtomaktab) = 109-bilet va keyingilari.
# Ikkalasi ham yagona manba: tahrir şu yerda (Tests → Questions), projects.AvtoTest undan avtomatik hosil qilinadi (projects/avtotest_sync.py).
DUPLICATE_BOOKS = {49: "/avtotest/"}


# Search Console (2026-11): "e avtomaktab" sörovlari ~9 700 körsatiş, /tests/?book_id=50 — 6-örin, CTR 0,1%.
# Sahifada faqat bilet plitkalari bor edi; tuşuntiriş matni va FAQ (FAQPage JSON-LD bilan) qöşiladi.
# Halollik: bu e-avtomaktab.uz platformasining rasmiy sayti emas — matnda aniq aytiladi.
BOOK_SEO = {
    50: {
        "uz": {
            "lead": "e-avtomaktab test savollari: 31 bilet, 305 savol töğri javoblari bilan. Onlayn, bepul va röyxatdan ötmasdan maşq qiling.",
            "text": [
                ("Bu qanday testlar?", "Bu yerda e-avtomaktab biletlari böyiça tuzilgan 305 ta savol jamlangan: 31 ta bilet, savollarning yarmiga yaqini rasmli. Har bir javobdan keyin töğri variant darhol körsatiladi, xatolaringiz saqlanadi va ularni alohida qayta işlaş mumkin."),
                ("e-avtomaktab.uz bilan farqi nima?", "complexprogrammer.uz — e-avtomaktab.uz platformasining rasmiy sayti emas. Masofaviy ta'lim, röyxatdan ötiş va platformadagi testlar uçun e-avtomaktab.uz saytidan foydalaning. Bu sahifa — bepul qöşimça maşq: savollarni xohlagança takrorlaş uçun."),
                ("Qanday tayyorlaniş kerak?", "Kuniga 2–3 bilet yeçing, hafta oxirida xatolaringizni takrorlang. Tayyor bölgaç, 20 savollik imtihon simulyatorida (25 daqiqa, köpi bilan 2 xato) özingizni sinab köring."),
            ],
            "faq": [
                ("e-avtomaktab testlari bepulmi?", "Ha, bu sahifadagi barça biletlar bepul va röyxatdan ötmasdan işlaydi."),
                ("e-avtomaktab'da neçta savol bor?", "Bu yerda 31 ta biletda 305 ta savol bor. Asosiy Avto test töplamida yana 1080 ta savol (108 bilet) mavjud."),
                ("Savollar qaysi tillarda?", "Özbek (lotin va kirill), rus va ingliz tillarida — sayt tilini almaştirsangiz, savollar ham şu tilda çiqadi."),
                ("Bu e-avtomaktab.uz rasmiy saytimi?", "Yöq. Bu mustaqil maşq sahifasi. e-avtomaktab platformasining öz sayti — e-avtomaktab.uz."),
            ],
        },
        "ru": {
            "lead": "Вопросы теста e-avtomaktab: 31 билет, 305 вопросов с правильными ответами. Тренируйтесь онлайн бесплатно и без регистрации.",
            "text": [
                ("Что это за тесты?", "Здесь собраны 305 вопросов по билетам e-avtomaktab: 31 билет, почти половина вопросов с картинками. После каждого ответа сразу показывается правильный вариант, ошибки сохраняются, и их можно повторить отдельно."),
                ("Чем отличается от e-avtomaktab.uz?", "complexprogrammer.uz — не официальный сайт платформы e-avtomaktab.uz. Для дистанционного обучения, регистрации и тестов платформы используйте сайт e-avtomaktab.uz. Эта страница — бесплатная дополнительная тренировка: повторяйте вопросы сколько угодно."),
                ("Как готовиться?", "Решайте 2–3 билета в день, в конце недели повторяйте ошибки. Когда будете готовы, проверьте себя в симуляторе экзамена: 20 вопросов, 25 минут, не больше 2 ошибок."),
            ],
            "faq": [
                ("Тесты e-avtomaktab бесплатные?", "Да, все билеты на этой странице бесплатны и работают без регистрации."),
                ("Сколько вопросов в e-avtomaktab?", "Здесь 305 вопросов в 31 билете. В основном сборнике «Автотест» есть ещё 1080 вопросов (108 билетов)."),
                ("На каких языках вопросы?", "На узбекском (латиница и кириллица), русском и английском — при смене языка сайта вопросы тоже меняются."),
                ("Это официальный сайт e-avtomaktab.uz?", "Нет. Это независимая страница для тренировки. Сайт самой платформы — e-avtomaktab.uz."),
            ],
        },
        "en": {
            "lead": "e-avtomaktab test questions: 31 tickets, 305 questions with correct answers. Practise online for free, no sign-up.",
            "text": [
                ("What are these tests?", "305 questions organised by e-avtomaktab ticket: 31 tickets, nearly half with pictures. The correct option is shown after each answer, and your mistakes are saved for review."),
                ("How is this different from e-avtomaktab.uz?", "complexprogrammer.uz is not the official site of the e-avtomaktab.uz platform. For distance learning, registration and the platform's own tests, use e-avtomaktab.uz. This page is free extra practice."),
                ("How should I prepare?", "Do 2–3 tickets a day and review your mistakes at the end of the week. When ready, try the 20-question exam simulator (25 minutes, at most 2 mistakes)."),
            ],
            "faq": [
                ("Are the e-avtomaktab tests free?", "Yes, every ticket on this page is free and needs no sign-up."),
                ("How many questions does e-avtomaktab have?", "There are 305 questions in 31 tickets here. The main Driving test collection has another 1,080 questions (108 tickets)."),
                ("Which languages are available?", "Uzbek (Latin and Cyrillic), Russian and English — switch the site language and the questions follow."),
                ("Is this the official e-avtomaktab.uz site?", "No. This is an independent practice page. The platform's own site is e-avtomaktab.uz."),
            ],
        },
    },
}


def _book_seo(request, context, book_id, lang):
    """BOOK_SEO dagi kitob uçun: lead, matn, FAQ va mos JSON-LD (BreadcrumbList + FAQPage)."""
    data = BOOK_SEO.get(book_id)
    if not data:
        return
    page = data.get(lang) or data["uz"]
    url_lang = getattr(request, "lang_prefix", "").strip("/") or "uz"
    crumbs = context.get("crumbs") or []
    items = [
        {"@type": "ListItem", "position": i, "name": name,
         "item": lang_url(url or f"/tests/?book_id={book_id}", url_lang)}
        for i, (name, url) in enumerate(crumbs, 1)
    ]
    graph = [{"@type": "BreadcrumbList", "itemListElement": items}] if items else []
    graph.append({
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]],
    })
    context.update(level_lead=page["lead"], seo_text=page["text"], seo_faq=page["faq"], seo_json_ld=json_ld_dump(graph))


def _count(path):
    """Savollar soni bilet → kitob zanjiri orqali (savoldagi type_id/group_id/book_id maktab testlarida izçil emas)."""
    prefix = f"{path}__" if path else ""
    return Count(f"{prefix}questions", distinct=True, filter=Q(**{f"{prefix}questions__is_deleted": False}))


def _name(obj, lang):
    if not obj:
        return ""
    return obj.get({"ru": "name_ru_ru", "en": "name_en_us"}.get(lang, "name_uz_uz")) or obj.get("name_uz_uz") or ""


def _crumbs(level, obj, lang):
    """Non yöli: [(nomi, manzil), ...] — Testlar › tur › guruh › kitob › bilet (oxirgisi — joriy sahifa, manzilsiz)."""
    if not obj or level == "type":
        return []
    chain = []
    if level == "question":
        chain.append((_name(obj, lang), None))
        obj, level = _book(obj.get("book_id")), "topic"
    if level == "topic" and obj:
        chain.append((_name(obj, lang), None if not chain else f"/tests/?book_id={obj['id']}"))
        obj, level = Groups.objects.filter(id=obj.get("group_id")).values().first(), "book"
    if level == "book" and obj:
        chain.append((_name(obj, lang), None if not chain else f"/tests/?group_id={obj['id']}"))
        obj, level = Types.objects.filter(id=obj.get("type_id")).values().first(), "group"
    if level == "group" and obj:
        chain.append((_name(obj, lang), None if not chain else f"/tests/?type_id={obj['id']}"))
    lang_word = {"ru": "Тесты", "en": "Tests"}.get(lang, "Testlar")
    return [(lang_word, "/tests/")] + list(reversed(chain))


def _book(book_id):
    return (
        Books.objects.filter(id=book_id)
        .annotate(
            name_en_us=F("book_type__name_en_us"), name_ru_ru=F("book_type__name_ru_ru"),
            name_uz_crl=F("book_type__name_uz_crl"), name_uz_uz=F("book_type__name_uz_uz"), image=F("book_type__image"),
        )
        .values()
        .first()
    )


def tests(request):
    data = []
    _type = "type"
    comments = page_comments(request)
    type_data = []
    type_id = request.GET.get("type_id", 0)
    group_id = request.GET.get("group_id", 0)
    book_id = request.GET.get("book_id", 0)
    topic_id = request.GET.get("topic_id", 0)
    question_id = request.GET.get("question_id", 0)
    if (
        type_id == 0
        and group_id == 0
        and book_id == 0
        and topic_id == 0
        and question_id == 0
    ):
        data = (
            Types.objects.filter(is_deleted=False)
            .annotate(n=_count("groups__books__topics"))
            .filter(n__gt=0)
            .order_by("sort_order")
            .values()
        )
    else:
        if type_id != 0:
            _type = "group"
            type_data = (
                Types.objects.filter(is_deleted=False, id=type_id).values().first()
            )
            data = (
                Groups.objects.filter(is_deleted=False, type_id=type_id)
                .annotate(n=_count("books__topics"))
                .filter(n__gt=0)  # savolsiz guruh/kitob/bilet — foydalanuvçini böş sahifaga olib bormasin
                .order_by("sort_order")
                .values()
            )
        if group_id != 0:
            _type = "book"
            type_data = (
                Groups.objects.filter(is_deleted=False, id=group_id).values().first()
            )
            data = (
                Books.objects.filter(is_deleted=False, group_id=group_id)
                .annotate(n=_count("topics"), topics_n=Count("topics", distinct=True, filter=Q(topics__is_deleted=False)))
                .filter(n__gt=0)
                .order_by("sort_order")
            )
            data = data.annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            ).values()
        if book_id != 0:
            _type = "topic"
            type_data = (
                Books.objects.filter(is_deleted=False, id=book_id)
                .annotate(
                    name_en_us=F("book_type__name_en_us"),
                    name_ru_ru=F("book_type__name_ru_ru"),
                    name_uz_crl=F("book_type__name_uz_crl"),
                    name_uz_uz=F("book_type__name_uz_uz"),
                    image=F("book_type__image"),
                )
                .values()
                .first()
            )
            data = (
                Topics.objects.filter(is_deleted=False, book_id=book_id)
                .annotate(n=_count(""))
                .filter(n__gt=0)
                .order_by("sort_order")
                .values()
            )
        if topic_id != 0:
            _type = "question"
            type_data = (
                Topics.objects.filter(is_deleted=False, id=topic_id).values().first()
            )
            data = (
                Questions.objects.filter(is_deleted=False, topic_id=topic_id)
                .order_by("sort_order")
                .values()
            )
        if question_id != 0:
            _type = "answer"
            type_data = (
                Questions.objects.filter(is_deleted=False, id=question_id)
                .values()
                .first()
            )
            data = (
                Answers.objects.filter(is_deleted=False, question_id=question_id)
                .order_by("sort_order")
                .values()
            )  # type: ignore

    lang = (translation.get_language() or "uz")[:2]
    context = {
        "data": data,
        "type": _type,
        "crumbs": _crumbs(_type, type_data if isinstance(type_data, dict) else None, lang),
        "level_name": _name(type_data, lang) if isinstance(type_data, dict) else "",
        "type_data": json.dumps(type_data, default=serialize_datetime),
        "type_obj": type_data or {},
        "comments": comments,
    }
    # Guruh sahifasi (?group_id=): brauzer tabi va ulaşişda guruh nomi körinsin.
    # Canonical /tests/ da qoladi (guruh sahifasi faqat kitoblar röyxati).
    if group_id and str(group_id).isdigit() and not book_id and isinstance(type_data, dict) and type_data:
        lang = (translation.get_language() or "uz")[:2]
        field = {"ru": "name_ru_ru", "en": "name_en_us"}.get(lang, "name_uz_uz")
        name = type_data.get(field) or type_data.get("name_uz_uz") or ""
        if name:
            context["seo_title"] = {
                "ru": f"{name} — онлайн-тесты",
                "en": f"{name} — online tests",
            }.get(lang, f"{name} — onlayn testlar")
    # Bilet (savollar) sahifasi: brauzer tabida «e-avtomaktab · 1-bilet» körinsin — bir neça tab oçilganda adaşmaslik uçun
    if topic_id and str(topic_id).isdigit() and _type == "question" and isinstance(type_data, dict) and type_data:
        book_name = _name(_book(type_data.get("book_id")), lang)
        topic_name = _name(type_data, lang)
        suffix = {"ru": "вопросы теста", "en": "test questions"}.get(lang, "test savollari")
        context["seo_title"] = " · ".join(x for x in (book_name, topic_name) if x) + f" — {suffix}"
    # Har bir kitob sahifasi qidiruvda öz sarlavhasi bilan çiqsin (sitemap'da ?book_id= bilan)
    if book_id and str(book_id).isdigit():
        book = Books.objects.filter(id=book_id, is_deleted=False).select_related("book_type").first()
        if book and book.book_type:
            lang = (translation.get_language() or "uz")[:2]
            field = {"ru": "name_ru_ru", "en": "name_en_us"}.get(lang, "name_uz_uz")
            name = getattr(book.book_type, field, "") or book.book_type.name_uz_uz
            # Search Console: "e avtomaktab test savollari" kabi so'rovlar — sarlavhada "savollari va javoblari" bölsin
            year = timezone.localdate().year
            context["seo_title"] = {
                "ru": f"{name} — вопросы и ответы теста {year}, онлайн",
                "en": f"{name} — test questions and answers {year}, online",
            }.get(lang, f"{name} test savollari va javoblari {year} — onlayn")
            questions = book.questions.filter(is_deleted=False).count()
            context["seo_description"] = {
                "ru": f"{name}: {questions} вопросов с правильными ответами. Решайте тест онлайн бесплатно, без регистрации.",
                "en": f"{name}: {questions} questions with correct answers. Take the test online for free, no sign-up.",
            }.get(lang, f"{name}: {questions} ta savol va töğri javoblari. Testni onlayn, bepul va röyxatdan ötmasdan yeçing.")
        if book is None or not book.questions.filter(is_deleted=False).exists():
            context["noindex"] = True  # öçirilgan yoki savolsiz kitob — böş sahifa qidiruvga çiqmasin
            context["hreflang_links"] = []
        if book and not context.get("noindex"):
            _book_seo(request, context, int(book_id), lang)
        # Bir xil savollar /avtotest/ da ham bor — qidiruvda raqobatlashmasligi uchun asosiysiga canonical
        main_path = DUPLICATE_BOOKS.get(int(book_id))
        if main_path:
            prefix = getattr(request, "lang_prefix", "")
            context["canonical_url"] = SITE_URL + prefix + main_path
            context["hreflang_links"] = alternates(main_path)
    return render(request, "tests/index.html", context=context)


def hide_draft_explanations(rows):
    """AI qoralamasi (explanation_status="draft") admin tasdiqlamaguncha foydalanuvçiga körsatilmaydi."""
    for row in rows:
        if row.pop("explanation_status", "") == "draft":
            for field in EXPLANATION_FIELDS:
                if field in row:
                    row[field] = ""
        row.pop("explanation_confidence", None)
    return rows


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def GetTypes(request):
    data = Types.objects.filter(is_deleted=False).order_by("sort_order").values()
    return JsonResponse(list(data), safe=False)


def GetGroups(request):
    type_id = request.GET.get("type_id", False)
    if type_id is False:
        data = Groups.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        if type_id == "1":
            type_id = 3
        data = (
            Groups.objects.filter(is_deleted=False, type_id=type_id)
            .order_by("sort_order")
            .values()
        )
    return JsonResponse(list(data), safe=False)


def GetBooks(request):
    type_id = request.GET.get("type_id", False)
    group_id = request.GET.get("group_id", False)
    if type_id is False:
        data = (
            Books.objects.filter(is_deleted=False)
            .order_by("sort_order")
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .values()
        )
    else:
        data = (
            Books.objects.filter(is_deleted=False, type_id=type_id)
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .order_by("sort_order")
            .values()
        )
    if group_id is False:
        data = (
            Books.objects.filter(is_deleted=False)
            .order_by("sort_order")
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .values()
        )
    else:
        data = (
            Books.objects.filter(is_deleted=False, group_id=group_id)
            .order_by("sort_order")
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .values()
        )
    return JsonResponse(list(data), safe=False)


def GetTopics(request):
    type_id = request.GET.get("type_id", False)
    group_id = request.GET.get("group_id", False)
    book_id = request.GET.get("book_id", False)
    if type_id is False:
        data = Topics.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = Topics.objects.filter(is_deleted=False, type_id=type_id).values()
    if group_id is False:
        data = Topics.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = (
            Topics.objects.filter(is_deleted=False, group_id=group_id)
            .order_by("sort_order")
            .values()
        )
    if book_id is False:
        data = Topics.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = (
            Topics.objects.filter(is_deleted=False, book_id=book_id)
            .order_by("sort_order")
            .values()
        )
    return JsonResponse(list(data), safe=False)


def GetQuestions(request):
    type_id = request.GET.get("type_id", False)
    group_id = request.GET.get("group_id", False)
    book_id = request.GET.get("book_id", False)
    topic_id = request.GET.get("topic_id", False)
    if type_id is False:
        data = (
            Questions.objects.filter(is_deleted=False).order_by("sort_order").values()
        )
    else:
        data = Questions.objects.filter(is_deleted=False, type_id=type_id).values()
    if group_id is False:
        data = (
            Questions.objects.filter(is_deleted=False).order_by("sort_order").values()
        )
    else:
        data = (
            Questions.objects.filter(is_deleted=False, group_id=group_id)
            .order_by("sort_order")
            .values()
        )
    if book_id is False:
        data = (
            Questions.objects.filter(is_deleted=False).order_by("sort_order").values()
        )
    else:
        data = (
            Questions.objects.filter(is_deleted=False, book_id=book_id)
            .order_by("sort_order")
            .values()
        )
    if topic_id is False:
        data = (
            Questions.objects.filter(is_deleted=False).order_by("sort_order").values()
        )
    else:
        data = (
            Questions.objects.filter(is_deleted=False, topic_id=topic_id)
            .order_by("sort_order")
            .values()
        )
    data = hide_draft_explanations(list(data))
    # ?with_answers=1 — har savolga javoblari ham qo'shiladi (sahifa har savol uchun alohida so'rov yubormasin)
    if request.GET.get("with_answers") and topic_id is not False:
        answers = {}
        for a in (
            Answers.objects.filter(is_deleted=False, topic_id=topic_id)
            .order_by("sort_order", "number")
            .values("id", "question_id", "number", "right", "image", "name_uz_uz", "name_ru_ru", "name_en_us", "name_uz_crl")
        ):
            answers.setdefault(a["question_id"], []).append(a)
        for q in data:
            q["answers"] = answers.get(q["id"], [])
    return JsonResponse(data, safe=False)


def GetAnswers(request):
    type_id = request.GET.get("type_id", False)
    group_id = request.GET.get("group_id", False)
    book_id = request.GET.get("book_id", False)
    topic_id = request.GET.get("topic_id", False)
    question_id = request.GET.get("question_id", False)
    if type_id is False:
        data = Answers.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = Answers.objects.filter(is_deleted=False, type_id=type_id).values()
    if group_id is False:
        data = Answers.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = (
            Answers.objects.filter(is_deleted=False, group_id=group_id)
            .order_by("sort_order")
            .values()
        )
    if book_id is False:
        data = Answers.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = (
            Answers.objects.filter(is_deleted=False, book_id=book_id)
            .order_by("sort_order")
            .values()
        )
    if topic_id is False:
        data = Answers.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = (
            Answers.objects.filter(is_deleted=False, topic_id=topic_id)
            .order_by("sort_order")
            .values()
        )
    if question_id is False:
        data = Answers.objects.filter(is_deleted=False).order_by("sort_order").values()
    else:
        data = (
            Answers.objects.filter(is_deleted=False, question_id=question_id)
            .order_by("sort_order")
            .values()
        )
    return JsonResponse(list(data), safe=False)


def GetCounts(request):
    type_id = request.GET.get("type_id", False)
    group_id = request.GET.get("group_id", False)
    book_id = request.GET.get("book_id", False)
    topic_id = request.GET.get("topic_id", False)
    question_id = request.GET.get("question_id", False)
    types_count = Types.objects.filter(is_deleted=False).count()
    if type_id is False:
        groups_count = Groups.objects.filter(is_deleted=False).count()
        books_count = Books.objects.filter(is_deleted=False).count()
        topics_count = Topics.objects.filter(is_deleted=False).count()
        questions_count = Questions.objects.filter(is_deleted=False).count()
        answers_count = Answers.objects.filter(is_deleted=False).count()
        group = Groups.objects.filter(is_deleted=False).values().first()
        book = (
            Books.objects.filter(is_deleted=False)
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .values()
            .first()
        )
        topic = Topics.objects.filter(is_deleted=False).values().first()
        question = Questions.objects.filter(is_deleted=False).values().first()
        answer = Answers.objects.filter(is_deleted=False).values().first()
    else:
        groups_count = Groups.objects.filter(is_deleted=False, type_id=type_id).count()
        books_count = Books.objects.filter(is_deleted=False, type_id=type_id).count()
        topics_count = Topics.objects.filter(is_deleted=False, type_id=type_id).count()
        questions_count = Questions.objects.filter(
            is_deleted=False, type_id=type_id
        ).count()
        answers_count = Answers.objects.filter(
            is_deleted=False, type_id=type_id
        ).count()
        group = (
            Groups.objects.filter(is_deleted=False, type_id=type_id).values().first()
        )
        book = (
            Books.objects.filter(is_deleted=False, type_id=type_id)
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .values()
            .first()
        )
        topic = (
            Topics.objects.filter(is_deleted=False, type_id=type_id).values().first()
        )
        question = (
            Questions.objects.filter(is_deleted=False, type_id=type_id).values().first()
        )
        answer = (
            Answers.objects.filter(is_deleted=False, type_id=type_id).values().first()
        )

    context = {
        "types_count": types_count,
        "groups_count": groups_count,
        "books_count": books_count,
        "topics_count": topics_count,
        "questions_count": questions_count,
        "answers_count": answers_count,
        "group": group,
        "book": book,
        "topic": topic,
        "question": question,
        "answer": answer,
        # 'group':json.dumps(group, default=serialize_datetime),
        # 'book':json.dumps(book, default=serialize_datetime),
        # 'topic':json.dumps(topic, default=serialize_datetime),
        # 'question':json.dumps(question, default=serialize_datetime),
        # 'answer':json.dumps(answer, default=serialize_datetime),
    }
    return JsonResponse(context, safe=False)


def GetAllData(request):
    type_id = request.GET.get("type_id", False)
    group_id = request.GET.get("group_id", False)
    book_id = request.GET.get("book_id", False)
    topic_id = request.GET.get("topic_id", False)
    question_id = request.GET.get("question_id", False)
    if type_id is False:
        types = Types.objects.filter(is_deleted=False).values()
        groups = Groups.objects.filter(is_deleted=False).values()
        books = (
            Books.objects.filter(is_deleted=False)
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .values()
        )
        topics = Topics.objects.filter(is_deleted=False).values()
        questions = Questions.objects.filter(is_deleted=False).values()
        answers = Answers.objects.filter(is_deleted=False).values()
    else:
        types = Types.objects.filter(is_deleted=False, id=type_id).values()
        groups = Groups.objects.filter(is_deleted=False, type_id=type_id).values()
        books = (
            Books.objects.filter(is_deleted=False, type_id=type_id)
            .annotate(
                name_en_us=F("book_type__name_en_us"),
                name_ru_ru=F("book_type__name_ru_ru"),
                name_uz_crl=F("book_type__name_uz_crl"),
                name_uz_uz=F("book_type__name_uz_uz"),
                image=F("book_type__image"),
            )
            .values()
        )
        topics = Topics.objects.filter(is_deleted=False, type_id=type_id).values()
        questions = Questions.objects.filter(is_deleted=False, type_id=type_id).values()
        answers = Answers.objects.filter(is_deleted=False, type_id=type_id).values()

    context = {
        "types": list(types),
        "groups": list(groups),
        "books": list(books),
        "topics": list(topics),
        "questions": hide_draft_explanations(list(questions)),
        "answers": list(answers),
    }
    return JsonResponse(context, safe=False)


def GetRoadSigns(request):
    categories = (
        RoadSignCategories.objects.filter(is_deleted=False)
        .order_by("sort_order")
        .values(
            "id",
            "code",
            "name_en_us",
            "name_ru_ru",
            "name_uz_crl",
            "name_uz_uz",
            "image",
            "sort_order",
        )
    )
    signs = (
        RoadSigns.objects.filter(is_deleted=False, category__is_deleted=False)
        .order_by("category__sort_order", "sort_order")
        .values(
            "id",
            "category_id",
            "number",
            "name_en_us",
            "name_ru_ru",
            "name_uz_crl",
            "name_uz_uz",
            "description_en_us",
            "description_ru_ru",
            "description_uz_crl",
            "description_uz_uz",
            "image",
            "sort_order",
        )
    )
    context = {
        "categories": list(categories),
        "signs": list(signs),
    }
    return JsonResponse(context, safe=False)


def tests_mistakes(request):
    """Foydalanuvchi xato qilgan savollar — ro'yxat brauzer localStorage'ida saqlanadi."""
    return render(request, "tests/mistakes.html", {"comments": page_comments(request)})


def GetQuestionsByIds(request):
    """?ids=1,2,3 — savollarni javoblari bilan birga qaytaradi (xatolar ustida işlaş uçun)."""
    raw = request.GET.get("ids", "")
    ids = [int(x) for x in raw.split(",") if x.strip().isdigit()][:200]
    if not ids:
        return JsonResponse([], safe=False)
    questions = list(
        Questions.objects.filter(is_deleted=False, id__in=ids).values(
            "id",
            "number",
            "image",
            "book_id",
            "topic_id",
            "topic__number",
            "topic__name_uz_uz",
            "topic__name_ru_ru",
            "topic__name_en_us",
            "name_uz_uz",
            "name_ru_ru",
            "name_en_us",
            "explanation_uz_uz",
            "explanation_ru_ru",
            "explanation_en_us",
            "explanation_status",
        )
    )
    hide_draft_explanations(questions)
    answers = {}
    for a in (
        Answers.objects.filter(is_deleted=False, question_id__in=ids)
        .order_by("sort_order", "number")
        .values("id", "question_id", "right", "image", "name_uz_uz", "name_ru_ru", "name_en_us")
    ):
        answers.setdefault(a["question_id"], []).append(a)
    for q in questions:
        q["answers"] = answers.get(q["id"], [])
    return JsonResponse(questions, safe=False)
