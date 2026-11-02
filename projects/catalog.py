"""/projects/ sahifasi uçun loyihalar katalogi: guruh, 4 tildagi nom va tavsif.

Bazadagi ``Project.title`` / ``sub_title`` faqat bitta tilda (köpi inglizça, ba'zilari slug körinişida:
``general-knowledge``), ``category`` esa "Web project" / "Web Project" kabi tartibsiz. Şu sababli sahifada
körinadigan matn şu yerdan olinadi; katalogda yöq loyiha bazadagi matn bilan "Boşqa" guruhida çiqadi.
"""

from django.utils import translation

GROUPS = {
    "tests": {"uz": "Testlar", "en": "Tests", "ru": "Тесты", "tr": "Testler"},
    "tools": {"uz": "Vositalar", "en": "Tools", "ru": "Инструменты", "tr": "Araçlar"},
    "finance": {"uz": "Moliya", "en": "Finance", "ru": "Финансы", "tr": "Finans"},
    "games": {"uz": "Öyinlar", "en": "Games", "ru": "Игры", "tr": "Oyunlar"},
    "other": {"uz": "Boşqa", "en": "Other", "ru": "Другое", "tr": "Diğer"},
}
GROUP_ORDER = ["tests", "tools", "finance", "games", "other"]

# url -> (guruh, {til: (nom, tavsif)})
CATALOG = {
    "avtotest": ("tests", {
        "uz": ("Avtotest 2026", "Haydovçilik guvohnomasi imtihoniga tayyorgarlik: biletlar, imtihon simulyatori, xatolar ustida işlaş."),
        "en": ("Driving test 2026", "Prepare for the Uzbekistan driving licence exam: tickets, exam simulator, mistake review."),
        "ru": ("Автотест 2026", "Подготовка к экзамену на права: билеты, симулятор экзамена, работа над ошибками."),
        "tr": ("Sürücü sınavı 2026", "Özbekistan ehliyet sınavına hazırlık: biletler, sınav simülatörü, hata tekrarı."),
    }),
    "tests": ("tests", {
        "uz": ("Barça testlar", "Fanlar va mavzular böyiça onlayn testlar: matematika, ingliz tili, umumiy bilim."),
        "en": ("All tests", "Online tests by subject and topic: maths, English, general knowledge."),
        "ru": ("Все тесты", "Онлайн-тесты по предметам и темам: математика, английский, общие знания."),
        "tr": ("Tüm testler", "Konulara göre çevrimiçi testler: matematik, İngilizce, genel kültür."),
    }),
    "tests?topic_id=1": ("tests", {
        "uz": ("Umumiy bilim", "Dunyoqaraşni kengaytiruvçi umumiy bilim savollari."),
        "en": ("General knowledge", "General knowledge quiz questions."),
        "ru": ("Общие знания", "Вопросы на общую эрудицию."),
        "tr": ("Genel kültür", "Genel kültür soruları."),
    }),
    "tests/?type_id=2": ("tests", {
        "uz": ("Maktab testlari", "Maktab öquvçilari uçun fanlar böyiça testlar."),
        "en": ("School tests", "Subject tests for school children."),
        "ru": ("Школьные тесты", "Тесты по предметам для школьников."),
        "tr": ("Okul testleri", "Öğrenciler için ders testleri."),
    }),
    "tests/?type_id=3": ("tests", {
        "uz": ("Avtotest: qöşimça savollar", "Mavzular böyiça guruhlangan qöşimça avtotest savollari."),
        "en": ("Driving test: extra questions", "Additional driving test questions grouped by topic."),
        "ru": ("Автотест: дополнительные вопросы", "Дополнительные вопросы автотеста по темам."),
        "tr": ("Sürücü sınavı: ek sorular", "Konulara göre ek sürücü sınavı soruları."),
    }),
    "password_generator": ("tools", {
        "uz": ("Parol generatori", "Bir zumda kuçli va xavfsiz parol yarating."),
        "en": ("Password generator", "Create strong, secure passwords in seconds."),
        "ru": ("Генератор паролей", "Надёжные пароли за секунду."),
        "tr": ("Şifre oluşturucu", "Saniyeler içinde güçlü şifreler oluşturun."),
    }),
    "pdf_tools": ("tools", {
        "uz": ("PDF vositalar", "PDF ni Word ga aylantiriş va boşqa PDF amallari."),
        "en": ("PDF tools", "Convert PDF to Word and other PDF operations."),
        "ru": ("PDF инструменты", "Конвертация PDF в Word и другие операции."),
        "tr": ("PDF araçları", "PDF'yi Word'e dönüştürme ve diğer işlemler."),
    }),
    "changetext": ("tools", {
        "uz": ("Lotin ↔ Kirill", "Matnni lotin (1995 va 2026) va kirill yozuvlari orasida ögiriş."),
        "en": ("Latin ↔ Cyrillic", "Convert Uzbek text between Latin (1995 and 2026) and Cyrillic."),
        "ru": ("Латиница ↔ Кириллица", "Перевод узбекского текста между латиницей и кириллицей."),
        "tr": ("Latin ↔ Kiril", "Özbekçe metni Latin ve Kiril alfabeleri arasında çevirin."),
    }),
    "translate": ("tools", {
        "uz": ("Tarjimon", "Özbek, rus, ingliz va boşqa tillar orasida tarjima."),
        "en": ("Translator", "Translate between Uzbek, Russian, English and more."),
        "ru": ("Переводчик", "Перевод между узбекским, русским, английским и другими языками."),
        "tr": ("Çevirmen", "Özbekçe, Rusça, İngilizce ve diğer diller arasında çeviri."),
    }),
    "ip": ("tools", {
        "uz": ("IP manzil", "IP manzilingiz va uning joylaşuvini aniqlang."),
        "en": ("IP finder", "Find your IP address and its location."),
        "ru": ("IP-адрес", "Узнайте свой IP-адрес и местоположение."),
        "tr": ("IP bulucu", "IP adresinizi ve konumunu öğrenin."),
    }),
    "imagecompare": ("tools", {
        "uz": ("Rasm soliştiriş", "Ikki rasm orasidagi farqlarni toping."),
        "en": ("Compare pictures", "Spot the differences between two images."),
        "ru": ("Сравнение картинок", "Найдите различия между двумя изображениями."),
        "tr": ("Resim karşılaştırma", "İki resim arasındaki farkları bulun."),
    }),
    "youtube_downloader": ("tools", {
        "uz": ("YouTube yuklovçi", "YouTube videolarini MP4 yoki MP3 formatida yuklab oliş."),
        "en": ("YouTube downloader", "Download YouTube videos as MP4 or MP3."),
        "ru": ("Загрузчик YouTube", "Скачивание видео с YouTube в MP4 или MP3."),
        "tr": ("YouTube indirici", "YouTube videolarını MP4 veya MP3 olarak indirin."),
    }),
    "sitemap": ("tools", {
        "uz": ("Sitemap generator", "Sayt uçun bepul XML sitemap yarating."),
        "en": ("XML sitemap generator", "Free online XML sitemap generator."),
        "ru": ("Генератор Sitemap", "Бесплатный генератор XML карты сайта."),
        "tr": ("Site haritası oluşturucu", "Ücretsiz XML site haritası oluşturucu."),
    }),
    "exchangerates": ("finance", {
        "uz": ("Valyuta kurslari", "Markaziy bank kurslari va valyuta kalkulyatori."),
        "en": ("Exchange rates", "Central Bank of Uzbekistan rates and currency calculator."),
        "ru": ("Курсы валют", "Курсы ЦБ Узбекистана и валютный калькулятор."),
        "tr": ("Döviz kurları", "Özbekistan Merkez Bankası kurları ve döviz hesaplayıcı."),
    }),
    "coins": ("finance", {
        "uz": ("Kripto narxlar", "Kriptovalyutalarning joriy narxlari."),
        "en": ("Crypto prices", "Current cryptocurrency prices."),
        "ru": ("Цены криптовалют", "Актуальные цены криптовалют."),
        "tr": ("Kripto fiyatları", "Güncel kripto para fiyatları."),
    }),
    "market": ("finance", {
        "uz": ("Kripto bozorlar", "BTC, USDT va LTC bozorlari."),
        "en": ("Crypto markets", "BTC, USDT and LTC markets."),
        "ru": ("Криптобиржи", "Рынки BTC, USDT и LTC."),
        "tr": ("Kripto piyasaları", "BTC, USDT ve LTC piyasaları."),
    }),
}

