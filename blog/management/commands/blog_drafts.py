"""Avtotest mavzusidagi blog maqolalarini QORALAMA sifatida yaratish.

    python manage.py blog_drafts            # yangi maqolalarni yaratadi (borlari tegilmaydi)
    python manage.py blog_drafts --update   # borlarining matnini ham yangilaydi (masalan, statistika o'zgarganda)
    python manage.py blog_drafts --dry-run  # bazaga yozmasdan nima yaratilishini ko'rsatadi

Maqolalar saytda ko'rinmaydi: nashr sanasi 2099-yil qilib qo'yiladi. Admin → Blog → Posts'da matnni o'qib chiqing,
kerak bo'lsa rasm qo'shing va "Publish time"ni bugungi sanaga o'zgartiring — shunda maqola saytda chiqadi va
(TELEGRAM_BOT_TOKEN sozlangan bo'lsa) kanalga avtomatik yuboriladi.

Raqamlar (biletlar soni, belgilar, eng ko'p xato qilingan savollar) yaratish paytida bazadan olinadi.
"""

import datetime
from html import escape as _escape

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.utils import timezone

from blog.models import Categories, Posts
from core.translit import latin_to_cyrillic
from tests.models import Answers, Questions, RoadSignCategories, RoadSigns, Topics

DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)
AVTOTEST_BOOK_ID = 49  # "Avto Test": /avtotest/ dagi 108 bilet bilan bir xil savollar
UZ_BOOKS = (49, 50)  # O'zbekiston avtotesti va e-avtomaktab (bot AQSh CDL testini ham beradi — u maqolaga kirmaydi)
BOT = "https://t.me/AvtoTestUzbBot"
LANGS = ("uz", "ru", "en")
FIELD = {"uz": "uz_uz", "ru": "ru_ru", "en": "en_us"}


def escape(text):
    return _escape(text, quote=False)


def _p(text):
    return f"<p>{text}</p>"


def _a(href, text):
    return f'<a href="{href}">{text}</a>'


# --- 1. Tayyorgarlik rejasi -------------------------------------------------------------------------------------

