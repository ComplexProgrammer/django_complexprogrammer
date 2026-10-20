"""«O'yinlar» kategoriyasidagi 3 ta maqola — 2026-yil holatiga moslab qayta yozilgan.

- CS 1.6 kodlari: eski ro'yxatdagi ko'p "kodlar" o'yinda mavjud emas edi (sv_aim, gl_zmax, sv_airclan...).
  Endi faqat ishlaydigan buyruqlar, qayerda ishlashi va xavfsizlik ogohlantirishi bilan.
- Ikkita CS:GO maqolasi: 2023-yil 27-sentabrda CS:GO o'rniga Counter-Strike 2 chiqdi. Bittasi yangi
  boshlovchilar uchun amaliy maslahatlar, ikkinchisi — jamoaviy strategiya (iqtisod, rollar, taktika).

Slug'lar o'zgarmaydi: Google'dagi va ulashilgan havolalar ishlashda davom etadi.
"""

LANGS = ("uz", "ru", "en")
CS16 = "/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/"
CS2_TIPS = "/blog/csgo-oyinida-yaxshi-strategiyalar/"
CS2_TEAM = "/blog/csgo-strategiyalari-galabaga-yetaklovchi-kalitlar/"


def _table(rows, head):
    body = "".join(f"<tr><td><code>{cmd}</code></td><td>{text}</td></tr>" for cmd, text in rows)
    return f"<table><thead><tr><th>{head[0]}</th><th>{head[1]}</th></tr></thead><tbody>{body}</tbody></table>"