_GAME_DESC = {
    "uz": "Brauzerda bepul onlayn öyin.",
    "en": "Free online browser game.",
    "ru": "Бесплатная онлайн-игра в браузере.",
    "tr": "Ücretsiz tarayıcı oyunu.",
}
for _url, _names in {
    "snake": ("Snake", "Ilon", "Змейка", "Yılan"),
    "car": ("Car Racing", "Maşina poygasi", "Гонки", "Araba yarışı"),
    "duckhunt": ("Duck Hunt", "Ördak ovi", "Утиная охота", "Ördek avı"),
    "motorcycle": ("Motorcycle", "Mototsikl poygasi", "Мотогонки", "Motosiklet"),
    "bubbleshooter": ("Bubble Shooter", "Bubble Shooter", "Bubble Shooter", "Bubble Shooter"),
    "pingpong": ("Ping Pong", "Ping Pong", "Пинг-понг", "Ping Pong"),
    "tictactoe": ("Tic Tac Toe", "X va O", "Крестики-нолики", "XOX"),
    "tetris": ("Tetris", "Tetris", "Тетрис", "Tetris"),
}.items():
    _en, _uz, _ru, _tr = _names
    CATALOG[_url] = ("games", {
        "uz": (_uz, _GAME_DESC["uz"]), "en": (_en, _GAME_DESC["en"]),
        "ru": (_ru, _GAME_DESC["ru"]), "tr": (_tr, _GAME_DESC["tr"]),
    })


def current_lang():
    code = (translation.get_language() or "uz").split("-")[0]
    return code if code in ("uz", "en", "ru", "tr") else "uz"


def annotate(projects, lang=None):
    """Har bir loyihaga ``group``, ``group_label``, ``display_title``, ``display_desc`` qöşadi va guruh böyiça tartiblaydi."""
    lang = lang or current_lang()
    items = list(projects)
    for p in items:
        group, texts = CATALOG.get((p.url or "").strip("/"), ("other", None))
        if texts:
            p.display_title, p.display_desc = texts.get(lang) or texts["uz"]
        else:
            p.display_title = p.title
            # Slug körinişidagi tavsif (general-knowledge) körsatilmaydi
            p.display_desc = "" if p.sub_title and " " not in p.sub_title.strip() else p.sub_title
        p.group = group
        p.group_label = GROUPS[group][lang]
    items.sort(key=lambda p: GROUP_ORDER.index(p.group))  # sort barqaror: guruh içida bazadagi tartib saqlanadi
    return items


def group_labels(lang=None):
    lang = lang or current_lang()
    return [(key, GROUPS[key][lang]) for key in GROUP_ORDER]
