"""«O'yinlar» kategoriyasi uchun yangi maqola: Google Play'dagi «Flying Bird: Qush Parvozi» o'yini + YouTube treyleri.

Ma'lumotlar Google Play sahifasidan olingan (2026-10-20 holati, 2026-10-14 yangilanishi): 3D arkada, Samarqand Registon,
Buxoro Ark, Xiva Ichan-Qal'a, Toshkent teleminorasi (kunduzgi va tungi), 5 ta qush (0/10/25/50/100 ochko), medallar
(10/25/50/100), oflayn, musiqa/ovoz/tebranish, o'zbek/rus/ingliz tillari, reklama bor, ma'lumot to'planmaydi
va uchinchi tomonga berilmaydi, 3+. Treyler: https://www.youtube.com/watch?v=UJWdVwgvvTM

Maqola bazada yo'q bo'lsa yaratiladi (manage.py blog_rewrite flying_bird [--publish]).
"""

from ._apps import GP, SITE, TG_CHANNEL, app_box, ol, shots, ul, youtube

LANGS = ("uz", "ru", "en")
PLAY_URL = "https://play.google.com/store/apps/details?id=flyingbird.complexprogrammer.uz"
VIDEO_ID = "UJWdVwgvvTM"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
IMG = "/media/post/images/flyingbird/"
SUDOKU = "/blog/sudoku-ozbek-tilida-android-oyini/"
FB = '<span translate="no">Flying Bird</span>'
NAME = {"uz": f"{FB}: Qush Parvozi", "ru": f"{FB}: Полёт Птицы", "en": f"{FB}: Flap &amp; Fly"}
META = {"uz": "Android · bepul · internetsiz · o'zbek, rus, ingliz tilida",
        "ru": "Android · бесплатно · без интернета · на русском, узбекском и английском",
        "en": "Android · free · offline · English, Uzbek and Russian"}

SHOTS = [
    ("boshlash.jpg", {"uz": "Bir marta teging va uching", "ru": "Коснитесь — и летите", "en": "Tap to fly"}),
    ("obidalar.jpg", {"uz": "Registon, Ark va Ichan-Qal'a", "ru": "Регистан, Арк и Ичан-Кала", "en": "Registan, Ark and Ichan-Kala"}),
    ("qushlar.jpg", {"uz": "5 ta rang-barang qush", "ru": "5 разноцветных птиц", "en": "5 colourful birds"}),
    ("medallar.jpg", {"uz": "Medallar va yangi rekord", "ru": "Медали и новый рекорд", "en": "Medals and a new high score"}),
    ("tungi.jpg", {"uz": "Tungi Toshkent teleminorasi", "ru": "Ночная Ташкентская телебашня", "en": "Tashkent TV Tower at night"}),
    ("sozlamalar.jpg", {"uz": "Sozlamalar va oflayn rejim", "ru": "Настройки и офлайн-режим", "en": "Settings and offline mode"}),
]

BIRDS = [  # (nomi, rangi, kerakli ochko)
    ("Classic", {"uz": "sariq", "ru": "жёлтая", "en": "yellow"}, 0),
    ("Ruby", {"uz": "qizil", "ru": "красная", "en": "red"}, 10),
    ("Lime", {"uz": "yashil", "ru": "зелёная", "en": "green"}, 25),
    ("Ocean", {"uz": "moviy", "ru": "синяя", "en": "blue"}, 50),
    ("Violet", {"uz": "binafsha", "ru": "фиолетовая", "en": "purple"}, 100),
]
MEDALS = [  # (ochko, nomi)
    (10, {"uz": "Bronza", "ru": "Бронзовая", "en": "Bronze"}),
    (25, {"uz": "Kumush", "ru": "Серебряная", "en": "Silver"}),
    (50, {"uz": "Oltin", "ru": "Золотая", "en": "Gold"}),
    (100, {"uz": "Platina", "ru": "Платиновая", "en": "Platinum"}),
]
HEAD = {"uz": ("Ochko", "Qush", "Medal"), "ru": ("Очки", "Птица", "Медаль"), "en": ("Score", "Bird", "Medal")}
FROM_START = {"uz": "boshidan ochiq", "ru": "открыта сразу", "en": "unlocked from the start"}


