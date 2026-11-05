"""/projects/ dagi test loyihalari haqidagi maqolalar (manage.py publish_project_posts).

``[[...]]`` — kirillga ögirilmaydigan nom (brend, qisqartma): matnda <span translate="no"> ga aylanadi.
``project_id`` — maqola qaysi /projects/ loyihasi uçun (Project.id).
"""

ARTICLES = [
    # ==========================================================================
    # 30 · Tests — umumiy bölim
    # ==========================================================================
    {
        "project_id": 30,
        "slug": "onlayn-testlar-maktab-fanlari-avtotest-cdl",
        "source_url": "https://complexprogrammer.uz/tests/",
        "categorie_id": 1,
        "image": "projects/images/test.png",
        "seo_title": "Onlayn testlar: maktab fanlari, avtotest va CDL — bepul",
        "seo_description": "Bepul onlayn testlar: 11 ta maktab fani, avtotest va e-avtomaktab biletlari, AQŞ CDL savollari. Javobdan keyin natija, xatolar ustida işlaş, 3 til.",
        "name": {
            "uz": "Onlayn testlar: maktab fanlari, avtotest va [[CDL]] savollari bir joyda",
            "ru": "Онлайн-тесты: школьные предметы, автотест и вопросы CDL в одном месте",
            "en": "Online tests: school subjects, driving test and CDL questions in one place",
        },
        "title": {
            "uz": "5 mingdan ortiq savol, darhol natija va xatolar ustida işlaş — röyxatdan ötmasdan, bepul.",
            "ru": "Более 5 тысяч вопросов, мгновенный результат и работа над ошибками — бесплатно и без регистрации.",
            "en": "Over 5,000 questions, instant results and mistake review — free, no sign-up.",
        },
        "body": {
            "uz": """
<p><a href="/tests/">Testlar</a> bölimi — bilimini tekşirmoqçi bölgan öquvçilar, haydovçilik guvohnomasiga tayyorlanayotganlar va AQŞda yuk maşinasi haydovçisi bölmoqçi bölganlar uçun bepul onlayn test platformasi. Savollar kitoblar va mavzular böyiça guruhlangan: keraklisini tanlaysiz va darhol boşlaysiz.</p>

<h2>Bölimda qanday testlar bor</h2>
<table>
  <thead><tr><th>Yönaliş</th><th>Nima bor</th><th>Savollar</th></tr></thead>
  <tbody>
    <tr><td><a href="/tests/?type_id=2">Maktab fanlari</a></td><td>Ona tili, adabiyot, matematika, algebra, ingliz tili, kimyo, geografiya, tarix va boşqalar — 11 fan</td><td>3 300+</td></tr>
    <tr><td><a href="/tests/?book_id=49">Avto test</a></td><td>108 ta bilet, rasmli savollar</td><td>1 080</td></tr>
    <tr><td><a href="/tests/?book_id=50">e-avtomaktab</a></td><td>31 ta bilet</td><td>305</td></tr>
    <tr><td><a href="/tests/?topic_id=1">[[CDL General Knowledge]]</a></td><td>AQŞ yuk maşinasi guvohnomasi nazariy imtihoni</td><td>191</td></tr>
  </tbody>
</table>

<h2>Qanday işlaydi</h2>
<ol>
  <li>Yönaliş va kitobni tanlang, söng mavzu yoki biletni oçing.</li>
  <li>Har bir savolga javob bering — töğri yoki notöğri ekani darhol körsatiladi.</li>
  <li>Oxirida umumiy natija çiqadi.</li>
  <li>Xato qilingan savollar brauzeringizda saqlanadi: ularni <a href="/tests/xatolar/">Xatolar</a> sahifasida qayta işlab, mustahkamlaysiz.</li>
</ol>

<h2>Nimasi qulay</h2>
<ul>
  <li><strong>Bepul va röyxatdan ötmasdan</strong> — sahifani oçib, darhol boşlaş mumkin.</li>
  <li><strong>3 til:</strong> savollar özbek, rus va ingliz tillarida (avtotest va [[CDL]] uçun ham).</li>
  <li><strong>Telefonda qulay:</strong> sahifa mobil ekranga moslaştirilgan.</li>
</ul>

<h2>Batafsil</h2>
<ul>
  <li><a href="/blog/maktab-oquvchilari-uchun-onlayn-testlar/">Maktab öquvçilari uçun onlayn testlar: 11 fan</a></li>
  <li><a href="/blog/e-avtomaktab-va-avto-test-savollari-biletlar-boyicha/">e-avtomaktab va avto test savollari biletlar böyiça</a></li>
  <li><a href="/blog/cdl-general-knowledge-testi-ozbek-tilida/">[[CDL General Knowledge]] testi özbek tilida</a></li>
</ul>
<p>Haydovçilik imtihoniga tayyorlanayotgan bölsangiz, <a href="/avtotest/">Avtotest</a> bölimidagi 20 savollik imtihon simulyatorini ham sinab köring.</p>
""",
            "ru": """
<p>Раздел <a href="/tests/">«Тесты»</a> — бесплатная онлайн-платформа для школьников, будущих водителей и тех, кто готовится к экзамену на коммерческие права (CDL) в США. Вопросы сгруппированы по книгам и темам: выбираете нужное и сразу начинаете.</p>

<h2>Какие тесты есть</h2>
<table>
  <thead><tr><th>Направление</th><th>Что внутри</th><th>Вопросов</th></tr></thead>
  <tbody>
    <tr><td><a href="/tests/?type_id=2">Школьные предметы</a></td><td>Родной язык, литература, математика, алгебра, английский, химия, география, история и др. — 11 предметов</td><td>3 300+</td></tr>
    <tr><td><a href="/tests/?book_id=49">Автотест</a></td><td>108 билетов, вопросы с картинками</td><td>1 080</td></tr>
    <tr><td><a href="/tests/?book_id=50">e-avtomaktab</a></td><td>31 билет</td><td>305</td></tr>
    <tr><td><a href="/tests/?topic_id=1">CDL General Knowledge</a></td><td>Теория для коммерческих прав США</td><td>191</td></tr>
  </tbody>
</table>

<h2>Как это работает</h2>
<ol>
  <li>Выберите направление и книгу, затем тему или билет.</li>
  <li>Отвечайте на вопросы — правильность показывается сразу.</li>
  <li>В конце выводится общий результат.</li>
  <li>Ошибки сохраняются в браузере — их можно повторить на странице <a href="/tests/xatolar/">«Ошибки»</a>.</li>
</ol>

<h2>Преимущества</h2>
<ul>
  <li><strong>Бесплатно и без регистрации.</strong></li>
  <li><strong>3 языка:</strong> узбекский, русский и английский.</li>
  <li><strong>Удобно на телефоне.</strong></li>
</ul>
<p>Подробнее: <a href="/blog/maktab-oquvchilari-uchun-onlayn-testlar/">тесты для школьников</a> · <a href="/blog/e-avtomaktab-va-avto-test-savollari-biletlar-boyicha/">билеты e-avtomaktab и автотеста</a> · <a href="/blog/cdl-general-knowledge-testi-ozbek-tilida/">тест CDL General Knowledge</a>. Готовитесь к экзамену на права — попробуйте <a href="/avtotest/imtihon/">симулятор экзамена</a>.</p>
""",
            "en": """
<p>The <a href="/tests/">Tests</a> section is a free online test platform for school students, future drivers in Uzbekistan and people preparing for the US commercial driver's license (CDL). Questions are grouped by book and topic: pick one and start right away.</p>

<h2>What's inside</h2>
<table>
  <thead><tr><th>Track</th><th>Contents</th><th>Questions</th></tr></thead>
  <tbody>
    <tr><td><a href="/tests/?type_id=2">School subjects</a></td><td>Uzbek language, literature, math, algebra, English, chemistry, geography, history and more — 11 subjects</td><td>3,300+</td></tr>
    <tr><td><a href="/tests/?book_id=49">Driving test</a></td><td>108 tickets, many with pictures</td><td>1,080</td></tr>
    <tr><td><a href="/tests/?book_id=50">e-avtomaktab</a></td><td>31 tickets</td><td>305</td></tr>
    <tr><td><a href="/tests/?topic_id=1">CDL General Knowledge</a></td><td>US commercial license theory test</td><td>191</td></tr>
  </tbody>
</table>

<h2>How it works</h2>
<ol>
  <li>Choose a track and a book, then a topic or ticket.</li>
  <li>Answer each question and see right away whether you were correct.</li>
  <li>Get your total score at the end.</li>
  <li>Wrong answers are saved in your browser so you can retry them on the <a href="/tests/xatolar/">Mistakes</a> page.</li>
</ol>
<p>Free, no sign-up, in Uzbek, Russian and English. More: <a href="/blog/maktab-oquvchilari-uchun-onlayn-testlar/">school tests</a> · <a href="/blog/e-avtomaktab-va-avto-test-savollari-biletlar-boyicha/">e-avtomaktab and driving test tickets</a> · <a href="/blog/cdl-general-knowledge-testi-ozbek-tilida/">CDL General Knowledge test</a>.</p>
""",
        },
    },
    # ==========================================================================
    # 28 · School Tests
    # ==========================================================================
    {
        "project_id": 28,
        "slug": "maktab-oquvchilari-uchun-onlayn-testlar",
        "source_url": "https://complexprogrammer.uz/tests/?type_id=2",
        "categorie_id": 7,
        "image": "projects/images/img.png",
        "seo_title": "Maktab öquvçilari uçun onlayn testlar — 11 fan, 3300+ savol",
        "seo_description": "Ona tili, matematika, ingliz tili, kimyo, tarix va yana 6 fan böyiça bepul onlayn testlar. Darhol natija, xatolar ustida işlaş, telefonda qulay.",
        "name": {
            "uz": "Maktab öquvçilari uçun onlayn testlar: 11 fan va 3 300 dan ortiq savol",
            "ru": "Онлайн-тесты для школьников: 11 предметов и более 3 300 вопросов",
            "en": "Online tests for school students: 11 subjects and 3,300+ questions",
        },
        "title": {
            "uz": "Ona tili, adabiyot, matematika, ingliz tili, kimyo, tarix va boşqa fanlardan bepul testlar — uyda tayyorlaniş va imtihon oldidan takrorlaş uçun.",
            "ru": "Бесплатные тесты по родному языку, литературе, математике, английскому, химии, истории и другим предметам — для подготовки дома и повторения перед экзаменом.",
            "en": "Free tests in Uzbek language, literature, math, English, chemistry, history and more — for home practice and review before exams.",
        },
        "body": {
            "uz": """
<p>Dars mavzusini mustahkamlaş yoki nazorat işi oldidan özini tekşiriş uçun eng oddiy yöl — qisqa testlar. <a href="/tests/?type_id=2">Maktab testlari</a> bölimida 11 ta fan böyiça 3 300 dan ortiq savol jamlangan. Hammasi bepul va röyxatdan ötmasdan işlaydi.</p>

<h2>Fanlar va savollar soni</h2>
<table>
  <thead><tr><th>Fan</th><th>Savollar</th><th>Fan</th><th>Savollar</th></tr></thead>
  <tbody>
    <tr><td>Ona tili</td><td>590</td><td>Kimyo</td><td>380</td></tr>
    <tr><td>Ingliz tili</td><td>560</td><td>Algebra</td><td>300</td></tr>
    <tr><td>Adabiyot</td><td>400</td><td>Matematika</td><td>200</td></tr>
    <tr><td>Geografiya</td><td>400</td><td>Özbekiston tarixi</td><td>150</td></tr>
    <tr><td>Jahon tarixi</td><td>150</td><td>Biologiya, Informatika</td><td>100 tadan</td></tr>
  </tbody>
</table>

<h2>Qanday foydalaniş kerak</h2>
<ol>
  <li><a href="/tests/?type_id=2">Maktab testlari</a> sahifasida fanni tanlang.</li>
  <li>Kitob va mavzuni oçing — savollar ketma-ket çiqadi.</li>
  <li>Javob berganingizdan keyin töğri variant darhol körsatiladi.</li>
  <li>Oxirida natijangizni körasiz, xato qilingan savollar esa <a href="/tests/xatolar/">Xatolar</a> sahifasida qayta işlaş uçun saqlanadi.</li>
</ol>

<h2>Samarali tayyorlaniş uçun maslahatlar</h2>
<ul>
  <li><strong>Har kuni oz-ozdan:</strong> bir kunda 20–30 ta savol bir haftada 150 dan ortiq savolni takrorlaş degani.</li>
  <li><strong>Xatolarga qayting:</strong> notöğri javob bergan savollarni 2–3 kundan keyin yana işlang — şunda ular esda yaxşiroq qoladi.</li>
  <li><strong>Darslik bilan birga:</strong> tuşunmagan savol mavzusini darslikdan qayta öqib çiqing, keyin testga qayting.</li>
  <li><strong>Ota-onalar uçun:</strong> farzandingiz bilan birga 10 daqiqa test işlaş uning qaysi mavzuda qiynalayotganini tez körsatadi.</li>
</ul>

<p>Testlar telefonda ham qulay oçiladi. Boşqa yönalişlar: <a href="/blog/onlayn-testlar-maktab-fanlari-avtotest-cdl/">barça onlayn testlar</a>.</p>
""",
            "ru": """
<p>Самый простой способ закрепить тему урока или проверить себя перед контрольной — короткие тесты. В разделе <a href="/tests/?type_id=2">«Школьные тесты»</a> собрано более 3 300 вопросов по 11 предметам. Бесплатно и без регистрации.</p>

<h2>Предметы и количество вопросов</h2>
<table>
  <thead><tr><th>Предмет</th><th>Вопросов</th><th>Предмет</th><th>Вопросов</th></tr></thead>
  <tbody>
    <tr><td>Родной (узбекский) язык</td><td>590</td><td>Химия</td><td>380</td></tr>
    <tr><td>Английский язык</td><td>560</td><td>Алгебра</td><td>300</td></tr>
    <tr><td>Литература</td><td>400</td><td>Математика</td><td>200</td></tr>
    <tr><td>География</td><td>400</td><td>История Узбекистана</td><td>150</td></tr>
    <tr><td>Всемирная история</td><td>150</td><td>Биология, информатика</td><td>по 100</td></tr>
  </tbody>
</table>
<p>Тесты по предметам составлены на узбекском языке.</p>

<h2>Как пользоваться</h2>
<ol>
  <li>Выберите предмет на странице <a href="/tests/?type_id=2">школьных тестов</a>.</li>
  <li>Откройте книгу и тему — вопросы идут по порядку.</li>
  <li>После ответа сразу видно правильный вариант.</li>
  <li>В конце — итоговый результат, а ошибки сохраняются на странице <a href="/tests/xatolar/">«Ошибки»</a>.</li>
</ol>

<h2>Советы</h2>
<ul>
  <li><strong>Понемногу каждый день:</strong> 20–30 вопросов в день — это 150+ вопросов в неделю.</li>
  <li><strong>Возвращайтесь к ошибкам</strong> через 2–3 дня — так материал запоминается лучше.</li>
  <li><strong>Вместе с учебником:</strong> непонятную тему перечитайте, затем вернитесь к тесту.</li>
</ul>
<p>Другие направления: <a href="/blog/onlayn-testlar-maktab-fanlari-avtotest-cdl/">все онлайн-тесты</a>.</p>
""",
            "en": """
<p>Short tests are the easiest way to reinforce a lesson or check yourself before a quiz. The <a href="/tests/?type_id=2">School tests</a> section has over 3,300 questions in 11 subjects. Free, no sign-up. The subject tests are in Uzbek.</p>

<h2>Subjects</h2>
<table>
  <thead><tr><th>Subject</th><th>Questions</th><th>Subject</th><th>Questions</th></tr></thead>
  <tbody>
    <tr><td>Uzbek language</td><td>590</td><td>Chemistry</td><td>380</td></tr>
    <tr><td>English</td><td>560</td><td>Algebra</td><td>300</td></tr>
    <tr><td>Literature</td><td>400</td><td>Mathematics</td><td>200</td></tr>
    <tr><td>Geography</td><td>400</td><td>History of Uzbekistan</td><td>150</td></tr>
    <tr><td>World history</td><td>150</td><td>Biology, Computer science</td><td>100 each</td></tr>
  </tbody>
</table>

<h2>How to use it</h2>
<ol>
  <li>Pick a subject on the <a href="/tests/?type_id=2">School tests</a> page.</li>
  <li>Open a book and a topic; questions come one by one.</li>
  <li>The correct option is shown right after you answer.</li>
  <li>See your score at the end; wrong answers are saved on the <a href="/tests/xatolar/">Mistakes</a> page.</li>
</ol>
<p>Tip: 20–30 questions a day adds up to 150+ a week, and revisiting mistakes after 2–3 days helps them stick. See also <a href="/blog/onlayn-testlar-maktab-fanlari-avtotest-cdl/">all online tests</a>.</p>
""",
        },
    },
    # ==========================================================================
    # 25 · General Knowledge (AQŞ CDL)
    # ==========================================================================
    {
        "project_id": 25,
        "slug": "cdl-general-knowledge-testi-ozbek-tilida",
        "source_url": "https://complexprogrammer.uz/tests/?topic_id=1",
        "categorie_id": 1,
        "image": "projects/images/maxresdefault.jpg",
        "seo_title": "CDL General Knowledge testi özbek tilida — 191 savol",
        "seo_description": "AQŞda yuk maşinasi guvohnomasi (CDL) uçun General Knowledge nazariy testi: 191 savol özbek, rus va ingliz tillarida, bepul onlayn maşq.",
        "name": {
            "uz": "[[CDL General Knowledge]] testi özbek tilida: AQŞda yuk maşinasi guvohnomasiga tayyorlaniş",
            "ru": "Тест CDL General Knowledge на узбекском и русском: подготовка к коммерческим правам в США",
            "en": "CDL General Knowledge practice test in Uzbek, Russian and English",
        },
        "title": {
            "uz": "191 ta savol özbek, rus va ingliz tillarida — imtihonni ingliz tilida topşirişdan oldin mazmunini öz tilingizda tuşunib oling.",
            "ru": "191 вопрос на узбекском, русском и английском — разберитесь в материале на родном языке перед экзаменом на английском.",
            "en": "191 questions in Uzbek, Russian and English — understand the material in your own language before the English exam.",
        },
        "body": {
            "uz": """
<p>AQŞda yuk maşinasi (truck) haydovçisi bölib işlaş uçun <strong>[[CDL]]</strong> (<em>[[Commercial Driver's License]]</em>) — tijorat haydovçilik guvohnomasi kerak. Uni oliş [[General Knowledge]] nazariy testidan boşlanadi. Imtihon ingliz tilida, şuning uçun köp özbek haydovçilar uçun eng qiyini — savolning mazmunini tuşuniş. <a href="/tests/?topic_id=1">Bizdagi test</a> aynan şunga yordam beradi: 191 ta savol <strong>özbek, rus va ingliz tillarida</strong>.</p>

<h2>[[General Knowledge]] testida nimalar söraladi</h2>
<ul>
  <li><strong>Transportni tekşiriş</strong> (<em>[[vehicle inspection]]</em>): safar oldidan, safar paytida va undan keyin nimalarni körib çiqiş kerak — rul qismlari, tormozlar, ğildiraklar, çiroqlar.</li>
  <li><strong>Xavfsiz haydaş:</strong> masofani saqlaş, tezlikni tanlaş, kunning qoronği vaqtida va yomon ob-havoda haydaş.</li>
  <li><strong>Yukni taşiş:</strong> yukni mahkamlaş, oğirlik taqsimoti, oğir yuk bilan tormozlaş.</li>
  <li><strong>Favqulodda vaziyatlar:</strong> tormoz işlamay qolsa, ğildirak yorilsa, yonğin çiqsa nima qiliş kerak.</li>
</ul>

<h2>Testdan qanday foydalaniş kerak</h2>
<ol>
  <li><a href="/tests/?topic_id=1">[[CDL General Knowledge]]</a> sahifasini oçing.</li>
  <li>Avval savollarni öz tilingizda (özbekça yoki rusça) işlab, mazmunini tuşunib oling.</li>
  <li>Söng tilni inglizçaga almaştirib, xuddi şu savollarni ingliz tilida yeçing — imtihonda ular aynan şunday körinadi.</li>
  <li>Xato qilgan savollaringiz <a href="/tests/xatolar/">Xatolar</a> sahifasida saqlanadi — ularni alohida takrorlang.</li>
</ol>

<h2>Muhim eslatmalar</h2>
<ul>
  <li>Imtihon qoidalari va savollar soni ştatga qarab farq qiladi. Rasmiy qöllanma — har bir ştatning <strong>[[CDL Manual]]</strong> kitobi; uni ştatingiz [[DMV]] saytidan yuklab oling.</li>
  <li>[[General Knowledge]] dan keyin yuk turiga qarab qöşimça testlar ([[Air Brakes]], [[Combination Vehicles]] va boşqalar) va amaliy imtihon topşiriladi.</li>
  <li>Bu test — maşq uçun. U rasmiy imtihon savollarining aynan nusxasi emas, lekin mavzular bir xil.</li>
</ul>
<p>Boşqa testlar: <a href="/blog/onlayn-testlar-maktab-fanlari-avtotest-cdl/">barça onlayn testlar</a>.</p>
""",
            "ru": """
<p>Чтобы работать водителем грузовика в США, нужны коммерческие права — <strong>CDL</strong> (<em>Commercial Driver's License</em>). Всё начинается с теоретического теста General Knowledge. Экзамен на английском, и для многих главная трудность — понять смысл вопроса. <a href="/tests/?topic_id=1">Наш тест</a> помогает именно с этим: 191 вопрос на <strong>узбекском, русском и английском</strong>.</p>

<h2>Что спрашивают в General Knowledge</h2>
<ul>
  <li><strong>Осмотр транспорта</strong> (<em>vehicle inspection</em>): что проверять до, во время и после поездки — рулевое управление, тормоза, колёса, свет.</li>
  <li><strong>Безопасное вождение:</strong> дистанция, выбор скорости, езда ночью и в плохую погоду.</li>
  <li><strong>Перевозка груза:</strong> крепление, распределение веса, торможение с тяжёлым грузом.</li>
  <li><strong>Аварийные ситуации:</strong> отказ тормозов, разрыв шины, пожар.</li>
</ul>

<h2>Как готовиться</h2>
<ol>
  <li>Откройте страницу <a href="/tests/?topic_id=1">CDL General Knowledge</a>.</li>
  <li>Сначала решите вопросы на русском или узбекском, чтобы понять смысл.</li>
  <li>Затем переключите язык на английский и пройдите те же вопросы — на экзамене они будут выглядеть так.</li>
  <li>Ошибки сохраняются на странице <a href="/tests/xatolar/">«Ошибки»</a> — повторяйте их отдельно.</li>
</ol>

<h2>Важно</h2>
<ul>
  <li>Правила и количество вопросов зависят от штата. Официальное пособие — <strong>CDL Manual</strong> вашего штата на сайте DMV.</li>
  <li>После General Knowledge сдаются дополнительные тесты (Air Brakes, Combination Vehicles и др.) и практический экзамен.</li>
  <li>Это тренировочный тест: не копия официальных вопросов, но темы те же.</li>
</ul>
""",
            "en": """
<p>To drive a truck professionally in the US you need a <strong>CDL</strong> (Commercial Driver's License), and it starts with the General Knowledge theory test. The exam is in English, which is the hardest part for many immigrant drivers. <a href="/tests/?topic_id=1">Our practice test</a> has 191 questions in <strong>Uzbek, Russian and English</strong>, so you can learn the content in your own language first.</p>

<h2>What the test covers</h2>
<ul>
  <li><strong>Vehicle inspection:</strong> what to check before, during and after a trip — steering, brakes, wheels, lights.</li>
  <li><strong>Safe driving:</strong> following distance, speed, night driving and bad weather.</li>
  <li><strong>Cargo:</strong> securing loads, weight distribution, braking with heavy loads.</li>
  <li><strong>Emergencies:</strong> brake failure, tire blowouts, fires.</li>
</ul>

<h2>How to practice</h2>
<ol>
  <li>Open <a href="/tests/?topic_id=1">CDL General Knowledge</a>.</li>
  <li>Work through the questions in Uzbek or Russian to understand them.</li>
  <li>Switch to English and do the same questions again, the way they appear in the exam.</li>
  <li>Review your saved mistakes on the <a href="/tests/xatolar/">Mistakes</a> page.</li>
</ol>
<p>Rules vary by state: use your state's official <strong>CDL Manual</strong> from the DMV website. After General Knowledge come endorsement tests (Air Brakes, Combination Vehicles, etc.) and the skills test. This is a practice test, not a copy of the official exam.</p>
""",
        },
    },
    # ==========================================================================
    # 29 · AVTO TEST 2025 (tests type 3: Avto Test + e-avtomaktab)
    # ==========================================================================
    {
        "project_id": 29,
        "slug": "e-avtomaktab-va-avto-test-savollari-biletlar-boyicha",
        "source_url": "https://complexprogrammer.uz/tests/?type_id=3",
        "categorie_id": 1,
        "image": "projects/images/img.jpg",
        "seo_title": "e-avtomaktab va avto test savollari biletlar böyiça — onlayn",
        "seo_description": "e-avtomaktab (31 bilet, 305 savol) va avto test (108 bilet, 1080 savol) savollarini onlayn işlang: rasmli savollar, darhol natija, 3 til, bepul.",
        "name": {
            "uz": "e-avtomaktab va avto test savollari biletlar böyiça: 1 385 savol onlayn",
            "ru": "Вопросы e-avtomaktab и автотеста по билетам: 1 385 вопросов онлайн",
            "en": "e-avtomaktab and driving test questions by ticket: 1,385 questions online",
        },
        "title": {
            "uz": "Ikki xil töplam — e-avtomaktab (31 bilet) va avto test (108 bilet): rasmli savollar, darhol natija va xatolar ustida işlaş.",
            "ru": "Два сборника — e-avtomaktab (31 билет) и автотест (108 билетов): вопросы с картинками, мгновенный результат и работа над ошибками.",
            "en": "Two collections — e-avtomaktab (31 tickets) and the driving test (108 tickets): picture questions, instant results and mistake review.",
        },
        "body": {
            "uz": """
<p>Haydovçilik guvohnomasiga tayyorlanayotganlar uçun <a href="/tests/?type_id=3">Avto test</a> yönalişida ikki xil savollar töplami bor. Ikkalasi ham biletlar böyiça tuzilgan, savollarning yarmidan köpi rasmli.</p>

<h2>Ikki töplam</h2>
<table>
  <thead><tr><th>Töplam</th><th>Biletlar</th><th>Savollar</th><th>Rasmli</th></tr></thead>
  <tbody>
    <tr><td><a href="/tests/?book_id=50">e-avtomaktab</a></td><td>31</td><td>305</td><td>154</td></tr>
    <tr><td><a href="/tests/?book_id=49">Avto test</a></td><td>108</td><td>1 080</td><td>774</td></tr>
  </tbody>
</table>
<p>Savollar özbek (lotin va kirill), rus va ingliz tillarida.</p>

<h2>Qanday tayyorlaniş kerak</h2>
<ol>
  <li><strong>Kuniga 2–3 bilet.</strong> Har bir biletda 10 tadan savol — bu kuniga 20–30 ta savol, ança yengil reja.</li>
  <li><strong>Xatolar ustida işlang.</strong> Notöğri javob bergan savollar <a href="/tests/xatolar/">Xatolar</a> sahifasida yiğiladi — haftasiga bir marta ularni alohida takrorlang.</li>
  <li><strong>Qoidani biling.</strong> Tuşunmagan savol mavzusini <a href="/yhq/">Yöl harakati qoidalari</a> matnidan öqing — savolni yodlaşdan köra qoidani tuşuniş işonçliroq.</li>
  <li><strong>Imtihon şaroitida sinang.</strong> Tayyor bölgaç, <a href="/avtotest/imtihon/">20 savollik imtihon simulyatori</a>da 25 daqiqa va 2 ta xato çegarasi bilan özingizni sinang.</li>
</ol>

<h2>Qaysi bölimni tanlaş kerak</h2>
<ul>
  <li><a href="/tests/?type_id=3">Testlar → Avto test</a> — kitob va bilet böyiça ketma-ket işlaş uçun.</li>
  <li><a href="/avtotest/">Avtotest</a> — har bir savolning alohida sahifasi, "Nega şunday?" izohlari, mavzular böyiça testlar va imtihon simulyatori.</li>
</ul>
<p>Foydali maqolalar: <a href="/blog/avtotestga-14-kunda-tayyorlanish/">Avtotestga 14 kunda tayyorlaniş rejasi</a> · <a href="/blog/avtotest-eng-kop-xato-qilinadigan-savollar/">Eng köp xato qilinadigan savollar</a>.</p>
""",
            "ru": """
<p>Для подготовки к экзамену на права в направлении <a href="/tests/?type_id=3">«Автотест»</a> есть два сборника вопросов. Оба составлены по билетам, больше половины вопросов — с картинками.</p>

<h2>Два сборника</h2>
<table>
  <thead><tr><th>Сборник</th><th>Билетов</th><th>Вопросов</th><th>С картинкой</th></tr></thead>
  <tbody>
    <tr><td><a href="/tests/?book_id=50">e-avtomaktab</a></td><td>31</td><td>305</td><td>154</td></tr>
    <tr><td><a href="/tests/?book_id=49">Автотест</a></td><td>108</td><td>1 080</td><td>774</td></tr>
  </tbody>
</table>
<p>Вопросы на узбекском (латиница и кириллица), русском и английском.</p>

<h2>Как готовиться</h2>
<ol>
  <li><strong>2–3 билета в день</strong> — это 20–30 вопросов, лёгкий темп.</li>
  <li><strong>Работайте над ошибками</strong> на странице <a href="/tests/xatolar/">«Ошибки»</a> раз в неделю.</li>
  <li><strong>Разбирайтесь в правилах:</strong> непонятную тему читайте в <a href="/ru/yhq/">ПДД Узбекистана</a>.</li>
  <li><strong>Проверьте себя</strong> в <a href="/avtotest/imtihon/">симуляторе экзамена</a>: 20 вопросов, 25 минут, не больше 2 ошибок.</li>
</ol>
<p>В разделе <a href="/avtotest/">«Автотест»</a> у каждого вопроса есть своя страница с пояснением «Почему?». Полезно: <a href="/blog/avtotestga-14-kunda-tayyorlanish/">план подготовки за 14 дней</a>.</p>
""",
            "en": """
<p>For driving license preparation, the <a href="/tests/?type_id=3">Driving test</a> track has two question collections. Both are organised by ticket, and more than half of the questions have pictures.</p>

<h2>Two collections</h2>
<table>
  <thead><tr><th>Collection</th><th>Tickets</th><th>Questions</th><th>With picture</th></tr></thead>
  <tbody>
    <tr><td><a href="/tests/?book_id=50">e-avtomaktab</a></td><td>31</td><td>305</td><td>154</td></tr>
    <tr><td><a href="/tests/?book_id=49">Driving test</a></td><td>108</td><td>1,080</td><td>774</td></tr>
  </tbody>
</table>

<h2>How to prepare</h2>
<ol>
  <li><strong>2–3 tickets a day</strong> (20–30 questions) is an easy pace.</li>
  <li><strong>Review mistakes</strong> weekly on the <a href="/tests/xatolar/">Mistakes</a> page.</li>
  <li><strong>Learn the rule</strong>, not just the answer, using the <a href="/yhq/">traffic rules</a>.</li>
  <li><strong>Test yourself</strong> in the <a href="/avtotest/imtihon/">exam simulator</a>: 20 questions, 25 minutes, at most 2 mistakes.</li>
</ol>
<p>In the <a href="/avtotest/">Driving test</a> section every question also has its own page with a "Why?" explanation.</p>
""",
        },
    },
]
