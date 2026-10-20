"""«O'yinlar» kategoriyasi uchun yangi maqola: Google Play'dagi «Sudoku: Classic Puzzle Game» ilovasi.

Ma'lumotlar Google Play sahifasidan olingan (2026-10-20 holati, 2.0.0 versiya): 5 daraja, o'rgatuvchi maslahatlar,
qalamcha qaydlari, kunlik bellashuv, statistika, xatolar chegarasi, 3 xil kiritish usuli, tun rejimi, oflayn,
reklama bor, «ma'lumot to'planmaydi», 3+. Skrinshotlar — media/post/images/sudoku/.

Maqola bazada yo'q bo'lsa, qoralama sifatida yaratiladi (manage.py blog_rewrite sudoku_app).
"""

from ._apps import GP, SITE, TG_CHANNEL, app_box, ol as _ol, shots, ul as _ul

LANGS = ("uz", "ru", "en")
PLAY_URL = "https://play.google.com/store/apps/details?id=sudoku.complexprogrammer.uz"
IMG = "/media/post/images/sudoku/"
APP_NAME = '<span translate="no">Sudoku: Classic Puzzle Game</span>'
META = {"uz": "Android · bepul · internetsiz · o'zbek tilida",
        "ru": "Android · бесплатно · без интернета",
        "en": "Android · free · offline"}

SHOTS = [
    ("oyin.jpg", {"uz": "O'yin maydoni", "ru": "Игровое поле", "en": "Game board"}),
    ("darajalar.jpg", {"uz": "5 ta qiyinchilik darajasi", "ru": "5 уровней сложности", "en": "5 difficulty levels"}),
    ("maslahat.jpg", {"uz": "O'rgatuvchi maslahat", "ru": "Обучающая подсказка", "en": "Teaching hint"}),
    ("qaydlar.jpg", {"uz": "Qalamcha qaydlari va xatolar chegarasi", "ru": "Заметки и лимит ошибок",
                     "en": "Pencil notes and mistake limit"}),
    ("kunlik.jpg", {"uz": "Kunlik bellashuv taqvimi", "ru": "Календарь ежедневных испытаний", "en": "Daily challenge calendar"}),
    ("statistika.jpg", {"uz": "Statistika va tun rejimi", "ru": "Статистика и тёмная тема", "en": "Statistics and dark mode"}),
]


def _shots(lang):
    return shots(IMG, SHOTS, lang)


def _app_box(lang):
    return app_box(APP_NAME, f"{IMG}icon.png", PLAY_URL, META, lang)


def _body(lang):
    t = TEXT[lang]
    return "".join([
        f"<p>{t['intro']}</p>",
        _app_box(lang),
        f"<h2>{t['rules_h']}</h2>",
        f"<p>{t['rules_p']}</p>",
        _ul(t["rules"]),
        f"<p>{t['rules_after']}</p>",
        f"<h2>{t['features_h']}</h2>",
        _ul(t["features"]),
        _shots(lang),
        f"<h2>{t['tips_h']}</h2>",
        _ol(t["tips"]),
        f"<p>{t['tips_after']}</p>",
        f"<h2>{t['why_h']}</h2>",
        f"<p>{t['why_p']}</p>",
        f"<h2>{t['safe_h']}</h2>",
        _ul(t["safe"]),
        _app_box(lang),
        f"<p>{t['outro']}</p>",
    ])