def _table(lang):
    medals = dict(MEDALS)
    rows = "".join(
        f'<tr><td>{score or "—"}</td><td><span translate="no">{name}</span> ({color[lang]}){" — " + FROM_START[lang] if not score else ""}</td>'
        f'<td>{medals[score][lang] if score in medals else "—"}</td></tr>'
        for name, color, score in BIRDS
    )
    h = HEAD[lang]
    return f"<table><thead><tr><th>{h[0]}</th><th>{h[1]}</th><th>{h[2]}</th></tr></thead><tbody>{rows}</tbody></table>"


def _app_box(lang):
    return app_box(NAME[lang], f"{IMG}icon.png", PLAY_URL, META, lang)


def _body(lang):
    t = TEXT[lang]
    return "".join([
        f"<p>{t['intro']}</p>",
        _app_box(lang),
        f"<h2>{t['video_h']}</h2>",
        youtube(VIDEO_ID, "Flying Bird — Android Gameplay &amp; Promo Trailer | Qush Parvozi"),
        f"<p>{t['video_p']}</p>",
        f"<h2>{t['how_h']}</h2>",
        ol(t["how"]),
        f"<h2>{t['places_h']}</h2>",
        f"<p>{t['places_p']}</p>",
        ul(t["places"]),
        f"<h2>{t['birds_h']}</h2>",
        f"<p>{t['birds_p']}</p>",
        _table(lang),
        shots(IMG, SHOTS, lang),
        f"<h2>{t['tips_h']}</h2>",
        ol(t["tips"]),
        f"<h2>{t['more_h']}</h2>",
        ul(t["more"]),
        _app_box(lang),
        f"<p>{t['outro']}</p>",
    ])


