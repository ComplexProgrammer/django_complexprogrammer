"""Sahifalar bo'yicha SEO ma'lumotlari: sarlavha, tavsif, H1, qisqa kirish, matn va FAQ (uz, ru, en).

Turk tili (tr) uchun inglizcha matn ishlatiladi.
- ``title``  — <title> (≈60 belgigacha), qidiruvda ko'rinadigan sarlavha
- ``desc``   — meta description (≈150 belgi), qidiruvda sarlavha ostidagi matn
- ``h1``     — sahifaning asosiy sarlavhasi (sahifada <h1> bo'lmasa chiqariladi)
- ``lead``   — H1 ostidagi qisqa jumla
- ``text``   — [(kichik sarlavha, paragraf), ...] — sahifa pastidagi tushuntirish matni
- ``faq``    — [(savol, javob), ...] — FAQ bloki va FAQPage JSON-LD
``kind``: home | tool | game | page — JSON-LD turini tanlash uchun.
"""

from datetime import date

# Sarlavhalardagi yil har yili o'zi yangilanadi ("avtotest 2027" kabi so'rovlar uchun)
YEAR = date.today().year

PAGES = {
    "/": {
        "kind": "home",
        "uz": {
            "title": "Complex Programmer — avtotest, onlayn vositalar va öyinlar",
            "desc": f"Avtotest {YEAR} biletlari, onlayn tarjimon, lotin-kirill o'girgich, PDF konvertor, valyuta kurslari va bepul o'yinlar — barchasi bitta saytda, ro'yxatdan o'tmasdan.",
            "h1": "Complex Programmer — bepul onlayn vositalar",
            "lead": "Avtotest, tarjimon, PDF konvertor, valyuta kurslari va boşqa foydali xizmatlar.",
            "text": [
                ("Saytda nimalar bor?", "Complex Programmer — kundalik işlarni osonlaştiradigan bepul onlayn vositalar töplami. Haydovçilik guvohnomasi imtihoniga tayyorlaniş uçun avtotest biletlari, 20 dan ortiq tilni qöllab-quvvatlaydigan tarjimon, özbek matnini lotin va kirill yozuvlari örtasida ögiruvçi vosita, PDF faylni Word va Excel'ga ötkaziş, Markaziy bank valyuta kurslari, kriptovalyuta narxlari, kuçli parol generatori va brauzerda öynaladigan öyinlar şu yerda."),
                ("Nega Complex Programmer?", "Barça vositalar bepul, röyxatdan ötişni talab qilmaydi va telefonda ham qulay işlaydi. Sayt özbek, rus, ingliz va turk tillarida mavjud. Blog bölimida dasturlaş va texnologiyalar haqida foydali maqolalar muntazam çop etiladi."),
            ],
            "faq": [
                ("Saytdan foydalaniş pullikmi?", "Yöq, barça vositalar va testlar bepul, röyxatdan ötiş şart emas."),
                ("Avtotestni telefonda işlaş mumkinmi?", "Ha, sayt mobil qurilmalarga moslaştirilgan. Bundan taşqari, Google Play'da Avtotest ilovasi ham bor."),
                ("Sayt qaysi tillarda işlaydi?", "Özbek, rus, ingliz va turk tillarida. Tilni yuqori paneldagi tanlagiç orqali almaştiriş mumkin."),
            ],
        },
        "ru": {
            "title": "Complex Programmer — автотест ПДД, онлайн-инструменты и игры",
            "desc": "Билеты автотеста ПДД Узбекистана, онлайн-переводчик, конвертер латиница-кириллица, PDF в Word, курсы валют ЦБ и бесплатные игры — без регистрации.",
            "h1": "Complex Programmer — бесплатные онлайн-инструменты",
            "lead": "Автотест, переводчик, PDF-конвертер, курсы валют и другие полезные сервисы.",
            "text": [
                ("Что есть на сайте?", "Complex Programmer — набор бесплатных онлайн-инструментов для повседневных задач. Билеты автотеста для подготовки к экзамену на водительские права в Узбекистане, переводчик более чем на 20 языков, конвертер узбекского текста между латиницей и кириллицей, преобразование PDF в Word и Excel, курсы валют Центрального банка, цены криптовалют, генератор надёжных паролей и браузерные игры."),
                ("Почему Complex Programmer?", "Все инструменты бесплатны, не требуют регистрации и удобно работают на телефоне. Сайт доступен на узбекском, русском, английском и турецком языках. В блоге регулярно публикуются статьи о программировании и технологиях."),
            ],
            "faq": [
                ("Сайт платный?", "Нет, все инструменты и тесты бесплатны, регистрация не нужна."),
                ("Можно ли проходить автотест с телефона?", "Да, сайт адаптирован для мобильных устройств. Также есть приложение Avtotest в Google Play."),
                ("На каких языках работает сайт?", "На узбекском, русском, английском и турецком. Язык переключается в верхней панели."),
            ],
        },
        "en": {
            "title": "Complex Programmer — driving test, free online tools and games",
            "desc": "Uzbekistan driving test tickets, online translator, Uzbek Latin–Cyrillic converter, PDF to Word, exchange rates and free browser games — no sign-up needed.",
            "h1": "Complex Programmer — free online tools",
            "lead": "Driving test, translator, PDF converter, exchange rates and more useful services.",
            "text": [
                ("What is on this site?", "Complex Programmer is a collection of free online tools for everyday tasks: Uzbekistan driving licence test tickets, a translator for 20+ languages, an Uzbek Latin–Cyrillic text converter, PDF to Word and Excel conversion, Central Bank exchange rates, cryptocurrency prices, a strong password generator and browser games."),
                ("Why Complex Programmer?", "Every tool is free, needs no registration and works well on phones. The site is available in Uzbek, Russian, English and Turkish, and the blog regularly publishes articles about programming and technology."),
            ],
            "faq": [
                ("Is the site free?", "Yes, all tools and tests are free and no registration is required."),
                ("Can I take the driving test on my phone?", "Yes, the site is mobile-friendly, and there is also an Avtotest app on Google Play."),
                ("Which languages are supported?", "Uzbek, Russian, English and Turkish. Switch the language in the top bar."),
            ],
        },
    },
    "/avtotest/": {
        "kind": "tool",
        "uz": {
            "title": f"Avto test 1000+ savol javoblari {YEAR} — onlayn va PDF",
            "desc": f"Avto test {YEAR}: 1385 ta savol va to'g'ri javoblar, 139 bilet, 20 savollik imtihon simulyatori va PDF yuklab olish. Bepul, ro'yxatdan o'tmasdan.",
            "h1": f"Avto test 1000+ savol javoblari {YEAR}",
            "lead": "Biletni tanlang va haqiqiy imtihondagidek savollarga javob bering.",
            "text": [
                ("Avtotest nima?", "Avtotest — Özbekistonda haydovçilik guvohnomasi oliş uçun topşiriladigan nazariy imtihon. Unda yöl harakati qoidalari, yöl belgilari, çorrahalardan ötiş, birinçi tibbiy yordam va xavfsiz haydaş böyiça savollar beriladi. Bu sahifada 139 ta bilet va 1385 ta savol jamlangan, har bir biletda 10 ta savol bor."),
                ("Qanday tayyorlaniş kerak?", "Har kuni bir neçta biletni işlang va xato qilgan savollaringizni \"Xatolar\" bölimida qayta körib çiqing. Javob belgilangaç, töğri variant darhol körsatiladi. Taymer haqiqiy imtihon şaroitiga könikişga yordam beradi. Savollar özbek (lotin), rus va ingliz tillarida mavjud."),
            ],
            "faq": [
                ("Avtotest imtihonida neçta savol beriladi?", "Imtihonda 20 ta savol beriladi, 25 daqiqa vaqt ajratiladi va köpi bilan 2 ta xato qiliş mumkin. Saytdagi imtihon simulyatori aynan şu formatda işlaydi; biletlarda esa 10 tadan savol bor."),
                ("Avto test savollari va javoblarini PDF'da yuklab olsa böladimi?", "Ha, barça savollar töğri javoblari va rasmlari bilan bitta PDF faylda — \"PDF yuklab oliş\" havolasi orqali bepul yuklab olinadi."),
                ("Biletlar rasmiy imtihondagi savollarga mosmi?", "Biletlar YHQ imtihon savollari asosida tuzilgan va rasmlar bilan birga beriladi."),
                ("Xato qilgan savollarimni qayerda köraman?", "Xatolaringiz brauzerda saqlanadi va \"Xatolar\" sahifasida ularni qayta işlaş mumkin."),
                ("Avtotest ilovasi bormi?", "Ha, Google Play'da \"Avtotest\" ilovasini yuklab olişingiz mumkin."),
            ],
        },
        "ru": {
            "title": f"Автотест 1000+ вопросов и ответов {YEAR} — онлайн и PDF",
            "desc": f"Автотест {YEAR}: 1385 вопросов ПДД Узбекистана с ответами, 139 билетов, симулятор экзамена на 20 вопросов и PDF для скачивания. Бесплатно.",
            "h1": f"Автотест 1000+ вопросов и ответов {YEAR}",
            "lead": "Выберите билет и отвечайте на вопросы как на настоящем экзамене.",
            "text": [
                ("Что такое автотест?", "Автотест — теоретический экзамен для получения водительского удостоверения в Узбекистане. В нём проверяется знание правил дорожного движения, дорожных знаков, проезда перекрёстков, первой помощи и безопасного вождения. Здесь собраны 139 билетов и 1385 вопросов, по 10 вопросов в каждом билете."),
                ("Как готовиться?", "Решайте несколько билетов каждый день и повторяйте вопросы, в которых ошиблись, в разделе «Ошибки». После ответа сразу показывается правильный вариант, а таймер помогает привыкнуть к условиям настоящего экзамена. Вопросы доступны на узбекском, русском и английском языках."),
            ],
            "faq": [
                ("Сколько вопросов на экзамене?", "На экзамене 20 вопросов, на них даётся 25 минут, допускается не более 2 ошибок. Симулятор экзамена на сайте работает в этом формате; в билетах — по 10 вопросов."),
                ("Можно ли скачать вопросы и ответы в PDF?", "Да, все вопросы с правильными ответами и картинками собраны в одном PDF-файле — скачать бесплатно по ссылке «Скачать PDF»."),
                ("Соответствуют ли билеты официальному экзамену?", "Билеты составлены на основе экзаменационных вопросов и сопровождаются иллюстрациями."),
                ("Где посмотреть свои ошибки?", "Ошибки сохраняются в браузере, их можно прорешать заново на странице «Ошибки»."),
                ("Есть ли приложение?", "Да, приложение «Avtotest» доступно в Google Play."),
            ],
        },
        "en": {
            "title": f"Uzbekistan driving test {YEAR} — 1000+ questions and answers",
            "desc": f"Uzbekistan driving test {YEAR}: 1385 questions with answers, 139 tickets, a 20-question exam simulator and a PDF download. Free, no registration.",
            "h1": "Avtotest — Uzbekistan driving exam tickets",
            "lead": "Pick a ticket and answer the questions just like in the real exam.",
            "text": [
                ("What is Avtotest?", "Avtotest is the theory exam for a driving licence in Uzbekistan. It covers traffic rules, road signs, intersections, first aid and safe driving. This page contains 139 tickets and 1385 questions, 10 questions per ticket."),
                ("How to prepare", "Solve a few tickets every day and revisit the questions you got wrong in the Mistakes section. The correct answer is shown right after you choose, and the timer helps you get used to real exam conditions. Questions are available in Uzbek, Russian and English."),
            ],
            "faq": [
                ("How many questions are in the exam?", "The exam has 20 questions, 25 minutes and at most 2 mistakes are allowed. The exam simulator on this site uses the same format; tickets have 10 questions each."),
                ("Can I download the questions and answers as a PDF?", "Yes, all questions with correct answers and pictures are in a single free PDF — use the “Download PDF” link."),
                ("Are the tickets based on the official exam?", "Yes, the tickets are based on the exam questions and include illustrations."),
                ("Where can I review my mistakes?", "Your mistakes are saved in the browser and can be practised again on the Mistakes page."),
                ("Is there a mobile app?", "Yes, the Avtotest app is available on Google Play."),
            ],
        },
    },
    "/tests/": {
        "kind": "tool",
        "uz": {
            "title": "Onlayn testlar — avtotest mavzulari va fanlar böyiça savollar",
            "desc": "Mavzular va kitoblar böyiça onlayn testlar: YHQ mavzulari, taymer, natijalar va xatolar ustida işlaş. Bepul va röyxatdan ötmasdan.",
            "h1": "Onlayn testlar",
            "lead": "Kitob va mavzuni tanlang, söng testni boşlang.",
            "text": [
                ("Testlar qanday işlaydi?", "Testlar kitoblar va mavzular böyiça guruhlangan. Kerakli bölimni tanlab, savollarga javob berasiz; har bir javobdan keyin natija körsatiladi, oxirida esa umumiy ball çiqadi. Xato qilingan savollar alohida saqlanadi."),
            ],
            "faq": [
                ("Testlar bepulmi?", "Ha, barça testlar bepul."),
                ("Natijalarim saqlanadimi?", "Xato qilingan savollar brauzeringizda saqlanadi va ularni qayta işlaş mumkin."),
            ],
        },
        "ru": {
            "title": "Онлайн-тесты — темы ПДД и вопросы по предметам",
            "desc": "Онлайн-тесты по книгам и темам: темы ПДД, таймер, результаты и работа над ошибками. Бесплатно и без регистрации.",
            "h1": "Онлайн-тесты",
            "lead": "Выберите книгу и тему, затем начните тест.",
            "text": [
                ("Как работают тесты?", "Тесты сгруппированы по книгам и темам. Выберите нужный раздел и отвечайте на вопросы: после каждого ответа показывается результат, в конце — общий балл. Вопросы с ошибками сохраняются отдельно."),
            ],
            "faq": [
                ("Тесты бесплатные?", "Да, все тесты бесплатны."),
                ("Сохраняются ли результаты?", "Вопросы с ошибками сохраняются в браузере, их можно прорешать снова."),
            ],
        },
        "en": {
            "title": "Online tests — driving theory topics and subject quizzes",
            "desc": "Online tests by book and topic: driving theory topics, timer, results and mistake review. Free, no registration.",
            "h1": "Online tests",
            "lead": "Choose a book and a topic, then start the test.",
            "text": [
                ("How the tests work", "Tests are grouped by books and topics. Pick a section and answer the questions: you see the result after each answer and your total score at the end. Questions you got wrong are saved separately."),
            ],
            "faq": [
                ("Are the tests free?", "Yes, all tests are free."),
                ("Are my results saved?", "Wrong answers are saved in your browser so you can practise them again."),
            ],
        },
    },
    "/translate/": {
        "kind": "tool",
        "uz": {
            "title": "Onlayn tarjimon — özbek, rus, ingliz va 20+ til, bepul",
            "desc": "Matnni özbek, rus, ingliz, turk va yana 18 ta tilga bepul tarjima qiling. Tilni avtomatik aniqlaş, 5000 belgigaça matn va ovozli öqiş.",
            "h1": "Onlayn tarjimon",
            "lead": "Matnni kiriting, tillarni tanlang — tarjima bir zumda tayyor.",
            "text": [
                ("Qaysi tillar qöllab-quvvatlanadi?", "Tarjimon 22 ta tilni qöllab-quvvatlaydi: özbek, rus, ingliz, turk, qozoq, qirğiz, tojik, turkman, ozarbayjon, nemis, fransuz, ispan, italyan, arab va boşqalar. Manba tilini bilmasangiz, \"Auto\" rejimi uni avtomatik aniqlaydi."),
                ("Qanday foydalaniladi?", "Çap maydonga 5000 belgigaça matn yozing yoki joylaştiring, manba va tarjima tilini tanlang. Natijani bir bosişda nusxalaş yoki ovozli tinglaş mumkin."),
            ],
            "faq": [
                ("Tarjimon bepulmi?", "Ha, röyxatdan ötmasdan bepul foydalaniş mumkin."),
                ("Bir martada qança matn tarjima qilsa böladi?", "Bir sörovda 5000 belgigaça."),
                ("Özbekçadan rusçaga tarjima qilsa böladimi?", "Ha, özbek, rus va ingliz tillari örtasida istalgan yönalişda tarjima qiliş mumkin."),
            ],
        },
        "ru": {
            "title": "Онлайн-переводчик — узбекский, русский, английский и 20+ языков",
            "desc": "Бесплатный перевод текста с узбекского, русского, английского, турецкого и ещё 18 языков. Автоопределение языка, до 5000 символов, озвучка.",
            "h1": "Онлайн-переводчик",
            "lead": "Введите текст, выберите языки — перевод готов мгновенно.",
            "text": [
                ("Какие языки поддерживаются?", "Переводчик поддерживает 22 языка: узбекский, русский, английский, турецкий, казахский, киргизский, таджикский, туркменский, азербайджанский, немецкий, французский, испанский, итальянский, арабский и другие. Режим «Auto» сам определит язык исходного текста."),
                ("Как пользоваться?", "Вставьте до 5000 символов текста, выберите исходный язык и язык перевода. Результат можно скопировать в один клик или прослушать."),
            ],
            "faq": [
                ("Переводчик бесплатный?", "Да, им можно пользоваться бесплатно и без регистрации."),
                ("Сколько текста можно перевести за раз?", "До 5000 символов за один запрос."),
                ("Можно ли переводить с узбекского на русский?", "Да, перевод между узбекским, русским и английским работает в любом направлении."),
            ],
        },
        "en": {
            "title": "Free online translator — Uzbek, Russian, English and 20+ languages",
            "desc": "Translate text between Uzbek, Russian, English, Turkish and 18 more languages for free. Auto language detection, up to 5000 characters, text-to-speech.",
            "h1": "Online translator",
            "lead": "Type your text, choose the languages and get the translation instantly.",
            "text": [
                ("Supported languages", "The translator supports 22 languages including Uzbek, Russian, English, Turkish, Kazakh, Kyrgyz, Tajik, Turkmen, Azerbaijani, German, French, Spanish, Italian and Arabic. The Auto mode detects the source language for you."),
                ("How to use it", "Paste up to 5000 characters, choose the source and target languages, then copy the result with one click or listen to it."),
            ],
            "faq": [
                ("Is the translator free?", "Yes, it is free and requires no registration."),
                ("How much text can I translate at once?", "Up to 5000 characters per request."),
                ("Can I translate Uzbek to English?", "Yes, translation between Uzbek, Russian and English works in every direction."),
            ],
        },
    },
    "/changetext/": {
        "kind": "tool",
        "uz": {
            "title": "Lotin-kirill ögirgiç — özbek matnini lotinga va kirillga ötkaziş",
            "desc": "Özbek matnini kirill yozuvidan lotinga va lotindan kirillga bepul ögiring. Ö, Ğ, ş, ç, ye kabi harflar töğri ötkaziladi.",
            "h1": "Lotin-kirill ögirgiç",
            "lead": "Matnni joylaştiring va yönalişni tanlang: lotin → kirill yoki kirill → lotin.",
            "text": [
                ("Nega maxsus ögirgiç kerak?", "Özbek tilida lotin va kirill alifbolari harfma-harf mos kelmaydi: \"ş\", \"ç\", \"ö\", \"ğ\", \"ye\", \"yo\", \"ts\" kabi birikmalar va söz boşidagi \"e\" alohida qoidalar bilan ögiriladi. Bu vosita şu qoidalarni hisobga oladi, şuning uçun hujjat, maqola yoki xabarni qölda tahrirlaşga hojat qolmaydi."),
                ("Qanday foydalaniladi?", "Matnni maydonga yozing yoki nusxalab joylaştiring, kerakli yönalişni tanlang va natijani bir bosişda nusxalang."),
            ],
            "faq": [
                ("Kirilldan lotinga ögiriş bepulmi?", "Ha, çeklovsiz va bepul."),
                ("Ö va Ğ harflari töğri çiqadimi?", "Ha, özbek lotin alifbosidagi barça harflar töğri ögiriladi."),
            ],
        },
        "ru": {
            "title": "Конвертер латиница — кириллица для узбекского текста",
            "desc": "Бесплатно переводите узбекский текст с кириллицы на латиницу и обратно. Корректно обрабатываются O', G', sh, ch, ye и другие буквы.",
            "h1": "Конвертер узбекского текста: латиница ⇄ кириллица",
            "lead": "Вставьте текст и выберите направление: латиница → кириллица или кириллица → латиница.",
            "text": [
                ("Зачем нужен специальный конвертер?", "Узбекские латиница и кириллица не совпадают побуквенно: сочетания «sh», «ch», «o'», «g'», «ye», «yo», «ts» и «е» в начале слова переводятся по отдельным правилам. Конвертер учитывает эти правила, поэтому документ или сообщение не придётся править вручную."),
                ("Как пользоваться?", "Вставьте текст в поле, выберите направление и скопируйте результат одним кликом."),
            ],
            "faq": [
                ("Это бесплатно?", "Да, без ограничений и бесплатно."),
                ("Правильно ли переводятся O' и G'?", "Да, все буквы узбекского латинского алфавита обрабатываются корректно."),
            ],
        },
        "en": {
            "title": "Uzbek Latin–Cyrillic converter — transliterate Uzbek text online",
            "desc": "Convert Uzbek text from Cyrillic to Latin and back for free. Letters like O', G', sh, ch and ye are handled correctly.",
            "h1": "Uzbek Latin ⇄ Cyrillic converter",
            "lead": "Paste your text and choose the direction: Latin → Cyrillic or Cyrillic → Latin.",
            "text": [
                ("Why a dedicated converter?", "Uzbek Latin and Cyrillic do not map letter-for-letter: combinations like \"sh\", \"ch\", \"o'\", \"g'\", \"ye\", \"yo\", \"ts\" and a word-initial \"e\" follow special rules. This tool applies them, so you do not have to fix the text by hand."),
                ("How to use it", "Paste your text, choose the direction and copy the result with one click."),
            ],
            "faq": [
                ("Is it free?", "Yes, free and unlimited."),
                ("Are O' and G' converted correctly?", "Yes, every letter of the Uzbek Latin alphabet is handled."),
            ],
        },
    },
    "/password_generator/": {
        "kind": "tool",
        "uz": {
            "title": "Parol generatori — kuçli va xavfsiz parol yaratiş onlayn",
            "desc": "Bir bosişda kuçli parol yarating: uzunlik, katta-kiçik harflar, raqamlar va belgilarni tanlang. Parol faqat brauzeringizda yaratiladi.",
            "h1": "Kuçli parol generatori",
            "lead": "Parol uzunligi va belgilar turini tanlang — xavfsiz parol tayyor.",
            "text": [
                ("Kuçli parol qanday böladi?", "Kuçli parol kamida 12–16 belgidan iborat bölib, katta va kiçik harflar, raqamlar hamda maxsus belgilarni öz içiga oladi. Unda ism, tuğilgan sana yoki luğatdagi sözlar bölmasligi kerak. Har bir sayt uçun alohida parol işlating."),
                ("Xavfsizlik", "Parol sizning brauzeringizda yaratiladi va serverga yuborilmaydi. Yaratilgan parolni işonçli parol menejerida saqlaş tavsiya etiladi."),
            ],
            "faq": [
                ("Parol serverda saqlanadimi?", "Yöq, parol faqat brauzeringizda yaratiladi."),
                ("Parol neça belgidan iborat bölişi kerak?", "Kamida 12 belgi, muhim akkauntlar uçun 16 va undan köp belgi tavsiya etiladi."),
            ],
        },
        "ru": {
            "title": "Генератор паролей — создать надёжный пароль онлайн",
            "desc": "Создайте надёжный пароль в один клик: длина, заглавные и строчные буквы, цифры и символы. Пароль генерируется только в вашем браузере.",
            "h1": "Генератор надёжных паролей",
            "lead": "Выберите длину и типы символов — безопасный пароль готов.",
            "text": [
                ("Каким должен быть надёжный пароль?", "Надёжный пароль содержит не менее 12–16 символов: заглавные и строчные буквы, цифры и спецсимволы. В нём не должно быть имён, дат рождения и словарных слов. Для каждого сайта используйте отдельный пароль."),
                ("Безопасность", "Пароль создаётся в вашем браузере и не отправляется на сервер. Храните его в надёжном менеджере паролей."),
            ],
            "faq": [
                ("Сохраняется ли пароль на сервере?", "Нет, пароль генерируется только в браузере."),
                ("Какой длины должен быть пароль?", "Не менее 12 символов, для важных аккаунтов — 16 и больше."),
            ],
        },
        "en": {
            "title": "Password generator — create a strong, secure password online",
            "desc": "Generate a strong password in one click: choose length, upper and lower case, numbers and symbols. Passwords are created only in your browser.",
            "h1": "Strong password generator",
            "lead": "Choose the length and character types to get a secure password.",
            "text": [
                ("What makes a strong password?", "A strong password has at least 12–16 characters and mixes upper and lower case letters, numbers and symbols. Avoid names, birth dates and dictionary words, and use a different password for every site."),
                ("Security", "The password is generated in your browser and never sent to the server. Keep it in a trusted password manager."),
            ],
            "faq": [
                ("Is the password stored on the server?", "No, it is generated only in your browser."),
                ("How long should a password be?", "At least 12 characters; 16 or more for important accounts."),
            ],
        },
    },
    "/exchangerates/": {
        "kind": "tool",
        "uz": {
            "title": "Valyuta kurslari bugun — Özbekiston Markaziy banki kursi",
            "desc": "Dollar, yevro, rubl va boşqa valyutalarning bugungi rasmiy kursi — Özbekiston Respublikasi Markaziy banki ma'lumotlari asosida, kunlik özgariş bilan.",
            "h1": "Valyuta kurslari — Markaziy bank",
            "lead": "Bugungi rasmiy kurslar va ularning kunlik özgarişi.",
            "text": [
                ("Kurslar qayerdan olinadi?", "Kurslar Özbekiston Respublikasi Markaziy bankining (cbu.uz) rasmiy ma'lumotlaridan olinadi va muntazam yangilanadi. Jadvalda AQŞ dollari, yevro, rossiya rubli, qozoq tengesi va boşqa valyutalarning sömdagi qiymati hamda kunlik özgarişi körsatiladi."),
                ("Muhim eslatma", "Markaziy bank kursi rasmiy hisob-kitoblar uçun belgilanadi. Banklarda valyuta sotib oliş va sotiş kurslari undan farq qilişi mumkin."),
            ],
            "faq": [
                ("Dollar kursi qaçon yangilanadi?", "Markaziy bank kurslarni har iş kuni e'lon qiladi; sahifadagi ma'lumot avtomatik yangilanadi."),
                ("Bankdagi kurs nega boşqaça?", "Banklar öz sotib oliş va sotiş kurslarini belgilaydi, Markaziy bank kursi esa rasmiy hisob-kitob kursi hisoblanadi."),
            ],
        },
        "ru": {
            "title": "Курсы валют сегодня — курс ЦБ Республики Узбекистан",
            "desc": "Официальный курс доллара, евро, рубля и других валют к суму на сегодня по данным Центрального банка Узбекистана, с дневным изменением.",
            "h1": "Курсы валют — Центральный банк Узбекистана",
            "lead": "Официальные курсы на сегодня и их дневное изменение.",
            "text": [
                ("Откуда берутся курсы?", "Курсы загружаются из официальных данных Центрального банка Республики Узбекистан (cbu.uz) и регулярно обновляются. В таблице — стоимость доллара США, евро, российского рубля, казахского тенге и других валют в сумах и их дневное изменение."),
                ("Важно", "Курс ЦБ устанавливается для официальных расчётов. Курсы покупки и продажи в банках могут отличаться."),
            ],
            "faq": [
                ("Когда обновляется курс доллара?", "ЦБ публикует курсы каждый рабочий день, данные на странице обновляются автоматически."),
                ("Почему в банке курс другой?", "Банки устанавливают свои курсы покупки и продажи, а курс ЦБ — официальный расчётный."),
            ],
        },
        "en": {
            "title": "Exchange rates today — Central Bank of Uzbekistan",
            "desc": "Today's official exchange rates of the US dollar, euro, rouble and other currencies to the Uzbek sum from the Central Bank of Uzbekistan, with the daily change.",
            "h1": "Exchange rates — Central Bank of Uzbekistan",
            "lead": "Today's official rates and their daily change.",
            "text": [
                ("Where do the rates come from?", "Rates are taken from the official data of the Central Bank of the Republic of Uzbekistan (cbu.uz) and updated regularly. The table shows the value of the US dollar, euro, Russian rouble, Kazakh tenge and other currencies in sum, together with the daily change."),
                ("Note", "The Central Bank rate is used for official settlements; buy and sell rates at commercial banks may differ."),
            ],
            "faq": [
                ("When is the dollar rate updated?", "The Central Bank publishes rates every business day and this page updates automatically."),
                ("Why is the bank rate different?", "Commercial banks set their own buy and sell rates; the Central Bank rate is the official reference."),
            ],
        },
    },
    "/coins/": {
        "kind": "tool",
        "uz": {
            "title": "Kriptovalyuta narxlari onlayn — Bitcoin, Ethereum va boşqalar",
            "desc": "Bitcoin, Ethereum va boşqa kriptovalyutalarning joriy narxi, 24 soatlik özgarişi va bozor kapitalizatsiyasi — CoinGecko ma'lumotlari asosida.",
            "h1": "Kriptovalyuta narxlari",
            "lead": "Eng maşhur kriptovalyutalarning joriy narxlari va özgarişi.",
            "text": [
                ("Ma'lumotlar manbasi", "Narxlar CoinGecko oçiq API'sidan olinadi. Har bir tanga uçun AQŞ dollaridagi narx, 24 soatlik özgariş va bozor kapitalizatsiyasi körsatiladi."),
            ],
            "faq": [
                ("Bitcoin narxi qançalik tez yangilanadi?", "Ma'lumotlar bir neça daqiqada bir marta yangilanadi."),
            ],
        },
        "ru": {
            "title": "Курсы криптовалют онлайн — Bitcoin, Ethereum и другие",
            "desc": "Текущая цена Bitcoin, Ethereum и других криптовалют, изменение за 24 часа и рыночная капитализация по данным CoinGecko.",
            "h1": "Курсы криптовалют",
            "lead": "Текущие цены и изменения самых популярных криптовалют.",
            "text": [
                ("Источник данных", "Цены загружаются из открытого API CoinGecko. Для каждой монеты показаны цена в долларах США, изменение за 24 часа и рыночная капитализация."),
            ],
            "faq": [
                ("Как часто обновляется цена биткоина?", "Данные обновляются раз в несколько минут."),
            ],
        },
        "en": {
            "title": "Cryptocurrency prices — Bitcoin, Ethereum and more",
            "desc": "Live prices of Bitcoin, Ethereum and other cryptocurrencies with 24h change and market cap, powered by CoinGecko data.",
            "h1": "Cryptocurrency prices",
            "lead": "Current prices and changes of the most popular coins.",
            "text": [
                ("Data source", "Prices come from the public CoinGecko API. Each coin shows its USD price, 24-hour change and market capitalisation."),
            ],
            "faq": [
                ("How often is the Bitcoin price updated?", "Data refreshes every few minutes."),
            ],
        },
    },
    "/ip/": {
        "kind": "tool",
        "uz": {
            "title": "IP manzilni aniqlaş — mening IP manzilim qanday?",
            "desc": "Öz IP manzilingizni va istalgan IP'ning joylaşuvi, provayderi, şahri va mamlakatini bepul aniqlang.",
            "h1": "IP manzilni aniqlaş",
            "lead": "Sizning IP manzilingiz va uning joylaşuvi haqida ma'lumot.",
            "text": [
                ("IP manzil nima?", "IP manzil — internetga ulangan qurilmaning raqamli identifikatori. U orqali taxminiy mamlakat, şahar va internet provayderini aniqlaş mumkin. Bu vosita sizning joriy IP manzilingizni körsatadi, şuningdek istalgan IP haqida ma'lumot topişga yordam beradi."),
            ],
            "faq": [
                ("IP orqali aniq manzilni biliş mumkinmi?", "Yöq, IP faqat taxminiy joylaşuvni (şahar yoki mintaqa) körsatadi."),
            ],
        },
        "ru": {
            "title": "Узнать IP адрес — мой IP и геолокация",
            "desc": "Узнайте свой IP-адрес, а также страну, город и провайдера любого IP бесплатно.",
            "h1": "Узнать IP-адрес",
            "lead": "Ваш IP-адрес и информация о его местоположении.",
            "text": [
                ("Что такое IP-адрес?", "IP-адрес — числовой идентификатор устройства в интернете. По нему можно определить примерную страну, город и провайдера. Инструмент показывает ваш текущий IP и позволяет проверить любой другой адрес."),
            ],
            "faq": [
                ("Можно ли по IP узнать точный адрес?", "Нет, IP показывает только примерное местоположение — город или регион."),
            ],
        },
        "en": {
            "title": "What is my IP address? — IP lookup and geolocation",
            "desc": "Find your public IP address and look up the country, city and ISP of any IP for free.",
            "h1": "IP address lookup",
            "lead": "Your IP address and information about its location.",
            "text": [
                ("What is an IP address?", "An IP address is the numeric identifier of a device on the internet. It reveals an approximate country, city and internet provider. This tool shows your current IP and lets you check any other address."),
            ],
            "faq": [
                ("Can an IP reveal my exact address?", "No, an IP only shows an approximate location such as a city or region."),
            ],
        },
    },
    "/imagecompare/": {
        "kind": "tool",
        "uz": {
            "title": "Ikki rasmni soliştiriş — farqlarni onlayn topiş",
            "desc": "Ikki rasmni yuklang va ular orasidagi farqlarni bir zumda köring. Dizayn, skrinşot va fotosuratlarni soliştiriş uçun bepul vosita.",
            "h1": "Ikki rasmni soliştiriş",
            "lead": "Ikkita rasmni yuklang — farq qilgan joylar ajratib körsatiladi.",
            "text": [
                ("Qaçon foydali?", "Vosita dizayn maketini tayyor sahifa bilan, eski va yangi skrinşotni yoki ikki fotosuratni soliştirişda yordam beradi. Rasmlar piksel darajasida taqqoslanadi va farqlar ajratib körsatiladi."),
            ],
            "faq": [
                ("Qaysi formatlar qöllab-quvvatlanadi?", "JPG, PNG va WebP kabi keng tarqalgan rasm formatlari."),
            ],
        },
        "ru": {
            "title": "Сравнение двух изображений — найти отличия онлайн",
            "desc": "Загрузите две картинки и сразу увидите различия между ними. Бесплатный инструмент для сравнения макетов, скриншотов и фото.",
            "h1": "Сравнение двух изображений",
            "lead": "Загрузите две картинки — отличающиеся места будут выделены.",
            "text": [
                ("Когда это полезно?", "Инструмент помогает сравнить макет с готовой страницей, старый и новый скриншот или две фотографии. Изображения сравниваются попиксельно, различия подсвечиваются."),
            ],
            "faq": [
                ("Какие форматы поддерживаются?", "Распространённые форматы: JPG, PNG и WebP."),
            ],
        },
        "en": {
            "title": "Compare two images — find differences online",
            "desc": "Upload two images and instantly see the differences. A free tool for comparing designs, screenshots and photos.",
            "h1": "Compare two images",
            "lead": "Upload two pictures and the differences are highlighted.",
            "text": [
                ("When is it useful?", "Compare a design mock-up with the finished page, an old and new screenshot, or two photos. Images are compared pixel by pixel and differences are highlighted."),
            ],
            "faq": [
                ("Which formats are supported?", "Common image formats such as JPG, PNG and WebP."),
            ],
        },
    },
    "/sitemap/": {
        "kind": "tool",
        "uz": {
            "title": "Sitemap generator — sayt xaritasi (sitemap.xml) yaratiş",
            "desc": "Sayt manzilini kiriting va Google hamda Yandex uçun tayyor sitemap.xml faylini bepul yarating.",
            "h1": "Sitemap generator",
            "lead": "Sayt manzilini kiriting — sitemap.xml avtomatik tuziladi.",
            "text": [
                ("Sitemap nima uçun kerak?", "sitemap.xml — saytdagi sahifalar röyxati bölib, qidiruv tizimlariga sahifalarni tezroq topiş va indekslaşga yordam beradi. Generator saytingizdagi havolalarni aylanib çiqadi va standartga mos XML fayl tayyorlaydi. Faylni sayt ildiziga joylab, Google Search Console va Yandex Webmaster'ga yuboring."),
            ],
            "faq": [
                ("Sitemap'ni qayerga joylaş kerak?", "Odatda sayt ildiziga: https://sayt.uz/sitemap.xml, söng uni robots.txt'da körsatiş tavsiya etiladi."),
            ],
        },
        "ru": {
            "title": "Генератор sitemap.xml — создать карту сайта онлайн",
            "desc": "Введите адрес сайта и бесплатно получите готовый файл sitemap.xml для Google и Яндекса.",
            "h1": "Генератор карты сайта",
            "lead": "Введите адрес сайта — sitemap.xml будет составлен автоматически.",
            "text": [
                ("Зачем нужен sitemap?", "sitemap.xml — список страниц сайта, который помогает поисковым системам быстрее находить и индексировать страницы. Генератор обходит ссылки на вашем сайте и формирует XML-файл по стандарту. Разместите его в корне сайта и отправьте в Google Search Console и Яндекс Вебмастер."),
            ],
            "faq": [
                ("Где разместить sitemap?", "Обычно в корне сайта: https://site.uz/sitemap.xml, и указать его в robots.txt."),
            ],
        },
        "en": {
            "title": "Sitemap generator — create sitemap.xml online",
            "desc": "Enter a website address and get a ready-to-use sitemap.xml for Google and Yandex for free.",
            "h1": "XML sitemap generator",
            "lead": "Enter a website address and the sitemap.xml is built automatically.",
            "text": [
                ("Why do you need a sitemap?", "sitemap.xml lists your site's pages and helps search engines discover and index them faster. The generator crawls the links on your site and produces a standards-compliant XML file. Upload it to your site root and submit it in Google Search Console and Yandex Webmaster."),
            ],
            "faq": [
                ("Where should the sitemap go?", "Usually at the site root, e.g. https://example.com/sitemap.xml, referenced from robots.txt."),
            ],
        },
    },
    "/pdf_tools/": {
        "kind": "tool",
        "uz": {
            "title": "PDF ni Word, Excel va rasmga ötkaziş — onlayn, bepul",
            "desc": "PDF faylni Word (DOCX), Excel (CSV) yoki rasmga (JPG) bepul ötkazing. Faylni yuklang va natijani bir zumda yuklab oling.",
            "h1": "PDF konvertor",
            "lead": "PDF faylni Word, Excel yoki rasm formatiga ötkazing.",
            "text": [
                ("Qanday işlaydi?", "Kerakli amalni tanlang (PDF → Word, PDF → Excel yoki PDF → rasm), faylni yuklang va tayyor natijani yuklab oling. Matn va jadvallar tahrirlanadigan körinişda saqlanadi."),
                ("Fayllar xavfsizligi", "Yuklangan fayllar faqat konvertatsiya uçun işlatiladi va vaqtinçalik saqlanadi."),
            ],
            "faq": [
                ("PDF'ni Word'ga ötkaziş bepulmi?", "Ha, röyxatdan ötmasdan bepul."),
                ("Jadvallar Excel'ga töğri ötadimi?", "Matnli PDF'dagi jadvallar Excel ustunlariga ajratiladi; skanerlangan PDF'lar uçun natija sifati pastroq bölişi mumkin."),
            ],
        },
        "ru": {
            "title": "PDF в Word, Excel и картинки — онлайн и бесплатно",
            "desc": "Бесплатно конвертируйте PDF в Word (DOCX), Excel (CSV) или изображения (JPG). Загрузите файл и сразу скачайте результат.",
            "h1": "PDF-конвертер",
            "lead": "Преобразуйте PDF в Word, Excel или изображения.",
            "text": [
                ("Как это работает?", "Выберите действие (PDF → Word, PDF → Excel или PDF → изображение), загрузите файл и скачайте готовый результат. Текст и таблицы сохраняются в редактируемом виде."),
                ("Безопасность файлов", "Загруженные файлы используются только для конвертации и хранятся временно."),
            ],
            "faq": [
                ("Конвертация PDF в Word бесплатна?", "Да, бесплатно и без регистрации."),
                ("Правильно ли переносятся таблицы в Excel?", "Таблицы из текстовых PDF разбиваются по столбцам; для сканов качество может быть ниже."),
            ],
        },
        "en": {
            "title": "Convert PDF to Word, Excel and images — free online",
            "desc": "Convert PDF to Word (DOCX), Excel (CSV) or images (JPG) for free. Upload a file and download the result instantly.",
            "h1": "PDF converter",
            "lead": "Turn a PDF into Word, Excel or image files.",
            "text": [
                ("How it works", "Choose an action (PDF → Word, PDF → Excel or PDF → image), upload your file and download the result. Text and tables are kept editable."),
                ("File security", "Uploaded files are used only for the conversion and stored temporarily."),
            ],
            "faq": [
                ("Is PDF to Word free?", "Yes, free and without registration."),
                ("Are tables converted to Excel correctly?", "Tables in text-based PDFs are split into columns; scanned PDFs may give lower quality."),
            ],
        },
    },
    "/youtube_downloader/": {
        "kind": "tool",
        "uz": {
            "title": "YouTube video yuklab oliş — onlayn, bepul",
            "desc": "YouTube videoni havolasi orqali yuklab oling: sifatni tanlang va faylni qurilmangizga saqlang.",
            "h1": "YouTube video yuklab oliş",
            "lead": "Video havolasini joylaştiring va formatni tanlang.",
            "text": [
                ("Qanday foydalaniladi?", "YouTube'dan video havolasini nusxalang, maydonga joylaştiring, kerakli formatni tanlang va faylni yuklab oling. Faqat özingizga tegişli yoki yuklab olişga ruxsat berilgan videolarni yuklab oling."),
            ],
            "faq": [],
        },
        "ru": {
            "title": "Скачать видео с YouTube — онлайн и бесплатно",
            "desc": "Скачивайте видео с YouTube по ссылке: выберите качество и сохраните файл на устройство.",
            "h1": "Скачать видео с YouTube",
            "lead": "Вставьте ссылку на видео и выберите формат.",
            "text": [
                ("Как пользоваться?", "Скопируйте ссылку на видео YouTube, вставьте её в поле, выберите формат и скачайте файл. Скачивайте только собственные видео или те, на которые есть разрешение."),
            ],
            "faq": [],
        },
        "en": {
            "title": "YouTube video downloader — free online",
            "desc": "Download a YouTube video by link: choose the quality and save the file to your device.",
            "h1": "YouTube video downloader",
            "lead": "Paste the video link and choose a format.",
            "text": [
                ("How to use it", "Copy a YouTube video link, paste it into the field, choose a format and download the file. Only download videos you own or have permission to download."),
            ],
            "faq": [],
        },
    },
    "/instagram-downloader/": {
        "kind": "tool",
        "uz": {"title": "Instagram yuklab oliş", "desc": "Instagram post va videolarini yuklab oliş vositasi.", "h1": "Instagram yuklab oliş"},
        "ru": {"title": "Скачать из Instagram", "desc": "Инструмент для скачивания постов и видео из Instagram.", "h1": "Скачать из Instagram"},
        "en": {"title": "Instagram downloader", "desc": "A tool for downloading Instagram posts and videos.", "h1": "Instagram downloader"},
    },
    "/blog/": {
        "kind": "page",
        "uz": {"title": "Blog — dasturlaş va texnologiyalar böyiça maqolalar", "desc": "Dasturlaş, veb-texnologiyalar, kiberxavfsizlik va foydali vositalar haqida özbek tilida maqolalar."},
        "ru": {"title": "Блог — статьи о программировании и технологиях", "desc": "Статьи о программировании, веб-технологиях, кибербезопасности и полезных инструментах."},
        "en": {"title": "Blog — programming and technology articles", "desc": "Articles about programming, web technologies, cybersecurity and useful tools."},
    },
    "/news/": {
        "kind": "page",
        "uz": {"title": "Yangiliklar — texnologiya va IT yangiliklari", "desc": "Texnologiya, kriptovalyuta va IT sohasidagi sönggi yangiliklar."},
        "ru": {"title": "Новости — технологии и IT", "desc": "Последние новости технологий, криптовалют и IT."},
        "en": {"title": "News — technology and IT", "desc": "The latest news on technology, cryptocurrency and IT."},
    },
    "/projects/": {
        "kind": "page",
        "uz": {"title": "Loyihalar va onlayn öyinlar — Complex Programmer", "desc": "Brauzerda bepul öynaladigan öyinlar (Snake, Tetris, Ping Pong, Tic Tac Toe) va boşqa loyihalar."},
        "ru": {"title": "Проекты и онлайн-игры — Complex Programmer", "desc": "Бесплатные браузерные игры (Snake, Tetris, Ping Pong, крестики-нолики) и другие проекты."},
        "en": {"title": "Projects and online games — Complex Programmer", "desc": "Free browser games (Snake, Tetris, Ping Pong, Tic Tac Toe) and other projects."},
    },
    "/arxiv/": {
        "kind": "page",
        "uz": {"title": "Arxiv — hujjatlar va patentlar", "desc": "Hujjatlar, ilmiy işlar va patentlar arxivi."},
        "ru": {"title": "Архив — документы и патенты", "desc": "Архив документов, научных работ и патентов."},
        "en": {"title": "Archive — documents and patents", "desc": "An archive of documents, papers and patents."},
    },
    "/markets/": {
        "kind": "page",
        "uz": {"title": "Bozorlar — dökonlar va mahsulotlar", "desc": "Dökonlar va mahsulotlar katalogi.", "h1": "Bozorlar"},
        "ru": {"title": "Рынки — магазины и товары", "desc": "Каталог магазинов и товаров.", "h1": "Рынки"},
        "en": {"title": "Markets — stores and products", "desc": "A catalogue of stores and products.", "h1": "Markets"},
    },
    "/cryptomarket/": {
        "kind": "page",
        "uz": {"title": "BTC bozori — kriptovalyuta birjalari", "desc": "Bitcoin va kriptovalyuta bozorlari böyiça ma'lumotlar.", "h1": "BTC bozorlari"},
        "ru": {"title": "Рынки BTC — криптобиржи", "desc": "Данные о рынках биткоина и криптовалют.", "h1": "Рынки BTC"},
        "en": {"title": "BTC markets — crypto exchanges", "desc": "Bitcoin and cryptocurrency market data.", "h1": "BTC markets"},
    },
    "/terms/": {
        "kind": "page",
        "uz": {"title": "Foydalaniş şartlari — Complex Programmer", "desc": "Complex Programmer saytidan foydalaniş şartlari.", "h1": "Foydalaniş şartlari"},
        "ru": {"title": "Условия использования — Complex Programmer", "desc": "Условия использования сайта Complex Programmer.", "h1": "Условия использования"},
        "en": {"title": "Terms of Service — Complex Programmer", "desc": "Terms of use of the Complex Programmer website.", "h1": "Terms of Service"},
    },
    "/privacy/": {
        "kind": "page",
        "uz": {"title": "Maxfiylik siyosati — Complex Programmer", "desc": "Complex Programmer saytining maxfiylik siyosati."},
        "ru": {"title": "Политика конфиденциальности — Complex Programmer", "desc": "Политика конфиденциальности сайта Complex Programmer."},
        "en": {"title": "Privacy Policy — Complex Programmer", "desc": "Privacy policy of the Complex Programmer website."},
    },
}