def _ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def _ol(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


HEAD = {"uz": ("Buyruq", "Nima qiladi"), "ru": ("Команда", "Что делает"), "en": ("Command", "What it does")}


# =====================================================================================================
# 1. Counter-Strike 1.6 kodlari
# =====================================================================================================

CS16_CHEATS = [
    ("sv_cheats 1", {"uz": "Chit-kodlarni yoqadi (avval shu yoziladi)", "ru": "Включает чит-коды (вводится первой)",
                     "en": "Enables cheat codes (type this first)"}),
    ("god", {"uz": "O'lmaslik. Qayta yozilsa o'chadi", "ru": "Бессмертие. Повторный ввод — выключить",
             "en": "God mode. Type again to turn off"}),
    ("noclip", {"uz": "Devorlar orqali uchib yurish", "ru": "Полёт сквозь стены", "en": "Fly through walls"}),
    ("give weapon_awp", {"uz": "Qurol olish: <code>weapon_ak47</code>, <code>weapon_m4a1</code>, <code>weapon_deagle</code>, <code>weapon_hegrenade</code> va h.k.",
                         "ru": "Выдать оружие: <code>weapon_ak47</code>, <code>weapon_m4a1</code>, <code>weapon_deagle</code>, <code>weapon_hegrenade</code> и т.д.",
                         "en": "Give a weapon: <code>weapon_ak47</code>, <code>weapon_m4a1</code>, <code>weapon_deagle</code>, <code>weapon_hegrenade</code>, etc."}),
]
CS16_SERVER = [
    ("mp_startmoney 16000", {"uz": "Boshlang'ich pul (eng ko'pi 16000). Keyingi raunddan ishlaydi",
                             "ru": "Стартовые деньги (максимум 16000). Действует со следующего раунда",
                             "en": "Starting money (max 16000). Applies from the next round"}),
    ("sv_restart 1", {"uz": "O'yinni 1 soniyadan keyin qaytadan boshlash", "ru": "Перезапуск игры через 1 секунду",
                      "en": "Restart the game in 1 second"}),
    ("mp_roundtime 5", {"uz": "Raund davomiyligi, daqiqa", "ru": "Длительность раунда, минуты", "en": "Round length, minutes"}),
    ("mp_freezetime 0", {"uz": "Raund boshidagi kutish vaqti, soniya", "ru": "Заморозка в начале раунда, секунды",
                         "en": "Freeze time at round start, seconds"}),
    ("mp_buytime 2", {"uz": "Qurol sotib olish vaqti, daqiqa", "ru": "Время на покупку, минуты", "en": "Buy time, minutes"}),
    ("mp_c4timer 35", {"uz": "Bomba portlashigacha vaqt, soniya", "ru": "Таймер бомбы, секунды", "en": "Bomb timer, seconds"}),
    ("mp_friendlyfire 0", {"uz": "Sherikka zarar: 0 — o'chiq, 1 — yoqiq", "ru": "Огонь по своим: 0 — выкл, 1 — вкл",
                           "en": "Friendly fire: 0 — off, 1 — on"}),
    ("mp_timelimit 30", {"uz": "Xaritaning umumiy vaqti, daqiqa", "ru": "Время на карту, минуты", "en": "Map time limit, minutes"}),
    ("mp_limitteams 0", {"uz": "Jamoalardagi o'yinchilar farqini cheklamaslik (masalan, 1 ga 10)",
                         "ru": "Не ограничивать разницу игроков в командах (например, 1 против 10)",
                         "en": "No limit on team size difference (e.g. 1 vs 10)"}),
    ("mp_autoteambalance 0", {"uz": "Jamoalarni avtomatik tenglashtirishni o'chirish", "ru": "Выключить автобаланс команд",
                              "en": "Turn off automatic team balance"}),
    ("sv_gravity 800", {"uz": "Gravitatsiya (standart 800). Masalan, 200 da juda baland sakraysiz",
                        "ru": "Гравитация (стандарт 800). Например, при 200 прыжки очень высокие",
                        "en": "Gravity (default 800). At 200 you jump very high"}),
    ("changelevel de_dust2", {"uz": "Xaritani almashtirish", "ru": "Сменить карту", "en": "Change the map"}),
]
CS16_BOTS = [
    ("bot_add", {"uz": "Bot qo'shish (<code>bot_add_ct</code>, <code>bot_add_t</code> — aniq jamoaga)",
                 "ru": "Добавить бота (<code>bot_add_ct</code>, <code>bot_add_t</code> — в нужную команду)",
                 "en": "Add a bot (<code>bot_add_ct</code>, <code>bot_add_t</code> for a specific team)"}),
    ("bot_quota 10", {"uz": "Serverdagi botlar soni", "ru": "Количество ботов на сервере", "en": "Number of bots on the server"}),
    ("bot_difficulty 2", {"uz": "Qiyinlik: 0 — oson … 3 — ekspert", "ru": "Сложность: 0 — лёгкая … 3 — эксперт",
                          "en": "Difficulty: 0 — easy … 3 — expert"}),
    ("bot_kick", {"uz": "Barcha botlarni chiqarish", "ru": "Удалить всех ботов", "en": "Kick all bots"}),
    ("bot_stop 1", {"uz": "Botlarni joyida to'xtatish (mashq uchun qulay)", "ru": "Остановить ботов (удобно для тренировки)",
                    "en": "Freeze bots in place (handy for practice)"}),
    ("bot_knives_only", {"uz": "Botlar faqat pichoq bilan. Shuningdek: <code>bot_pistols_only</code>, <code>bot_snipers_only</code>, <code>bot_all_weapons</code>",
                         "ru": "Боты только с ножами. Также: <code>bot_pistols_only</code>, <code>bot_snipers_only</code>, <code>bot_all_weapons</code>",
                         "en": "Bots use knives only. Also: <code>bot_pistols_only</code>, <code>bot_snipers_only</code>, <code>bot_all_weapons</code>"}),
]
CS16_CLIENT = [
    ("fps_max 100", {"uz": "FPS chegarasi", "ru": "Ограничение FPS", "en": "FPS cap"}),
    ('cl_crosshair_color "50 250 50"', {"uz": "Pricel rangi (RGB)", "ru": "Цвет прицела (RGB)", "en": "Crosshair colour (RGB)"}),
    ("cl_crosshair_size small", {"uz": "Pricel o'lchami: small / medium / large", "ru": "Размер прицела: small / medium / large",
                                 "en": "Crosshair size: small / medium / large"}),
    ("cl_dynamiccrosshair 0", {"uz": "Pricel yugurganda kattalashmaydi", "ru": "Прицел не расширяется при движении",
                               "en": "Crosshair doesn't expand while moving"}),
    ("hud_fastswitch 1", {"uz": "Qurolni bir bosishda almashtirish", "ru": "Смена оружия одним нажатием",
                          "en": "Switch weapons with one key press"}),
    ("cl_righthand 0", {"uz": "Qurol chap qo'lda ko'rinadi", "ru": "Оружие в левой руке", "en": "Show the weapon in the left hand"}),
    ("net_graph 3", {"uz": "FPS va pingni ko'rsatish", "ru": "Показать FPS и пинг", "en": "Show FPS and ping"}),
    ("timeleft", {"uz": "Xaritaning qolgan vaqti", "ru": "Сколько осталось времени на карте", "en": "Time left on the map"}),
]


def _cs16(lang):
    T = {
        "uz": {
            "intro": "Counter-Strike 1.6 chiqqaniga 25 yildan oshdi, lekin u hali ham kompyuter klublarida va kuchsiz noutbuklarda "
                     "eng ko'p o'ynaladigan o'yinlardan biri. Internetdagi «kodlar» ro'yxatlarining ko'pchiligida o'yinda umuman "
                     "mavjud bo'lmagan buyruqlar yozilgan. Quyida faqat ishlaydigan buyruqlar to'plandi.",
            "console": "Konsolni qanday ochish",
            "console_steps": [
                "<b>Options → Keyboard → Advanced</b> bo'limida «Enable developer console» belgisini qo'ying.",
                "O'yin ichida <code>~</code> tugmasini bosing (klaviaturada <b>Ё</b> tugmasi).",
                "Yoki Steam'da: o'yin ustida o'ng tugma → <b>Properties → Launch options</b> → <code>-console</code>.",
            ],
            "where": "Muhim: kodlar qayerda ishlaydi",
            "where_text": "Chit-kodlar faqat o'zingiz yaratgan serverda — <b>New Game</b> yoki LAN orqali, botlar bilan — ishlaydi. "
                          "Onlayn serverlarda ular o'chirilgan. Wallhack, aimbot kabi uchinchi tomon dasturlari esa akkauntni VAC "
                          "orqali bloklanishiga olib keladi va ko'pincha ichida virus bo'ladi — ulardan foydalanmang.",
            "cheats": "Chit-kodlar (<code>sv_cheats 1</code> kerak)",
            "server": "Pul, raund va server sozlamalari",
            "server_note": "Bu buyruqlar ham faqat o'zingizning serveringizda ishlaydi. Pul o'zgarishi kuchga kirishi uchun "
                           "<code>sv_restart 1</code> yozing.",
            "bots": "Botlar bilan mashq",
            "bots_note": "Steam'dagi CS 1.6 da rasmiy botlar bor. Eski (Steam'siz) versiyalarda ular bo'lmasligi mumkin.",
            "client": "Pricel, FPS va qulaylik (har qanday serverda)",
            "save": "Sozlamalarni saqlab qo'yish",
            "save_text": "Har safar qayta yozmaslik uchun bu buyruqlarni <code>cstrike</code> papkasidagi <code>userconfig.cfg</code> "
                         "fayliga har birini alohida qatorga yozing (fayl bo'lmasa, oddiy matn fayli sifatida yarating). "
                         "O'yin ochilganda u avtomatik o'qiladi.",
            "next": "CS 1.6 dan keyin: Counter-Strike 2",
            "next_text": f"Valve 2023-yilda CS:GO o'rniga bepul <b>Counter-Strike 2</b> ni chiqardi. Unga o'tmoqchi bo'lsangiz: "
                         f"<a href=\"{CS2_TIPS}\">CS2 bo'yicha yangi boshlovchilar uchun 10 ta maslahat</a> va "
                         f"<a href=\"{CS2_TEAM}\">CS2 jamoaviy strategiyalari</a>.",
        },
        "ru": {
            "intro": "Counter-Strike 1.6 больше 25 лет, но она до сих пор одна из самых популярных игр в компьютерных клубах и на слабых "
                     "ноутбуках. Во многих списках «кодов» в интернете есть команды, которых в игре просто нет. Ниже — только рабочие команды.",
            "console": "Как открыть консоль",
            "console_steps": [
                "В <b>Options → Keyboard → Advanced</b> включите «Enable developer console».",
                "В игре нажмите <code>~</code> (клавиша <b>Ё</b>).",
                "Или в Steam: правый клик по игре → <b>Properties → Launch options</b> → <code>-console</code>.",
            ],
            "where": "Важно: где работают коды",
            "where_text": "Чит-коды работают только на вашем собственном сервере — через <b>New Game</b> или LAN, с ботами. На онлайн-серверах "
                          "они отключены. Сторонние программы (wallhack, aimbot) приводят к блокировке аккаунта через VAC и часто "
                          "содержат вирусы — не используйте их.",
            "cheats": "Чит-коды (нужен <code>sv_cheats 1</code>)",
            "server": "Деньги, раунды и настройки сервера",
            "server_note": "Эти команды тоже работают только на вашем сервере. Чтобы изменения денег вступили в силу, введите "
                           "<code>sv_restart 1</code>.",
            "bots": "Тренировка с ботами",
            "bots_note": "В Steam-версии CS 1.6 есть официальные боты. В старых (не Steam) сборках их может не быть.",
            "client": "Прицел, FPS и удобство (на любом сервере)",
            "save": "Как сохранить настройки",
            "save_text": "Чтобы не вводить команды каждый раз, запишите их по одной в строке в файл <code>userconfig.cfg</code> в папке "
                         "<code>cstrike</code> (если файла нет — создайте обычный текстовый файл). Игра прочитает его при запуске.",
            "next": "После CS 1.6: Counter-Strike 2",
            "next_text": f"В 2023 году Valve заменила CS:GO бесплатной <b>Counter-Strike 2</b>. Если хотите перейти на неё: "
                         f"<a href=\"{CS2_TIPS}\">10 советов новичкам в CS2</a> и <a href=\"{CS2_TEAM}\">командные стратегии CS2</a>.",
        },
        "en": {
            "intro": "Counter-Strike 1.6 is over 25 years old, yet it is still one of the most played games in internet cafés and on "
                     "low-end laptops. Many “cheat code” lists online include commands that simply don't exist in the game. "
                     "Below are only the commands that actually work.",
            "console": "How to open the console",
            "console_steps": [
                "In <b>Options → Keyboard → Advanced</b>, tick “Enable developer console”.",
                "In game, press <code>~</code>.",
                "Or in Steam: right-click the game → <b>Properties → Launch options</b> → <code>-console</code>.",
            ],
            "where": "Important: where the codes work",
            "where_text": "Cheat codes only work on a server you create yourself — via <b>New Game</b> or LAN, with bots. They are "
                          "disabled on online servers. Third-party programs such as wallhacks or aimbots get your account VAC-banned "
                          "and often contain malware — don't use them.",
            "cheats": "Cheat codes (require <code>sv_cheats 1</code>)",
            "server": "Money, rounds and server settings",
            "server_note": "These also work only on your own server. Type <code>sv_restart 1</code> for money changes to take effect.",
            "bots": "Practising with bots",
            "bots_note": "The Steam version of CS 1.6 has official bots. Older non-Steam builds may not.",
            "client": "Crosshair, FPS and comfort (any server)",
            "save": "Saving your settings",
            "save_text": "To avoid typing them every time, put the commands one per line into <code>userconfig.cfg</code> in the "
                         "<code>cstrike</code> folder (create it as a plain text file if it doesn't exist). The game reads it on start.",
            "next": "After CS 1.6: Counter-Strike 2",
            "next_text": f"In 2023 Valve replaced CS:GO with the free <b>Counter-Strike 2</b>. If you want to move on: "
                         f"<a href=\"{CS2_TIPS}\">10 tips for CS2 beginners</a> and <a href=\"{CS2_TEAM}\">CS2 team strategies</a>.",
        },
    }[lang]
    rows = lambda items: [(cmd, text[lang]) for cmd, text in items]  # noqa: E731
    return "".join([
        f"<p>{T['intro']}</p>",
        f"<h2>{T['console']}</h2>", _ol(T["console_steps"]),
        f"<h2>{T['where']}</h2>", f"<blockquote>{T['where_text']}</blockquote>",
        f"<h2>{T['cheats']}</h2>", _table(rows(CS16_CHEATS), HEAD[lang]),
        f"<h2>{T['server']}</h2>", f"<p>{T['server_note']}</p>", _table(rows(CS16_SERVER), HEAD[lang]),
        f"<h2>{T['bots']}</h2>", f"<p>{T['bots_note']}</p>", _table(rows(CS16_BOTS), HEAD[lang]),
        f"<h2>{T['client']}</h2>", _table(rows(CS16_CLIENT), HEAD[lang]),
        f"<h2>{T['save']}</h2>", f"<p>{T['save_text']}</p>",
        f"<h2>{T['next']}</h2>", f"<p>{T['next_text']}</p>",
    ])


# =====================================================================================================
# 2. CS2: yangi boshlovchilar uchun 10 ta maslahat
# =====================================================================================================

CS2_PRACTICE = [
    ("sv_cheats 1", {"uz": "Mashq buyruqlarini yoqadi", "ru": "Включает тренировочные команды", "en": "Enables practice commands"}),
    ("sv_infinite_ammo 1", {"uz": "Cheksiz o'q va granatalar", "ru": "Бесконечные патроны и гранаты", "en": "Infinite ammo and grenades"}),
    ("mp_buy_anywhere 1", {"uz": "Xaritaning istalgan joyida sotib olish", "ru": "Покупка в любой точке карты", "en": "Buy anywhere on the map"}),
    ("mp_roundtime_defuse 60", {"uz": "Raund vaqti 60 daqiqa — shoshilmasdan o'rganish uchun", "ru": "Раунд на 60 минут — учиться без спешки",
                                "en": "60-minute rounds so you can learn without rushing"}),
    ("sv_rethrow_last_grenade", {"uz": "Oxirgi granatani o'sha joydan qayta otish", "ru": "Повторить последний бросок гранаты",
                                 "en": "Re-throw your last grenade"}),
    ("bot_kick", {"uz": "Botlarni chiqarish", "ru": "Убрать ботов", "en": "Kick bots"}),
    ("mp_restartgame 1", {"uz": "Sozlamalarni qo'llab, o'yinni qayta boshlash", "ru": "Перезапустить игру с новыми настройками",
                          "en": "Restart the game with the new settings"}),
]


def _cs2_tips(lang):
    T = {
        "uz": {
            "intro": "2023-yil 27-sentabrda Valve CS:GO ni <b>Counter-Strike 2</b> bilan almashtirdi. O'yin Source 2 dvigateliga "
                     "ko'chdi, bepul qoldi, CS:GO dagi inventar esa saqlanib qoldi. Yangi grafika, «sub-tick» tizimi va hajmli "
                     "tutunlar paydo bo'ldi, lekin g'alaba asoslari o'zgarmadi. Quyida tezroq o'sish uchun 10 ta amaliy maslahat.",
            "tips": [
                ("Sozlamalarni bir marta to'g'ri qiling",
                 "Past sezgirlik (sensitivity) aniqroq nishon beradi: sichqonchani stol bo'ylab taxminan 30–45 sm surganda 360° "
                 "burilsangiz, yaxshi boshlanish. Pricelni <b>Settings → Game → Crosshair</b> bo'limida sozlang — u yerda "
                 "pro o'yinchilarning pricel kodini import qilish ham mumkin. Kompyuter ko'tarsa, FPS ni monitor chastotasidan "
                 "yuqori ushlang."),
                ("Quloqchin bilan o'ynang",
                 "CS2 da ovoz — eng muhim ma'lumot manbai: qadamlar, qurol qayta o'qlanishi, bomba qo'yilishi. Musiqani "
                 "o'chiring, quloqchin taqing va raqib qayerdan kelayotganini eshitishni o'rganing."),
                ("To'xtab o'q uzing (counter-strafe)",
                 "Yugurayotganda o'qlar sochilib ketadi. Chapga (A) harakatlanayotgan bo'lsangiz, otishdan oldin o'ngga (D) "
                 "qisqa bosing — personaj darhol to'xtaydi va birinchi o'q aniq ketadi."),
                ("Pricel doim bosh balandligida",
                 "Pricelni yerga emas, raqib chiqishi mumkin bo'lgan burchakka va bosh balandligiga qaratib yuring. Shunda "
                 "raqib ko'ringanda sichqonchani kam surasiz."),
                ("Uzoqqa qisqa seriyalar bilan",
                 "AK-47 va M4 da uzoq masofada 2–3 o'qdan otish (tap yoki burst) uzun seriyadan aniqroq. Yaqin masofada esa "
                 "spray chizig'ini Deathmatch'da mashq qiling."),
                ("Har bir granatani o'rganing",
                 "Tutun (smoke) ko'rishni yopadi, flesh ko'zni qamashtiradi, HE zarar beradi, molotov/incendiary joyni egallaydi. "
                 "CS2 da tutun hajmli: HE granata yoki o'qlar uni bir zumga teshadi, molotovni esa tutun o'chiradi."),
                ("Avval 1–2 xaritani chuqur biling",
                 "Hamma xaritani yuzaki bilgandan ko'ra Mirage yoki Dust II ni to'liq bilgan yaxshi: joy nomlari (callout), "
                 "asosiy pozitsiyalar va 3–4 ta foydali tutun."),
                ("Jamoa bilan birga xarid qiling",
                 f"Bir kishi to'liq qurollanib, qolganlar pulsiz qolsa, raund odatda yutqaziladi. Iqtisod haqida batafsil — "
                 f"<a href=\"{CS2_TEAM}\">CS2 jamoaviy strategiyalari</a> maqolasida."),
                ("Har kuni 15 daqiqa mashq",
                 "Deathmatch'da isinib oling, Workshop'dagi aim xaritalarida (masalan, Aim Botz) mashq qiling yoki o'z "
                 "serveringizda quyidagi buyruqlar bilan granatalarni o'rganing."),
                ("Asabni saqlang va halol o'ynang",
                 "Ketma-ket yutqazsangiz, tanaffus qiling. Haqoratli o'yinchilarni ovozsiz qiling (mute). Chit dasturlari "
                 "VAC orqali akkauntni butunlay bloklaydi."),
            ],
            "practice": "Mashq serveri uchun buyruqlar",
            "practice_note": "Avval <b>Settings → Game</b> bo'limida «Enable Developer Console» ni yoqing. Keyin <b>Play</b> menyusidagi mashq (Practice) rejimida xarita oching va <code>~</code> tugmasi bilan konsolga yozing:",
            "ranks": "Reyting qanday ishlaydi",
            "ranks_text": "<b>Premier</b> rejimida raqamli <b>CS Rating</b> beriladi, oddiy <b>Competitive</b> rejimida esa har bir "
                          "xarita uchun alohida unvon bor. Avval Competitive'da 2–3 xaritani o'rganib, keyin Premier'ga o'tish qulay.",
            "outro": f"Klassik CS 1.6 ni ham o'ynasangiz: <a href=\"{CS16}\">CS 1.6 kodlari va konsol buyruqlari</a>.",
        },
        "ru": {
            "intro": "27 сентября 2023 года Valve заменила CS:GO на <b>Counter-Strike 2</b>. Игра перешла на движок Source 2, осталась "
                     "бесплатной, а инвентарь из CS:GO сохранился. Появились новая графика, система «sub-tick» и объёмные дымы, но "
                     "основы победы не изменились. Ниже — 10 практических советов, чтобы расти быстрее.",
            "tips": [
                ("Один раз правильно настройте игру",
                 "Низкая чувствительность даёт точность: хорошая отправная точка — разворот на 360° примерно за 30–45 см движения "
                 "мыши. Прицел настраивается в <b>Settings → Game → Crosshair</b> — там же можно импортировать код прицела "
                 "про-игроков. Если позволяет ПК, держите FPS выше частоты монитора."),
                ("Играйте в наушниках",
                 "Звук в CS2 — главный источник информации: шаги, перезарядка, установка бомбы. Выключите музыку, наденьте "
                 "наушники и учитесь слышать, откуда идёт противник."),
                ("Стреляйте с остановки (counter-strafe)",
                 "На бегу пули разлетаются. Если двигаетесь влево (A), перед выстрелом коротко нажмите вправо (D) — персонаж "
                 "мгновенно остановится, и первая пуля полетит точно."),
                ("Прицел всегда на уровне головы",
                 "Держите прицел не в пол, а в угол, откуда может выйти противник, на уровне головы. Тогда при встрече двигать "
                 "мышь придётся меньше."),
                ("На дальних дистанциях — короткими очередями",
                 "Из AK-47 и M4 на дальней дистанции 2–3 выстрела (тапы или очереди) точнее длинной очереди. Спрей для ближнего "
                 "боя отрабатывайте в Deathmatch."),
                ("Изучите каждую гранату",
                 "Дым закрывает обзор, флешка ослепляет, HE наносит урон, молотов/зажигательная занимает зону. В CS2 дым объёмный: "
                 "HE-граната или выстрелы ненадолго пробивают его, а дым тушит молотов."),
                ("Сначала глубоко выучите 1–2 карты",
                 "Лучше знать Mirage или Dust II полностью, чем все карты поверхностно: названия позиций (коллауты), ключевые "
                 "точки и 3–4 полезных дыма."),
                ("Закупайтесь вместе с командой",
                 f"Если один полностью закупился, а остальные без денег, раунд обычно проигран. Подробно об экономике — в статье "
                 f"<a href=\"{CS2_TEAM}\">командные стратегии CS2</a>."),
                ("15 минут тренировки каждый день",
                 "Разминайтесь в Deathmatch, тренируйтесь на aim-картах из Мастерской (например, Aim Botz) или учите гранаты на "
                 "своём сервере с командами ниже."),
                ("Сохраняйте спокойствие и играйте честно",
                 "После серии поражений сделайте перерыв. Токсичных игроков отключайте (mute). Читы приводят к блокировке "
                 "аккаунта через VAC навсегда."),
            ],
            "practice": "Команды для тренировочного сервера",
            "practice_note": "Сначала включите «Enable Developer Console» в <b>Settings → Game</b>. Затем откройте карту в режиме тренировки (Practice) в меню <b>Play</b> и введите в консоль (клавиша <code>~</code>):",
            "ranks": "Как работает рейтинг",
            "ranks_text": "В режиме <b>Premier</b> выдаётся числовой <b>CS Rating</b>, а в обычном <b>Competitive</b> — отдельное звание "
                          "для каждой карты. Удобно сначала выучить 2–3 карты в Competitive, а потом переходить в Premier.",
            "outro": f"Если играете и в классическую CS 1.6: <a href=\"{CS16}\">коды и консольные команды CS 1.6</a>.",
        },
        "en": {
            "intro": "On 27 September 2023 Valve replaced CS:GO with <b>Counter-Strike 2</b>. The game moved to the Source 2 engine, "
                     "stayed free and kept your CS:GO inventory. It brought new graphics, the “sub-tick” system and volumetric smokes, "
                     "but the fundamentals of winning haven't changed. Here are 10 practical tips to improve faster.",
            "tips": [
                ("Set up your settings once, properly",
                 "Lower sensitivity means better accuracy: a full 360° turn over roughly 30–45 cm of mouse movement is a good "
                 "starting point. Tune your crosshair in <b>Settings → Game → Crosshair</b>, where you can also import pro "
                 "players' crosshair codes. If your PC allows it, keep FPS above your monitor's refresh rate."),
                ("Play with headphones",
                 "Sound is the most important information in CS2: footsteps, reloads, the bomb being planted. Turn off music, "
                 "wear headphones and learn to hear where enemies come from."),
                ("Stop before you shoot (counter-strafe)",
                 "Bullets spread while you run. If you're moving left (A), tap right (D) just before firing — you stop instantly "
                 "and the first bullet is accurate."),
                ("Keep your crosshair at head level",
                 "Aim at the corner an enemy might appear from, at head height, not at the floor. Then you barely need to move "
                 "the mouse when they peek."),
                ("Use short bursts at range",
                 "With the AK-47 and M4, 2–3 shots (taps or bursts) at long range are more accurate than a long spray. Practise "
                 "the spray for close range in Deathmatch."),
                ("Learn every grenade",
                 "Smokes block vision, flashes blind, HEs deal damage, molotovs/incendiaries deny an area. In CS2 smokes are "
                 "volumetric: an HE or bullets briefly clear a hole, and a smoke puts out a molotov."),
                ("Master 1–2 maps first",
                 "Knowing Mirage or Dust II inside out beats knowing every map a little: callouts, key positions and 3–4 useful smokes."),
                ("Buy together with your team",
                 f"If one player full-buys while the rest have no money, the round is usually lost. More on the economy in "
                 f"<a href=\"{CS2_TEAM}\">CS2 team strategies</a>."),
                ("Practise 15 minutes a day",
                 "Warm up in Deathmatch, train on Workshop aim maps (such as Aim Botz), or learn grenades on your own server with "
                 "the commands below."),
                ("Stay calm and play fair",
                 "Take a break after a losing streak. Mute toxic players. Cheats get your account permanently VAC-banned."),
            ],
            "practice": "Commands for a practice server",
            "practice_note": "First enable “Enable Developer Console” in <b>Settings → Game</b>. Then open a map in Practice mode from the <b>Play</b> menu and type in the console (<code>~</code> key):",
            "ranks": "How ranking works",
            "ranks_text": "<b>Premier</b> gives you a numeric <b>CS Rating</b>, while regular <b>Competitive</b> has a separate rank for "
                          "each map. It's easiest to learn 2–3 maps in Competitive first and then move to Premier.",
            "outro": f"If you also play classic CS 1.6: <a href=\"{CS16}\">CS 1.6 codes and console commands</a>.",
        },
    }[lang]
    parts = [f"<p>{T['intro']}</p>"]
    for i, (head, text) in enumerate(T["tips"], 1):
        parts += [f"<h2>{i}. {head}</h2>", f"<p>{text}</p>"]
    parts += [
        f"<h2>{T['practice']}</h2>", f"<p>{T['practice_note']}</p>",
        _table([(cmd, text[lang]) for cmd, text in CS2_PRACTICE], HEAD[lang]),
        f"<h2>{T['ranks']}</h2>", f"<p>{T['ranks_text']}</p>",
        f"<p>{T['outro']}</p>",
    ]
    return "".join(parts)


# =====================================================================================================
# 3. CS2 jamoaviy strategiyalari
# =====================================================================================================

def _cs2_team(lang):
    T = {
        "uz": {
            "intro": "Counter-Strike 2 da kuchli nishon raundni yutadi, jamoaviy reja esa o'yinni. CS2 da o'yin <b>MR12</b> formatida: "
                     "har yarim 12 raund, g'alaba uchun 13 raund kerak. Raundlar CS:GO dagiga qaraganda kam, shuning uchun har bir "
                     "xato — ayniqsa iqtisoddagi xato — qimmatroq tushadi.",
            "eco": "1. Iqtisod: qachon sotib olish, qachon tejash",
            "eco_list": [
                "Har yarimning boshida hamma <b>800$</b> bilan boshlaydi, eng ko'p pul — <b>16 000$</b>.",
                "Yutqazilgan raund uchun bonus ketma-ket mag'lubiyatlarda oshib boradi: <b>1400$</b> dan <b>3400$</b> gacha. "
                "Shuning uchun bitta raundni tejab o'tkazish keyingi raundda to'liq xaridga imkon beradi.",
                "<b>Full buy</b> — miltiq, zirh va granatalar. <b>Eco</b> — deyarli hech narsa olinmaydi. <b>Force buy</b> — "
                "pul yetmasa ham bor pulga xarid; muhim raundlarda (masalan, raqib ham kambag'al bo'lsa) foydali.",
                "Eco raundda SMG yaxshi tanlov: undan o'ldirish uchun mukofot <b>600$</b> (P90 dan tashqari; AWP dan esa atigi <b>100$</b>).",
                "Puli ko'p o'yinchi sherigiga qurol tashlab bersin (drop) — jamoa bir xil kuchda bo'lsin.",
                "Asosiy qoida: <b>jamoa birga xarid qiladi yoki birga tejaydi</b>.",
            ],
            "roles": "2. Jamoadagi rollar",
            "roles_list": [
                "<b>IGL (sardor)</b> — taktikani tanlaydi, iqtisodni boshqaradi, raund davomida qaror qabul qiladi.",
                "<b>Entry</b> — nuqtaga birinchi kiradi va joy ochadi. Sherigi uni darhol «trade» qilishi (qasos olishi) kerak.",
                "<b>AWPer</b> — snayper: uzoq yo'laklarni ushlaydi, raqibning birinchi harakatini to'xtatadi.",
                "<b>Support</b> — tutun va fleshlar bilan sheriklarga yo'l ochadi.",
                "<b>Lurker</b> — xaritaning boshqa tomonida yolg'iz yurib, raqibni chalg'itadi va orqadan zarba beradi.",
            ],
            "t": "3. Hujum (T tomoni)",
            "t_list": [
                "<b>Default</b>: raund boshida shoshilmang — xaritani nazorat qilib, raqib qayerda ekanini aniqlang.",
                "<b>Execute</b>: nuqtaga birga, granatalar bilan kiring — CT pozitsiyalariga tutun, burchaklarga molotov, kirishda flesh.",
                "<b>Fake</b>: bir nuqtaga granata tashlab shovqin qiling, asosiy kuch bilan esa boshqasiga boring.",
                "Bomba qo'yilgach (<b>40 soniya</b> taymer) himoyaga o'ting: bombani ko'rib turadigan, lekin bir-biringizni "
                "qo'llab-quvvatlaydigan joylarni egallang.",
            ],
            "ct": "4. Himoya (CT tomoni)",
            "ct_list": [
                "Ikki nuqtali xaritalarda klassik joylashuv — <b>2-1-2</b>: ikkitadan nuqtalarda, bittasi o'rtada.",
                "Bitta pozitsiyadan ketma-ket bir xil chiqmang — raqib buni tez o'rganadi.",
                "Nuqta yo'qotilsa, yolg'iz qaytmang: jamoa yig'ilib, granatalar bilan birga <b>retake</b> qiling.",
                "Defuse to'plamini (kit) unutmang: bomba u bilan <b>5 soniyada</b>, usiz <b>10 soniyada</b> zararsizlantiriladi.",
            ],
            "comms": "5. Aloqa: qisqa va aniq",
            "comms_text": "Yaxshi xabar — joy, son va holat: «B da ikkita, bittasi 90 HP». Halok bo'lsangiz, tirik o'yinchiga "
                          "xalaqit bermang — faqat zarur ma'lumotni ayting.",
            "review": "6. Xatolar ustida ishlash",
            "review_text": "O'z o'yiningiz yozuvini (demo) ko'ring: qayerda yolg'iz o'lgansiz, qaysi raundda xarid noto'g'ri bo'lgan. "
                           "Professional turnirlarni (masalan, Major) tomosha qilib, jamoalar granatani qanday ishlatishini kuzating.",
            "outro": f"Yangi boshlayotgan bo'lsangiz, avval <a href=\"{CS2_TIPS}\">CS2 bo'yicha 10 ta asosiy maslahat</a> bilan tanishing.",
        },
        "ru": {
            "intro": "В Counter-Strike 2 сильный аим выигрывает раунд, а командный план — матч. Матчи в CS2 идут в формате <b>MR12</b>: "
                     "по 12 раундов в половине, для победы нужно 13. Раундов меньше, чем в CS:GO, поэтому каждая ошибка — особенно "
                     "в экономике — обходится дороже.",
            "eco": "1. Экономика: когда покупать, когда копить",
            "eco_list": [
                "В начале каждой половины у всех <b>800$</b>, максимум денег — <b>16 000$</b>.",
                "Бонус за проигранный раунд растёт с каждым поражением подряд: от <b>1400$</b> до <b>3400$</b>. Поэтому сэкономленный "
                "раунд даёт полную закупку в следующем.",
                "<b>Full buy</b> — винтовка, броня и гранаты. <b>Eco</b> — почти ничего не покупаем. <b>Force buy</b> — закупка на все "
                "деньги, даже если не хватает на полный набор; полезна в важных раундах (например, когда соперник тоже беден).",
                "В эко-раунде хорош SMG: награда за убийство из него <b>600$</b> (кроме P90; а из AWP — всего <b>100$</b>).",
                "У кого много денег — дропните оружие тиммейту, чтобы команда была одинаково сильной.",
                "Главное правило: <b>команда закупается вместе или копит вместе</b>.",
            ],
            "roles": "2. Роли в команде",
            "roles_list": [
                "<b>IGL (капитан)</b> — выбирает тактику, управляет экономикой и принимает решения по ходу раунда.",
                "<b>Entry</b> — заходит на точку первым и открывает пространство. Напарник должен сразу его «разменять».",
                "<b>AWPer</b> — снайпер: держит дальние линии и останавливает первый выход соперника.",
                "<b>Support</b> — дымами и флешками открывает путь союзникам.",
                "<b>Lurker</b> — в одиночку играет на другой стороне карты, отвлекает соперника и бьёт в спину.",
            ],
            "t": "3. Атака (сторона T)",
            "t_list": [
                "<b>Default</b>: не спешите в начале раунда — контролируйте карту и выясните, где соперник.",
                "<b>Execute</b>: заходите на точку вместе и с гранатами — дым на позиции CT, молотовы в углы, флешки на заходе.",
                "<b>Fake</b>: шумите гранатами на одной точке, а основными силами идите на другую.",
                "После установки бомбы (таймер <b>40 секунд</b>) переходите в оборону: занимайте позиции, откуда видно бомбу и "
                "можно прикрывать друг друга.",
            ],
            "ct": "4. Защита (сторона CT)",
            "ct_list": [
                "На картах с двумя точками классическая расстановка — <b>2-1-2</b>: по двое на точках, один в центре.",
                "Не выходите несколько раз подряд с одной позиции — соперник быстро это заметит.",
                "Если точка потеряна, не идите в одиночку: соберитесь и делайте <b>ретейк</b> вместе, с гранатами.",
                "Не забывайте дефьюз-кит: с ним бомба разминируется за <b>5 секунд</b>, без него — за <b>10</b>.",
            ],
            "comms": "5. Коммуникация: коротко и по делу",
            "comms_text": "Хорошая информация — место, количество и состояние: «двое на B, один 90 HP». Если вы погибли, не мешайте живому "
                          "игроку — говорите только важное.",
            "review": "6. Работа над ошибками",
            "review_text": "Смотрите записи (демо) своих матчей: где вы погибли в одиночку, в каком раунде закупка была неверной. "
                           "Смотрите профессиональные турниры (например, мейджоры) и обращайте внимание, как команды используют гранаты.",
            "outro": f"Если вы только начинаете, сначала прочитайте <a href=\"{CS2_TIPS}\">10 базовых советов по CS2</a>.",
        },
        "en": {
            "intro": "In Counter-Strike 2, good aim wins rounds and a team plan wins matches. CS2 matches use <b>MR12</b>: 12 rounds per "
                     "half, 13 to win. There are fewer rounds than in CS:GO, so every mistake — especially an economic one — costs more.",
            "eco": "1. Economy: when to buy and when to save",
            "eco_list": [
                "Everyone starts each half with <b>$800</b>; the money cap is <b>$16,000</b>.",
                "The loss bonus grows with consecutive losses, from <b>$1,400</b> up to <b>$3,400</b>. That's why saving one round "
                "lets you full-buy the next.",
                "<b>Full buy</b> — rifle, armour and grenades. <b>Eco</b> — buy almost nothing. <b>Force buy</b> — spend everything "
                "even without a full kit; useful in key rounds (for example when the enemy is also broke).",
                "SMGs are great on eco rounds: a kill pays <b>$600</b> (except the P90; the AWP pays only <b>$100</b>).",
                "Players with lots of money should drop weapons to teammates so the whole team is equally strong.",
                "The golden rule: <b>the team buys together or saves together</b>.",
            ],
            "roles": "2. Team roles",
            "roles_list": [
                "<b>IGL (in-game leader)</b> — picks the tactic, manages the economy and makes calls during the round.",
                "<b>Entry</b> — goes into the site first and creates space. A teammate must trade them immediately.",
                "<b>AWPer</b> — the sniper: holds long angles and stops the enemy's first push.",
                "<b>Support</b> — opens the way for teammates with smokes and flashes.",
                "<b>Lurker</b> — plays alone on the other side of the map, distracting enemies and hitting them from behind.",
            ],
            "t": "3. Attack (T side)",
            "t_list": [
                "<b>Default</b>: don't rush at round start — take map control and find out where the enemy is.",
                "<b>Execute</b>: hit the site together with utility — smokes on CT positions, molotovs in corners, flashes on entry.",
                "<b>Fake</b>: make noise with grenades on one site, then go to the other with your main force.",
                "After planting (a <b>40-second</b> bomb timer) switch to defence: hold spots where you can see the bomb and cover each other.",
            ],
            "ct": "4. Defence (CT side)",
            "ct_list": [
                "On two-site maps the classic setup is <b>2-1-2</b>: two on each site, one in the middle.",
                "Don't peek from the same position several times in a row — the enemy will notice quickly.",
                "If a site is lost, don't go back alone: regroup and <b>retake</b> together with utility.",
                "Buy a defuse kit: with it the bomb is defused in <b>5 seconds</b>, without it in <b>10</b>.",
            ],
            "comms": "5. Communication: short and clear",
            "comms_text": "Good info is place, number and status: “two B, one is 90 HP”. If you're dead, don't distract the player who's "
                          "still alive — say only what matters.",
            "review": "6. Learning from mistakes",
            "review_text": "Watch your own demos: where did you die alone, which round had the wrong buy? Watch pro tournaments (such as "
                           "the Majors) and note how teams use their utility.",
            "outro": f"If you're just starting, read <a href=\"{CS2_TIPS}\">10 essential CS2 tips</a> first.",
        },
    }[lang]
    return "".join([
        f"<p>{T['intro']}</p>",
        f"<h2>{T['eco']}</h2>", _ul(T["eco_list"]),
        f"<h2>{T['roles']}</h2>", _ul(T["roles_list"]),
        f"<h2>{T['t']}</h2>", _ul(T["t_list"]),
        f"<h2>{T['ct']}</h2>", _ul(T["ct_list"]),
        f"<h2>{T['comms']}</h2>", f"<p>{T['comms_text']}</p>",
        f"<h2>{T['review']}</h2>", f"<p>{T['review_text']}</p>",
        f"<p>{T['outro']}</p>",
    ])


ARTICLES = [
    {
        "slug": "counter-strike-16-oyinida-ishlatiladigan-kodlar",
        "name": {"uz": "Counter-Strike 1.6 kodlari va konsol buyruqlari (2026)",
                 "ru": "Коды и консольные команды Counter-Strike 1.6 (2026)",
                 "en": "Counter-Strike 1.6 cheat codes and console commands (2026)"},
        "title": {"uz": "Botlar bilan mashq, server sozlamalari, pricel va FPS uchun ishlaydigan buyruqlar — tekshirilgan ro'yxat.",
                  "ru": "Рабочие команды для тренировки с ботами, настроек сервера, прицела и FPS — проверенный список.",
                  "en": "Working commands for bot practice, server settings, crosshair and FPS — a checked list."},
        "body": {lang: _cs16(lang) for lang in LANGS},
        "seo_title": "CS 1.6 kodlari va konsol buyruqlari — 2026 ro'yxati",
        "seo_description": "Counter-Strike 1.6 uchun ishlaydigan kodlar: sv_cheats, god, noclip, give, botlar, pul va raund "
                           "sozlamalari, pricel va FPS buyruqlari.",
    },
    {
        "slug": "csgo-oyinida-yaxshi-strategiyalar",
        "name": {"uz": "CS2: yangi boshlovchilar uchun 10 ta maslahat",
                 "ru": "CS2: 10 советов для новичков",
                 "en": "CS2: 10 tips for beginners"},
        "title": {"uz": "CS:GO o'rniga kelgan Counter-Strike 2 da tezroq o'sish: sozlamalar, harakat, nishon, granatalar va mashq.",
                  "ru": "Как быстрее прогрессировать в Counter-Strike 2, сменившей CS:GO: настройки, движение, стрельба, гранаты и тренировка.",
                  "en": "Improve faster in Counter-Strike 2, the successor to CS:GO: settings, movement, aim, grenades and practice."},
        "body": {lang: _cs2_tips(lang) for lang in LANGS},
        "seo_title": "CS2 yangi boshlovchilar uchun: 10 ta maslahat",
        "seo_description": "Counter-Strike 2 da tezroq o'sish: sozlamalar, counter-strafe, pricel, granatalar, xaritalar va "
                           "mashq buyruqlari.",
    },
    {
        "slug": "csgo-strategiyalari-galabaga-yetaklovchi-kalitlar",
        "name": {"uz": "CS2 strategiyalari: iqtisod, rollar va jamoaviy taktika",
                 "ru": "Стратегии CS2: экономика, роли и командная тактика",
                 "en": "CS2 strategies: economy, roles and team tactics"},
        "title": {"uz": "MR12 formatida g'alaba uchun: qachon xarid qilish, kim qaysi rolda o'ynashi, T va CT tomonlarida qanday harakat qilish.",
                  "ru": "Как побеждать в формате MR12: когда закупаться, кто какую роль играет и как действовать за T и CT.",
                  "en": "Winning in MR12: when to buy, who plays which role and how to play the T and CT sides."},
        "body": {lang: _cs2_team(lang) for lang in LANGS},
        "seo_title": "CS2 strategiyalari: iqtisod, rollar va taktika",
        "seo_description": "Counter-Strike 2 jamoaviy strategiyasi: eco va force buy, IGL, entry va AWPer rollari, T va CT "
                           "tomonidagi taktikalar.",
    },
]