TEXT = {
    "uz": {
        "intro": f"Bir barmoq bilan boshqariladigan, lekin to'xtatib bo'lmaydigan o'yinlarni yaxshi ko'rasizmi? "
                 f"<strong>«{NAME['uz']}»</strong> — {SITE} muallifining yangi "
                 f"3D arkada o'yini. Ekranga teging, qushcha qanot qoqadi — vazifangiz uni yashil quvurlar orasidan "
                 f"o'tkazish. Eng yoqimlisi: parvoz Samarqand, Buxoro, Xiva va Toshkentning mashhur obidalari uzra "
                 f"o'tadi. O'yin {GP}da bepul.",
        "video_h": "Treyler: o'yinni harakatda ko'ring",
        "video_p": f'Video ochilmasa, uni <a href="{VIDEO_URL}"><span translate="no">YouTube</span>\'da ko\'ring</a>.',
        "how_h": "Qanday o'ynaladi",
        "how": [
            "Ekranga teging — qushcha qanot qoqib yuqoriga ko'tariladi.",
            "Teginmasangiz, qushcha pastga tushadi. Teginishlar orasidagi vaqtni to'g'ri tanlab, quvurlar orasidagi "
            "bo'shliqdan o'ting.",
            "Quvurga yoki yerga tegsangiz, o'yin tugaydi.",
            "Har bir o'tilgan quvur — 1 ochko. O'z rekordingizni yangilang va natijani do'stlaringiz bilan ulashing.",
        ],
        "places_h": "O'zbekiston obidalari uzra parvoz",
        "places_p": "O'yin fonida O'zbekistonning taniqli joylari chizilgan — har bir parvoz qisqa sayohatga o'xshaydi:",
        "places": [
            "<strong>Samarqand — Registon maydoni.</strong> Ulug'bek, Sherdor va Tillakori madrasalari bir maydonda "
            "turgan mashhur ansambl.",
            "<strong>Buxoro — Ark qal'asi.</strong> Asrlar davomida Buxoro hukmdorlarining qarorgohi bo'lgan qadimiy qal'a.",
            "<strong>Xiva — Ichan-Qal'a.</strong> Minoralari va madrasalari bilan mashhur ichki shahar; 1990 yilda "
            "YUNESKO Butunjahon merosi ro'yxatiga kiritilgan.",
            "<strong>Toshkent — teleminora.</strong> Kunduzgi va yulduzli tungi ko'rinishda. Minoraning balandligi — 375 metr.",
        ],
        "birds_h": "5 ta qush va medallar",
        "birds_p": "Rekordingiz oshgani sari yangi qushlar ochiladi, natijangiz uchun esa medal beriladi:",
        "tips_h": "Rekordni yangilash uchun 5 ta maslahat",
        "tips": [
            "<strong>Qushga emas, keyingi bo'shliqqa qarang.</strong> Ko'z oldinda bo'lsa, qachon teginish kerakligini "
            "oldindan sezasiz.",
            "<strong>Qisqa va bir maromda teging.</strong> Ketma-ket tez-tez teginish qushni juda baland ko'tarib yuboradi.",
            "<strong>Ekran o'rtasida uching.</strong> O'rtadan keyingi bo'shliqqa yetib borish — yuqori yoki pastki "
            "chetdan ko'ra osonroq.",
            "<strong>Ritmni tinglang.</strong> Ovoz effektlari teginish ritmini ushlashga yordam beradi. Agar "
            "chalg'itsa, sozlamalardan musiqani o'chirib qo'ying.",
            "<strong>Rekord yaqinlashganda shoshilmang.</strong> Ko'pchilik aynan shu paytda hayajonlanib xato qiladi — "
            "odatdagi ritmni saqlang.",
        ],
        "more_h": "Yana nimalar bor",
        "more": [
            "<strong>To'liq oflayn</strong> — internet kerak emas: yo'lda, samolyotda, istalgan joyda o'ynaysiz.",
            "<strong>Musiqa, ovoz effektlari va tebranish</strong> — har birini sozlamalardan alohida yoqib-o'chirish mumkin.",
            "<strong>3 til:</strong> o'zbek, rus va ingliz.",
            "<strong>Bepul</strong>; xarajatlarni qoplash uchun reklama ko'rsatiladi.",
            f"{GP}dagi «Ma'lumotlar xavfsizligi» bo'limiga ko'ra o'yin ma'lumot <strong>to'plamaydi</strong> va uchinchi "
            "tomonlarga <strong>bermaydi</strong>. Yosh chegarasi — 3+, bolalar ham bemalol o'ynaydi.",
        ],
        "outro": f"Mantiqiy o'yinlarni yoqtirsangiz, bizning <a href=\"{SUDOKU}\">o'zbek tilidagi Sudoku</a> o'yinimizni "
                 f"ham sinab ko'ring. Rekordingiz va takliflaringizni {GP}dagi sharhlarda yoki "
                 f'<a href="{TG_CHANNEL}">Telegram kanalimizda</a> qoldiring.',
    },
    "ru": {
        "intro": f"Любите игры, где управление — одно касание, а оторваться невозможно? "
                 f"<strong>«{NAME['ru']}»</strong> — новая 3D-аркада от автора "
                 f"{SITE}. Касайтесь экрана, птичка взмахивает крыльями, а ваша задача — провести её между зелёными трубами. "
                 f"Самое приятное: полёт проходит над знаменитыми памятниками Самарканда, Бухары, Хивы и Ташкента. "
                 f"Игра бесплатна в {GP}.",
        "video_h": "Трейлер: игра в движении",
        "video_p": f'Если видео не открывается, <a href="{VIDEO_URL}">смотрите его на YouTube</a>.',
        "how_h": "Как играть",
        "how": [
            "Коснитесь экрана — птичка взмахнёт крыльями и поднимется.",
            "Без касаний она снижается. Подбирайте паузы между касаниями, чтобы пролетать в просвет между трубами.",
            "Столкновение с трубой или землёй заканчивает игру.",
            "Каждая пройденная труба — 1 очко. Бейте свой рекорд и делитесь результатом с друзьями.",
        ],
        "places_h": "Полёт над достопримечательностями Узбекистана",
        "places_p": "На фоне игры нарисованы известные места Узбекистана — каждый полёт похож на короткое путешествие:",
        "places": [
            "<strong>Самарканд — площадь Регистан.</strong> Знаменитый ансамбль из трёх медресе: Улугбека, Шердор и Тилля-Кари.",
            "<strong>Бухара — крепость Арк.</strong> Древняя цитадель, веками служившая резиденцией правителей Бухары.",
            "<strong>Хива — Ичан-Кала.</strong> Внутренний город с минаретами и медресе; в 1990 году включён в список "
            "Всемирного наследия ЮНЕСКО.",
            "<strong>Ташкент — телебашня.</strong> В дневном и звёздном ночном виде. Высота башни — 375 метров.",
        ],
        "birds_h": "5 птиц и медали",
        "birds_p": "С ростом рекорда открываются новые птицы, а за результат выдаются медали:",
        "tips_h": "5 советов, чтобы побить рекорд",
        "tips": [
            "<strong>Смотрите не на птицу, а на следующий просвет.</strong> Так вы заранее почувствуете, когда касаться.",
            "<strong>Касайтесь коротко и ритмично.</strong> Частые касания подряд подбрасывают птицу слишком высоко.",
            "<strong>Держитесь середины экрана.</strong> Из центра проще долететь до следующего просвета, чем от края.",
            "<strong>Слушайте ритм.</strong> Звуковые эффекты помогают поймать темп. Если отвлекает — выключите музыку "
            "в настройках.",
            "<strong>Не торопитесь у рекорда.</strong> Многие ошибаются именно от волнения — сохраняйте привычный ритм.",
        ],
        "more_h": "Что ещё есть в игре",
        "more": [
            "<strong>Полностью офлайн</strong> — интернет не нужен: в дороге, в самолёте, где угодно.",
            "<strong>Музыка, звуковые эффекты и вибрация</strong> — каждое можно отдельно включить или выключить.",
            "<strong>3 языка:</strong> русский, узбекский и английский.",
            "<strong>Бесплатно</strong>; чтобы покрывать расходы, показывается реклама.",
            f"Согласно разделу «Безопасность данных» в {GP}, игра <strong>не собирает</strong> данные и <strong>не "
            "передаёт</strong> их третьим лицам. Возрастной рейтинг — 3+, подходит и детям.",
        ],
        "outro": f"Любите логические игры — попробуйте и наше <a href=\"{SUDOKU}\">Судоку</a>. Делитесь рекордами и "
                 f'идеями в отзывах {GP} или в нашем <a href="{TG_CHANNEL}">Telegram-канале</a>.',
    },
    "en": {
        "intro": f"Do you love one-tap games you just can't put down? <strong>“{NAME['en']}”</strong> is a new 3D arcade game from the author of {SITE}. Tap the screen and the little bird "
                 f"flaps its wings — your job is to guide it between the green pipes. The best part: you fly over famous "
                 f"landmarks of Samarkand, Bukhara, Khiva and Tashkent. The game is free on {GP}.",
        "video_h": "Trailer: see it in action",
        "video_p": f'If the video doesn\'t load, <a href="{VIDEO_URL}">watch it on YouTube</a>.',
        "how_h": "How to play",
        "how": [
            "Tap the screen — the bird flaps and rises.",
            "Without taps it falls. Time your taps to pass through the gap between the pipes.",
            "Hitting a pipe or the ground ends the game.",
            "Every pipe you pass is 1 point. Beat your record and share it with friends.",
        ],
        "places_h": "A flight over Uzbekistan's landmarks",
        "places_p": "The backgrounds show famous places in Uzbekistan, so every run feels like a short trip:",
        "places": [
            "<strong>Samarkand — Registan Square.</strong> The famous ensemble of three madrasas: Ulugh Beg, Sher-Dor "
            "and Tilya-Kori.",
            "<strong>Bukhara — the Ark.</strong> An ancient citadel that was the residence of Bukhara's rulers for centuries.",
            "<strong>Khiva — Ichan-Kala.</strong> The walled inner city of minarets and madrasas, a UNESCO World Heritage "
            "Site since 1990.",
            "<strong>Tashkent — the TV Tower.</strong> In daylight and under a starry night sky. The tower is 375 metres tall.",
        ],
        "birds_h": "5 birds and medals",
        "birds_p": "New birds unlock as your high score grows, and you earn medals for your results:",
        "tips_h": "5 tips to beat your high score",
        "tips": [
            "<strong>Watch the next gap, not the bird.</strong> Looking ahead tells you when to tap.",
            "<strong>Tap short and steady.</strong> Rapid taps in a row send the bird too high.",
            "<strong>Stay in the middle of the screen.</strong> It's easier to reach the next gap from the centre than "
            "from an edge.",
            "<strong>Listen to the rhythm.</strong> Sound effects help you keep the beat. If they distract you, turn the "
            "music off in settings.",
            "<strong>Don't rush near your record.</strong> That's when most players slip — keep your usual rhythm.",
        ],
        "more_h": "What else is inside",
        "more": [
            "<strong>100% offline</strong> — no internet needed: on the road, on a plane, anywhere.",
            "<strong>Music, sound effects and vibration</strong> — each can be switched on or off separately.",
            "<strong>3 languages:</strong> English, Uzbek and Russian.",
            "<strong>Free</strong>; ads help cover the costs.",
            f"According to the Data safety section on {GP}, the game <strong>collects no data</strong> and <strong>shares "
            "none</strong> with third parties. Rated 3+, so kids can play too.",
        ],
        "outro": f"If you like logic games, try our <a href=\"{SUDOKU}\">Sudoku</a> too. Share your high score and ideas in a "
                 f'{GP} review or in our <a href="{TG_CHANNEL}">Telegram channel</a>.',
    },
}