# O'yinlar: nomi bir xil, tavsif shabloni tilga qarab
GAMES = {
    "/snake/": "Snake",
    "/snake2/": "Snake 2",
    "/tetris/": "Tetris",
    "/tictactoe/": "Tic Tac Toe",
    "/pingpong/": "Ping Pong",
    "/car/": "Car Racing",
    "/duckhunt/": "Duck Hunt",
    "/motorcycle/": "Motorcycle",
    "/bubbleshooter/": "Bubble Shooter",
}
for _path, _name in GAMES.items():
    PAGES[_path] = {
        "kind": "game",
        "uz": {
            "title": f"{_name} — onlayn öynaş bepul",
            "desc": f"{_name} öyinini brauzerda yuklab olmasdan va röyxatdan ötmasdan bepul öynang. Kompyuter va telefonda işlaydi.",
            "h1": f"{_name} — onlayn öyin",
        },
        "ru": {
            "title": f"{_name} — играть онлайн бесплатно",
            "desc": f"Играйте в {_name} прямо в браузере бесплатно, без скачивания и регистрации. Работает на компьютере и телефоне.",
            "h1": f"{_name} — онлайн-игра",
        },
        "en": {
            "title": f"{_name} — play online for free",
            "desc": f"Play {_name} in your browser for free, with no download or sign-up. Works on desktop and mobile.",
            "h1": f"{_name} — online game",
        },
    }