def plan_article():
    tickets = Topics.objects.filter(is_deleted=False, book_id=AVTOTEST_BOOK_ID).count() or 108
    questions = tickets * 10
    links = {
        "/avtotest/": {"uz": "bilet", "ru": "билетов", "en": "tickets"},
        "/avtotest/mavzular/": {"uz": "mavzular", "ru": "тем", "en": "topics"},
        "/yhq/": {"uz": "YHQ matni", "ru": "текст ПДД", "en": "the traffic rules"},
        "/yol-belgilari/": {"uz": "yo'l belgilari", "ru": "дорожные знаки", "en": "road signs"},
        "/avtotest/imtihon/": {"uz": "Imtihon simulyatori", "ru": "Симулятор экзамена", "en": "exam simulator"},
        "/avtotest/kun-savoli/": {"uz": "kun savoli", "ru": "вопрос дня", "en": "question of the day"},
    }
    keys = {"bilet": "/avtotest/", "mavzu": "/avtotest/mavzular/", "yhq": "/yhq/", "belgi": "/yol-belgilari/",
            "imtihon": "/avtotest/imtihon/", "kun": "/avtotest/kun-savoli/"}

    def lk(key, lang):
        if key == "bot":
            return _a(BOT, "@AvtoTestUzbBot")
        return _a(keys[key], links[keys[key]][lang])

    body = {
        "uz": "".join([
            _p(f"Haydovchilik guvohnomasi imtihonining nazariy qismida 20 ta savol beriladi, javob uchun 25 daqiqa vaqt bor va "
               f"2 tadan ortiq xato qilmaslik kerak. Bazada {tickets} ta bilet ({questions} ga yaqin savol) bor — ularni "
               f"tartib bilan ishlab chiqsangiz, imtihonda notanish savol deyarli qolmaydi. Quyida 14 kunlik reja."),
            "<h2>1–3-kun: qoidalarni tushunish</h2>",
            _p(f"Savollarni yodlashdan oldin {lk('yhq', 'uz')} va {lk('belgi', 'uz')} bilan tanishing. Har kuni 1–2 bobni "
               f"o'qing va {lk('mavzu', 'uz')} bo'limidan shu bobga oid savollarni yeching — shunda javob nima uchun to'g'ri ekani esda qoladi."),
            "<h2>4–10-kun: biletlar</h2>",
            _p(f"Har kuni 10–15 ta {lk('bilet', 'uz')}ni yeching. Bilet tugagach natijaga qarang: 18 tadan kam bo'lsa, "
               f"o'sha biletni ertasi kuni qayta ishlang. Noto'g'ri javob berilgan savollar avtomatik «Xatolarim» bo'limiga "
               f"tushadi — kun oxirida faqat ularni takrorlang."),
            "<h2>11–13-kun: imtihon sharoitida mashq</h2>",
            _p(f"{lk('imtihon', 'uz')} haqiqiy imtihon kabi: tasodifiy 20 savol, "
               f"25 daqiqa, 2 tagacha xato. Kuniga 3–4 marta ishlang. Ketma-ket 5 marta o'tsangiz, tayyorsiz."),
            "<h2>14-kun: yengil takrorlash</h2>",
            _p("Imtihon arafasida yangi narsa o'rganmang: faqat «Xatolarim» bo'limini ko'rib chiqing va yaxshi dam oling."),
            "<h2>Har kuni 5 daqiqa</h2>",
            _p(f"Telegramdagi {lk('bot', 'uz')} botida «Tezkor mashq» (5 savol) va kunlik eslatma bor, saytda esa har kuni "
               f"yangi {lk('kun', 'uz')} chiqadi. Natijalaringiz saqlanib qolishi uchun saytga Telegram orqali kiring."),
        ]),
        "ru": "".join([
            _p(f"В теоретической части экзамена на права — 20 вопросов, 25 минут и не более 2 ошибок. В базе {tickets} "
               f"билетов (около {questions} вопросов): если пройти их по порядку, незнакомых вопросов на экзамене почти не "
               f"останется. Ниже — план на 14 дней."),
            "<h2>Дни 1–3: понять правила</h2>",
            _p(f"Прежде чем заучивать ответы, прочитайте {lk('yhq', 'ru')} и изучите {lk('belgi', 'ru')}. Каждый день — "
               f"1–2 главы и вопросы из раздела {lk('mavzu', 'ru')}: так вы запомните, почему ответ правильный."),
            "<h2>Дни 4–10: билеты</h2>",
            _p(f"Решайте 10–15 {lk('bilet', 'ru')} в день. Если в билете меньше 18 правильных ответов, повторите его "
               f"на следующий день. Вопросы с ошибками автоматически попадают в раздел «Мои ошибки» — в конце дня "
               f"повторяйте только их."),
            "<h2>Дни 11–13: в условиях экзамена</h2>",
            _p(f"{lk('imtihon', 'ru')} устроен как настоящий экзамен: 20 случайных вопросов, 25 минут, не более 2 ошибок. "
               f"Проходите его 3–4 раза в день. Сдали 5 раз подряд — вы готовы."),
            "<h2>День 14: лёгкое повторение</h2>",
            _p("Накануне экзамена не учите новое: просмотрите «Мои ошибки» и хорошо отдохните."),
            "<h2>5 минут каждый день</h2>",
            _p(f"В Telegram-боте {lk('bot', 'ru')} есть «Быстрая тренировка» (5 вопросов) и ежедневное напоминание, а на "
               f"сайте каждый день новый {lk('kun', 'ru')}. Чтобы результаты сохранялись, войдите на сайт через Telegram."),
        ]),
        "en": "".join([
            _p(f"The theory part of the driving licence exam has 20 questions, 25 minutes and at most 2 mistakes. The site "
               f"has {tickets} tickets (about {questions} questions): work through them in order and almost nothing on the "
               f"exam will be new. Here is a 14-day plan."),
            "<h2>Days 1–3: understand the rules</h2>",
            _p(f"Before memorising answers, read {lk('yhq', 'en')} and learn the {lk('belgi', 'en')}. Each day take 1–2 "
               f"chapters and solve the questions from the matching {lk('mavzu', 'en')}, so you remember why an answer is right."),
            "<h2>Days 4–10: tickets</h2>",
            _p(f"Solve 10–15 {lk('bilet', 'en')} a day. If a ticket scores below 18, repeat it the next day. Questions you "
               f"get wrong go to “My mistakes” automatically — review only those at the end of the day."),
            "<h2>Days 11–13: exam conditions</h2>",
            _p(f"The {lk('imtihon', 'en')} works like the real exam: 20 random questions, 25 minutes, up to 2 mistakes. "
               f"Take it 3–4 times a day. Pass 5 times in a row and you are ready."),
            "<h2>Day 14: light review</h2>",
            _p("Don't learn anything new the day before the exam: go over “My mistakes” and get some rest."),
            "<h2>5 minutes a day</h2>",
            _p(f"The {lk('bot', 'en')} Telegram bot has a 5-question “Quick practice” and a daily reminder, and the site "
               f"posts a new {lk('kun', 'en')} every day. Sign in with Telegram so your results are saved."),
        ]),
    }
    return {
        "slug": "avtotestga-14-kunda-tayyorlanish",
        "name": {"uz": "Avtotestga 14 kunda tayyorlanish rejasi", "ru": "Как подготовиться к автотесту за 14 дней",
                 "en": "A 14-day plan to prepare for the driving theory test"},
        "title": {"uz": f"{tickets} ta biletni qanday tartibda yechish, imtihon simulyatori va xatolar ustida ishlash.",
                  "ru": f"В каком порядке решать {tickets} билетов, симулятор экзамена и работа над ошибками.",
                  "en": f"How to work through {tickets} tickets, the exam simulator and reviewing your mistakes."},
        "body": body,
        "seo_title": "Avtotestga tayyorlanish: 14 kunlik reja",
        "seo_description": f"Haydovchilik imtihoniga 14 kunda tayyorlanish: {tickets} ta bilet, imtihon simulyatori "
                           f"(20 savol, 25 daqiqa) va xatolar ustida ishlash.",
    }