TEXT = {
    "uz": {
        "intro": f"Sudoku — qog'oz va qalam davridan beri eng sevimli mantiqiy boshqotirmalardan biri. Endi uni telefoningizda, "
                 f"o'zbek tilida o'ynash mumkin: <strong>«{APP_NAME}»</strong> ilovasi {GP}da bepul chiqdi. Uni "
                 f"{SITE} muallifi yaratgan. Bu oddiy jumboqlar to'plami emas: o'yin davomida sudoku yechish "
                 f"usullarini ham o'rgatadi.",
        "rules_h": "Sudoku qoidalari — bir daqiqada",
        "rules_p": "O'yin maydoni 9×9 katakdan iborat va 3×3 o'lchamdagi 9 ta kvadratga bo'lingan. Ba'zi kataklarda raqamlar "
                   "oldindan berilgan. Vazifa — bo'sh kataklarni 1 dan 9 gacha raqamlar bilan shunday to'ldirish kerakki:",
        "rules": [
            "har bir <strong>qatorda</strong> 1–9 raqamlari bir martadan uchrasin;",
            "har bir <strong>ustunda</strong> ham;",
            "har bir <strong>3×3 kvadratda</strong> ham.",
        ],
        "rules_after": "Matematika kerak emas — faqat mantiq. To'g'ri tuzilgan sudokuning yechimi bitta bo'ladi, shuning uchun "
                       "uni taxmin qilmasdan, qadam-baqadam oxirigacha yechish mumkin.",
        "features_h": "Ilovada nimalar bor",
        "features": [
            "<strong>5 ta qiyinchilik darajasi.</strong> Oddiy, O'rta, Qiyin, Juda qiyin va Ekspert — miyani qizdirishdan "
            "tortib haqiqiy sinovgacha.",
            "<strong>O'rgatuvchi aqlli maslahatlar.</strong> Ko'p ilovalar shunchaki javobni ochib beradi. Bu yerda esa maslahat "
            "qaysi katakka qarash kerakligini va <em>nima uchun</em> aynan shu raqam mos kelishini tushuntiradi. Haqiqiy yechish "
            "usullari (<span translate=\"no\">Naked Single, Hidden Single</span>, qator va ustun bo'yicha istisno qilish) "
            "bosqichma-bosqich ko'rsatiladi.",
            "<strong>Qalamcha qaydlari.</strong> Qog'ozdagidek katakka nomzod raqamlarni yozib qo'yasiz. To'g'ri raqam "
            "qo'yilganda qaydlar avtomatik yangilanadi.",
            "<strong>Kunlik bellashuv.</strong> Har kuni yangi jumboq, to'xtovsiz seriya va oylik taqvim bo'yicha kuboklar.",
            "<strong>Batafsil statistika.</strong> Har bir daraja bo'yicha o'ynalgan o'yinlar, g'alaba foizi, eng yaxshi va "
            "o'rtacha vaqt, xatosiz o'yinlar va seriyalar.",
            "<strong>Xatolar chegarasi va ikkinchi imkoniyat.</strong> Odatiy 3 ta xato chegarasi bilan o'ynash yoki uni "
            "o'chirib, bemalol yechish mumkin. Qiyin jumboqda chegaraga yetsangiz, ikkinchi imkoniyat bilan davom ettirasiz.",
            "<strong>Raqam kiritishning 3 usuli:</strong> oddiy raqamlar paneli, bitta raqamni tanlab qo'yib chiqish yoki "
            "katak ustida ochiladigan menyu.",
            "<strong>Tun rejimi.</strong> Ko'zni charchatmaydigan qorong'i mavzu kechqurun o'ynash uchun qulay.",
            "<strong>To'liq oflayn.</strong> Internet kerak emas — metroda, yo'lda yoki samolyotda ham o'ynaysiz.",
        ],
        "tips_h": "Yangi boshlovchilar uchun 5 ta usul",
        "tips": [
            "<strong>Eng to'la joydan boshlang.</strong> Raqamlari ko'p qator, ustun yoki kvadratni tanlang — u yerda bo'sh "
            "kataklar kam, demak javob tezroq topiladi.",
            "<strong>Yagona nomzod</strong> (<span translate=\"no\">Naked Single</span>). Katakning qatori, ustuni va "
            "kvadratida qaysi raqamlar borligini ko'ring. 9 ta raqamdan 8 tasi band bo'lsa, qolgan bittasi — javob.",
            "<strong>Yashirin yagona</strong> (<span translate=\"no\">Hidden Single</span>). Teskarisini o'ylang: masalan, "
            "5 raqami shu kvadratning qayeriga tushishi mumkin? Faqat bitta katak qolgan bo'lsa, 5 o'sha yerga yoziladi — "
            "o'sha katakka boshqa raqamlar ham to'g'ri kelayotgandek ko'rinsa ham.",
            "<strong>Qator va ustunlarni «chizib chiqing».</strong> Bitta raqamni tanlang va u turgan qator hamda ustunlarni "
            "xayolan o'chiring. Kvadratda bo'sh qolgan yagona joy — shu raqamniki.",
            "<strong>Taxmin qilmang, qayd yozing.</strong> Qiyin darajalarda nomzodlarni qalamcha bilan yozib boring. Taxmin "
            "bilan qo'yilgan bitta raqam keyinroq butun yechimni buzishi mumkin.",
        ],
        "tips_after": "Qaysidir joyda to'xtab qolsangiz, ilovadagi «Maslahat» tugmasini bosing: u javobni emas, keyingi qadamni "
                      "qanday topishni ko'rsatadi. Bir necha o'yindan keyin bu usullarni o'zingiz qo'llay boshlaysiz.",
        "why_h": "Nega har kuni sudoku o'ynash foydali",
        "why_p": "Sudoku — miya uchun qisqa mashg'ulot: diqqatni bir joyga jamlashni, mantiqiy ketma-ketlikda fikrlashni va "
                 "sabrni mashq qildiradi. Kuniga 10–15 daqiqa yetarli. Kunlik bellashuv aynan shu odatni shakllantirishga "
                 "yordam beradi: seriyani uzmaslik uchun har kuni bitta jumboq yechasiz.",
        "safe_h": "Bepulmi va xavfsizmi?",
        "safe": [
            "Ilova <strong>bepul</strong>; xarajatlarni qoplash uchun unda reklama ko'rsatiladi.",
            f"{GP}dagi «Ma'lumotlar xavfsizligi» bo'limiga ko'ra ilova foydalanuvchi ma'lumotlarini <strong>to'plamaydi</strong>, "
            "uzatiladigan ma'lumotlar esa shifrlanadi.",
            "Yosh chegarasi — <strong>3+</strong>, ya'ni bolalar ham o'ynashi mumkin.",
        ],
        "outro": f"Fikr va takliflaringizni {GP}dagi sharhlarda yoki "
                 f'<a href="{TG_CHANNEL}" target="_blank" rel="noopener">Telegram kanalimizda</a> qoldiring — keyingi '
                 f"yangilanishlar aynan sizning fikrlaringiz asosida chiqadi.",
    },
    "ru": {
        "intro": f"Судоку — одна из самых любимых логических головоломок ещё со времён газет и карандаша. Теперь в неё можно "
                 f"играть на телефоне: приложение <strong>«{APP_NAME}»</strong> бесплатно вышло в {GP}. Его создал автор "
                 f"{SITE}, и это не просто сборник головоломок — по ходу игры оно учит приёмам решения судоку.",
        "rules_h": "Правила судоку за минуту",
        "rules_p": "Поле состоит из 9×9 клеток и разделено на 9 квадратов 3×3. Часть клеток уже заполнена. Нужно заполнить "
                   "пустые клетки цифрами от 1 до 9 так, чтобы:",
        "rules": [
            "в каждой <strong>строке</strong> цифры 1–9 встречались ровно по одному разу;",
            "в каждом <strong>столбце</strong> — тоже;",
            "и в каждом <strong>квадрате 3×3</strong> — тоже.",
        ],
        "rules_after": "Математика не нужна — только логика. У правильно составленного судоку одно решение, поэтому его можно "
                       "решить до конца шаг за шагом, ничего не угадывая.",
        "features_h": "Что есть в приложении",
        "features": [
            "<strong>5 уровней сложности.</strong> Лёгкий, Средний, Сложный, Очень сложный и Эксперт — от разминки для ума "
            "до настоящего испытания.",
            "<strong>Умные обучающие подсказки.</strong> Многие приложения просто открывают ответ. Здесь подсказка показывает, "
            "на какую клетку смотреть и <em>почему</em> подходит именно эта цифра. Настоящие приёмы решения "
            "(<span translate=\"no\">Naked Single, Hidden Single</span>, исключение по строкам и столбцам) объясняются "
            "пошагово.",
            "<strong>Карандашные заметки.</strong> Записывайте в клетки цифры-кандидаты, как на бумаге. Когда вы ставите "
            "правильную цифру, заметки обновляются автоматически.",
            "<strong>Ежедневные испытания.</strong> Новая головоломка каждый день, серия без пропусков и кубки в месячном "
            "календаре.",
            "<strong>Подробная статистика.</strong> По каждому уровню: сыгранные партии, процент побед, лучшее и среднее "
            "время, игры без ошибок и серии.",
            "<strong>Лимит ошибок и второй шанс.</strong> Играйте со стандартным лимитом в 3 ошибки или отключите его. "
            "Если лимит исчерпан на сложной головоломке, второй шанс позволит доиграть.",
            "<strong>3 способа ввода:</strong> обычная цифровая панель, режим одной выбранной цифры или меню прямо над "
            "клеткой.",
            "<strong>Тёмная тема.</strong> Не утомляет глаза при игре вечером.",
            "<strong>Полностью офлайн.</strong> Интернет не нужен — играйте в метро, в дороге или в самолёте.",
        ],
        "tips_h": "5 приёмов для начинающих",
        "tips": [
            "<strong>Начинайте с самых заполненных мест.</strong> Выберите строку, столбец или квадрат, где больше всего "
            "цифр: там меньше пустых клеток, и ответ находится быстрее.",
            "<strong>Единственный кандидат</strong> (<span translate=\"no\">Naked Single</span>). Посмотрите, какие цифры "
            "уже есть в строке, столбце и квадрате клетки. Если заняты 8 из 9, оставшаяся — ответ.",
            "<strong>Скрытый одиночка</strong> (<span translate=\"no\">Hidden Single</span>). Подумайте наоборот: куда в этом "
            "квадрате может встать, например, цифра 5? Если подходит только одна клетка, 5 ставится туда — даже если "
            "кажется, что в эту клетку подходят и другие цифры.",
            "<strong>«Вычёркивайте» строки и столбцы.</strong> Выберите цифру и мысленно зачеркните строки и столбцы, где она "
            "уже стоит. Единственное свободное место в квадрате — её.",
            "<strong>Не угадывайте — делайте заметки.</strong> На сложных уровнях записывайте кандидатов карандашом. Одна "
            "угаданная цифра может позже сломать всё решение.",
        ],
        "tips_after": "Застряли — нажмите «Подсказку»: она покажет не ответ, а то, как найти следующий шаг. Через несколько "
                      "партий вы начнёте применять эти приёмы сами.",
        "why_h": "Чем полезно играть в судоку каждый день",
        "why_p": "Судоку — короткая тренировка для мозга: она учит концентрироваться, рассуждать последовательно и не спешить. "
                 "Достаточно 10–15 минут в день. Ежедневные испытания помогают выработать эту привычку: чтобы не прервать "
                 "серию, вы решаете одну головоломку каждый день.",
        "safe_h": "Это бесплатно и безопасно?",
        "safe": [
            "Приложение <strong>бесплатное</strong>; чтобы покрывать расходы, в нём показывается реклама.",
            f"Согласно разделу «Безопасность данных» в {GP}, приложение <strong>не собирает</strong> данные пользователей, "
            "а передаваемые данные шифруются.",
            "Возрастной рейтинг — <strong>3+</strong>, играть могут и дети.",
        ],
        "outro": f"Оставляйте отзывы и предложения в {GP} или в нашем "
                 f'<a href="{TG_CHANNEL}" target="_blank" rel="noopener">Telegram-канале</a> — следующие обновления выходят '
                 f"именно с учётом ваших пожеланий.",
    },
    "en": {
        "intro": f"Sudoku has been one of the best-loved logic puzzles since the days of newspapers and pencils. Now you can "
                 f"play it on your phone: <strong>“{APP_NAME}”</strong> is out for free on {GP}. It was made by the author "
                 f"of {SITE}, and it is more than a puzzle collection — it teaches you real Sudoku solving "
                 f"techniques as you play.",
        "rules_h": "Sudoku rules in one minute",
        "rules_p": "The board is a 9×9 grid divided into nine 3×3 boxes. Some cells are already filled in. Fill the empty "
                   "cells with digits 1 to 9 so that:",
        "rules": [
            "every <strong>row</strong> contains each digit 1–9 exactly once;",
            "every <strong>column</strong> does too;",
            "and so does every <strong>3×3 box</strong>.",
        ],
        "rules_after": "No maths is needed — only logic. A well-made Sudoku has exactly one solution, so you can solve it step "
                       "by step without guessing.",
        "features_h": "What's in the app",
        "features": [
            "<strong>5 difficulty levels.</strong> Easy, Medium, Hard, Very Hard and Expert — from a gentle warm-up to a real "
            "challenge.",
            "<strong>Smart teaching hints.</strong> Many apps just reveal the answer. Here a hint shows which cell to look at "
            "and <em>why</em> that digit fits, walking you through real techniques (Naked Single, Hidden Single, row and "
            "column exclusion) step by step.",
            "<strong>Pencil notes.</strong> Jot candidate digits in cells just like on paper. When you place a correct digit, "
            "the notes update automatically.",
            "<strong>Daily challenges.</strong> A fresh puzzle every day, a streak to keep and trophies on a monthly calendar.",
            "<strong>In-depth statistics.</strong> For each level: games played, win rate, best and average time, perfect "
            "games and streaks.",
            "<strong>Mistake limit and second chance.</strong> Play with the standard 3-mistake limit or turn it off for "
            "relaxed play. Hit the limit on a tough board? A second chance lets you finish it.",
            "<strong>3 input modes:</strong> a standard number pad, single-digit focus, or a pop-up right over the cell.",
            "<strong>Dark mode.</strong> Easy on the eyes when playing at night.",
            "<strong>100% offline.</strong> No internet needed — play on the metro, on the road or on a plane.",
        ],
        "tips_h": "5 techniques for beginners",
        "tips": [
            "<strong>Start where it's busiest.</strong> Pick the row, column or box with the most digits: fewer empty cells "
            "means the answer comes faster.",
            "<strong>Naked Single.</strong> Check which digits are already in the cell's row, column and box. If 8 of the 9 "
            "are taken, the remaining one is the answer.",
            "<strong>Hidden Single.</strong> Think the other way round: where in this box can, say, a 5 go? If only one cell "
            "is left, the 5 goes there — even if other digits seem to fit that cell too.",
            "<strong>Cross-hatch rows and columns.</strong> Choose a digit and mentally cross out every row and column that "
            "already has it. The only free spot left in a box belongs to that digit.",
            "<strong>Don't guess — take notes.</strong> On harder levels, pencil in the candidates. One guessed digit can "
            "break the whole solution later.",
        ],
        "tips_after": "Stuck? Tap “Hint”: it shows how to find the next step rather than the answer. After a few games you'll "
                      "start using these techniques on your own.",
        "why_h": "Why play Sudoku every day",
        "why_p": "Sudoku is a short workout for your brain: it trains focus, step-by-step reasoning and patience. Ten to "
                 "fifteen minutes a day is enough, and the daily challenge helps build the habit — to keep your streak "
                 "alive, you solve one puzzle every day.",
        "safe_h": "Is it free and safe?",
        "safe": [
            "The app is <strong>free</strong>; it shows ads to cover its costs.",
            f"According to the Data safety section on {GP}, the app <strong>collects no user data</strong>, and data in "
            "transit is encrypted.",
            "It is rated <strong>3+</strong>, so kids can play too.",
        ],
        "outro": f"Share your feedback in a {GP} review or in our "
                 f'<a href="{TG_CHANNEL}" target="_blank" rel="noopener">Telegram channel</a> — the next updates are shaped '
                 f"by your suggestions.",
    },
}

