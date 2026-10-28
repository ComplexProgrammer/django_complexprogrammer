"""Complex Programmer (/projects/) bölimidagi barça onlayn öyinlar uçun blog maqolalarini rasmlari bilan birga naşr qiliş yoki yangilaş.

Işlatiş:
    python manage.py publish_games_posts                  # barça 8 ta öyin maqolasini naşr qiladi
    python manage.py publish_games_posts --update         # mavjud maqolalarni ham yangilaydi
    python manage.py publish_games_posts --draft          # qoralama sifatida saqlaydi (2099-yil)
    python manage.py publish_games_posts --dry-run        # bazaga yozmasdan tekşiradi
    python manage.py publish_games_posts --game snake     # faqat bitta öyin maqolasini naşr qiladi
"""

import datetime
import os
import re
import threading
import time

DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)

GAMES_ARTICLES = [
    # ==========================================================================
    # 1. SNAKE (ILON ÖYINI)
    # ==========================================================================
    {
        "key": "snake",
        "slug": "snake-ilon-oyini-onlayn-oynash",
        "image": "post/images/snake_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/snake/",
        "seo_title": "Snake (Ilon öyini) onlayn öynaş — bepul klassik arkada",
        "seo_description": (
            "Klassik Snake (Ilon) öyinini brauzerda bepul öynang: 20×20 maydon, "
            "3 xil tezlik, 2 xil devor rejimi, klaviatura va mobil sensor boşqaruvi."
        ),
        "uz": {
            "name": "Snake (Ilon öyini) — klassik arkadani yangi imkoniyatlar bilan onlayn öynang",
            "title": (
                "20×20 katakli maydon, 3 xil tezlik va 2 xil devor rejimi: brauzerda "
                "bepul öynaladigan zamonaviy Ilon öyini qoidalari, boşqaruvi va sirlari."
            ),
            "body": """
<p>Afsonaviy telefonlardan tortib zamonaviy kompyuterlargaça millionlab insonlarning sevimli vaqt çöğlik vositasiga aylangan <strong><span translate="no">Snake</span> (Ilon öyini)</strong> bugun yangilangan, silliq va qulay veb-talqinda taqdim etilmoqda. <a href="https://complexprogrammer.uz/snake/"><strong>Complex Programmer — Ilon öyini</strong></a> sahifasida heç qanday ilova yuklab olmasdan va röyxatdan ötmasdan kompyuter yoki smartfon brauzerida darhol öynaşingiz mumkin.</p>

<p>Uşbu talqin klassik arkada ruhini saqlagan holda, tezlikni moslaştiriş, devor rejimini tanlaş, klaviatura navbati (<span translate="no">Input Queue</span>) va natijalarni <span translate="no">Telegram</span> orqali döstlar bilan ulașiş kabi zamonaviy imkoniyatlar bilan boyitilgan.</p>

<h2>1. Öyin qoidalari va dinamik tezlik tizimi</h2>
<p>Öyin <strong>20×20 katakli</strong> şaxmat uslubidagi yaşil maydonda keçadi. Siz 3 boğindan iborat ilonça bilan harakatni boşlaysiz. Maydonning boş kataklarida qizil olmalar paydo böladi:</p>
<ul>
  <li>Har bir yeyilgan olma uçun <strong>+1 ball</strong> beriladi va ilonning tanasi bitta boğinga uzayadi.</li>
  <li>Har <strong>5 ta olmadan keyin</strong> ilonning harakat tezligi avtomatik ravişda <strong>8% ga oşib boradi</strong> (maksimal tezlik soniyasiga 24 qadamgaça yetadi).</li>
  <li>Ilonning közlari har doim harakat yönalişiga qarab buriladi, tana boğinlari esa boşdan dumga qarab oç yaşildan töq zumrad rangga silliq ötadi.</li>
  <li>Maqsad — ilon öz dumi yoki qattiq devorga urilib ketmasdan imkon qadar köproq olma yigiş va şaxsiy rekordni yangilaşdir.</li>
</ul>

<h2>2. Tezlik va devor rejimlarini erkin tanlaş</h2>
<p>Har bir öyinçi öz tajribasi va kayfiyatiga mos sozlamalarni öyin oldidan yoki pauza vaqtida tanlaşi mumkin:</p>
<ul>
  <li><strong>3 xil boşlanğiç tezlik:</strong> <em>Sekin</em> (soniyasiga 6.5 qadam — yangi öyinçilar uçun), <em>Örta</em> (soniyasiga 9.5 qadam — optimal muvozanat) va <em>Tez</em> (soniyasiga 13.5 qadam — tezkor reaksiya ustalari uçun).</li>
  <li><strong>«Ötib ketadi» devor rejimi:</strong> Ilon maydonning öng çetidan çiqsa, çap tomondan, yuqoridan çiqsa pastki tomondan paydo böladi. Bu rejimda öyin faqat ilon öz tanasiga urilgandagina yakunlanadi.</li>
  <li><strong>«Urilsa — öyin tugaydi» rejimi:</strong> Klassik qattiq çegarali rejim bölib, maydon devoriga tegiş darhol öyinni töxtatadi va yuqori diqqatni talab qiladi.</li>
</ul>

<h2>3. Qulay boşqaruv: Kompyuter va Mobil qurilmalar</h2>
<p>Öyin barça turdagi ekranlar va kiritiş qurilmalari uçun mukammal moslaştirilgan:</p>
<table>
  <thead>
    <tr>
      <th>Qurilma turi</th>
      <th>Harakatlantiriş</th>
      <th>Pauza va Qöşimça</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Kompyuter (Klaviatura)</strong></td>
      <td><code>↑ ↓ ← →</code> strelkalari yoki <code>W A S D</code> (kirill klaviaturasida ham <code>Ц Ы Ф В</code> avtomatik işlaydi)</td>
      <td><code>Space</code>, <code>P</code> yoki <code>Esc</code> — pauza; boşqa tabga ötganda avto-pauza</td>
    </tr>
    <tr>
      <td><strong>Smartfon va Planşet</strong></td>
      <td>Maydon ustida barmoqni silaş (<em>svayp</em>) yoki ekran ostidagi <code>▲ ◀ ▼ ▶</code> sensor tugmalar</td>
      <td>Yuqori paneldagi <strong>⏸ Pauza</strong> va <strong>🔄 Qayta</strong> tugmalari</td>
    </tr>
  </tbody>
</table>
<p>Maxsus <strong>tugmalar navbati (<span translate="no">Input Queue</span>)</strong> tufayli ikkita tugmani juda tez ketma-ket bosganingizda ham ilon öz-öziga teskari burilib urilib ketmaydi — burilişlar ketma-ket ikki qadamda aniq bajariladi.</p>

<h2>4. Yuqori ball töplaş sirlari</h2>
<ol>
  <li><strong>Maydon çetlari böylab zigzag harakatlaning:</strong> Ilon uzayganida maydon markazida qamalib qolmaslik uçun devor yaqinida tizimli aylana hosil qiling.</li>
  <li><strong>«Ötib ketadi» rejimidan unumli foydalaning:</strong> Olma maydonning qarama-qarşi burçağida çiqsa, butun maydonni kesib ötmasdan yaqin devor orqali bir zumda öting.</li>
  <li><strong>Dumingiz ortidan yuring:</strong> Ilon maydonning yarmini egallaganda eng xavfsiz yöl — öz dumingiz böşatayotgan kataklar izidan harakatlanişdir.</li>
</ol>

<p><a class="b-btn" href="https://complexprogrammer.uz/snake/">🐍 Snake (Ilon öyini)ni hoziroq öynaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Snake (Илон ўйини) — классик аркадани янги имкониятлар билан онлайн ўйнанг",
            "title": (
                "20×20 катакли майдон, 3 хил тезлик ва 2 хил девор режими: браузерда "
                "бепул ўйналадиган замонавий Илон ўйини қоидалари, бошқаруви ва сирлари."
            ),
        },
        "ru": {
            "name": "Snake (Змейка) онлайн — классическая аркада с новыми режимами скорости и стен",
            "title": (
                "Играйте в классическую Змейку на поле 20×20 бесплатно в браузере: "
                "3 скорости, 2 режима стен, управление WASD/свайпами и таблица личных рекордов."
            ),
            "body": """
<p>Легендарная аркада <strong>Snake (Змейка)</strong>, знакомая каждому со времен классических телефонов, доступна в современном веб-исполнении на <a href="https://complexprogrammer.uz/snake/"><strong>Complex Programmer — Snake</strong></a>. Игра запускается мгновенно в браузере компьютера или смартфона без установки приложений и регистрации.</p>

<h2>1. Правила игры и динамическое ускорение</h2>
<p>Действие разворачивается на клетчатом зеленом поле размером <strong>20×20 клеток</strong>:</p>
<ul>
  <li>За каждое съеденное красное яблоко начисляется <strong>+1 очко</strong>, а змейка увеличивается на один сегмент.</li>
  <li>Каждые <strong>5 яблок</strong> скорость движения плавно <strong>возрастает на 8%</strong> (вплоть до 24 шагов в секунду).</li>
  <li>Умная очередь нажатий (<em>Input Queue</em>) защищает от случайного разворота в самого себя при быстрых двойных нажатиях клавиш.</li>
</ul>

<h2>2. Выбор скорости и режима стен</h2>
<ul>
  <li><strong>3 уровня начальной скорости:</strong> <em>Медленно</em> (6.5 шаг/с), <em>Средне</em> (9.5 шаг/с) и <em>Быстро</em> (13.5 шаг/с).</li>
  <li><strong>Режим «Проходит сквозь стены»:</strong> змейка телепортируется через противоположный край поля.</li>
  <li><strong>Режим «Столкновение — конец игры»:</strong> классические твердые границы для ценителей хардкора.</li>
</ul>

<h2>3. Управление на ПК и смартфонах</h2>
<ul>
  <li><strong>Клавиатура:</strong> стрелки <code>↑ ↓ ← →</code> или клавиши <code>W A S D</code> (работает даже при включенной русской раскладке <code>Ц Ы Ф В</code>). Пауза — <code>Space</code>, <code>P</code> или <code>Esc</code>.</li>
  <li><strong>Мобильные устройства:</strong> свайпы по игровому полю или удобный блок кнопок <code>▲ ◀ ▼ ▶</code> под экраном. При переключении вкладки браузера срабатывает автопауза.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/snake/">🐍 Играть в Snake (Змейку) онлайн</a></p>
""",
        },
        "en": {
            "name": "Play Snake Online — Classic Arcade Game with Custom Speeds and Wall Modes",
            "title": (
                "Enjoy a modern, responsive 20×20 Snake game in your browser: "
                "3 speed presets, wrap-around or solid walls, input queue, and mobile touch controls."
            ),
            "body": """
<p>The timeless <strong>Snake</strong> arcade game returns in a sleek, responsive browser edition on <a href="https://complexprogrammer.uz/snake/"><strong>Complex Programmer — Snake</strong></a>. Play instantly on desktop or mobile with zero downloads or sign-ups.</p>

<h2>1. Gameplay Mechanics & Dynamic Speed</h2>
<ul>
  <li>Navigate a <strong>20×20 checkerboard grid</strong>, collecting red apples to grow longer and earn <strong>+1 point</strong> per apple.</li>
  <li>Every <strong>5 apples</strong>, the snake accelerates by <strong>8%</strong> (up to a brisk 24 steps per second).</li>
  <li>Built-in <strong>Input Queueing</strong> buffers rapid two-key turns so you never accidentally reverse into your own neck.</li>
</ul>

<h2>2. Customizable Speed & Wall Modes</h2>
<ul>
  <li><strong>3 Speed Presets:</strong> <em>Slow</em> (6.5 steps/s), <em>Medium</em> (9.5 steps/s), and <em>Fast</em> (13.5 steps/s).</li>
  <li><strong>Wrap-Around Walls:</strong> Pass through one edge of the arena and emerge on the opposite side.</li>
  <li><strong>Solid Walls:</strong> Classic rules where touching the perimeter ends the run immediately.</li>
</ul>

<h2>3. Desktop & Mobile Controls</h2>
<ul>
  <li><strong>Desktop:</strong> Arrow keys (<code>↑ ↓ ← →</code>) or <code>W A S D</code>; press <code>Space</code>, <code>P</code>, or <code>Esc</code> to pause. Automatic pause activates when switching browser tabs.</li>
  <li><strong>Mobile:</strong> Swipe anywhere on the board or use the on-screen <code>▲ ◀ ▼ ▶</code> directional pad.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/snake/">🐍 Play Snake Online Now</a></p>
""",
        },
    },

    # ==========================================================================
    # 2. CAR RACING (AVTOPOYGA)
    # ==========================================================================
    {
        "key": "car",
        "slug": "car-racing-mashina-poygasi-onlayn-oyin",
        "image": "post/images/car_racing_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/car/",
        "seo_title": "Car Racing (Avtopoyga) — onlayn maşina poygasi öyini",
        "seo_description": (
            "3 polosali magistralda sport avtomobilini boşqaring! Tirbandlikdagi "
            "maşinalardan çap bering, tezlikni oşiring va yangi rekord örnating."
        ),
        "uz": {
            "name": "Car Racing (Avtopoyga) — 3 polosali magistralda tezlik va reaksiya sinovi",
            "title": (
                "Qizil sport avtomobilini tirbandlik orasidan olib öting: aqlli trafik "
                "tizimi, ovoz effektlari, klaviatura va mobil boşqaruv hamda Google Play ilovasi."
            ),
            "body": """
<p>Yuqori tezlik, tezkor manyovrlar va adrenalinni yoqtiruvçilar uçun <a href="https://complexprogrammer.uz/car/"><strong>Complex Programmer — Car Racing (Avtopoyga)</strong></a> onlayn öyini ajoyib tanlovdir. Siz qizil sport avtomobilini uç polosali katta magistralda boşqarib, oldinda harakatlanayotgan turli rangdagi maşinalar bilan töqnaşib ketmasdan maksimal masofani bosib ötişingiz kerak.</p>

<p>Öyin ham kompyuter va smartfon brauzerida, ham rasmiy <a href="https://play.google.com/store/apps/details?id=car.complexprogrammeruz" target="_blank" rel="noopener"><strong><span translate="no">Google Play</span> Android ilovasi</strong></a> körinişida bepul taqdim etilgan.</p>

<h2>1. Öyin jarayoni va aqlli trafik generatori</h2>
<p>Magistral uçta harakat yölakçasidan iborat bölib, vaqt ötgani sayin avtomobilingizning tezligi (<code>km/soat</code>) va yigayotgan ballaringiz muttasil oşib boradi:</p>
<ul>
  <li><strong>Adolatli va aqlli trafik:</strong> Maxsus algoritm bir vaqtning özida uçala yölakçani ham töliq yopib qöymaydi — har qanday vaziyatda kamida bitta oçiq yölak qoldiriladi. Demak, natija omadga emas, faqat sizning reaksiyangizga boğliq!</li>
  <li><strong>Tezlikni nazorat qiliş:</strong> Gazni bosib tezlikni oşirişingiz (va köproq ball olişingiz) yoki xavfli tirbandlik oldidan tormoz bosib tezlikni pasaytirişingiz mumkin.</li>
  <li><strong>Ovoz va vizual effektlar:</strong> Dvigatel ovozi va töqnaşuv zarbasi (ekran titraşi hamda ovozni öçirib-yoqiş tugmasi bilan) poyga muhitini jonlantiradi.</li>
</ul>

<h2>2. Boşqaruv tugmalari (Kompyuter va Mobil)</h2>
<table>
  <thead>
    <tr>
      <th>Qurilma</th>
      <th>Çapga / Öngga manyovr</th>
      <th>Gaz / Tormoz va Pauza</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Klaviatura</strong></td>
      <td><code>←</code> / <code>→</code> strelkalari yoki <code>A</code> / <code>D</code> tugmalari</td>
      <td><code>↑</code> / <code>W</code> — tezlaşiş, <code>↓</code> / <code>S</code> — sekinlaşiş, <code>Space</code> / <code>P</code> — pauza</td>
    </tr>
    <tr>
      <td><strong>Smartfon (Sensor)</strong></td>
      <td>Ekran ostidagi <code>◀</code> va <code>▶</code> tugmalari yoki yölning çap/öng yarmiga bosib turiş</td>
      <td><code>▲</code> (Gaz) va <code>▼</code> (Tormoz) sensor tugmalari</td>
    </tr>
  </tbody>
</table>

<h2>3. Magistralda uzoqroq masofani zabt etiş sirlari</h2>
<ol>
  <li><strong>Örta yölakni asosiy pozitsiya sifatida tanlang:</strong> Markaziy polosada turganingizda ham çapga, ham öngga bir xil vaqtda qoçiş imkoniyatingiz böladi.</li>
  <li><strong>Uzoqqa qarang:</strong> Nigohingizni öz maşinangiz kapotiga emas, ekranning yuqori çetidan çiqib kelayotgan yangi maşinalar oqimiga qarating.</li>
  <li><strong>Tor joylarda tormozdan foydalaning:</strong> Ikki qator maşina orasidan siqilib ötişda <code>↓</code> yoki <code>S</code> tugmasi bilan tezlikni biroz tuşiriş töqnaşuvning oldini oladi.</li>
</ol>

<p><a class="b-btn" href="https://complexprogrammer.uz/car/">🏎️ Car Racing poygasini hoziroq boşlaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Car Racing (Автопойга) — 3 полосали магистралда тезлик ва реакция синови",
            "title": (
                "Қизил спорт автомобилини тирбандлик орасидан олиб ўтинг: ақлли трафик "
                "тизими, овоз эффектлари, клавиатура ва мобил бошқарув ҳамда Google Play иловаси."
            ),
        },
        "ru": {
            "name": "Car Racing (Автогонки) онлайн — проверьте реакцию на трехполосной трассе",
            "title": (
                "Управляйте красным спорткаром в плотном потоке машин: умная генерация "
                "трафика, контроль скорости, звуковые эффекты и приложение в Google Play."
            ),
            "body": """
<p>Динамичная аркадная гонка <a href="https://complexprogrammer.uz/car/"><strong>Complex Programmer — Car Racing</strong></a> предлагает испытать водительские рефлексы на скоростном трехполосном шоссе. Лавируйте между попутными автомобилями, контролируйте спидометр (<code>км/ч</code>) и ставьте новые рекорды дистанции.</p>

<h2>1. Особенности геймплея и умный трафик</h2>
<ul>
  <li><strong>Гарантированный проход:</strong> генератор трафика исключает появление непроходимых «стен» из трех машин в ряд — на трассе всегда остается минимум одна свободная полоса.</li>
  <li><strong>Управление тягой:</strong> ускоряйтесь для быстрого набора очков или притормаживайте перед плотными связками машин.</li>
  <li><strong>Атмосфера гонки:</strong> реальный звук мотора, эффект тряски экрана при аварии и четкая векторная графика для экранов Retina.</li>
</ul>

<h2>2. Управление на ПК и телефонах</h2>
<ul>
  <li><strong>Клавиатура:</strong> <code>← →</code> или <code>A D</code> — перестроение, <code>↑ W</code> — газ, <code>↓ S</code> — тормоз, <code>Space / P</code> — пауза.</li>
  <li><strong>Смартфон:</strong> 4 удобные экранные педали (<code>◀ ▼ ▲ ▶</code>) либо нажатия по левой и правой половине дороги. Также доступно официальное Android-приложение в <a href="https://play.google.com/store/apps/details?id=car.complexprogrammeruz" target="_blank" rel="noopener">Google Play</a>.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/car/">🏎️ Начать заезд в Car Racing</a></p>
""",
        },
        "en": {
            "name": "Car Racing Online — High-Speed 3-Lane Highway Arcade Game",
            "title": (
                "Steer your red sports car through dense highway traffic with fair lane "
                "generation, throttle control, sound effects, and mobile touch pedals."
            ),
            "body": """
<p>Put your reflexes to the test in <a href="https://complexprogrammer.uz/car/"><strong>Complex Programmer — Car Racing</strong></a>. Pilot a sleek red sports car down a bustling 3-lane highway, dodge colorful traffic vehicles, and push your speedometer to the limit.</p>

<h2>1. Key Features & Fair Traffic Spawner</h2>
<ul>
  <li><strong>Smart Traffic Logic:</strong> The wave generator guarantees at least one open lane at all times—every crash is avoidable with quick reactions.</li>
  <li><strong>Throttle & Brake Control:</strong> Accelerate to boost your score faster or tap the brakes when weaving through tight gaps.</li>
  <li><strong>Audio & Visual Polish:</strong> Engine and crash sound effects (with mute toggle), collision screen-shake, and an official <a href="https://play.google.com/store/apps/details?id=car.complexprogrammeruz" target="_blank" rel="noopener">Google Play Android app</a>.</li>
</ul>

<h2>2. Controls</h2>
<ul>
  <li><strong>Desktop:</strong> <code>← →</code> or <code>A D</code> to steer, <code>↑ W</code> to accelerate, <code>↓ S</code> to brake, <code>Space / P</code> to pause.</li>
  <li><strong>Mobile:</strong> On-screen <code>◀ ▼ ▲ ▶</code> touch controls or tap the left/right half of the road.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/car/">🏎️ Play Car Racing Online</a></p>
""",
        },
    },

    # ==========================================================================
    # 3. DUCK HUNT (ÖRDAK OVI)
    # ==========================================================================
    {
        "key": "duckhunt",
        "slug": "duck-hunt-ordak-ovi-onlayn-oyin",
        "image": "post/images/duck_hunt_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/duckhunt/",
        "seo_title": "Duck Hunt (Ördak ovi) — merganlik va reaksiya onlayn öyini",
        "seo_description": (
            "Klassik Duck Hunt (Ördak ovi) öyinini onlayn öynang: 10 ta ördakni "
            "eng qisqa vaqtda urib tuşiring, aniqlik foizini oşiring va rekord yangilang."
        ),
        "uz": {
            "name": "Duck Hunt (Ördak ovi) — merganlik, tezlik va aniqlikni sinovçi onlayn öyin",
            "title": (
                "10 ta ördakni eng qisqa soniyalarda urib tuşiring: jonli aniqlik "
                "statistikasi, tolqinsimon parvoz fizikasi va kompyuter/mobil nişon tizimi."
            ),
            "body": """
<p>Retro konsollarning eng maşhur merganlik öyini — <strong><span translate="no">Duck Hunt</span> (Ördak ovi)</strong> endi zamonaviy tezkor musobaqa formatida <a href="https://complexprogrammer.uz/duckhunt/"><strong>Complex Programmer — Duck Hunt</strong></a> sahifasida! Bu yerda asosiy maqsad şunçaki ördaklarni uriş emas, balki <strong>10 ta ördakni imkon qadar qisqa vaqt (soniya) içida</strong> nişonga olişdir.</p>

<h2>1. Öyin qoidalari va vaqt poygasi</h2>
<p>Öyin boşlanişi bilan soniyaölçagiç (taymer) işga tuşadi va yam-yaşil ötloq uzra ördaklar parvoz qila boşlaydi:</p>
<ul>
  <li><strong>Maqsad — 10 ta ördak:</strong> 10-ördak urib tuşirilgan lahzada vaqt töxtaydi. Qança kam soniya sarflasangiz, rekordingiz şunça yuqori hisoblanadi!</li>
  <li><strong>Qiyinlaşib boruvçi parvoz:</strong> Ekranda bir vaqtning özida 2 tagaça ördak tolqinsimon trayektoriyada uçadi. Har bir aniq öqdan keyin keyingi ördaklarning parvoz tezligi oşib boradi.</li>
  <li><strong>5.5 soniyalik çegara:</strong> Agar ördakni 5.5 soniya içida urib ulgurmasangiz, u osmonga tik kötarilib uçib ketadi va qimmatli vaqtingizni yöqotasiz.</li>
  <li><strong>Jonli statistika:</strong> Yuqori panelda urilgan ördaklar soni (<code>0/10</code>), ötgan vaqt (<code>s</code>) va merganlik aniqligi (<code>%</code>) real vaqtda körsatib boriladi.</li>
</ul>

<h2>2. Kompyuter va Smartfonda nişonga oliş</h2>
<ul>
  <li><strong>Kompyuterda (Siçqonça):</strong> Maydon ustida kursor qizil optik nişon (<em>crosshair</em>) şakliga kiradi. Ördak ustiga olib borib çap tugmani bosiş kifoya.</li>
  <li><strong>Mobil qurilmalarda (Sensor ekran):</strong> Barmoq bilan ekranga tegib otiş qulay bölişi uçun mobil rejimda ördakning zarba maydoni (<em>hitbox</em>) <strong>1.6 barobar kengaytirilgan</strong>.</li>
  <li><strong>Vizual va ovozli javob:</strong> Har bir aniq zarbadan söng patlar soçilişi animatsiyasi, ördakning aylanib qulaşi va öq ovozi (ovozni öçiriş tugmasi bilan) işlaydi.</li>
</ul>

<h2>3. Rekord vaqt (10 soniyadan tez) qayd etiş sirlari</h2>
<ol>
  <li><strong>Oldinroqqa möljal oling:</strong> Ördaklar tolqinsimon harakat qilgani sababli nişonni ördakning dumiga emas, tumşuğidan biroz oldinroqqa olib borib oting.</li>
  <li><strong>Bir vaqtda ikkita ördak çiqqanda yaqinroğini uring:</strong> Ekran çetiga yaqinlaşib qolgan ördak uçib ketmasligi uçun avval uni nişonga oling.</li>
  <li><strong>Boş öqlarni kamaytiring:</strong> Har bir xato otilgan öq umumiy aniqlik foizini (<code>%</code>) tuşiradi va diqqatni çalğitadi.</li>
</ol>

<p><a class="b-btn" href="https://complexprogrammer.uz/duckhunt/">🦆 Duck Hunt (Ördak ovi)ni hoziroq öynaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Duck Hunt (Ўрдак ови) — мерганлик, тезлик ва аниқликни синовчи онлайн ўйин",
            "title": (
                "10 та ўрдакни энг қисқа сонияларда уриб туширинг: жонли аниқлик "
                "статистикаси, тўлқинсимон парвоз физикаси ва компьютер/мобил нишон тизими."
            ),
        },
        "ru": {
            "name": "Duck Hunt (Утиная охота) онлайн — скоростной тир на точность и реакцию",
            "title": (
                "Сбейте 10 уток за минимальное время: живая статистика меткости, "
                "волновая траектория полета и удобный прицел для мыши и сенсорных экранов."
            ),
            "body": """
<p>Классическая аркада <strong>Duck Hunt (Утиная охота)</strong> переосмыслена в формате скоростного челленджа на <a href="https://complexprogrammer.uz/duckhunt/"><strong>Complex Programmer — Duck Hunt</strong></a>. Ваша задача — поразить <strong>10 летящих уток за минимальное количество секунд</strong>, сохранив высокую точность стрельбы.</p>

<h2>1. Механика игры и счетчик времени</h2>
<ul>
  <li>На экране одновременно летают до 2 уток по синусоидальной траектории. С каждым попаданием скорость полета возрастает.</li>
  <li>Если не сбить утку за <strong>5.5 секунды</strong>, она улетает вверх за пределы экрана, отнимая драгоценное время.</li>
  <li>На верхней панели в реальном времени отображаются: количество сбитых целей (<code>0/10</code>), секундомер и процент меткости (<code>%</code>).</li>
</ul>

<h2>2. Управление мышью и на мобильных экранах</h2>
<ul>
  <li><strong>ПК:</strong> наводите красный снайперский прицел мышью и стреляйте левой кнопкой.</li>
  <li><strong>Смартфоны и планшеты:</strong> стреляйте касанием пальца — для комфортной игры на тачскринах область попадания (<em>hitbox</em>) увеличена в <strong>1.6 раза</strong>.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/duckhunt/">🦆 Играть в Duck Hunt онлайн</a></p>
""",
        },
        "en": {
            "name": "Play Duck Hunt Online — Fast-Paced Reflex & Accuracy Shooting Game",
            "title": (
                "Shoot 10 flying ducks in the shortest time possible with live accuracy "
                "tracking, wave flight physics, and desktop/mobile targeting."
            ),
            "body": """
<p>Experience the nostalgic <strong>Duck Hunt</strong> arcade shooter reimagined as a high-speed time trial on <a href="https://complexprogrammer.uz/duckhunt/"><strong>Complex Programmer — Duck Hunt</strong></a>. Challenge your aim by shooting down <strong>10 ducks in the fastest time possible</strong>.</p>

<h2>1. Rules & Speed-Shooting Challenge</h2>
<ul>
  <li>Up to two mallard ducks fly across the meadow simultaneously in wave trajectories, getting faster with every hit.</li>
  <li>Ducks that aren't hit within <strong>5.5 seconds</strong> fly away upward, costing you valuable seconds.</li>
  <li>The live HUD tracks your hits (<code>0/10</code>), elapsed time in seconds, and shooting accuracy percentage (<code>%</code>).</li>
</ul>

<h2>2. Mouse & Touch Controls</h2>
<ul>
  <li><strong>Desktop:</strong> Aim with the custom red crosshair and click to fire.</li>
  <li><strong>Mobile:</strong> Tap directly on flying ducks—touch hitboxes are <strong>1.6× wider</strong> for comfortable finger tapping.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/duckhunt/">🦆 Play Duck Hunt Online</a></p>
""",
        },
    },

    # ==========================================================================
    # 4. MOTORCYCLE (MOTOKROSS POYGASI)
    # ==========================================================================
    {
        "key": "motorcycle",
        "slug": "motorcycle-mototsikl-poygasi-onlayn-oyin",
        "image": "post/images/motorcycle_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/motorcycle/",
        "seo_title": "Motorcycle (Motokross) — 2D fizika va tepaliklar poygasi",
        "seo_description": (
            "Haqiqiy 2D fizika asosidagi mototsikl poygasi: protsedurali tepaliklar "
            "va tramplinlardan sakrang, havoda muvozanat saqlang va uzoq masofaga yeting."
        ),
        "uz": {
            "name": "Motorcycle (Mototsikl poygasi) — 2D fizika, tepaliklar va tramplinlar oşa parvoz",
            "title": (
                "Protsedurali tepaliklar va yoğoç tramplinlardan sakrab eng uzoq masofani "
                "zabt eting: havoda muvozanat saqlaş fizikasi va trassadagi rekord bayroği."
            ),
            "body": """
<p>Fizikaga asoslangan motokross va <span translate="no">Hill Climb</span> janridagi öyinlar muxlislari uçun <a href="https://complexprogrammer.uz/motorcycle/"><strong>Complex Programmer — Motorcycle (Mototsikl poygasi)</strong></a> haqiqiy mahorat maydonidir. Bu yerda siz çeksiz protsedurali tepaliklar va baland yoğoç tramplinlar oşa mototsiklni boşqarib, ağdarilib ketmasdan eng uzoq masofani (<code>metr</code>) bosib ötişingiz lozim.</p>

<h2>1. Haqiqiy 2D fizika va trassa tuzilişi</h2>
<p>Öyin oddiy animatsiya emas, balki tölaqonli ikki ölçovli fizika dvigateli asosida işlaydi:</p>
<ul>
  <li><strong>Ikki ğildirak va tortişiş fizikasi:</strong> Old va orqa ğildiraklarning yer bilan tutaşuvi alohida hisoblanadi. Tepalikka çiqişda tezlik pasayadi, qiyalikdan tuşişda esa mototsikl tezlaşadi.</li>
  <li><strong>Yoğoç tramplinlar (150 metrdan keyin):</strong> Dastlabki 150 metrdan söng har ~70 metrda maxsus tramplinlar çiqadi. Ulardan katta tezlikda sakraganda havoda muvozanatni saqlaş hal qiluvçi ahamiyatga ega.</li>
  <li><strong>Trassada şaxsiy rekord bayroği (🏆):</strong> Avvalgi eng yaxşi natijangiz trassaning aynan öşa metrida oltin bayroq sifatida qadab qöyiladi — uni quvib ötiş haqiqiy zavq bağişlaydi! Har 100 metrda masofa ustunlari ham joylaşgan.</li>
</ul>

<h2>2. Boşqaruv va havoda muvozanat saqlaş</h2>
<p>Mototsikl haydovçisi boşi bilan yerga tegsa yoki haddan taşqari tik burçak ostida qulasa, öyin tugaydi. Şuning uçun gaz va tormozni töğri taqsimlaş kerak:</p>
<table>
  <thead>
    <tr>
      <th>Harakat</th>
      <th>Klaviatura (PK)</th>
      <th>Smartfon / Planşet</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Gaz va Havoda oldinga egiliş</strong></td>
      <td><code>→</code>, <code>D</code> (yerda gaz), <code>↓</code> yoki <code>S</code> (havoda oldinga egiliş)</td>
      <td><strong>Gaz ▶</strong> tugmasi yoki ekranning öng tomonini bosib turiş</td>
    </tr>
    <tr>
      <td><strong>Tormoz va Havoda orqaga tortiş</strong></td>
      <td><code>←</code>, <code>A</code> (yerda tormoz), <code>↑</code> yoki <code>W</code> (havoda orqaga tortiş)</td>
      <td><strong>◀ Tormoz</strong> tugmasi yoki ekranning çap tomonini bosib turiş</td>
    </tr>
  </tbody>
</table>
<p>Klaviatura boşqaruvi fizik tugma kodlari (<code>KeyW</code>, <code>KeyA</code>, <code>KeyS</code>, <code>KeyD</code>) orqali işlagani sababli, kompyuteringizda lotin yoki kirill alifbosi yoqilganidan qat’i nazar uzluksiz işlaydi.</p>

<h2>3. Uzoq masofaga boriş uçun 3 ta oltin qoida</h2>
<ol>
  <li><strong>Tramplin uçida gazni me’yorida bering:</strong> Tramplindan uçayotganda gazni qattiq bosib tursangiz, mototsiklning oldi kötarilib orqaga ağdarilib ketişi mumkin.</li>
  <li><strong>Qiyalik burçagiga mos qöning:</strong> Qöniş nuqtasi pastga qiya bölsa, havoda old ğildirakni biroz pastga yönaltiring — şunda ikkala ğildirak yerga yumşoq tuşadi.</li>
  <li><strong>Tepalik çöqqisida ehtiyot böling:</strong> Tik tepalikdan oşib ötayotganda beixtiyor havoga kötarilasiz, darhol muvozanatni tekislang.</li>
</ol>

<p><a class="b-btn" href="https://complexprogrammer.uz/motorcycle/">🏍️ Motorcycle poygasini hoziroq öynaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Motorcycle (Мотоцикл пойгаси) — 2D физика, тепаликлар ва трамплинлар оша парвоз",
            "title": (
                "Процедурали тепаликлар ва ёғоч трамплинлардан сакраб энг узоқ масофани "
                "забт этинг: ҳавода мувозанат сақлаш физикаси ва трассадаги рекорд байроғи."
            ),
        },
        "ru": {
            "name": "Motorcycle (Мотокросс) онлайн — 2D-физика, холмы и прыжки с трамплинов",
            "title": (
                "Преодолейте максимальную дистанцию по процедурным холмам и деревянным "
                "трамплинам: баланс мотоцикла в воздухе и флажок личного рекорда на трассе."
            ),
            "body": """
<p>Любителям физических аркад в духе <em>Hill Climb</em> и классического мотокросса понравится <a href="https://complexprogrammer.uz/motorcycle/"><strong>Complex Programmer — Motorcycle</strong></a>. Управляйте кроссовым мотоциклом по бесконечным холмам и деревянным трамплинам, удерживайте равновесие в прыжках и ставьте рекорды дальности в метрах.</p>

<h2>1. Честная 2D-физика и трасса</h2>
<ul>
  <li><strong>Независимый контакт колес:</strong> учитываются гравитация, уклон поверхности и крутящий момент в воздухе. Приземление на голову гонщика или под критическим углом приводит к аварии.</li>
  <li><strong>Деревянные трамплины:</strong> начиная со 150 метров, каждые ~70 метров на трассе появляются трамплины для затяжных прыжков.</li>
  <li><strong>Флаг личного рекорда (🏆):</strong> ваш лучший результат отмечается золотым флагом прямо на холмах трассы, а каждые 100 метров стоят километровые столбики.</li>
</ul>

<h2>2. Управление на ПК и смартфонах</h2>
<ul>
  <li><strong>Клавиатура:</strong> <code>→ / D</code> — газ, <code>← / A</code> — тормоз; в воздухе <code>↑ / W</code> наклоняет мотоцикл назад, а <code>↓ / S</code> — вперед (работает при любой раскладке клавиатуры).</li>
  <li><strong>Мобильные устройства:</strong> кнопки <strong>«Газ ▶»</strong> и <strong>«◀ Тормоз»</strong> или нажатие по правой/левой части экрана.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/motorcycle/">🏍️ Играть в Motorcycle онлайн</a></p>
""",
        },
        "en": {
            "name": "Play Motorcycle Online — 2D Physics Hill-Climb & Motocross Game",
            "title": (
                "Ride across procedural hills and wooden ramps with realistic 2D suspension "
                "and mid-air pitch physics to beat your personal best distance flag."
            ),
            "body": """
<p>Conquer rolling hills and launch off wooden ramps in <a href="https://complexprogrammer.uz/motorcycle/"><strong>Complex Programmer — Motorcycle</strong></a>, a 2D physics-based motocross and hill-climb browser game. Balance your bike in mid-air and ride as far as possible without crashing.</p>

<h2>1. Authentic 2D Physics & Track Milestones</h2>
<ul>
  <li><strong>Real Wheel & Slope Physics:</strong> Gravity, slope acceleration, and mid-air angular momentum require careful throttle control. Landing on your rider's head or at an extreme angle ends the run.</li>
  <li><strong>Launch Ramps:</strong> Wooden ramps appear after 150m every ~70m, launching you into high-flying jumps.</li>
  <li><strong>On-Track Record Flag (🏆):</strong> Your personal best distance is marked right on the terrain with a golden trophy flag alongside 100m distance signposts.</li>
</ul>

<h2>2. Controls</h2>
<ul>
  <li><strong>Desktop:</strong> <code>→ / D</code> for gas, <code>← / A</code> for brake, <code>↑ / W</code> to lean back in mid-air, and <code>↓ / S</code> to lean forward.</li>
  <li><strong>Mobile:</strong> Use the on-screen <strong>Gas ▶</strong> and <strong>◀ Brake</strong> buttons or hold the right/left side of the screen.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/motorcycle/">🏍️ Play Motorcycle Online</a></p>
""",
        },
    },

    # ==========================================================================
    # 5. BUBBLE SHOOTER (ŞARÇALAR OTIŞ)
    # ==========================================================================
    {
        "key": "bubbleshooter",
        "slug": "bubble-shooter-sharchalar-otish-onlayn-oyin",
        "image": "post/images/bubble_shooter_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/bubbleshooter/",
        "seo_title": "Bubble Shooter (Şarçalar) — rangli şarçalarni yoriş öyini",
        "seo_description": (
            "Bubble Shooter mantiqiy arkada öyinini bepul öynang: 6 xil rangdagi "
            "şarçalarni lazer möljal bilan oting, 3 tasini birlaştirib yoring va bonus oling."
        ),
        "uz": {
            "name": "Bubble Shooter (Şarçalar) — rangli şarçalarni möljalga oling va portlating",
            "title": (
                "6 xil rangdagi şarçalardan 3 va undan ortiğini birlaştirib yoring: "
                "devordan qaytuvçi möljal çiziği, şarça almaştiriş (Swap) va +1000 bonus ball."
            ),
            "body": """
<p>Rang-barang, tinçlantiruvçi va şu bilan birga mantiqiy hisob-kitobni talab qiluvçi <strong><span translate="no">Bubble Shooter</span> (Şarçalar otiş)</strong> öyini <a href="https://complexprogrammer.uz/bubbleshooter/"><strong>Complex Programmer — Bubble Shooter</strong></a> sahifasida sizni kutmoqda. Olti burçakli (geksagonal) panjarada joylaşgan 6 xil rangdagi şarçalarni aniq möljalga olib yoring va maydonni töliq tozalang!</p>

<h2>1. Öyin qoidalari va ball hisoblaş tizimi</h2>
<ul>
  <li><strong>3 va undan ortiq moslik:</strong> Bir xil rangdagi kamida <strong>3 ta şarçani</strong> bir-biriga tekkizsangiz, ular portlab ketadi va har bir yorilgan şarça uçun <strong>+100 ball</strong> beriladi.</li>
  <li><strong>Uzilib tuşuvçi şodalar bonusi:</strong> Yuqoridagi şarçalarni yorganingizda ularga osilib turgan pastki (hatto boşqa rangdagi) şarçalar tayançsiz qolib pastga qulaydi va ularning har biri uçun ham <strong>+100 bonus ball</strong> qöşiladi!</li>
  <li><strong>Maydonni töliq tozalaş:</strong> Ekrandagi barça şarçalarni bitta ham qoldirmasdan yorsangiz, qöşimça <strong>+1000 ball</strong> mukofot olasiz.</li>
  <li><strong>Yangi qator tuşişi (5 ta xato):</strong> Pastki çap burçakdagi 5 ta sariq nuqta ketma-ket natijasiz otilgan öqlarni bildiradi. 5 marta şarça portlamasa, yuqoridan yangi qator tuşadi. Şarçalar pastdagi qizil çiziqqa yetsa — öyin tugaydi.</li>
</ul>

<h2>2. Lazer möljal çiziği va şarça almaştiriş (🔁)</h2>
<p>Öyinda ğalaba qozonişni osonlaştiruvçi ikkita muhim mexanika mavjud:</p>
<ul>
  <li><strong>Devorlardan qaytuvçi nuqtali möljal:</strong> Siçqonça yoki barmoqni harakatlantirganingizda şarçaning yon devorlardan qanday burçak ostida sakrab borişi nuqtali lazer çiziği bilan aniq körsatiladi.</li>
  <li><strong>Joriy va keyingi şarçani almaştiriş:</strong> Agar hozirgi şarça rangi qulay bölmasa, yuqoridagi <strong>🔁 Almaştiriş</strong> tugmasini, klaviaturada <code>S</code> harfini yoki pastdagi kiçik zaxira şarçasini bosib ularni özaro almaştirişingiz mumkin.</li>
  <li><strong>Otişni bekor qiliş (Mobil):</strong> Smartfonda möljal olayotib fikringizdan qaytsangiz, barmoqni pastga (puşka çiziğidan quyiga) tortib qöyib yuboring — şarça otilmaydi!</li>
</ul>

<h2>3. Yuqori natija sirlari</h2>
<ol>
  <li><strong>Pastdagilarni emas, yuqori ildizni nişonga oling:</strong> Devordan rikoşet qilib yuqoridagi tayanç şarçalarni yorsangiz, butun bir katta şoda bir zarbada qulab tuşadi.</li>
  <li><strong>5 ta sariq nuqtani kuzatib boring:</strong> Oxirgi 1–2 ta imkoniyat qolganida tavakkal qilmasdan, aniq portlaydigan 3 talik kombinatsiyani tanlang.</li>
</ol>

<p><a class="b-btn" href="https://complexprogrammer.uz/bubbleshooter/">🫧 Bubble Shooter öyinini hoziroq öynaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Bubble Shooter (Шарчалар) — рангли шарчаларни мўлжалга олинг ва портлатинг",
            "title": (
                "6 хил рангдаги шарчалардан 3 ва ундан ортиғини бирлаштириб ёринг: "
                "девордан қайтувчи мўлжал чизиғи, шарча алмаштириш (Swap) ва +1000 бонус балл."
            ),
        },
        "ru": {
            "name": "Bubble Shooter (Шарики) онлайн — лопайте цветные пузыри с лазерным прицелом",
            "title": (
                "Собирайте комбинации из 3+ шариков одного цвета: пунктирная траектория "
                "рикошета от стен, смена текущего шарика (S) и бонус +1000 за очистку поля."
            ),
            "body": """
<p>Увлекательная головоломка <strong>Bubble Shooter (Шарики)</strong> доступна бесплатно в браузере на <a href="https://complexprogrammer.uz/bubbleshooter/"><strong>Complex Programmer — Bubble Shooter</strong></a>. Прицеливайтесь, используйте рикошеты от боковых стен и обрушивайте целые гроздья разноцветных шаров!</p>

<h2>1. Правила и система бонусов</h2>
<ul>
  <li><strong>Комбинации 3+:</strong> соедините 3 или более шариков одного цвета, чтобы лопнуть их и получить <strong>+100 очков</strong> за каждый шар.</li>
  <li><strong>Каскадное обрушение:</strong> все шары, потерявшие связь с верхним рядом, автоматически падают вниз и приносят по <strong>+100 бонусных очков</strong>.</li>
  <li><strong>Полная зачистка:</strong> очистите игровое поле целиком и получите супербонус <strong>+1000 очков</strong>!</li>
  <li><strong>Индикатор промахов:</strong> каждые 5 выстрелов без лопания шаров добавляют новый ряд сверху. Не дайте шарам пересечь красную линию!</li>
</ul>

<h2>2. Прицеливание и смена шара (🔁)</h2>
<ul>
  <li><strong>Пунктирная линия прицела</strong> показывает точную траекторию полета, включая отскок от стены.</li>
  <li>Нажмите кнопку <strong>🔁 Сменить</strong>, клавишу <code>S</code> или кликните по малому шарику предпросмотра, чтобы поменять местами текущий и следующий снаряды.</li>
  <li>На смартфоне можно отменить выстрел, просто отведя палец вниз под пушку перед отпусканием.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/bubbleshooter/">🫧 Играть в Bubble Shooter онлайн</a></p>
""",
        },
        "en": {
            "name": "Play Bubble Shooter Online — Classic Color-Matching Arcade Puzzle",
            "title": (
                "Match 3 or more colorful bubbles using wall-bounce laser aiming, "
                "swap your active bubble anytime, and drop floating clusters for massive bonuses."
            ),
            "body": """
<p>Aim, bounce, and pop your way to a high score in <a href="https://complexprogrammer.uz/bubbleshooter/"><strong>Complex Programmer — Bubble Shooter</strong></a>. Featuring a 9-column hexagonal grid and 6 vibrant bubble colors, this browser puzzle blends relaxing visuals with tactical shot planning.</p>

<h2>1. Scoring & Cluster Mechanics</h2>
<ul>
  <li><strong>Match 3 or More:</strong> Pop connected groups of 3+ same-colored bubbles for <strong>+100 points</strong> per bubble.</li>
  <li><strong>Avalanche Drops:</strong> Any bubbles detached from the ceiling fall automatically, awarding <strong>+100 bonus points</strong> each.</li>
  <li><strong>Full Board Clear:</strong> Pop every bubble on the screen for a <strong>+1000 point</strong> bonus!</li>
  <li><strong>Row Drop Counter:</strong> Every 5 non-popping shots drops a new row from the top. Keep the stack above the red danger line!</li>
</ul>

<h2>2. Aim Trajectory & Bubble Swap</h2>
<ul>
  <li>A dotted trajectory line previews your exact path, including bank shots off the side walls.</li>
  <li>Press <code>S</code>, tap the <strong>🔁 Swap</strong> button, or tap the preview bubble to switch your current and next bubble at any time.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/bubbleshooter/">🫧 Play Bubble Shooter Online</a></p>
""",
        },
    },

    # ==========================================================================
    # 6. PING PONG (STOL TENNISI)
    # ==========================================================================
    {
        "key": "pingpong",
        "slug": "ping-pong-stol-tennisi-onlayn-oyin",
        "image": "post/images/ping_pong_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/pingpong/",
        "seo_title": "Ping Pong (Stol tennisi) — sun’iy intellektga qarşi onlayn öyin",
        "seo_description": (
            "Klassik Ping Pong (Stol tennisi) öyinini 3 xil qiyinlikdagi sun’iy "
            "intellektga qarşi bepul öynang. Burama zarbalar va moslaşuvçan stol rejimi."
        ),
        "uz": {
            "name": "Ping Pong (Stol tennisi) — sun’iy intellektga qarşi 3 xil qiyinlikda belluv",
            "title": (
                "5 oçkogaça davom etadigan dinamik stol tennisi: burama zarbalar fizikasi, "
                "har zarbada +6% tezlaşiş hamda kompyuter va mobil ekranlar uçun moslaşuvçan stol."
            ),
            "body": """
<p>Videoöyinlar tarixini boşlab bergan afsonaviy <strong><span translate="no">Ping Pong</span> (Stol tennisi)</strong> zamonaviy neon effektlar va aqlli sun’iy intellekt bilan <a href="https://complexprogrammer.uz/pingpong/"><strong>Complex Programmer — Ping Pong</strong></a> sahifasida jamlandi! Raketkani boşqaring, burçakli zarbalar bering va kompyuter raqibini <strong>5 oçkogaça</strong> bölgan partiyada mağlub eting.</p>

<h2>1. Öyin fizikasi va 3 xil AI qiyinlik darajasi</h2>
<p>Har bir rally (töp almaşinuvi) haqiqiy stol tennisi kabi keskin va qiziqarli keçadi:</p>
<ul>
  <li><strong>Har zarbada +6% tezlaşiş:</strong> Töp raketkaga har safar tekkanida uning tezligi 6 foizga oşadi — uzoq davom etgan almaşinuvlar haqiqiy çepdastlik talab qiladi.</li>
  <li><strong>Raketka çeti va burama zarba (Spin):</strong> Töpni raketkaning qoq markazi bilan ursangiz — u töğriga, çetki qismi bilan yoki raketkani tez siljitib ursangiz — keskin burçak ostida uçadi.</li>
  <li><strong>3 xil sun’iy intellekt (AI) darajasi:</strong>
    <ul>
      <li><em>Oson:</em> Yangi öyinçilar uçun — raqib sekinroq harakat qiladi va murakkab rikoşetlarda xato qilişi mumkin.</li>
      <li><em>Örtaça:</em> Muvozanatli raqib — töpning devordan qaytiş nuqtasini oldindan hisoblaydi.</li>
      <li><em>Qiyin:</em> Yuqori tezlik va aniq pozitsiya tanlaydigan kuçli AI.</li>
    </ul>
  </li>
</ul>

<h2>2. Aqlli moslaşuvçan stol: Gorizontal va Vertikal rejim</h2>
<p>Öyinning eng ajoyib texnik jihati — uning qurilma ekraniga avtomatik moslaşuvidir:</p>
<ul>
  <li><strong>Kompyuter va gorizontal ekranlarda:</strong> Stol klassik <em>çapdan-öngga</em> (siz çapda, raqib öngda) körinişida joylaşadi; raketka yuqori va pastga (<code>↑ ↓</code>, <code>W S</code> yoki siçqonça bilan) harakatlanadi.</li>
  <li><strong>Smartfon (tik / portret) ekranlarda:</strong> Stol avtomatik ravişda <strong>90 darajaga buriladi</strong> — sizning raketkangiz pastda, raqibniki esa yuqorida joylaşadi! Raketkani barmoq bilan çapga-öngga surib juda qulay boşqarasiz.</li>
</ul>

<h2>3. Raqibni yengiş sirlari</h2>
<ol>
  <li><strong>Raketka çetidan foydalaning:</strong> Töpni raketkaning yuqori yoki pastki çeti bilan qaytarsangiz, u devordan bir neça marta sakrab AI kutmagan nuqtaga boradi.</li>
  <li><strong>Zarbadan keyin markazga qayting:</strong> Töpni urib yuborgaç, keyingi zarbani istalgan burçakdan qaytariş uçun stol markaziga yaqinroq turing.</li>
</ol>

<p><a class="b-btn" href="https://complexprogrammer.uz/pingpong/">🏓 Ping Pong (Stol tennisi)ni hoziroq öynaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Ping Pong (Стол тенниси) — сунъий интеллектга қарши 3 хил қийинликда беллув",
            "title": (
                "5 очкогача давом этадиган динамик стол тенниси: бурама зарбалар физикаси, "
                "ҳар зарбада +6% тезлашиш ҳамда компьютер ва мобил экранлар учун мослашувчан стол."
            ),
        },
        "ru": {
            "name": "Ping Pong (Настольный теннис) онлайн — матч против ИИ на 3 уровнях сложности",
            "title": (
                "Сыграйте партию до 5 очков: физика подкрутки мяча, ускорение +6% с каждым "
                "ударом и адаптивный стол (горизонтальный на ПК и вертикальный на смартфоне)."
            ),
            "body": """
<p>Классический аркадный <strong>Ping Pong (Настольный теннис)</strong> с неоновыми эффектами шлейфа мяча и умным искусственным интеллектом доступен на <a href="https://complexprogrammer.uz/pingpong/"><strong>Complex Programmer — Ping Pong</strong></a>. Первым наберите <strong>5 очков</strong> и пополните копилку своих побед!</p>

<h2>1. Физика отскока и 3 уровня ИИ</h2>
<ul>
  <li><strong>Ускорение ралли:</strong> при каждом касании ракетки скорость мяча увеличивается на <strong>6%</strong>.</li>
  <li><strong>Угол и подкрутка:</strong> удар краем ракетки или удар в движении придает мячу острый угол отскока.</li>
  <li><strong>3 сложности соперника:</strong> <em>Легкий</em>, <em>Средний</em> и <em>Сложный</em> (ИИ прогнозирует рикошеты от бортов с учетом человеческой задержки реакции).</li>
</ul>

<h2>2. Адаптивная ориентация стола (ПК и Смартфон)</h2>
<ul>
  <li><strong>На компьютере:</strong> горизонтальный корт (вы слева, соперник справа), управление мышью или клавишами <code>↑ ↓ / W S</code>.</li>
  <li><strong>На телефоне (портретный режим):</strong> стол автоматически поворачивается вертикально (ваша ракетка внизу, соперник вверху) для удобного управления пальцем влево-вправо!</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/pingpong/">🏓 Играть в Ping Pong онлайн</a></p>
""",
        },
        "en": {
            "name": "Play Ping Pong Online — Arcade Table Tennis vs. 3-Level AI",
            "title": (
                "First to 5 points wins: experience paddle-edge spin physics, +6% rally "
                "acceleration, and an adaptive horizontal/vertical court for desktop and mobile."
            ),
            "body": """
<p>Step up to the table in <a href="https://complexprogrammer.uz/pingpong/"><strong>Complex Programmer — Ping Pong</strong></a>. Face off against a predictive AI opponent in fast-paced matches to <strong>5 points</strong>, complete with comet ball trails and impact sparks.</p>

<h2>1. Rally Physics & 3 AI Difficulty Levels</h2>
<ul>
  <li><strong>Dynamic Acceleration:</strong> The ball speeds up by <strong>6%</strong> on every paddle hit, turning long rallies into intense reflex battles.</li>
  <li><strong>Angle & Spin Control:</strong> Striking the ball with the outer edges of your paddle or while moving imparts sharp angles.</li>
  <li><strong>3 AI Tiers:</strong> Choose between <em>Easy</em>, <em>Medium</em>, and <em>Hard</em> difficulty at any time.</li>
</ul>

<h2>2. Adaptive Desktop & Mobile Court</h2>
<ul>
  <li><strong>Desktop (Horizontal):</strong> Classic left-vs-right layout controlled via mouse, touch, or <code>↑ ↓ / W S</code> keys.</li>
  <li><strong>Mobile Portrait (Vertical):</strong> The table automatically rotates 90° so you defend the bottom goal with natural left-to-right finger dragging.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/pingpong/">🏓 Play Ping Pong Online</a></p>
""",
        },
    },

    # ==========================================================================
    # 7. TIC TAC TOE (X VA O)
    # ==========================================================================
    {
        "key": "tictactoe",
        "slug": "tic-tac-toe-x-va-o-onlayn-oyin",
        "image": "post/images/tic_tac_toe_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/tictactoe/",
        "seo_title": "Tic Tac Toe (X va O) — Minimax AI va 2 kişilik mantiqiy öyin",
        "seo_description": (
            "3×3 maydondagi klassik X va O (Tic Tac Toe) öyinini Yengilmas Minimax "
            "sun’iy intellektiga qarşi yoki döstingiz bilan 2 kişilik rejimda öynang."
        ),
        "uz": {
            "name": "Tic Tac Toe (X va O) — Yengilmas Minimax AI yoki döstingizga qarşi mantiqiy öyin",
            "title": (
                "Klassik 3×3 X va O öyinining zamonaviy talqini: 3 xil sun’iy intellekt "
                "(Oson, Örtaça, Yengilmas Minimax), 2 kişilik rejim va doimiy statistika."
            ),
            "body": """
<p>Maktab daftarlaridan tortib zamonaviy algoritmlargaça eng maşhur mantiqiy belluv — <strong><span translate="no">Tic Tac Toe</span> (X va O / Krestik-nolik)</strong> endi <a href="https://complexprogrammer.uz/tictactoe/"><strong>Complex Programmer — Tic Tac Toe</strong></a> sahifasida! Bu yerda siz yolğiz holda sun’iy intellektga qarşi yoki bitta qurilmada döstingiz bilan <strong>2 kişilik rejimda</strong> kuç sinaşişingiz mumkin.</p>

<h2>1. Ikki xil öyin rejimi va 3 darajali Sun’iy Intellekt</h2>
<ul>
  <li><strong>🤖 Kompyuterga qarşi:</strong> Özingizga ma’qul belgini tanlang — <code>X</code> (birinçi yuradi) yoki <code>O</code> (ikkinçi yuradi) — va 3 xil qiyinlik darajasidan birida bellaşing:
    <ul>
      <li><em>Oson:</em> Tasodifiy va oddiy yurişlar qiladi.</li>
      <li><em>Örtaça:</em> Sizning yutuşingizni tösişga harakat qiladi, ammo ba’zan taktik imkoniyat qoldiradi.</li>
      <li><em>Yengilmas (<span translate="no">Minimax</span>):</em> Matematik <strong><span translate="no">Minimax</span> algoritmi</strong> asosida öyin daraxtidagi barça ehtimoliy yurişlarni oxirigaça hisoblab çiqadi. Bu rejimda kompyuterni yengib bölmaydi — eng yuqori natija durangdir!</li>
    </ul>
  </li>
  <li><strong>👥 2 kişi (Bitta qurilmada):</strong> Telefon yoki kompyuterni döstingiz bilan navbatma-navbat boşqarib, kim kuçliroq strateg ekanini aniqlang.</li>
</ul>

<h2>2. Boşqaruv va doimiy statistika</h2>
<ul>
  <li><strong>Siçqonça, Sensor va Raqamli klaviatura:</strong> Katakçalarni siçqonça yoki barmoq bilan bosişdan taşqari, klaviaturadagi <code>1</code> dan <code>9</code> gaça bölgan raqam tugmalari orqali ham tezkor yuriş qiliş mumkin.</li>
  <li><strong>Doimiy hisoblagiç:</strong> Öyin sizning <strong>Ğalaba</strong>, <strong>Durang</strong> va <strong>Mağlubiyat</strong>laringizni kompyuter va 2 kişilik rejimlar uçun alohida-alohida xotirada saqlab boradi.</li>
</ul>

<h2>3. X va O öyinida yutqazmaslik strategiyasi</h2>
<ol>
  <li><strong>Markaziy katak (5-katak) ustunligi:</strong> Agar ikkinçi bölib (<code>O</code> bilan) öynayotgan bölsangiz va raqib burçakdan boşlasa, albatta markaziy katakni egallang — aks holda ikki tomonlama «ayri» (<em>fork</em>) tuzoğiga tuşib qolasiz.</li>
  <li><strong>Burçakdan hujum qiling:</strong> Birinçi yurişda (<code>X</code>) burçak katakni tanlaş raqibga xato qiliş uçun eng köp imkoniyat qoldiradi.</li>
</ol>

<p><a class="b-btn" href="https://complexprogrammer.uz/tictactoe/">❌⭕ Tic Tac Toe (X va O) öyinini hoziroq öynaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Tic Tac Toe (X ва O) — Енгилмас Minimax AI ёки дўстингизга қарши мантиқий ўйин",
            "title": (
                "Классик 3×3 X ва O ўйинининг замонавий талқини: 3 хил сунъий интеллект "
                "(Осон, Ўртача, Енгилмас Minimax), 2 кишилик режим ва доимий статистика."
            ),
        },
        "ru": {
            "name": "Tic Tac Toe (Крестики-нолики) онлайн — режим на 2 игроков и непобедимый Minimax ИИ",
            "title": (
                "Сыграйте в классические Крестики-нолики 3×3: выбор стороны X или O, "
                "3 уровня ИИ (включая алгоритм Minimax), режим для двоих и статистика матчей."
            ),
            "body": """
<p>Классическая логическая игра <strong>Tic Tac Toe (Крестики-нолики)</strong> на поле 3×3 доступна в современном дизайне на <a href="https://complexprogrammer.uz/tictactoe/"><strong>Complex Programmer — Tic Tac Toe</strong></a>. Сразитесь с алгоритмом искусственного интеллекта или сыграйте вдвоем с другом на одном экране!</p>

<h2>1. Режимы игры и алгоритм Minimax</h2>
<ul>
  <li><strong>🤖 Против компьютера:</strong> выбирайте знак (<code>X</code> ходит первым, <code>O</code> — вторым) и один из трех уровней сложности: <em>Легкий</em>, <em>Средний</em> или <em>Непобедимый</em>. На максимальном уровне используется классический математический <strong>алгоритм Minimax</strong>, просчитывающий все варианты партии до конца.</li>
  <li><strong>👥 2 игрока:</strong> режим для игры вдвоем на одном смартфоне или ПК.</li>
</ul>

<h2>2. Управление и статистика</h2>
<ul>
  <li>Делайте ходы кликом мыши, касанием экрана или клавишами <code>1–9</code> на клавиатуре.</li>
  <li>Все результаты (<strong>Победы</strong>, <strong>Ничьи</strong>, <strong>Поражения</strong>) автоматически сохраняются отдельно для одиночного и парного режимов.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/tictactoe/">❌⭕ Играть в Крестики-нолики онлайн</a></p>
""",
        },
        "en": {
            "name": "Play Tic Tac Toe Online — Unbeatable Minimax AI & 2-Player Mode",
            "title": (
                "Challenge three AI difficulty tiers including an unbeatable Minimax "
                "algorithm or play pass-and-play with a friend on a sleek 3×3 grid."
            ),
            "body": """
<p>Enjoy the timeless 3×3 strategy classic on <a href="https://complexprogrammer.uz/tictactoe/"><strong>Complex Programmer — Tic Tac Toe</strong></a>. Featuring smooth animated SVG marks, side selection (<code>X</code> or <code>O</code>), and persistent match statistics.</p>

<h2>1. Game Modes & Minimax AI</h2>
<ul>
  <li><strong>🤖 Vs. Computer:</strong> Test your tactics across <em>Easy</em>, <em>Medium</em>, and <em>Unbeatable</em> difficulty levels. The Unbeatable tier runs a full <strong>Minimax decision-tree algorithm</strong>—the best possible outcome against it is a draw!</li>
  <li><strong>👥 2 Players:</strong> Pass-and-play mode on a single device for quick matches with friends.</li>
</ul>

<h2>2. Controls & Persistent Scoreboard</h2>
<ul>
  <li>Click/tap any cell or press keys <code>1–9</code> on your keyboard to place your mark.</li>
  <li>Wins, Draws, and Losses are saved automatically for both solo and 2-player modes.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/tictactoe/">❌⭕ Play Tic Tac Toe Online</a></p>
""",
        },
    },

    # ==========================================================================
    # 8. TETRIS (KLASSIK BOŞQOTIRMA)
    # ==========================================================================
    {
        "key": "tetris",
        "slug": "tetris-klassik-boshqotirma-onlayn-oyin",
        "image": "post/images/tetris_online_game.jpg",
        "source_url": "https://complexprogrammer.uz/tetris/",
        "seo_title": "Tetris onlayn öynaş — 7-bag, Ghost va Hold tizimli boşqotirma",
        "seo_description": (
            "Zamonaviy Guideline qoidalari asosidagi Tetris öyinini bepul öynang: "
            "10×20 maydon, 7-bag tasodifiy tizimi, SRS aylanma, Ghost va Hold imkoniyati."
        ),
        "uz": {
            "name": "Tetris — zamonaviy Guideline qoidalari asosidagi klassik boşqotirmani onlayn öynang",
            "title": (
                "10×20 matritsa, 7-bag tasodifiy tizimi, SRS devordan sakraş, Ghost (soya) "
                "figurasi, Hold (saqlaş) va 3 ta Next navbati bilan mukammal Tetris."
            ),
            "body": """
<p>Dunyo miqyosida eng köp öynalgan va tafakkurni çiniqtiruvçi afsonaviy boşqotirma — <strong><span translate="no">Tetris</span></strong> xalqaro <em><span translate="no">Tetris Guideline</span></em> standartlariga töliq mos ravişda <a href="https://complexprogrammer.uz/tetris/"><strong>Complex Programmer — Tetris</strong></a> sahifasida taqdim etildi! Bu yerda siz professional <span translate="no">Tetris</span> öyinçilari qadrlaydigan barça zamonaviy mexanikalardan bepul foydalana olasiz.</p>

<h2>1. Zamonaviy <span translate="no">Tetris Guideline</span> imkoniyatlari</h2>
<p>Oddiy eski klonlardan farqli ölaroq, uşbu <span translate="no">Tetris</span> professional mexanikalar bilan jihozlangan:</p>
<ul>
  <li><strong><code>7-bag</code> tasodifiy generatori:</strong> 7 xil tetromino figurasi (<code>I, J, L, O, S, T, Z</code>) xaltadan navbat bilan tortiladi. Bu degani — uzun <code>I</code>-tayoqçani 20–30 yurişlab kutib qolmaysiz, u har 7 ta figura içida albatta tuşadi!</li>
  <li><strong><span translate="no">SRS</span> (<span translate="no">Super Rotation System</span>):</strong> Figuralarni soat strelkasi böylab va unga teskari aylantiriş hamda devor yoki boşqa bloklarga taqalganda <em>devordan sakraş (<span translate="no">Wall Kick</span>)</em> tizimi mavjud.</li>
  <li><strong><span translate="no">Ghost Piece</span> (Soya figurasi):</strong> Maydon tubida joriy figuraning aynan qayerga tuşişini körsatuvçi yarim şaffof kontur — <span translate="no">Hard Drop</span> (<code>Space</code>) bosganda xato qilmaysiz.</li>
  <li><strong><span translate="no">Hold</span> (Saqlaş) va 3 ta <span translate="no">Next</span> navbati:</strong> Hozir noqulay bölgan figurani <code>C</code> yoki <code>Shift</code> tugmasi bilan «Saqlaş» qutisiga olib qöyib, keyingi 3 ta figurani oldindan rejalaştira olasiz.</li>
  <li><strong><span translate="no">Lock Delay</span> (0.5s) va <span translate="no">DAS/ARR</span>:</strong> Figura yerga tekkandan keyin ham uni 0.5 soniya davomida (15 martagaça) suriş yoki aylantiriş mumkin.</li>
</ul>

<h2>2. Ball hisoblaş jadvali va Darajalar</h2>
<p>Har <strong>10 ta tozalangan qatordan</strong> keyin daraja (<span translate="no">Level</span>) oşadi va figuralar tezroq tuşa boşlaydi:</p>
<table>
  <thead>
    <tr>
      <th>Harakat turi</th>
      <th>Beriladigan ball</th>
      <th>Izoh</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1 qator (<span translate="no">Single</span>)</strong></td>
      <td><code>100 × daraja</code></td>
      <td>Oddiy bittalik tozalaş</td>
    </tr>
    <tr>
      <td><strong>2 qator (<span translate="no">Double</span>)</strong></td>
      <td><code>300 × daraja</code></td>
      <td>Bir vaqtda 2 ta qator</td>
    </tr>
    <tr>
      <td><strong>3 qator (<span translate="no">Triple</span>)</strong></td>
      <td><code>500 × daraja</code></td>
      <td>Bir vaqtda 3 ta qator</td>
    </tr>
    <tr>
      <td><strong>4 qator (<span translate="no">TETRIS!</span>)</strong></td>
      <td><code>800 × daraja</code></td>
      <td>Uzun <code>I</code>-figura bilan 4 qatorni birdaniga portlatiş</td>
    </tr>
    <tr>
      <td><strong><span translate="no">Soft Drop</span> / <span translate="no">Hard Drop</span></strong></td>
      <td><code>+1</code> / <code>+2</code> har katak uçun</td>
      <td>Pastga tez tuşiriş (<code>↓</code>) yoki bir zumda taşlaş (<code>Space</code>)</td>
    </tr>
  </tbody>
</table>

<h2>3. Boşqaruv: Klaviatura, Sensor tugmalar va Svayp</h2>
<ul>
  <li><strong>Klaviatura:</strong> <code>← →</code> yoki <code>A D</code> — suriş, <code>↑</code> / <code>X</code> / <code>W</code> — öngga aylantiriş, <code>Z</code> / <code>Q</code> — çapga aylantiriş, <code>↓</code> / <code>S</code> — tez tuşiriş (<span translate="no">Soft Drop</span>), <code>Space</code> — bir zumda taşlaş (<span translate="no">Hard Drop</span>), <code>C</code> / <code>Shift</code> — saqlaş (<span translate="no">Hold</span>).</li>
  <li><strong>Smartfon va Planşet:</strong> Ekran ostidagi 6 ta maxsus sensor tugma (<code>◀ ▶ ⟳ ▼ ⤓ ⇄</code>) yoki maydon ustida barmoq bilan svayp qiliş (çap/öngga suriş, bosib aylantiriş, pastga tez siltab taşlaş, yuqoriga siltab saqlaş).</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/tetris/">🧱 Tetris öyinini hoziroq öynaş</a></p>
""",
        },
        "uz_crl": {
            "name": "Tetris — замонавий Guideline қоидалари асосидаги классик бошқотирмани онлайн ўйнанг",
            "title": (
                "10×20 матрица, 7-bag тасодифий тизими, SRS девордан сакраш, Ghost (соя) "
                "фигураси, Hold (сақлаш) ва 3 та Next навбати билан мукаммал Tetris."
            ),
        },
        "ru": {
            "name": "Tetris (Тетрис) онлайн — классическая головоломка по стандарту Guideline",
            "title": (
                "Играйте в современный Тетрис 10×20 бесплатно: генератор 7-bag, система "
                "вращения SRS, теневая фигура (Ghost), карман Hold и очередь из 3 фигур."
            ),
            "body": """
<p>Легендарная головоломка <strong>Tetris (Тетрис)</strong> реализована в полном соответствии с международным стандартом <em>Tetris Guideline</em> на <a href="https://complexprogrammer.uz/tetris/"><strong>Complex Programmer — Tetris</strong></a>. Наслаждайтесь отзывчивым управлением и всеми профессиональными механиками прямо в браузере.</p>

<h2>1. Профессиональные механики Tetris Guideline</h2>
<ul>
  <li><strong>Честный рандомайзер <code>7-bag</code>:</strong> все 7 тетромино (<code>I, J, L, O, S, T, Z</code>) выпадают перемешанными наборами без затяжных серий без «палки».</li>
  <li><strong>Система вращения SRS (Super Rotation System):</strong> вращение по и против часовой стрелки с поддержкой отскоков от стен (<em>Wall Kicks</em>).</li>
  <li><strong>Ghost Piece (Тень):</strong> полупрозрачный силуэт на дне стакана показывает точное место посадки фигуры перед мгновенным сбросом.</li>
  <li><strong>Карман Hold и очередь Next (3):</strong> откладывайте нужную фигуру про запас клавишей <code>C</code> или <code>Shift</code> и планируйте ходы на 3 шага вперед.</li>
  <li><strong>Lock Delay (0.5 с) и DAS/ARR:</strong> плавное автосмещение и полсекунды на маневр после касания дна.</li>
</ul>

<h2>2. Очки и управление</h2>
<ul>
  <li>1 линия — <code>100×уровень</code>, 2 линии — <code>300×уровень</code>, 3 линии — <code>500×уровень</code>, 4 линии (<strong>TETRIS!</strong>) — <code>800×уровень</code>. Каждые 10 линий повышают уровень скорости.</li>
  <li><strong>ПК:</strong> <code>← → / A D</code> — движение, <code>↑ / X / W</code> — поворот по часовой, <code>Z / Q</code> — против часовой, <code>↓ / S</code> — мягкий сброс, <code>Space</code> — мгновенный сброс (Hard Drop), <code>C / Shift</code> — Hold.</li>
  <li><strong>Смартфон:</strong> 6 удобных кнопок под полем (<code>◀ ▶ ⟳ ▼ ⤓ ⇄</code>) и поддержка жестов/свайпов по стакану.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/tetris/">🧱 Играть в Tetris онлайн</a></p>
""",
        },
        "en": {
            "name": "Play Tetris Online — Modern Guideline Puzzle with 7-Bag, Ghost & Hold",
            "title": (
                "Experience a responsive 10×20 Tetris game featuring 7-bag piece generation, "
                "Super Rotation System (SRS), Ghost piece preview, Hold queue, and DAS/ARR."
            ),
            "body": """
<p>Stack tetrominoes and clear four-line <strong>TETRIS</strong> combos in <a href="https://complexprogrammer.uz/tetris/"><strong>Complex Programmer — Tetris</strong></a>. Built to modern <em>Tetris Guideline</em> specifications, this browser edition delivers crisp controls on both desktop keyboards and mobile touchscreens.</p>

<h2>1. Modern Guideline Features</h2>
<ul>
  <li><strong><code>7-Bag</code> Randomizer:</strong> Deals all 7 tetrominoes (<code>I, J, L, O, S, T, Z</code>) in shuffled bags of seven, preventing long droughts without an <code>I</code>-piece.</li>
  <li><strong>Super Rotation System (SRS):</strong> Rotate clockwise and counter-clockwise with standard wall kicks.</li>
  <li><strong>Ghost Piece:</strong> A translucent outline at the bottom of the matrix shows exactly where your active piece will land.</li>
  <li><strong>Hold Queue & 3-Piece Next Preview:</strong> Stash a piece for later with <code>C</code> / <code>Shift</code> and plan ahead with 3 upcoming pieces visible.</li>
  <li><strong>Responsive DAS/ARR & 0.5s Lock Delay:</strong> Smooth horizontal auto-shift and up to 15 move/rotate resets before a grounded piece locks.</li>
</ul>

<h2>2. Scoring & Controls</h2>
<ul>
  <li>Single: <code>100×level</code>, Double: <code>300×level</code>, Triple: <code>500×level</code>, <strong>Tetris (4 lines)</strong>: <code>800×level</code>, Soft Drop: <code>+1/cell</code>, Hard Drop: <code>+2/cell</code>. Level increases every 10 lines.</li>
  <li><strong>Desktop:</strong> <code>← → / A D</code> move, <code>↑ / X / W</code> rotate CW, <code>Z / Q</code> rotate CCW, <code>↓ / S</code> soft drop, <code>Space</code> hard drop, <code>C / Shift</code> hold.</li>
  <li><strong>Mobile:</strong> 6 dedicated touch buttons (<code>◀ ▶ ⟳ ▼ ⤓ ⇄</code>) plus intuitive swipe gestures on the board.</li>
</ul>

<p><a class="b-btn" href="https://complexprogrammer.uz/tetris/">🧱 Play Tetris Online</a></p>
""",
        },
    },
]


def _strip_translate_spans(html):
    """<span translate="no">...</span> teglarini matnni saqlagan holda tozalaydi."""
    return re.sub(r'<span\s+translate="no">(.*?)</span>', r"\1", html, flags=re.S)


try:
    from django.core.management.base import BaseCommand, CommandError
except ImportError:
    class BaseCommand:
        pass

    class CommandError(Exception):
        pass


class Command(BaseCommand):
    help = "Complex Programmer (/projects/) bölimidagi 8 ta onlayn öyin uçun blog maqolalarini rasmlari bilan naşr qiliş yoki yangilaş."

    def add_arguments(self, parser):
        parser.add_argument(
            "--update",
            action="store_true",
            help="Mavjud maqolalar matni va rasmlarini yangilaş",
        )
        parser.add_argument(
            "--draft",
            action="store_true",
            help="Saytda körsatmasdan qoralama (2099-yil) sifatida saqlaş",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Bazaga özgartiriş kiritmasdan tekşiriş",
        )
        parser.add_argument(
            "--game",
            type=str,
            default="",
            help="Faqat bitta öyin kaliti yoki slug böyiça naşr qiliş (masalan: snake, tetris)",
        )

    def _wait_for_telegram_threads(self):
        for t in list(threading.enumerate()):
            if t is not threading.main_thread() and t.is_alive():
                if getattr(t, "name", "").startswith("Thread"):
                    t.join(timeout=25)

    def handle(self, *args, **opts):
        from django.conf import settings
        from django.contrib.auth.models import User
        from django.core.cache import cache
        from django.utils import timezone
        from blog.models import Categories, Posts
        from core.translit import latin_to_cyrillic

        target = (opts.get("game") or "").strip().lower()
        articles = GAMES_ARTICLES
        if target:
            articles = [
                a for a in GAMES_ARTICLES
                if a["key"] == target or a["slug"] == target
            ]
            if not articles:
                valid = ", ".join(a["key"] for a in GAMES_ARTICLES)
                raise CommandError(f"Öyin topilmadi: '{target}'. Mavjud öyinlar: {valid}")

        if not opts["dry_run"]:
            author = User.objects.filter(is_superuser=True).order_by("id").first()
            if not author:
                author = User.objects.order_by("id").first()
            if not author:
                raise CommandError("Muallif uçun birorta ham User topilmadi.")

            category = (
                Categories.objects.filter(id=3, is_deleted=False).first()
                or Categories.objects.filter(name_uz_uz__icontains="yin", is_deleted=False).first()
                or Categories.objects.filter(name_en_us__icontains="game", is_deleted=False).first()
                or Categories.objects.filter(is_deleted=False).first()
            )
        else:
            author = None
            category = None

        base_time = DRAFT_TIME if opts["draft"] else timezone.now()
        published_count = 0

        self.stdout.write(self.style.SUCCESS("=" * 68))
        self.stdout.write(self.style.SUCCESS(f"🎮 Jami tayyorlangan öyin maqolalari: {len(articles)} ta"))
        self.stdout.write(self.style.SUCCESS("=" * 68))

        for idx, item in enumerate(articles):
            slug = item["slug"]
            image_rel = item["image"]
            image_full = os.path.join(settings.MEDIA_ROOT, image_rel)
            has_image = os.path.exists(image_full)

            uz_body_raw = item["uz"]["body"].strip()
            uz_body_clean = _strip_translate_spans(uz_body_raw)
            cyr_body_clean = _strip_translate_spans(latin_to_cyrillic(uz_body_raw))

            cyr_meta = item.get("uz_crl", {})
            cyr_name = (cyr_meta.get("name") or latin_to_cyrillic(item["uz"]["name"])).strip()
            cyr_title = (cyr_meta.get("title") or latin_to_cyrillic(item["uz"]["title"])).strip()

            # Har bir maqola tartib bilan çiqişi uçun publish_time'ga +idx soniya qöşamiz
            pub_time = (
                DRAFT_TIME
                if opts["draft"]
                else base_time - datetime.timedelta(seconds=(len(articles) - 1 - idx) * 2)
            )

            fields = {
                "name_uz_uz": item["uz"]["name"].strip(),
                "title_uz_uz": item["uz"]["title"].strip(),
                "body_uz_uz": uz_body_clean,

                "name_uz_crl": cyr_name,
                "title_uz_crl": cyr_title,
                "body_uz_crl": cyr_body_clean,

                "name_ru_ru": item["ru"]["name"].strip(),
                "title_ru_ru": item["ru"]["title"].strip(),
                "body_ru_ru": item["ru"]["body"].strip(),

                "name_en_us": item["en"]["name"].strip(),
                "title_en_us": item["en"]["title"].strip(),
                "body_en_us": item["en"]["body"].strip(),

                "seo_title": item["seo_title"][:70],
                "seo_description": item["seo_description"][:200],
                "source_url": item["source_url"],
                "publish_time": pub_time,
                "image": image_rel if has_image else "",
            }

            if not has_image:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ [{item['key']}] Rasm topilmadi: {image_full}")
                )

            if opts["dry_run"]:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"[DRY-RUN] {idx + 1}. {fields['name_uz_uz']}\n"
                        f"          Slug: {slug} | Rasm: {image_rel} (mavjud={has_image})"
                    )
                )
                published_count += 1
                continue

            post = Posts.objects.filter(slug=slug).first()
            if post and not opts["update"]:
                self.stdout.write(
                    self.style.WARNING(
                        f"⏭ [{item['key']}] Allaqaçon mavjud ({slug}). Yangilaş uçun --update bering."
                    )
                )
                continue

            if not post:
                post = Posts(slug=slug, created_by=author, categorie=category)
                action = "yaratildi va naşr qilindi"
            else:
                action = "yangilandi"

            for k, v in fields.items():
                setattr(post, k, v)
            if category and not post.categorie:
                post.categorie = category

            post.save()
            self._wait_for_telegram_threads()
            time.sleep(0.3)

            published_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ [{idx + 1}/{len(articles)}] {item['key'].upper()} — {action}!\n"
                    f"   🖼 Rasm: {image_rel}\n"
                    f"   🔗 Havola: https://complexprogrammer.uz/blog/{slug}/"
                )
            )

        if not opts["dry_run"] and published_count:
            try:
                cache.clear()
            except Exception:
                pass

        status_text = (
            "TEKŞIRUV (DRY-RUN)"
            if opts["dry_run"]
            else ("Qoralama (2099-yil)" if opts["draft"] else "Naşr qilindi (jonli efirda)")
        )
        self.stdout.write(self.style.SUCCESS("=" * 68))
        self.stdout.write(
            self.style.SUCCESS(f"✨ Yakunlandi! {published_count} ta maqola tayyor ({status_text}).")
        )
        self.stdout.write(self.style.SUCCESS("=" * 68))