# Avtotest biletlari (/avtotest/<n>/) uchun shablon
BILET = {
    "uz": {
        "title": "Avtotest {n}-bilet — YHQ imtihon savollari va javoblari",
        "desc": "Avtotest {n}-bilet: 10 ta savol, rasmlar va töğri javoblar. Haydovçilik guvohnomasi imtihoniga onlayn tayyorlaning.",
        "h1": "Avtotest — {n}-bilet",
    },
    "ru": {
        "title": "Автотест билет {n} — вопросы и ответы ПДД Узбекистана",
        "desc": "Билет {n} автотеста: 10 вопросов с картинками и правильными ответами. Готовьтесь к экзамену на права онлайн.",
        "h1": "Автотест — билет {n}",
    },
    "en": {
        "title": "Avtotest ticket {n} — Uzbekistan driving test questions",
        "desc": "Driving test ticket {n}: 10 questions with pictures and correct answers. Prepare for the Uzbekistan licence exam online.",
        "h1": "Avtotest — ticket {n}",
    },
}

# Sarlavhalar uchun tarjimalar (breadcrumb, FAQ bloki)
LABELS = {
    "uz": {"home": "Boş sahifa", "faq": "Köp beriladigan savollar", "games": "Öyinlar"},
    "ru": {"home": "Главная", "faq": "Частые вопросы", "games": "Игры"},
    "en": {"home": "Home", "faq": "Frequently asked questions", "games": "Games"},
}