ARTICLES = [
    {
        "slug": "flying-bird-qush-parvozi-android-oyini",
        "create": {"categorie_id": 3, "image": "post/images/flying_bird_qush_parvozi.jpg"},
        "name": {"uz": "Flying Bird: Qush Parvozi — O'zbekiston obidalari uzra uchadigan o'yin",
                 "uz_crl": "Flying Bird: Қуш Парвози — Ўзбекистон обидалари узра учадиган ўйин",
                 "ru": "Flying Bird: Полёт Птицы — игра с полётом над достопримечательностями Узбекистана",
                 "en": "Flying Bird: Flap & Fly — a game that flies over Uzbekistan's landmarks"},
        "title": {"uz": "Bir teginish bilan boshqariladigan bepul 3D arkada: Registon, Ark, Ichan-Qal'a va Toshkent teleminorasi, "
                        "5 ta qush, medallar va internetsiz o'yin. Treyler va rekord uchun maslahatlar.",
                  "ru": "Бесплатная 3D-аркада в одно касание: Регистан, Арк, Ичан-Кала и Ташкентская телебашня, 5 птиц, "
                        "медали и игра без интернета. Трейлер и советы для рекорда.",
                  "en": "A free one-tap 3D arcade game: Registan, the Ark, Ichan-Kala and the Tashkent TV Tower, 5 birds, "
                        "medals and offline play. Trailer and tips for a high score."},
        "body": {lang: _body(lang) for lang in LANGS},
        "seo_title": "Flying Bird: Qush Parvozi — bepul Android o'yini",
        "seo_description": "Flying Bird: Qush Parvozi — Samarqand, Buxoro, Xiva va Toshkent obidalari uzra uchadigan bepul "
                           "3D arkada: 5 ta qush, medallar, oflayn o'yin. Treyler va maslahatlar.",
    },
]