# --- 2. Yo'l belgilari guruhlari -------------------------------------------------------------------------------

SIGN_GROUPS = {
    "warning": {
        "uz": "Odatda qizil hoshiyali uchburchak. Oldinda xavfli joy borligini bildiradi — tezlikni pasaytirib, ehtiyot bo'lish kerak.",
        "ru": "Обычно треугольник с красной каймой. Предупреждают об опасном участке впереди — нужно снизить скорость и быть внимательнее.",
        "en": "Usually a triangle with a red border. They warn of a hazard ahead, so slow down and stay alert.",
    },
    "priority": {
        "uz": "Chorrahalar va tor joylarda kim birinchi o'tishini belgilaydi («Asosiy yo'l», «Yo'l bering», «To'xtamasdan harakatlanish taqiqlangan»).",
        "ru": "Определяют очерёдность проезда перекрёстков и узких участков («Главная дорога», «Уступите дорогу», «Движение без остановки запрещено»).",
        "en": "They set who goes first at junctions and narrow sections (“Priority road”, “Give way”, “Stop”).",
    },
    "prohibitory": {
        "uz": "Odatda qizil hoshiyali doira. Muayyan harakatni taqiqlaydi yoki cheklaydi (kirish, quvib o'tish, tezlik, to'xtash).",
        "ru": "Обычно круг с красной каймой. Запрещают или ограничивают действие (въезд, обгон, скорость, остановку).",
        "en": "Usually a circle with a red border. They forbid or limit an action (entry, overtaking, speed, stopping).",
    },
    "mandatory": {
        "uz": "Ko'k doira, oq rasm. Muayyan yo'nalish yoki harakat usulini majburiy qiladi.",
        "ru": "Синий круг с белым изображением. Обязывают двигаться в определённом направлении или определённым образом.",
        "en": "A blue circle with a white symbol. They require a specific direction or way of moving.",
    },
    "information": {
        "uz": "To'rtburchak belgilar: harakatning alohida tartibi, aholi punktlari, yo'nalish va masofa haqida ma'lumot beradi.",
        "ru": "Прямоугольные знаки: сообщают об особом режиме движения, населённых пунктах, направлениях и расстояниях.",
        "en": "Rectangular signs about special traffic rules, towns, directions and distances.",
    },
    "service": {
        "uz": "Ko'k to'rtburchak ichida oq maydon: yoqilg'i quyish shoxobchasi, tibbiy yordam, ovqatlanish joyi va boshqa xizmatlar.",
        "ru": "Синий прямоугольник с белым полем: АЗС, медпомощь, пункт питания и другие услуги.",
        "en": "A blue rectangle with a white field: fuel, first aid, food and other services.",
    },
    "additional": {
        "uz": "Asosiy belgi ostidagi kichik lavhalar: belgining amal qilish masofasi, vaqti yoki qaysi transportga tegishliligini aniqlaydi.",
        "ru": "Таблички под основным знаком: уточняют зону действия, время или вид транспорта, к которому относится знак.",
        "en": "Small plates under a main sign that narrow its distance, time or the vehicles it applies to.",
    },
}