ARTICLES = [
    {
        "slug": "sudoku-ozbek-tilida-android-oyini",
        "create": {"categorie_id": 3, "image": "post/images/sudoku_classic_puzzle.jpg"},
        "name": {"uz": "Sudoku o'zbek tilida: Android uchun bepul boshqotirma",
                 "ru": "Судоку на телефоне: бесплатная головоломка для Android",
                 "en": "Sudoku on your phone: a free puzzle game for Android"},
        "title": {"uz": "5 ta daraja, yechish usullarini o'rgatadigan maslahatlar, kunlik bellashuvlar va internetsiz o'yin. "
                        "Qoidalar va yangi boshlovchilar uchun 5 ta usul ham shu yerda.",
                  "ru": "5 уровней, подсказки, которые учат приёмам решения, ежедневные испытания и игра без интернета. "
                        "Плюс правила и 5 приёмов для начинающих.",
                  "en": "5 levels, hints that teach real solving techniques, daily challenges and offline play. Plus the "
                        "rules and 5 techniques for beginners."},
        "body": {lang: _body(lang) for lang in LANGS},
        "seo_title": "Sudoku o'zbek tilida — bepul Android o'yini va yechish usullari",
        "seo_description": "Sudoku: Classic Puzzle Game — o'zbek tilidagi bepul Android ilova: 5 daraja, o'rgatuvchi "
                           "maslahatlar, kunlik bellashuv, oflayn. Qoidalar va 5 ta yechish usuli.",
    },
]
