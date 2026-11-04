"""/avtotest/qollanma/ — haydovçilik guvohnomasi imtihoniga tayyorlaniş qöllanmasi (uz, ru, en).

Search Console: "avto test 1000 savol javoblar", "imtihon savollari 2026" kabi sörovlar uçun uzun matnli sahifa.
Raqamlar ({n} savol, {b} bilet, {s} belgi) view'da bazadan qöyiladi; imtihon qoidalari (20 savol, 25 daqiqa,
2 xato) driving.views.EXAM_* bilan bir xil. Tartib va tölovlar özgarişi mumkin bölgani uçun matnda rasmiy
manbaga yönaltiriladi — aniq bilinmagan raqamlar (yoş, tölov summasi, qayta topşiriş muddati) yozilmagan.
"""

GUIDE = {
    "uz": {
        "title": "Haydovçilik imtihoniga qanday tayyorlaniş kerak — {year} qöllanma",
        "desc": "Avtotest imtihoni qanday ötadi, neçta savol va xato mumkin, 4 haftalik tayyorgarlik rejasi va eng köp xato qilinadigan mavzular. Bepul onlayn maşq.",
        "h1": "Haydovçilik imtihoniga tayyorlaniş qöllanmasi",
        "lead": "Nazariy imtihon qanday ötadi, nimani örganiş kerak va saytdagi {n} ta savol bilan qanday maşq qiliş — bir sahifada.",
        "steps_h": "Guvohnoma olişning asosiy bosqiçlari",
        "steps": [
            ("Avtomaktabda ta'lim", "Nazariy (yöl harakati qoidalari, xavfsizlik asoslari, birinçi yordam) va amaliy haydaş maşğulotlari."),
            ("Tibbiy ma'lumotnoma", "Haydovçilikka yaroqlilik haqidagi tibbiy körikdan ötiş."),
            ("Nazariy imtihon", "Kompyuterda test: 20 ta savol, 25 daqiqa, köpi bilan 2 ta xato."),
            ("Amaliy imtihon", "Avtodromda maşqlar va şahar yöllarida haydaş."),
            ("Guvohnomani oliş", "Ikkala imtihondan ötgandan keyin haydovçilik guvohnomasi beriladi."),
        ],
        "steps_note": "Hujjatlar röyxati, yoş talablari va tölovlar özgarib turadi — ularni avtomaktabingizdan yoki IIV rasmiy manbalaridan aniqlaştiring.",
        "exam_h": "Nazariy imtihon qanday ötadi",
        "exam": [
            "Savollar rasmiy savollar bazasidan tasodifiy tanlanadi: saytda {b} ta biletga bölingan {n} ta savol bor.",
            "Har bir savolga bitta javob tanlanadi. 3-xatoda imtihon topşirilmagan hisoblanadi, şuning uçun «taxminan biladigan» savollar ham xavfli.",
            "Köp savollar rasmga asoslangan: yöl belgisi, çorrahadagi vaziyat yoki svetofor işorasi. Matnni oxirigaça öqiş va rasmdagi barça belgilarni köriş muhim.",
        ],
        "plan_h": "4 haftalik tayyorgarlik rejasi",
        "plan": [
            ("1-hafta: asoslar", "Yöl belgilari va çiziqlarini örganing, YHQ'ning umumiy qoidalar boblarini öqing. Har kuni 2–3 ta bilet yeçing."),
            ("2-hafta: mavzular", "Mavzular böyiça savollarni işlang: çorrahalar, ustunlik, svetofor, piyodalar, quvib ötiş. Bir mavzuni 90% dan yuqori natija bilan tugatmasdan keyingisiga ötmang."),
            ("3-hafta: xatolar", "«Xatolarim» bölimida xato qilgan savollaringizni qayta-qayta yeçing — bu eng tez natija beradigan bosqiç. Har bir xato uçun tegişli YHQ bandini öqing."),
            ("4-hafta: imtihon rejimi", "Imtihon simulyatorida (20 savol, 25 daqiqa) kuniga 2–3 marta sinab köring. Ketma-ket 3–5 marta 0–1 xato bilan ötsangiz, haqiqiy imtihonga tayyorsiz."),
        ],
        "topics_h": "Eng köp xato qilinadigan mavzular",
        "topics_lead": "Quyidagi mavzular imtihonda tez-tez uçraydi va nomzodlar köpinça şu yerda adaşadi:",
        "tips_h": "Imtihon kuni uçun maslahatlar",
        "tips": [
            "Savolni va barça variantlarni oxirigaça öqing — «emas», «faqat», «ruxsat etiladimi» kabi sözlar ma'noni butunlay özgartiradi.",
            "Vaqt yetarli: 20 ta savolga 25 daqiqa, ya'ni bitta savolga taxminan 1 daqiqadan ortiq. Şoşilmang.",
            "Bilmagan savolni keyinga qoldiring va oxirida qaytib keling.",
            "Rasmdagi vaziyatni öz haydovçi örningizdan körib, «menga qaysi belgi tegişli?» deb öylang.",
        ],
        "tools_h": "Saytdagi bepul vositalar",
        "faq": [
            ("Nazariy imtihonda neçta savol bor?", "20 ta savol, ularga 25 daqiqa beriladi."),
            ("Neçta xato qiliş mumkin?", "Köpi bilan 2 ta. 3 ta xato qilinsa, imtihon topşirilmagan hisoblanadi."),
            ("Avto test 1000 savol javoblari bilan qayerda bor?", "Saytda barça {n} ta savol töğri javoblari va rasmlari bilan {b} ta biletga bölingan, PDF variantini ham yuklab oliş mumkin."),
            ("Imtihonga tayyorlaniş uçun qança vaqt kerak?", "Kuniga 1–2 soat maşq qilinsa, odatda 3–4 hafta yetarli. Simulyatorda ketma-ket bir neçta marta xatosiz ötiş — tayyorlikning yaxşi belgisi."),
        ],
    },
    "ru": {
        "title": "Как подготовиться к экзамену на права в Узбекистане — гид {year}",
        "desc": "Как проходит теоретический экзамен ПДД, сколько вопросов и ошибок допускается, план подготовки на 4 недели и самые сложные темы. Бесплатная онлайн-практика.",
        "h1": "Как подготовиться к экзамену на водительские права",
        "lead": "Как проходит теоретический экзамен, что учить и как тренироваться на {n} вопросах сайта — на одной странице.",
        "steps_h": "Основные этапы получения прав",
        "steps": [
            ("Обучение в автошколе", "Теория (ПДД, основы безопасности, первая помощь) и практические занятия по вождению."),
            ("Медицинская справка", "Медосмотр о годности к управлению транспортным средством."),
            ("Теоретический экзамен", "Тест на компьютере: 20 вопросов, 25 минут, не более 2 ошибок."),
            ("Практический экзамен", "Упражнения на автодроме и вождение по городу."),
            ("Получение прав", "После сдачи обоих экзаменов выдаётся водительское удостоверение."),
        ],
        "steps_note": "Список документов, требования к возрасту и платежи меняются — уточняйте их в автошколе или на официальных ресурсах МВД.",
        "exam_h": "Как проходит теоретический экзамен",
        "exam": [
            "Вопросы выбираются случайно из официальной базы: на сайте {n} вопросов, разбитых на {b} билетов.",
            "На каждый вопрос выбирается один ответ. На 3-й ошибке экзамен не сдан, поэтому вопросы, которые вы знаете «примерно», тоже опасны.",
            "Многие вопросы основаны на картинке: дорожный знак, ситуация на перекрёстке или сигнал светофора. Важно дочитать текст и рассмотреть все знаки на рисунке.",
        ],
        "plan_h": "План подготовки на 4 недели",
        "plan": [
            ("1-я неделя: основы", "Выучите дорожные знаки и разметку, прочитайте общие главы ПДД. Решайте 2–3 билета в день."),
            ("2-я неделя: темы", "Проработайте вопросы по темам: перекрёстки, приоритет, светофор, пешеходы, обгон. Не переходите к следующей теме, пока не наберёте больше 90%."),
            ("3-я неделя: ошибки", "Решайте вопросы из раздела «Мои ошибки» снова и снова — это самый быстрый способ улучшить результат. К каждой ошибке читайте соответствующий пункт ПДД."),
            ("4-я неделя: режим экзамена", "Проходите симулятор экзамена (20 вопросов, 25 минут) 2–3 раза в день. Если 3–5 раз подряд сдаёте с 0–1 ошибкой — вы готовы."),
        ],
        "topics_h": "Темы, в которых ошибаются чаще всего",
        "topics_lead": "Эти темы часто встречаются на экзамене, и кандидаты чаще всего ошибаются именно в них:",
        "tips_h": "Советы на день экзамена",
        "tips": [
            "Дочитывайте вопрос и все варианты — слова «не», «только», «разрешено ли» полностью меняют смысл.",
            "Времени достаточно: 25 минут на 20 вопросов, то есть больше минуты на вопрос. Не спешите.",
            "Пропустите вопрос, в котором не уверены, и вернитесь к нему в конце.",
            "Смотрите на ситуацию на рисунке с места водителя и спрашивайте себя: «какой знак относится ко мне?»",
        ],
        "tools_h": "Бесплатные инструменты сайта",
        "faq": [
            ("Сколько вопросов на теоретическом экзамене?", "20 вопросов, на них даётся 25 минут."),
            ("Сколько ошибок можно допустить?", "Не более 2. При 3 ошибках экзамен считается не сданным."),
            ("Где найти автотест 1000 вопросов с ответами?", "На сайте все {n} вопросов с правильными ответами и картинками разбиты на {b} билетов, также можно скачать PDF."),
            ("Сколько времени нужно на подготовку?", "При занятиях 1–2 часа в день обычно хватает 3–4 недель. Хороший признак готовности — несколько безошибочных попыток подряд в симуляторе."),
        ],
    },
    "en": {
        "title": "How to prepare for the Uzbekistan driving test — {year} guide",
        "desc": "How the theory exam works, how many questions and mistakes are allowed, a 4-week study plan and the hardest topics. Free online practice.",
        "h1": "How to prepare for the driving licence exam",
        "lead": "How the theory exam works, what to study and how to practise with the {n} questions on this site — on one page.",
        "steps_h": "Main steps to get a licence",
        "steps": [
            ("Driving school", "Theory (traffic rules, safety basics, first aid) and practical driving lessons."),
            ("Medical certificate", "A medical check confirming fitness to drive."),
            ("Theory exam", "A computer test: 20 questions, 25 minutes, at most 2 mistakes."),
            ("Practical exam", "Manoeuvres on a training ground and driving in the city."),
            ("Getting the licence", "After passing both exams the driving licence is issued."),
        ],
        "steps_note": "Required documents, age limits and fees change — check them with your driving school or official Ministry of Internal Affairs sources.",
        "exam_h": "How the theory exam works",
        "exam": [
            "Questions are picked at random from the official question bank: this site has {n} questions split into {b} tickets.",
            "You choose one answer per question. The third mistake fails the exam, so questions you only “roughly” know are risky too.",
            "Many questions are based on a picture: a road sign, a junction situation or a traffic light signal. Read the text to the end and look at every sign in the picture.",
        ],
        "plan_h": "A 4-week study plan",
        "plan": [
            ("Week 1: basics", "Learn road signs and markings and read the general chapters of the traffic rules. Solve 2–3 tickets a day."),
            ("Week 2: topics", "Practise by topic: junctions, right of way, traffic lights, pedestrians, overtaking. Don't move on until you score above 90%."),
            ("Week 3: mistakes", "Solve the questions in “My mistakes” again and again — the fastest way to improve. Read the matching traffic rule for every mistake."),
            ("Week 4: exam mode", "Take the exam simulator (20 questions, 25 minutes) 2–3 times a day. If you pass 3–5 times in a row with 0–1 mistakes, you are ready."),
        ],
        "topics_h": "Topics with the most mistakes",
        "topics_lead": "These topics come up often in the exam and are where candidates most often go wrong:",
        "tips_h": "Tips for exam day",
        "tips": [
            "Read the question and all options to the end — words like “not”, “only” or “is it allowed” change the meaning completely.",
            "There is enough time: 25 minutes for 20 questions, more than a minute each. Don't rush.",
            "Skip a question you are unsure about and come back to it at the end.",
            "Look at the picture from the driver's seat and ask yourself: “which sign applies to me?”",
        ],
        "tools_h": "Free tools on this site",
        "faq": [
            ("How many questions are in the theory exam?", "20 questions, with 25 minutes to answer them."),
            ("How many mistakes are allowed?", "At most 2. With 3 mistakes the exam is failed."),
            ("Where can I find the 1000+ driving test questions with answers?", "This site has all {n} questions with correct answers and pictures, split into {b} tickets; a PDF version can be downloaded too."),
            ("How long does preparation take?", "With 1–2 hours of practice a day, 3–4 weeks is usually enough. Several mistake-free attempts in a row in the simulator are a good sign you are ready."),
        ],
    },
}

# Mavzular sahifalari (driving.topics.TOPICS slug'lari) — Search Console'da körinadigan mavzular
HARD_TOPICS = ("yol-belgilari", "yol-chiziqlari", "svetofor", "piyodalar", "temir-yol-kesishmasi")
