"""/projects/ dagi onlayn vositalar haqidagi maqolalar (manage.py publish_project_posts).

``[[...]]`` — kirillga ögirilmaydigan nom (brend, qisqartma): matnda <span translate="no"> ga aylanadi.
Faktlar vositalarning öz kodidan olingan (projects/views.py, templates/projects/*.html, core/seo_pages.py).
"""

ARTICLES = [
    # ==========================================================================
    # 2 · Parol generatori
    # ==========================================================================
    {
        "project_id": 2,
        "slug": "kuchli-parol-yaratish-parol-generatori",
        "source_url": "https://complexprogrammer.uz/password_generator/",
        "categorie_id": 7,
        "image": "projects/images/password-generator.png",
        "seo_title": "Kuçli parol qanday yaratiladi — bepul parol generatori",
        "seo_description": "Kuçli parol qoidalari va bepul onlayn parol generatori: 4–64 belgi, harflar, raqamlar, belgilar, öxşaş belgilarsiz rejim. Parol serverga yuborilmaydi.",
        "name": {
            "uz": "Kuçli parol qanday yaratiladi: qoidalar va bepul onlayn parol generatori",
            "ru": "Как создать надёжный пароль: правила и бесплатный онлайн-генератор",
            "en": "How to create a strong password: rules and a free online generator",
        },
        "title": {
            "uz": "Parol nega buziladi, qança uzun bölişi kerak va uni bir bosişda xavfsiz yaratiş — parol faqat brauzeringizda tuğiladi.",
            "ru": "Почему пароли взламывают, какой длины они должны быть и как создать надёжный пароль в один клик — прямо в браузере.",
            "en": "Why passwords get cracked, how long they should be and how to make a safe one in one click — right in your browser.",
        },
        "body": {
            "uz": """
<p>Köp akkauntlar murakkab hujum bilan emas, oddiy parol tufayli buziladi: <code>123456</code>, <code>qwerty</code>, ism yoki tuğilgan yil. Kuçli parolni öylab topiş qiyin, eslab qoliş undan ham qiyin. <a href="/password_generator/">Parol generatori</a> bu işni bir bosişda bajaradi.</p>

<h2>Kuçli parol qoidalari</h2>
<ul>
  <li><strong>Uzunlik — eng muhimi.</strong> Kamida 12 belgi, poçta, bank va ijtimoiy tarmoqlar uçun 16 va undan köp.</li>
  <li><strong>Aralaş belgilar:</strong> katta va kiçik harflar, raqamlar, maxsus belgilar (<code>!@#$%</code>).</li>
  <li><strong>Şaxsiy ma'lumot yöq:</strong> ism, familiya, tuğilgan sana, telefon raqami, uy hayvoni nomi bölmasin.</li>
  <li><strong>Har bir sayt uçun alohida parol.</strong> Bitta sayt ma'lumotlari tarqalsa, qolgan akkauntlaringiz xavfsiz qoladi.</li>
</ul>

<h2>Generatorning imkoniyatlari</h2>
<ul>
  <li>Uzunlik <strong>4 dan 64 belgigaça</strong> — surgiç bilan tanlanadi.</li>
  <li>Katta harflar, kiçik harflar, raqamlar va belgilarni alohida yoqiş yoki öçiriş.</li>
  <li><strong>"Öxşaş belgilarsiz"</strong> rejimi: <code>I</code>, <code>l</code>, <code>1</code>, <code>O</code>, <code>0</code> kabi bir-biriga öxşaş belgilar işlatilmaydi — parolni qöl bilan yozganda adaşmaysiz.</li>
  <li>Bir bosişda nusxalaş, yangilaş va <strong>yana 5 ta variant</strong> köriş.</li>
</ul>

<h2>Xavfsizmi?</h2>
<p>Ha. Parol <strong>sizning brauzeringizda</strong> yaratiladi va serverga yuborilmaydi — biz uni körmaymiz va saqlamaymiz. Yaratilgan parolni işonçli parol menejerida (masalan, brauzer yoki telefoningizning öz menejerida) saqlang va muhim akkauntlarda ikki bosqiçli tekşirişni (2FA) yoqing.</p>
<p>Boşqa foydali vositalar: <a href="/blog/ip-manzilni-aniqlash-mening-ip-manzilim/">IP manzilni aniqlaş</a> · <a href="/blog/onlayn-tarjimon-ozbek-rus-ingliz/">onlayn tarjimon</a>.</p>
""",
            "ru": """
<p>Большинство аккаунтов взламывают не сложными атаками, а из-за простых паролей: <code>123456</code>, <code>qwerty</code>, имя или год рождения. <a href="/password_generator/">Генератор паролей</a> создаёт надёжный пароль в один клик.</p>

<h2>Правила надёжного пароля</h2>
<ul>
  <li><strong>Длина важнее всего:</strong> минимум 12 символов, для почты, банка и соцсетей — 16 и больше.</li>
  <li><strong>Смешанные символы:</strong> заглавные и строчные буквы, цифры, спецсимволы.</li>
  <li><strong>Без личных данных:</strong> имени, даты рождения, номера телефона.</li>
  <li><strong>Свой пароль для каждого сайта</strong> — утечка на одном сайте не затронет остальные.</li>
</ul>

<h2>Возможности генератора</h2>
<ul>
  <li>Длина <strong>от 4 до 64 символов</strong>.</li>
  <li>Отдельное включение заглавных, строчных букв, цифр и символов.</li>
  <li>Режим <strong>«Без похожих символов»</strong>: не используются <code>I l 1 O 0</code>.</li>
  <li>Копирование в один клик, обновление и <strong>ещё 5 вариантов</strong>.</li>
</ul>
<p>Пароль создаётся <strong>в вашем браузере</strong> и не отправляется на сервер. Храните его в менеджере паролей и включите двухфакторную аутентификацию (2FA).</p>
""",
            "en": """
<p>Most accounts are broken into because of weak passwords like <code>123456</code>, <code>qwerty</code>, a name or a birth year, not sophisticated attacks. The <a href="/password_generator/">password generator</a> makes a strong one in a click.</p>

<h2>Rules for a strong password</h2>
<ul>
  <li><strong>Length matters most:</strong> at least 12 characters, 16+ for email, banking and social media.</li>
  <li><strong>Mix characters:</strong> upper and lower case, digits and symbols.</li>
  <li><strong>No personal data:</strong> names, birthdays, phone numbers.</li>
  <li><strong>One password per site</strong>, so one leak does not expose the rest.</li>
</ul>

<h2>What the generator offers</h2>
<ul>
  <li>Length <strong>from 4 to 64</strong> characters.</li>
  <li>Toggle upper case, lower case, digits and symbols.</li>
  <li><strong>Exclude look-alikes</strong> (<code>I l 1 O 0</code>) for passwords you type by hand.</li>
  <li>One-click copy, regenerate and <strong>5 more options</strong>.</li>
</ul>
<p>Passwords are generated <strong>in your browser</strong> and never sent to the server. Keep them in a password manager and turn on two-factor authentication.</p>
""",
        },
    },
    # ==========================================================================
    # 26 · PDF Tools
    # ==========================================================================
    {
        "project_id": 26,
        "slug": "pdf-ni-word-excel-va-rasmga-otkazish",
        "source_url": "https://complexprogrammer.uz/pdf_tools/",
        "categorie_id": 7,
        "image": "projects/images/0b0040d43c285926eb01.png",
        "seo_title": "PDF ni Word, Excel va rasmga ötkaziş — bepul onlayn",
        "seo_description": "PDF faylni Word (DOCX), Excel (CSV) yoki JPG rasmga bepul ötkazing. Qaçon qaysi format kerak, skanerlangan PDF bilan nima qiliş va fayllar xavfsizligi.",
        "name": {
            "uz": "[[PDF]] ni [[Word]], [[Excel]] va rasmga ötkaziş: bepul onlayn vosita va foydali maslahatlar",
            "ru": "Как перевести PDF в Word, Excel и картинку: бесплатный онлайн-инструмент",
            "en": "Convert PDF to Word, Excel and images: a free online tool",
        },
        "title": {
            "uz": "Matnni tahrirlaş uçun [[DOCX]], jadval uçun [[CSV]], ulaşiş uçun [[JPG]] — faylni yuklang va natijani bir zumda oling.",
            "ru": "DOCX для редактирования текста, CSV для таблиц, JPG для отправки — загрузите файл и получите результат сразу.",
            "en": "DOCX to edit text, CSV for tables, JPG for sharing — upload a file and get the result right away.",
        },
        "body": {
            "uz": """
<p>[[PDF]] — hujjatni har qanday qurilmada bir xil körsatadigan format, lekin uni tahrirlaş noqulay. Şartnomadagi bitta sözni özgartiriş yoki hisobotdagi jadvalni hisoblaş kerak bölsa, faylni boşqa formatga ötkaziş kerak. <a href="/pdf_tools/">PDF Tools</a> buni brauzerda, dastur örnatmasdan bajaradi.</p>

<h2>Uç xil ötkaziş</h2>
<table>
  <thead><tr><th>Amal</th><th>Natija</th><th>Qaçon kerak</th></tr></thead>
  <tbody>
    <tr><td>[[PDF]] → [[Word]]</td><td>[[DOCX]]</td><td>Matnni tahrirlaş: şartnoma, ariza, rezyume</td></tr>
    <tr><td>[[PDF]] → [[Excel]]</td><td>[[CSV]]</td><td>Jadvaldagi raqamlar bilan işlaş: hisobot, narxlar röyxati</td></tr>
    <tr><td>[[PDF]] → rasm</td><td>[[JPG]]</td><td>Sahifani messenjerda ulaşiş yoki taqdimotga qöyiş</td></tr>
  </tbody>
</table>

<h2>Qanday foydalaniladi</h2>
<ol>
  <li><a href="/pdf_tools/">PDF Tools</a> sahifasida kerakli amalni tanlang.</li>
  <li>[[PDF]] faylni yuklang.</li>
  <li>Tayyor faylni yuklab oling.</li>
</ol>

<h2>Bilib qöyiş kerak</h2>
<ul>
  <li><strong>Matnli va skanerlangan [[PDF]] farqi.</strong> Kompyuterda yaratilgan [[PDF]]dagi matn va jadvallar yaxşi ötadi. Skanerlangan hujjat aslida rasm bölgani uçun undagi matnni ajratiş qiyin — natija sifati pastroq böladi.</li>
  <li><strong>[[CSV]] faylni [[Excel]]da oçiş:</strong> [[Excel]]da "Fayl → Oçiş" orqali tanlang; ustunlar alohida kataklarga ajraladi.</li>
  <li><strong>Xavfsizlik:</strong> yuklangan fayllar faqat ötkaziş uçun işlatiladi va serverdan <strong>1 soat içida avtomatik öçiriladi</strong>. Şunga qaramay, juda maxfiy hujjatlarni (pasport nusxasi, bank ma'lumotlari) onlayn xizmatlarga yuklamaslik tavsiya etiladi.</li>
</ul>
<p>Matnni lotin va kirill orasida ögiriş kerakmi? <a href="/blog/lotin-kirill-ogirgich-changetext/">Lotin-kirill ögirgiç</a>dan foydalaning.</p>
""",
            "ru": """
<p>PDF одинаково выглядит на любом устройстве, но редактировать его неудобно. Чтобы поправить договор или посчитать цифры в таблице, файл нужно перевести в другой формат. <a href="/pdf_tools/">PDF Tools</a> делает это в браузере, без установки программ.</p>

<h2>Три вида конвертации</h2>
<table>
  <thead><tr><th>Действие</th><th>Результат</th><th>Когда нужно</th></tr></thead>
  <tbody>
    <tr><td>PDF → Word</td><td>DOCX</td><td>Редактировать текст: договор, заявление, резюме</td></tr>
    <tr><td>PDF → Excel</td><td>CSV</td><td>Работать с цифрами: отчёт, прайс-лист</td></tr>
    <tr><td>PDF → картинка</td><td>JPG</td><td>Отправить страницу в мессенджере или вставить в презентацию</td></tr>
  </tbody>
</table>

<h2>Полезно знать</h2>
<ul>
  <li><strong>Текстовый и сканированный PDF.</strong> Текст и таблицы из PDF, созданного на компьютере, переносятся хорошо. Скан — это картинка, поэтому качество результата ниже.</li>
  <li><strong>CSV в Excel</strong> откройте через «Файл → Открыть» — столбцы разделятся по ячейкам.</li>
  <li><strong>Безопасность:</strong> файлы используются только для конвертации и <strong>удаляются с сервера в течение часа</strong>. Особо конфиденциальные документы лучше не загружать ни в какие онлайн-сервисы.</li>
</ul>
""",
            "en": """
<p>PDF looks the same everywhere but is awkward to edit. To change a contract or work with numbers in a table, you need another format. <a href="/pdf_tools/">PDF Tools</a> does it in the browser, nothing to install.</p>

<h2>Three conversions</h2>
<table>
  <thead><tr><th>Action</th><th>Output</th><th>Use it for</th></tr></thead>
  <tbody>
    <tr><td>PDF → Word</td><td>DOCX</td><td>Editing text: contracts, applications, CVs</td></tr>
    <tr><td>PDF → Excel</td><td>CSV</td><td>Working with numbers: reports, price lists</td></tr>
    <tr><td>PDF → image</td><td>JPG</td><td>Sharing a page in a messenger or a presentation</td></tr>
  </tbody>
</table>
<p><strong>Good to know:</strong> text and tables from computer-generated PDFs convert well; scanned PDFs are images, so results are weaker. Open CSV files in Excel via File → Open. Uploaded files are used only for conversion and <strong>deleted from the server within an hour</strong>; still, avoid uploading highly sensitive documents to any online service.</p>
""",
        },
    },
    # ==========================================================================
    # 3 · IP Finder
    # ==========================================================================
    {
        "project_id": 3,
        "slug": "ip-manzilni-aniqlash-mening-ip-manzilim",
        "source_url": "https://complexprogrammer.uz/ip/",
        "categorie_id": 7,
        "image": "projects/images/ipfinder.png",
        "seo_title": "IP manzilni aniqlaş: mening IP manzilim qanday? — bepul",
        "seo_description": "IP manzil nima, undan nimani biliş mumkin va nimani emas. Öz IP manzilingizni va istalgan IP'ning mamlakati, şahri, provayderi va vaqt mintaqasini aniqlang.",
        "name": {
            "uz": "[[IP]] manzilni aniqlaş: mening [[IP]] manzilim qanday va undan nimani biliş mumkin",
            "ru": "Как узнать IP-адрес: какой у меня IP и что по нему можно определить",
            "en": "What is my IP address and what can it reveal?",
        },
        "title": {
            "uz": "[[IP]] manzil nima, nega özgaradi, undan qaysi ma'lumotlarni biliş mumkin va qaysilarini — yöq.",
            "ru": "Что такое IP-адрес, почему он меняется и какие данные по нему можно узнать, а какие — нет.",
            "en": "What an IP address is, why it changes and what it can and cannot tell about you.",
        },
        "body": {
            "uz": """
<p>Internetga ulangan har bir qurilma raqamli manzil — <strong>[[IP]] manzil</strong> oladi. U orqali saytlar ma'lumotni kimga yuboriş kerakligini biladi. <a href="/ip/">[[IP]] manzilni aniqlaş</a> vositasi sahifani oçişingiz bilan sizning joriy [[IP]] manzilingizni körsatadi; istalgan boşqa [[IP]] haqida ham ma'lumot topiş mumkin.</p>

<h2>Vosita nimalarni körsatadi</h2>
<ul>
  <li><strong>Joylaşuv:</strong> mamlakat, viloyat, şahar, poçta indeksi, taxminiy koordinatalar va xaritada oçiş.</li>
  <li><strong>Tarmoq:</strong> internet provayderi, [[ASN]] raqami, tarmoq bloki, [[IP]] versiyasi ([[IPv4]] yoki [[IPv6]]).</li>
  <li><strong>Vaqt:</strong> vaqt mintaqasi, [[UTC]] farqi va u yerdagi hozirgi vaqt.</li>
</ul>

<h2>[[IP]] orqali nimani biliş mumkin emas</h2>
<p>[[IP]] manzil uyingizning aniq manzilini, ismingizni yoki telefon raqamingizni <strong>körsatmaydi</strong>. Joylaşuv taxminiy: köpinça provayderning şahri yoki markaziy uzeli körinadi. Mobil internetda boşqa şahar körinişi ham tabiiy.</p>

<h2>Qaçon foydali</h2>
<ul>
  <li><strong>[[VPN]] işlayaptimi?</strong> [[VPN]] yoqilganda körsatilgan mamlakat özgarişi kerak.</li>
  <li><strong>Sozlaş va texnik yordam:</strong> provayder yoki administrator [[IP]] manzilingizni söraganda.</li>
  <li><strong>Şubhali kirişlar:</strong> akkauntga notanış [[IP]]'dan kirilgan bölsa, uning qaysi mamlakat va provayderga tegişli ekanini tekşiriş.</li>
</ul>

<h2>Nega [[IP]] manzilim özgarib turadi?</h2>
<p>Köpçilik provayderlar uy va mobil foydalanuvçilarga <strong>dinamik [[IP]]</strong> beradi: router qayta yoqilganda yoki ma'lum vaqtdan keyin manzil yangilanadi. Doimiy (statik) [[IP]] odatda alohida xizmat sifatida beriladi.</p>
<p>Yana: <a href="/blog/kuchli-parol-yaratish-parol-generatori/">kuçli parol yaratiş</a>.</p>
""",
            "ru": """
<p>Каждое устройство в интернете получает числовой адрес — <strong>IP-адрес</strong>. Инструмент <a href="/ip/">«Узнать IP»</a> сразу показывает ваш текущий IP и позволяет проверить любой другой.</p>

<h2>Что показывает инструмент</h2>
<ul>
  <li><strong>Местоположение:</strong> страна, регион, город, почтовый индекс, примерные координаты и карта.</li>
  <li><strong>Сеть:</strong> провайдер, номер ASN, сетевой блок, версия IP (IPv4 или IPv6).</li>
  <li><strong>Время:</strong> часовой пояс, смещение от UTC и местное время.</li>
</ul>

<h2>Чего по IP узнать нельзя</h2>
<p>IP <strong>не показывает</strong> точный домашний адрес, имя или номер телефона. Местоположение примерное — часто это город провайдера; в мобильном интернете может отображаться другой город.</p>

<h2>Когда полезно</h2>
<ul>
  <li>Проверить, работает ли <strong>VPN</strong> — страна должна смениться.</li>
  <li>Сообщить IP провайдеру или администратору.</li>
  <li>Проверить подозрительный вход в аккаунт с незнакомого IP.</li>
</ul>
<p>IP часто меняется, потому что провайдеры выдают <strong>динамические адреса</strong>; постоянный (статический) IP обычно подключается отдельно.</p>
""",
            "en": """
<p>Every device online gets a numeric address, its <strong>IP address</strong>. The <a href="/ip/">IP lookup</a> tool shows yours as soon as the page opens and lets you check any other IP.</p>

<h2>What it shows</h2>
<ul>
  <li><strong>Location:</strong> country, region, city, postal code, approximate coordinates and a map link.</li>
  <li><strong>Network:</strong> ISP, ASN, network block, IP version (IPv4 or IPv6).</li>
  <li><strong>Time:</strong> time zone, UTC offset and local time.</li>
</ul>
<p>An IP address does <strong>not</strong> reveal your street address, name or phone number; the location is approximate, often the ISP's city. It is handy for checking that a VPN works, giving your IP to support, or investigating an unfamiliar login. Most home and mobile connections use <strong>dynamic IPs</strong>, which is why yours changes.</p>
""",
        },
    },
    # ==========================================================================
    # 5 · Valyuta kurslari
    # ==========================================================================
    {
        "project_id": 5,
        "slug": "valyuta-kurslari-markaziy-bank-kursi-bugun",
        "source_url": "https://complexprogrammer.uz/exchangerates/",
        "categorie_id": 8,
        "image": "projects/images/exchangerates.png",
        "seo_title": "Valyuta kurslari bugun: Markaziy bank kursi va bank kursi farqi",
        "seo_description": "Dollar, yevro, rubl kursi bugun — Özbekiston Markaziy banki rasmiy ma'lumotlari. Rasmiy kurs nima, banklardagi kurs nega boşqaça va kursni qanday kuzatiş kerak.",
        "name": {
            "uz": "Valyuta kurslari bugun: Markaziy bank kursi nima va banklardagi kurs nega boşqaça",
            "ru": "Курс валют сегодня: что такое курс ЦБ Узбекистана и почему в банках он другой",
            "en": "Exchange rates today: the Central Bank of Uzbekistan rate vs bank rates",
        },
        "title": {
            "uz": "Dollar, yevro, rubl va boşqa valyutalarning rasmiy kursi — Özbekiston Markaziy banki ma'lumotlari asosida, kunlik özgariş bilan.",
            "ru": "Официальный курс доллара, евро, рубля и других валют — по данным ЦБ Узбекистана, с дневным изменением.",
            "en": "Official dollar, euro, ruble and other rates from the Central Bank of Uzbekistan, with daily change.",
        },
        "body": {
            "uz": """
<p>Dollar yoki rubl kursini bilmoqçi bölganda köpçilik turli saytlarda turli raqamlarni köradi. Sabab oddiy: <strong>rasmiy kurs</strong> va <strong>banklardagi kurs</strong> boşqa-boşqa narsalar. <a href="/exchangerates/">Valyuta kurslari</a> sahifasi Özbekiston Respublikasi Markaziy bankining (<a href="https://cbu.uz" target="_blank" rel="noopener">[[cbu.uz]]</a>) rasmiy ma'lumotlarini körsatadi.</p>

<h2>Sahifada nima bor</h2>
<ul>
  <li>AQŞ dollari, yevro, Rossiya rubli, Qozoğiston tengesi va boşqa valyutalarning sömdagi rasmiy qiymati.</li>
  <li>Har bir valyutaning <strong>kunlik özgarişi</strong> — kurs oşdimi yoki tuşdimi.</li>
  <li>Ma'lumot Markaziy bank e'lon qilişi bilan avtomatik yangilanadi.</li>
</ul>

<h2>Rasmiy kurs va bank kursi</h2>
<table>
  <thead><tr><th></th><th>Markaziy bank kursi</th><th>Tijorat banki kursi</th></tr></thead>
  <tbody>
    <tr><td>Kim belgilaydi</td><td>Markaziy bank, har iş kuni</td><td>Har bir bank özi</td></tr>
    <tr><td>Nima uçun</td><td>Rasmiy hisob-kitoblar, bojxona, buxgalteriya, soliqlar</td><td>Valyuta sotib oliş va sotiş</td></tr>
    <tr><td>Neçta kurs</td><td>Bitta</td><td>Ikkita: sotib oliş va sotiş</td></tr>
  </tbody>
</table>
<p>Bankda valyuta sotganda oladigan pulingiz rasmiy kursdan biroz kam, sotib olganda esa biroz köp böladi — bu farq bankning daromadi.</p>

<h2>Foydali maslahatlar</h2>
<ul>
  <li><strong>Katta summani almaştirişdan oldin</strong> bir neça bankning kursini soliştiring — farq sezilarli bölişi mumkin.</li>
  <li><strong>Kartadan çet elda tölaşda</strong> bank öz kursi va komissiyasini qöllaydi; rasmiy kurs faqat taxminiy hisob uçun.</li>
  <li><strong>Kurs prognozlariga ehtiyot böling:</strong> qisqa muddatli özgarişlarni heçkim aniq ayta olmaydi.</li>
</ul>
<p>Kriptovalyutalar narxi kerakmi? <a href="/blog/kriptovalyuta-narxlari-onlayn-bitcoin-ethereum/">Kriptovalyuta narxlari onlayn</a>.</p>
""",
            "ru": """
<p>Ища курс доллара или рубля, люди видят разные цифры на разных сайтах. Причина: <strong>официальный курс</strong> и <strong>курс в банках</strong> — разные вещи. Страница <a href="/exchangerates/">«Курсы валют»</a> показывает официальные данные Центрального банка Республики Узбекистан (<a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a>).</p>

<h2>Что на странице</h2>
<ul>
  <li>Официальная стоимость доллара США, евро, российского рубля, казахстанского тенге и других валют в сумах.</li>
  <li><strong>Дневное изменение</strong> по каждой валюте.</li>
  <li>Автоматическое обновление после публикации ЦБ.</li>
</ul>

<h2>Курс ЦБ и курс банка</h2>
<table>
  <thead><tr><th></th><th>Курс ЦБ</th><th>Курс коммерческого банка</th></tr></thead>
  <tbody>
    <tr><td>Кто устанавливает</td><td>Центробанк, каждый рабочий день</td><td>Каждый банк сам</td></tr>
    <tr><td>Для чего</td><td>Официальные расчёты, таможня, бухгалтерия, налоги</td><td>Покупка и продажа валюты</td></tr>
    <tr><td>Сколько курсов</td><td>Один</td><td>Два: покупка и продажа</td></tr>
  </tbody>
</table>
<p>Перед обменом крупной суммы сравните курсы нескольких банков. При оплате картой за границей банк применяет свой курс и комиссию.</p>
""",
            "en": """
<p>People searching for the dollar rate often see different numbers on different sites, because the <strong>official rate</strong> and <strong>bank rates</strong> are not the same thing. The <a href="/exchangerates/">Exchange rates</a> page shows official data from the Central Bank of the Republic of Uzbekistan (<a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a>): the value of the US dollar, euro, Russian ruble, Kazakh tenge and other currencies in soums, with the daily change.</p>

<h2>Official rate vs bank rate</h2>
<table>
  <thead><tr><th></th><th>Central Bank rate</th><th>Commercial bank rate</th></tr></thead>
  <tbody>
    <tr><td>Set by</td><td>Central Bank, every business day</td><td>Each bank</td></tr>
    <tr><td>Used for</td><td>Official accounting, customs, taxes</td><td>Buying and selling currency</td></tr>
    <tr><td>How many</td><td>One</td><td>Two: buy and sell</td></tr>
  </tbody>
</table>
<p>Compare several banks before exchanging a large amount; card payments abroad use the bank's own rate plus fees.</p>
""",
        },
    },
    # ==========================================================================
    # 7 · Rasmlarni soliştiriş
    # ==========================================================================
    {
        "project_id": 7,
        "slug": "ikki-rasmni-solishtirish-farqlarni-topish",
        "source_url": "https://complexprogrammer.uz/imagecompare/",
        "categorie_id": 7,
        "image": "projects/images/imagecompare.png",
        "seo_title": "Ikki rasmni soliştiriş va farqlarni topiş — onlayn, bepul",
        "seo_description": "Ikki rasm orasidagi farqlarni bir zumda toping: farqlar va slayder rejimi, sezgirlik, öxşaşlik foizi, PNG natija. Rasmlar serverga yuborilmaydi.",
        "name": {
            "uz": "Ikki rasmni soliştiriş: farqlarni bir zumda topadigan bepul onlayn vosita",
            "ru": "Сравнение двух изображений: бесплатный онлайн-инструмент для поиска отличий",
            "en": "Compare two images and find the differences online, free",
        },
        "title": {
            "uz": "Dizayn maketi va tayyor sahifa, eski va yangi skrinşot yoki ikki fotosurat — farqlar qizil bilan belgilanadi, rasmlar brauzeringizdan çiqmaydi.",
            "ru": "Макет и готовая страница, старый и новый скриншот или две фотографии — отличия выделяются красным, изображения не покидают браузер.",
            "en": "Mockup vs live page, old vs new screenshot or two photos — differences are marked in red and images never leave your browser.",
        },
        "body": {
            "uz": """
<p>Ikki rasm bir xilga öxşaydi, lekin qayerdadir farq bor — uni köz bilan topiş uzoq va işonçsiz. <a href="/imagecompare/">Rasmlarni soliştiriş</a> vositasi ikki rasmni piksel darajasida taqqoslaydi va farqli joylarni ajratib körsatadi.</p>

<h2>Qanday işlaydi</h2>
<ol>
  <li>1-rasmni (asl) va 2-rasmni (özgargan) yuklang: faylni taşlang, tanlang yoki <code>Ctrl+V</code> bilan qöying.</li>
  <li><strong>"Soliştiriş"</strong> tugmasini bosing.</li>
  <li>Natija: farqli joylar <strong>qizil</strong> bilan, farqlar sohasi <strong>ramka</strong> bilan belgilanadi; <strong>öxşaşlik foizi</strong> va özgargan piksellar soni körsatiladi.</li>
</ol>

<h2>Imkoniyatlar</h2>
<ul>
  <li><strong>Farqlar rejimi</strong> — özgargan piksellar ustma-ust belgilanadi.</li>
  <li><strong>Slayder rejimi</strong> — surgiçni surib, bir rasmdan ikkinçisiga ötasiz: çapda 1-rasm, öngda 2-rasm.</li>
  <li><strong>Sezgirlik</strong> — siqiş (kompressiya) tufayli paydo bölgan mayda farqlarni e'tiborsiz qoldiriş uçun.</li>
  <li>Rasmlar örnini almaştiriş va natijani <strong>[[PNG]]</strong> qilib yuklab oliş.</li>
</ul>

<h2>Kimga foydali</h2>
<ul>
  <li><strong>Dizayner va dasturçilar:</strong> maket bilan tayyor sahifani yoki yangilanişdan oldingi va keyingi skrinşotni soliştiriş.</li>
  <li><strong>Hujjatlar bilan işlaydiganlar:</strong> ikki skan yoki skrinşotda nima özgarganini topiş.</li>
  <li><strong>Boşqotirma ixlosmandlari:</strong> "farqni top" rasmlaridagi javoblarni tekşiriş.</li>
</ul>

<h2>Maxfiylik</h2>
<p>Soliştiriş butunlay <strong>brauzeringizda</strong> bajariladi — rasmlar serverga yuborilmaydi. Ikki rasmning ölçamlari har xil bölsa, 2-rasm 1-rasm ölçamiga moslab çöziladi; bunday holatda natija unçalik aniq bölmasligi mumkin, şuning uçun bir xil ölçamdagi rasmlarni işlating.</p>
""",
            "ru": """
<p>Две картинки кажутся одинаковыми, но где-то есть отличие — искать его глазами долго. <a href="/imagecompare/">«Сравнение изображений»</a> сопоставляет два изображения попиксельно и выделяет отличия.</p>

<h2>Как работает</h2>
<ol>
  <li>Загрузите изображение 1 (оригинал) и изображение 2 (изменённое): перетащите, выберите файл или вставьте через <code>Ctrl+V</code>.</li>
  <li>Нажмите <strong>«Сравнить»</strong>.</li>
  <li>Отличия выделяются <strong>красным</strong>, область — <strong>рамкой</strong>; показываются <strong>процент сходства</strong> и число изменённых пикселей.</li>
</ol>

<h2>Возможности</h2>
<ul>
  <li><strong>Режим «Отличия»</strong> и <strong>режим «Слайдер»</strong> (слева — изображение 1, справа — 2).</li>
  <li><strong>Чувствительность</strong> — чтобы игнорировать мелкие артефакты сжатия.</li>
  <li>Обмен изображений местами и скачивание результата в <strong>PNG</strong>.</li>
</ul>
<p>Сравнение выполняется <strong>в браузере</strong>, изображения на сервер не отправляются. Если размеры разные, второе изображение растягивается под первое — для точного результата используйте картинки одного размера.</p>
""",
            "en": """
<p>Two images look identical, yet something differs, and finding it by eye is slow. <a href="/imagecompare/">Image compare</a> checks them pixel by pixel and highlights the differences.</p>

<h2>How it works</h2>
<ol>
  <li>Add image 1 (original) and image 2 (changed): drop, pick a file or paste with <code>Ctrl+V</code>.</li>
  <li>Click <strong>Compare</strong>.</li>
  <li>Differences are marked in <strong>red</strong> with a <strong>box</strong> around the changed area, plus a <strong>similarity percentage</strong> and changed-pixel count.</li>
</ol>
<p>Switch between <strong>Differences</strong> and <strong>Slider</strong> modes, tune <strong>sensitivity</strong> to ignore compression noise, swap images and download the result as <strong>PNG</strong>. Everything runs <strong>in your browser</strong>; images are not uploaded. Use images of the same size for accurate results.</p>
""",
        },
    },
    # ==========================================================================
    # 8 · Onlayn tarjimon
    # ==========================================================================
    {
        "project_id": 8,
        "slug": "onlayn-tarjimon-ozbek-rus-ingliz",
        "source_url": "https://complexprogrammer.uz/translate/",
        "categorie_id": 7,
        "image": "projects/images/translate.jpg",
        "seo_title": "Onlayn tarjimon: özbek, rus, ingliz va 22 til — bepul",
        "seo_description": "Matnni özbek, rus, ingliz, turk va yana 18 tilga bepul tarjima qiling: tilni avtomatik aniqlaş, 5000 belgigaça matn, nusxalaş va ovozli tinglaş.",
        "name": {
            "uz": "Onlayn tarjimon: özbek, rus, ingliz va yana 19 til örtasida bepul tarjima",
            "ru": "Онлайн-переводчик: узбекский, русский, английский и ещё 19 языков бесплатно",
            "en": "Online translator: Uzbek, Russian, English and 19 more languages, free",
        },
        "title": {
            "uz": "Tilni avtomatik aniqlaş, 5000 belgigaça matn, bir bosişda nusxalaş va ovozli tinglaş — röyxatdan ötmasdan.",
            "ru": "Автоопределение языка, до 5000 символов, копирование в один клик и озвучка — без регистрации.",
            "en": "Automatic language detection, up to 5,000 characters, one-click copy and text-to-speech — no sign-up.",
        },
        "body": {
            "uz": """
<p>Rus tilidagi xatni tuşuniş, inglizça yöriqnomani öqiş yoki özbekça matnni turk hamkoringizga yuboriş kerakmi? <a href="/translate/">Onlayn tarjimon</a> 22 ta til örtasida bepul tarjima qiladi.</p>

<h2>Qaysi tillar bor</h2>
<p>Özbek, rus, ingliz, turk, qozoq, qirğiz, tojik, turkman, ozarbayjon, nemis, fransuz, ispan, italyan, arab va boşqa tillar — jami 22 ta. Manba tilini bilmasangiz, <strong>"[[Auto]]"</strong> rejimi uni özi aniqlaydi.</p>

<h2>Qanday foydalaniladi</h2>
<ol>
  <li>Çap maydonga matnni yozing yoki joylaştiring — bir martada <strong>5000 belgigaça</strong>.</li>
  <li>Manba va tarjima tilini tanlang.</li>
  <li>Natijani bir bosişda <strong>nusxalang</strong> yoki <strong>ovozli tinglang</strong> — talaffuzni eşitiş til örganayotganlar uçun foydali.</li>
</ol>

<h2>Yaxşi tarjima uçun maslahatlar</h2>
<ul>
  <li><strong>Gaplarni töliq va aniq yozing.</strong> Qisqartma va jargon tarjimani buzadi.</li>
  <li><strong>Imloga e'tibor bering.</strong> Xato yozilgan söz notöğri tarjima qilinadi.</li>
  <li><strong>Muhim hujjatlarni tekşirtiring.</strong> Maşina tarjimasi mazmunni tuşuniş uçun yaxşi, lekin şartnoma, tibbiy yoki huquqiy matnlar uçun mutaxassis tekşiruvi kerak.</li>
  <li><strong>Teskari tekşiriş:</strong> tarjimani yana asl tilga ögirib köring — mazmun saqlangan bölsa, tarjima töğri.</li>
</ul>
<p>Lotin va kirill yozuvi orasida ögiriş kerak bölsa — <a href="/blog/lotin-kirill-ogirgich-changetext/">Lotin-kirill ögirgiç</a>. Yangi alifbo harflarini yoziş: <a href="/blog/yangi-ozbek-alifbosi-klaviaturasi/">Yangi özbek alifbosi klaviaturasi</a>.</p>
""",
            "ru": """
<p>Нужно понять письмо на русском, прочитать инструкцию на английском или отправить узбекский текст турецкому партнёру? <a href="/translate/">Онлайн-переводчик</a> бесплатно переводит между 22 языками.</p>

<h2>Языки</h2>
<p>Узбекский, русский, английский, турецкий, казахский, киргизский, таджикский, туркменский, азербайджанский, немецкий, французский, испанский, итальянский, арабский и другие — всего 22. Режим <strong>«Auto»</strong> сам определяет исходный язык.</p>

<h2>Как пользоваться</h2>
<ol>
  <li>Вставьте текст — до <strong>5000 символов</strong> за раз.</li>
  <li>Выберите языки.</li>
  <li><strong>Скопируйте</strong> результат или <strong>прослушайте</strong> его.</li>
</ol>

<h2>Советы</h2>
<ul>
  <li>Пишите полными, понятными предложениями, без сокращений и сленга.</li>
  <li>Следите за орфографией — ошибка в слове портит перевод.</li>
  <li>Договоры, медицинские и юридические тексты отдавайте на проверку специалисту.</li>
  <li>Сделайте обратный перевод: если смысл сохранился, перевод верный.</li>
</ul>
""",
            "en": """
<p>Need to understand a letter in Russian, read English instructions or send Uzbek text to a Turkish partner? The <a href="/translate/">online translator</a> translates between 22 languages for free: Uzbek, Russian, English, Turkish, Kazakh, Kyrgyz, Tajik, Turkmen, Azerbaijani, German, French, Spanish, Italian, Arabic and more. <strong>Auto</strong> mode detects the source language.</p>

<h2>How to use it</h2>
<ol>
  <li>Paste up to <strong>5,000 characters</strong>.</li>
  <li>Choose the languages.</li>
  <li><strong>Copy</strong> the result or <strong>listen</strong> to it.</li>
</ol>
<p><strong>Tips:</strong> write full sentences without slang, check spelling, have contracts and medical or legal texts reviewed by a professional, and back-translate to check the meaning survived.</p>
""",
        },
    },
    # ==========================================================================
    # 9 · Kriptovalyuta narxlari (Coins)
    # ==========================================================================
    {
        "project_id": 9,
        "slug": "kriptovalyuta-narxlari-onlayn-bitcoin-ethereum",
        "source_url": "https://complexprogrammer.uz/coins/",
        "categorie_id": 4,
        "image": "projects/images/btc.png",
        "seo_title": "Kriptovalyuta narxlari onlayn: Bitcoin, Ethereum — dollar va sömda",
        "seo_description": "Top 250 kriptovalyuta narxi dollar va sömda, 24 soat va 7 kunlik özgariş, kapitalizatsiya va savdo hajmi — CoinGecko ma'lumotlari, har 5 daqiqada yangilanadi.",
        "name": {
            "uz": "Kriptovalyuta narxlari onlayn: [[Bitcoin]], [[Ethereum]] va top 250 tanga dollar va sömda",
            "ru": "Курсы криптовалют онлайн: Bitcoin, Ethereum и топ-250 монет в долларах и сумах",
            "en": "Crypto prices online: Bitcoin, Ethereum and the top 250 coins in USD and soum",
        },
        "title": {
            "uz": "Narx, 24 soat va 7 kunlik özgariş, bozor kapitalizatsiyasi va savdo hajmi — jadvalni qanday öqiş va nimalarga e'tibor beriş kerak.",
            "ru": "Цена, изменение за 24 часа и 7 дней, капитализация и объём торгов — как читать таблицу и на что обращать внимание.",
            "en": "Price, 24-hour and 7-day change, market cap and volume — how to read the table and what to watch out for.",
        },
        "body": {
            "uz": """
<p><a href="/coins/">Kriptovalyuta narxlari</a> sahifasida bozor kapitalizatsiyasi böyiça eng yirik <strong>250 ta tanga</strong> — [[Bitcoin]], [[Ethereum]], [[Solana]] va boşqalar körsatiladi. Narxlar dollarda va <strong>sömda</strong>; ma'lumotlar [[CoinGecko]]'dan olinadi va <strong>har 5 daqiqada</strong> yangilanadi.</p>

<h2>Jadvalni qanday öqiş kerak</h2>
<table>
  <thead><tr><th>Ustun</th><th>Ma'nosi</th></tr></thead>
  <tbody>
    <tr><td>Narx</td><td>Bitta tanganing joriy narxi (dollar va söm)</td></tr>
    <tr><td>24 soat / 7 kun</td><td>Şu davrda narx neça foizga özgargani</td></tr>
    <tr><td>Kapitalizatsiya</td><td>Barça tangalar soni × narx — loyihaning bozordagi "ölçami"</td></tr>
    <tr><td>Hajm (24 soat)</td><td>Bir sutkada qança savdo qilingani — likvidlik körsatkiçi</td></tr>
  </tbody>
</table>
<p>Sahifa tepasida umumiy bozor kapitalizatsiyasi, [[Bitcoin]] uluşi hamda 24 soatda eng köp ösgan va tuşgan tangalar körinadi. Tangani nomi bilan qidiriş va narx, özgariş, kapitalizatsiya yoki hajm böyiça saralaş mumkin.</p>

<h2>Sömdagi narx qanday hisoblanadi</h2>
<p>Dollar narxi Markaziy bankning rasmiy dollar kursiga köpaytiriladi. Birjalarda va P2P savdoda real söm narxi bundan farq qilişi mumkin. Rasmiy kurslar: <a href="/blog/valyuta-kurslari-markaziy-bank-kursi-bugun/">Valyuta kurslari bugun</a>.</p>

<h2>Muhim ogohlantiriş</h2>
<ul>
  <li><strong>Kriptovalyuta narxi juda tez özgaradi</strong> — bir kunda 10–20% tebraniş oddiy hol.</li>
  <li>Kiçik kapitalizatsiyali va savdo hajmi past tangalar ayniqsa xavfli.</li>
  <li>Özbekistonda kriptoaktivlar bilan bağliq faoliyat qonunçilik bilan tartibga solinadi — savdo qilişdan oldin amaldagi qoidalar bilan tanişing.</li>
  <li>Bu sahifa — <strong>ma'lumot uçun</strong>, investitsiya maslahati emas. Yöqotişga tayyor bölmagan pulni kiritmang.</li>
</ul>
""",
            "ru": """
<p>На странице <a href="/coins/">«Курсы криптовалют»</a> — <strong>250 крупнейших монет</strong> по капитализации: Bitcoin, Ethereum, Solana и другие. Цены в долларах и <strong>сумах</strong>, данные CoinGecko обновляются <strong>каждые 5 минут</strong>.</p>

<h2>Как читать таблицу</h2>
<table>
  <thead><tr><th>Столбец</th><th>Значение</th></tr></thead>
  <tbody>
    <tr><td>Цена</td><td>Текущая цена одной монеты</td></tr>
    <tr><td>24 ч / 7 дн</td><td>Изменение цены в процентах</td></tr>
    <tr><td>Капитализация</td><td>Количество монет × цена — «размер» проекта</td></tr>
    <tr><td>Объём (24 ч)</td><td>Сколько наторговано за сутки — показатель ликвидности</td></tr>
  </tbody>
</table>
<p>Вверху — общая капитализация рынка, доля Bitcoin, лидеры роста и падения за сутки. Есть поиск по названию и сортировка.</p>

<h2>Цена в сумах</h2>
<p>Долларовая цена умножается на официальный курс доллара ЦБ; на биржах и в P2P реальная цена может отличаться.</p>

<h2>Предупреждение</h2>
<p>Криптовалюты очень волатильны: колебания на 10–20% за день — обычное дело. Деятельность с криптоактивами в Узбекистане регулируется законом — ознакомьтесь с правилами. Это <strong>информация, а не инвестиционный совет</strong>.</p>
""",
            "en": """
<p>The <a href="/coins/">Crypto prices</a> page lists the <strong>top 250 coins</strong> by market cap — Bitcoin, Ethereum, Solana and more — in US dollars and <strong>soums</strong>. Data comes from CoinGecko and refreshes <strong>every 5 minutes</strong>.</p>

<h2>Reading the table</h2>
<table>
  <thead><tr><th>Column</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>Price</td><td>Current price of one coin</td></tr>
    <tr><td>24h / 7d</td><td>Price change in percent</td></tr>
    <tr><td>Market cap</td><td>Coins in circulation × price</td></tr>
    <tr><td>Volume (24h)</td><td>Traded in the last day — a liquidity signal</td></tr>
  </tbody>
</table>
<p>The top of the page shows total market cap, Bitcoin dominance and the biggest 24-hour gainers and losers; you can search and sort. Soum prices use the Central Bank's official dollar rate, so exchange and P2P prices may differ. Crypto is highly volatile and regulated in Uzbekistan; this page is <strong>information, not investment advice</strong>.</p>
""",
        },
    },
    # ==========================================================================
    # 1 · Sitemap generator
    # ==========================================================================
    {
        "project_id": 1,
        "slug": "sitemap-xml-yaratish-bepul-generator",
        "source_url": "https://complexprogrammer.uz/sitemap/",
        "categorie_id": 7,
        "image": "projects/images/sitemap.png",
        "seo_title": "sitemap.xml yaratiş: bepul generator va Google'ga yuboriş",
        "seo_description": "Sayt xaritasi (sitemap.xml) nima uçun kerak, uni bepul generator bilan qanday yaratiş, robots.txt'ga qöşiş va Google Search Console hamda Yandex Webmaster'ga yuboriş.",
        "name": {
            "uz": "[[sitemap.xml]] yaratiş: bepul generator va [[Google]] hamda [[Yandex]]ga yuboriş qöllanmasi",
            "ru": "Как создать sitemap.xml: бесплатный генератор и отправка в Google и Яндекс",
            "en": "How to create sitemap.xml: a free generator and submitting it to Google",
        },
        "title": {
            "uz": "Sayt xaritasi qidiruv tizimlariga sahifalarni tezroq topişga yordam beradi — 300 tagaça sahifani avtomatik topib, tayyor fayl beradigan vosita va keyingi 3 qadam.",
            "ru": "Карта сайта помогает поисковикам быстрее находить страницы — инструмент сам находит до 300 страниц и выдаёт готовый файл, плюс 3 следующих шага.",
            "en": "A sitemap helps search engines find your pages faster — this tool crawls up to 300 pages and gives you a ready file, plus the 3 next steps.",
        },
        "body": {
            "uz": """
<p><strong>[[sitemap.xml]]</strong> — saytingizdagi sahifalar röyxati yozilgan maxsus fayl. Qidiruv tizimlari ([[Google]], [[Yandex]], [[Bing]]) uni öqib, sahifalarni tezroq topadi va indekslaydi. Ayniqsa yangi sayt, köp sahifali sayt yoki bir-biriga kam bağlangan sahifalar uçun muhim.</p>

<h2>Generator qanday işlaydi</h2>
<ol>
  <li><a href="/sitemap/">Sitemap generator</a> sahifasiga sayt manzilini kiriting, masalan <code>example.uz</code>.</li>
  <li><strong>"Sitemap yaratiş"</strong>ni bosing — vosita saytingizdagi havolalarni aylanib çiqadi va <strong>300 tagaça sahifa</strong> topadi.</li>
  <li>Topilgan sahifalar röyxatini va tayyor [[XML]]ni köring, keyin <code>sitemap.xml</code> faylini yuklab oling yoki nusxalang.</li>
</ol>
<p><code>robots.txt</code> taqiqlagan, <code>noindex</code> bilan belgilangan va [[HTML]] bölmagan sahifalar xaritaga kirmaydi — qidiruvga keraksiz sahifalar tuşmaydi.</p>

<h2>Keyingi 3 qadam</h2>
<ol>
  <li><strong>Faylni joylang:</strong> <code>sitemap.xml</code>ni saytning boş papkasiga yuklang, u <code>https://example.uz/sitemap.xml</code> manzilida oçilişi kerak.</li>
  <li><strong><code>robots.txt</code>ga qöşing:</strong> <code>Sitemap: https://example.uz/sitemap.xml</code></li>
  <li><strong>Yuboring:</strong> [[Google Search Console]] (Sitemaps bölimi) va [[Yandex Webmaster]] (Indeksirovanie → Fayly Sitemap) ga sitemap manzilini kiriting.</li>
</ol>

<h2>Foydali maslahatlar</h2>
<ul>
  <li>Saytga yangi sahifalar qöşilganda sitemap'ni yangilang (köp [[CMS]]lar buni özi qiladi).</li>
  <li>Sitemap indekslanişni kafolatlamaydi — u faqat qidiruv tizimiga "bu sahifalar bor" deb aytadi. Sifatli matn va içki havolalar ham kerak.</li>
  <li>Bitta faylda 50 000 tadan ortiq manzil bölmasligi kerak; katta saytlar bir neça fayl va sitemap index işlatadi.</li>
</ul>
""",
            "ru": """
<p><strong>sitemap.xml</strong> — файл со списком страниц сайта. Поисковые системы (Google, Яндекс, Bing) читают его и быстрее находят и индексируют страницы. Особенно важно для новых и больших сайтов.</p>

<h2>Как работает генератор</h2>
<ol>
  <li>Введите адрес сайта на странице <a href="/sitemap/">генератора sitemap</a>, например <code>example.uz</code>.</li>
  <li>Нажмите <strong>«Создать sitemap»</strong> — инструмент обойдёт ссылки и найдёт <strong>до 300 страниц</strong>.</li>
  <li>Посмотрите список страниц и готовый XML, скачайте <code>sitemap.xml</code> или скопируйте.</li>
</ol>
<p>Страницы, закрытые в <code>robots.txt</code>, с <code>noindex</code> и не-HTML в карту не попадают.</p>

<h2>3 следующих шага</h2>
<ol>
  <li>Загрузите <code>sitemap.xml</code> в корень сайта: <code>https://example.uz/sitemap.xml</code>.</li>
  <li>Добавьте в <code>robots.txt</code>: <code>Sitemap: https://example.uz/sitemap.xml</code></li>
  <li>Отправьте адрес в Google Search Console (Sitemaps) и Яндекс Вебмастер (Индексирование → Файлы Sitemap).</li>
</ol>
<p>Sitemap не гарантирует индексацию — нужны качественный текст и внутренние ссылки. В одном файле — не более 50 000 адресов.</p>
""",
            "en": """
<p><strong>sitemap.xml</strong> lists your site's pages so search engines (Google, Yandex, Bing) can find and index them faster, which matters most for new or large sites.</p>

<h2>How the generator works</h2>
<ol>
  <li>Enter your site on the <a href="/sitemap/">sitemap generator</a> page, e.g. <code>example.uz</code>.</li>
  <li>Click <strong>Create sitemap</strong>; the tool follows your links and finds <strong>up to 300 pages</strong>.</li>
  <li>Review the page list and XML, then download or copy <code>sitemap.xml</code>.</li>
</ol>
<p>Pages blocked by <code>robots.txt</code>, marked <code>noindex</code>, or not HTML are left out.</p>

<h2>Next 3 steps</h2>
<ol>
  <li>Upload it to your site root: <code>https://example.uz/sitemap.xml</code>.</li>
  <li>Add to <code>robots.txt</code>: <code>Sitemap: https://example.uz/sitemap.xml</code></li>
  <li>Submit it in Google Search Console (Sitemaps) and Yandex Webmaster.</li>
</ol>
<p>A sitemap does not guarantee indexing; content quality and internal links still matter. Keep each file under 50,000 URLs.</p>
""",
        },
    },
]