def signs_article():
    cats = list(RoadSignCategories.objects.filter(is_deleted=False, code__in=SIGN_GROUPS).order_by("sort_order"))
    if not cats:
        return None
    signs = {}
    for s in RoadSigns.objects.filter(is_deleted=False, category__in=cats).order_by("sort_order"):
        signs.setdefault(s.category_id, []).append(s)
    intro = {
        "uz": f"Yo'l belgilari {len(cats)} guruhga bo'linadi. Belgining shakli va rangi uning guruhini bildiradi — buni bilsangiz, "
              f"notanish belgining ma'nosini ham taxmin qila olasiz. Avtotestdagi savollarning katta qismi aynan belgilarga oid.",
        "ru": f"Дорожные знаки делятся на {len(cats)} групп. Форма и цвет знака подсказывают его группу — зная это, можно понять "
              f"смысл даже незнакомого знака. Большая часть вопросов автотеста связана именно со знаками.",
        "en": f"Road signs fall into {len(cats)} groups. A sign's shape and colour tell you its group, so you can guess even an "
              f"unfamiliar sign. A large share of driving test questions are about signs.",
    }
    examples = {"uz": "Misollar", "ru": "Примеры", "en": "Examples"}
    all_link = {"uz": "Barcha belgilar rasmlari va tavsifi bilan", "ru": "Все знаки с картинками и описанием",
                "en": "All signs with pictures and descriptions"}
    body = {}
    for lang in LANGS:
        f = FIELD[lang]
        parts = [_p(intro[lang])]
        for i, cat in enumerate(cats, 1):
            parts.append(f"<h2>{i}. {escape(getattr(cat, 'name_' + f) or cat.name_uz_uz)}</h2>")
            parts.append(_p(SIGN_GROUPS[cat.code][lang]))
            sample = signs.get(cat.id, [])[:4]
            if sample:
                items = "".join(
                    f"<li>{_a(f'/yol-belgilari/{s.pk}/', escape(((s.number + ' ') if s.number else '') + (getattr(s, 'name_' + f) or s.name_uz_uz)))}</li>"
                    for s in sample
                )
                parts.append(f"<p><b>{examples[lang]}:</b></p><ul>{items}</ul>")
        parts.append(_p(_a("/yol-belgilari/", all_link[lang] + " →")))
        body[lang] = "".join(parts)
    return {
        "slug": "yol-belgilari-guruhlari",
        "name": {"uz": "Yo'l belgilari: guruhlari va ularni tez eslab qolish", "ru": "Дорожные знаки: группы и как их быстро запомнить",
                 "en": "Road signs: the groups and how to remember them"},
        "title": {"uz": "Belgining shakli va rangi uning ma'nosini qanday aytib beradi — har bir guruh misollar bilan.",
                  "ru": "Как форма и цвет знака подсказывают его смысл — каждая группа с примерами.",
                  "en": "How a sign's shape and colour reveal its meaning, with examples from every group."},
        "body": body,
        "seo_title": "Yo'l belgilari guruhlari — misollar bilan",
        "seo_description": f"Yo'l belgilarining {len(cats)} guruhi: ogohlantiruvchi, imtiyoz, taqiqlovchi, buyuruvchi va boshqalar. "
                           f"Shakli, rangi va misollar.",
    }


# --- 3. Eng ko'p xato qilinadigan savollar (Telegram-bot statistikasi) -------------------------------------------

def mistakes_article(limit=10, min_users=2, per_ticket=2):
    with connection.cursor() as cur:
        try:
            cur.execute(
                "SELECT question_id, COUNT(DISTINCT user_id) AS n FROM avtotest_bot_mistakes "
                "GROUP BY question_id HAVING n >= %s ORDER BY n DESC, question_id LIMIT %s",
                [min_users, limit * 10],
            )
        except Exception:  # noqa: BLE001 — bot jadvali hali yaratilmagan bo'lishi mumkin
            return None
        counts = dict(cur.fetchall())
        cur.execute("SELECT COUNT(DISTINCT user_id) FROM avtotest_bot_mistakes")
        users = cur.fetchone()[0]
    questions = {
        q.id: q for q in Questions.objects.filter(id__in=counts, is_deleted=False).select_related("topic")
    }
    # Bot foydalanuvchilarining ko'pi birinchi biletlardan boshlaydi — ro'yxat bitta biletdan iborat bo'lib qolmasin
    ids, per = [], {}
    for qid in counts:
        q = questions.get(qid)
        if q is None or q.book_id not in UZ_BOOKS or per.get(q.topic_id, 0) >= per_ticket:
            continue
        per[q.topic_id] = per.get(q.topic_id, 0) + 1
        ids.append(qid)
        if len(ids) >= limit:
            break
    if len(ids) < 5:
        return None  # statistikasi yetarli emas — maqola yaratilmaydi
    right = {a.question_id: a for a in Answers.objects.filter(question_id__in=ids, right=True, is_deleted=False)}
    head = {
        "uz": f"Telegramdagi {_a(BOT, '@AvtoTestUzbBot')} botida test ishlagan {users} nafar foydalanuvchining javoblari bo'yicha "
              f"eng ko'p xato qilingan {len(ids)} ta savol. Har birida to'g'ri javob va savol joylashgan bilet havolasi bor.",
        "ru": f"По ответам {users} пользователей Telegram-бота {_a(BOT, '@AvtoTestUzbBot')} — {len(ids)} вопросов, в которых "
              f"ошибаются чаще всего. Для каждого указан правильный ответ и ссылка на билет.",
        "en": f"Based on the answers of {users} users of the {_a(BOT, '@AvtoTestUzbBot')} Telegram bot, these are the {len(ids)} "
              f"questions people get wrong most often, each with the correct answer and a link to its ticket.",
    }
    labels = {
        "uz": ("To'g'ri javob", "Nima uchun", "Biletni ochish", "nafar xato qilgan"),
        "ru": ("Правильный ответ", "Почему", "Открыть билет", "ошиблись"),
        "en": ("Correct answer", "Why", "Open the ticket", "got it wrong"),
    }
    tail = {
        "uz": f"O'zingizni sinab ko'ring: {_a('/avtotest/imtihon/', 'imtihon simulyatori')} — 20 savol, 25 daqiqa.",
        "ru": f"Проверьте себя: {_a('/avtotest/imtihon/', 'симулятор экзамена')} — 20 вопросов, 25 минут.",
        "en": f"Test yourself: the {_a('/avtotest/imtihon/', 'exam simulator')} — 20 questions, 25 minutes.",
    }
    body = {}
    for lang in LANGS:
        f = FIELD[lang]
        ans_label, why, open_label, wrong_label = labels[lang]
        parts = [_p(head[lang])]
        for i, qid in enumerate(ids, 1):
            q, a = questions[qid], right.get(qid)
            text = getattr(q, "name_" + f) or q.name_uz_uz
            parts.append(f"<h2>{i}. {escape(text)}</h2>")
            if q.image:
                parts.append(f'<p><img src="{q.image.url}" alt="" style="max-width:100%"></p>')
            if a is not None:
                parts.append(_p(f"<b>{ans_label}:</b> {escape(getattr(a, 'name_' + f) or a.name_uz_uz)}"))
            expl = getattr(q, "explanation_" + f) if q.explanation_status != "draft" else ""
            if expl:
                parts.append(_p(f"<b>{why}:</b> {escape(expl)}"))
            parts.append(_p(f"{_a(f'/tests?topic_id={q.topic_id}', open_label + ' →')} · {counts[qid]} {wrong_label}"))
        parts.append(_p(tail[lang]))
        body[lang] = "".join(parts)
    return {
        "slug": "avtotest-eng-kop-xato-qilinadigan-savollar",
        "name": {"uz": f"Avtotestda eng ko'p xato qilinadigan {len(ids)} ta savol",
                 "ru": f"{len(ids)} вопросов автотеста, в которых ошибаются чаще всего",
                 "en": f"The {len(ids)} driving test questions people get wrong most"},
        "title": {"uz": "Telegram-bot foydalanuvchilarining javoblari asosida — to'g'ri javoblar va izohlar bilan.",
                  "ru": "По ответам пользователей Telegram-бота — с правильными ответами и пояснениями.",
                  "en": "Based on our Telegram bot users' answers, with correct answers and explanations."},
        "body": body,
        "seo_title": "Avtotestda eng ko'p xato qilinadigan savollar",
        "seo_description": "Haydovchilik imtihoni savollaridan eng ko'p xato qilinganlari: to'g'ri javob, izoh va bilet havolasi.",
    }


ARTICLES = (plan_article, signs_article, mistakes_article)


class Command(BaseCommand):
    help = "Avtotest mavzusidagi blog maqolalarini qoralama (2099-yil sanasi bilan) sifatida yaratish."

    def add_arguments(self, parser):
        parser.add_argument("--update", action="store_true", help="Mavjud qoralamalar matnini ham yangilash")
        parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmasdan ko'rsatish")

    def handle(self, *args, **opts):
        author = User.objects.filter(is_superuser=True).order_by("id").first()
        if author is None:
            raise CommandError("Superuser topilmadi (maqola muallifi uchun kerak).")
        category = Categories.objects.filter(name_uz_uz__iexact="Testlar", is_deleted=False).first()
        for build in ARTICLES:
            art = build()
            if art is None:
                self.stdout.write(f"- {build.__name__}: ma'lumot yetarli emas, o'tkazib yuborildi.")
                continue
            fields = {"seo_title": art["seo_title"][:70], "seo_description": art["seo_description"][:200]}
            for lang in LANGS:
                f = FIELD[lang]
                fields["name_" + f] = art["name"][lang]
                fields["title_" + f] = art["title"][lang]
                fields["body_" + f] = art["body"][lang]
            fields["name_uz_crl"] = latin_to_cyrillic(art["name"]["uz"])
            fields["title_uz_crl"] = latin_to_cyrillic(art["title"]["uz"])
            fields["body_uz_crl"] = latin_to_cyrillic(art["body"]["uz"])

            post = Posts.objects.filter(slug=art["slug"]).first()
            if post is not None and not opts["update"]:
                self.stdout.write(f"= {art['slug']}: allaqachon bor (yangilash uchun --update).")
                continue
            if post is not None and post.publish_time <= timezone.now():
                self.stdout.write(f"= {art['slug']}: nashr qilingan — tegilmadi.")
                continue
            if opts["dry_run"]:
                self.stdout.write(f"+ {art['slug']}: {art['name']['uz']} ({len(art['body']['uz'])} belgi)")
                continue
            if post is None:
                post = Posts(slug=art["slug"], created_by=author, categorie=category, publish_time=DRAFT_TIME)
            for k, v in fields.items():
                setattr(post, k, v)
            post.save()
            self.stdout.write(self.style.SUCCESS(f"+ {art['slug']}: {art['name']['uz']}"))
        self.stdout.write("Admin → Blog → Posts: matnni tekshirib, «Publish time»ni bugungi sanaga o'zgartiring.")
