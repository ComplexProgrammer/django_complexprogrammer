"""CS 1.6 mavzusidagi maqolalar turkumi: pricel, FPS va tarmoq ("headshot") sozlamalari.

Saytga keladigan qidiruv trafigining köp qismi bitta maqoladan keladi:
«Counter-Strike 1.6 kodlari» (/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/). Search Console'da
«cs 1.6 pricel», «headshot kodlari», «fps» kabi alohida sörovlar ham bor, lekin ularga alohida sahifa yöq edi.
Bu buyruq şu sörovlar uçun maqolalar çiqaradi va ularni asosiy maqola bilan özaro bağlaydi.

Işlatiş:
    python manage.py publish_cs16_posts               # 3 ta maqolani naşr qiladi
    python manage.py publish_cs16_posts --update      # mavjudlarini ham yangilaydi
    python manage.py publish_cs16_posts --draft       # qoralama (2099-yil) — saytda körinmaydi
    python manage.py publish_cs16_posts --dry-run     # bazaga yozmasdan tekşiradi
    python manage.py publish_cs16_posts --only fps    # faqat bitta maqola (pricel | fps | headshot)

Diqqat: naşr qilingan maqola blog signali orqali Telegram kanaliga ham avtomatik joylanadi.
"""

import datetime
import re
import threading
import time

from django.core.management.base import BaseCommand, CommandError

DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)
MAIN_SLUG = "counter-strike-16-oyinida-ishlatiladigan-kodlar"
IMAGE = "post/images/cs16_kodlari_konsol_buyruqlari.jpg"
LINKS_MARKER = "<!-- cs16-turkum -->"

ARTICLES = [
    # ==========================================================================
    # 1. PRICEL (CROSSHAIR)
    # ==========================================================================
    {
        "key": "pricel",
        "slug": "cs-16-pricel-sozlamalari",
        "image": "post/images/cs16_pricel_sozlamalari.jpg",
        "seo_title": "CS 1.6 pricel sozlamalari — rang, ölçam va buyruqlar (2026)",
        "seo_description": "CS 1.6 da pricel (crosshair) rangi, ölçami va şaffofligini konsol buyruqlari bilan sozlaş: cl_crosshair_color, cl_crosshair_size, saqlab qöyiş.",
        "uz": {
            "name": "CS 1.6 pricel sozlamalari: rang, ölçam va konsol buyruqlari",
            "title": "Pricel (crosshair) rangini, ölçamini va şaffofligini sozlaydigan buyruqlar, tayyor rang kodlari va sozlamani saqlab qöyiş.",
            "body": """
<p>Pricel (inglizça <em>crosshair</em>) — ekran örtasidagi nişon belgisi. Uni öz közingizga moslab olsangiz, nişonni tezroq topasiz va xaritaning yoruğ yoki qoronği joylarida yöqotib qöymaysiz. Quyidagi buyruqlar CS 1.6 ning istalgan serverida işlaydi: ular <code>sv_cheats</code> talab qilmaydi va çit hisoblanmaydi.</p>

<h2>Konsolni oçiş</h2>
<p>Klaviaturadagi <code>~</code> (Esc ostidagi) tugmasini bosing. Konsol oçilmasa: <em>Options → Keyboard → Advanced → Enable developer console</em> belgisini qöying. Buyruqni yozib, Enter bosing.</p>

<h2>Asosiy pricel buyruqlari</h2>
<table>
  <thead><tr><th>Buyruq</th><th>Nima qiladi</th></tr></thead>
  <tbody>
    <tr><td><code>crosshair 1</code></td><td>Pricelni yoqadi (<code>0</code> — öçiradi)</td></tr>
    <tr><td><code>cl_crosshair_color "50 250 50"</code></td><td>Rang: uçta son — qizil, yaşil, kök (0–255)</td></tr>
    <tr><td><code>cl_crosshair_size small</code></td><td>Ölçam: <code>auto</code>, <code>small</code>, <code>medium</code>, <code>large</code></td></tr>
    <tr><td><code>cl_crosshair_translucent 0</code></td><td><code>1</code> — yarim şaffof, <code>0</code> — tiniq (aniqroq körinadi)</td></tr>
    <tr><td><code>cl_dynamiccrosshair 1</code></td><td>Yugurganda va otganda pricel kengayadi (<code>0</code> — doim bir xil). Steam'dagi yangi versiyada bor</td></tr>
  </tbody>
</table>

<h2>Tayyor rang kodlari</h2>
<ul>
  <li><strong>Yaşil (standart):</strong> <code>cl_crosshair_color "50 250 50"</code></li>
  <li><strong>Qizil:</strong> <code>cl_crosshair_color "250 50 50"</code></li>
  <li><strong>Kök:</strong> <code>cl_crosshair_color "50 50 250"</code></li>
  <li><strong>Sariq:</strong> <code>cl_crosshair_color "250 250 50"</code></li>
  <li><strong>Moviy (cyan):</strong> <code>cl_crosshair_color "50 250 250"</code></li>
  <li><strong>Puşti:</strong> <code>cl_crosshair_color "250 50 250"</code></li>
</ul>
<p>Qaysi rang qulay? Köp xaritalarda (de_dust2, de_inferno) devorlar sarğiş, şuning uçun <strong>yaşil</strong> yoki <strong>moviy</strong> yaxşi ajralib turadi. Qoronği xaritalarda sariq rang yaxşiroq körinadi.</p>

<h2>Professional öyinçilar uslubi</h2>
<p>Köp tajribali öyinçilar kiçik va tiniq pricel tanlaydi. Bunda nişon ostidagi raqib boşi yopilib qolmaydi:</p>
<pre><code>crosshair 1
cl_crosshair_size small
cl_crosshair_translucent 0
cl_crosshair_color "50 250 250"
cl_dynamiccrosshair 1</code></pre>
<p>Dinamik pricel foydali: u kengaysa, öq hozir nişondan qoçişini bildiradi. Töxtab, keyin otiş kerakligini körsatadi.</p>

<h2>Sozlamani saqlab qöyiş</h2>
<p>Öyin yopilganda <code>config.cfg</code> qayta yoziladi, şuning uçun özingiz yozgan buyruqlarni alohida faylga saqlang: öyin papkasidagi <code>cstrike</code> içida <code>userconfig.cfg</code> faylini yarating (Bloknot bilan) va yuqoridagi qatorlarni unga qöying. Öyin uni har safar özi yuklaydi. Tekşiriş uçun konsolda: <code>exec userconfig.cfg</code>.</p>

<h2>Tez-tez beriladigan savollar</h2>
<p><strong>AWP'da pricel nega yöq?</strong> Snayper miltiqlarida pricel faqat optika (öng tugma) bilan körinadi — bu öyin qoidasi, buyruq bilan özgarmaydi.</p>
<p><strong>Ekranga yopiştiriladigan "pricel dasturlari"çi?</strong> Köp serverlar ularni çit deb hisoblaydi va ban beradi. Yuqoridagi standart buyruqlar xavfsiz.</p>
<p>Boşqa foydali buyruqlar: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">CS 1.6 kodlari va konsol buyruqlari</a> · <a href="/blog/cs-16-fps-oshirish/">CS 1.6 da FPS oşiriş</a> · <a href="/blog/cs-16-headshot-sozlamalari/">Headshot uçun tarmoq va siçqonça sozlamalari</a>.</p>
""",
        },
        "ru": {
            "name": "Настройки прицела в CS 1.6: цвет, размер и консольные команды",
            "title": "Команды для цвета, размера и прозрачности прицела (crosshair), готовые коды цветов и сохранение настроек.",
            "body": """
<p>Прицел (<em>crosshair</em>) — метка в центре экрана. Если настроить его под себя, цель находится быстрее и прицел не теряется на светлых и тёмных участках карты. Команды ниже работают на любом сервере CS 1.6: им не нужен <code>sv_cheats</code>, и это не читы.</p>

<h2>Как открыть консоль</h2>
<p>Нажмите <code>~</code> (клавиша под Esc). Если консоль не открывается: <em>Options → Keyboard → Advanced → Enable developer console</em>. Введите команду и нажмите Enter.</p>

<h2>Основные команды прицела</h2>
<table>
  <thead><tr><th>Команда</th><th>Что делает</th></tr></thead>
  <tbody>
    <tr><td><code>crosshair 1</code></td><td>Включает прицел (<code>0</code> — выключает)</td></tr>
    <tr><td><code>cl_crosshair_color "50 250 50"</code></td><td>Цвет: три числа — красный, зелёный, синий (0–255)</td></tr>
    <tr><td><code>cl_crosshair_size small</code></td><td>Размер: <code>auto</code>, <code>small</code>, <code>medium</code>, <code>large</code></td></tr>
    <tr><td><code>cl_crosshair_translucent 0</code></td><td><code>1</code> — полупрозрачный, <code>0</code> — чёткий</td></tr>
    <tr><td><code>cl_dynamiccrosshair 1</code></td><td>Прицел расширяется при беге и стрельбе (<code>0</code> — всегда одинаковый). Есть в новой версии Steam</td></tr>
  </tbody>
</table>

<h2>Готовые коды цветов</h2>
<ul>
  <li><strong>Зелёный (стандарт):</strong> <code>cl_crosshair_color "50 250 50"</code></li>
  <li><strong>Красный:</strong> <code>cl_crosshair_color "250 50 50"</code></li>
  <li><strong>Синий:</strong> <code>cl_crosshair_color "50 50 250"</code></li>
  <li><strong>Жёлтый:</strong> <code>cl_crosshair_color "250 250 50"</code></li>
  <li><strong>Голубой (cyan):</strong> <code>cl_crosshair_color "50 250 250"</code></li>
  <li><strong>Розовый:</strong> <code>cl_crosshair_color "250 50 250"</code></li>
</ul>
<p>На большинстве карт (de_dust2, de_inferno) стены жёлтых оттенков, поэтому лучше всего заметны <strong>зелёный</strong> и <strong>голубой</strong>. На тёмных картах удобнее жёлтый.</p>

<h2>Стиль опытных игроков</h2>
<p>Опытные игроки обычно выбирают маленький чёткий прицел — он не закрывает голову противника:</p>
<pre><code>crosshair 1
cl_crosshair_size small
cl_crosshair_translucent 0
cl_crosshair_color "50 250 250"
cl_dynamiccrosshair 1</code></pre>
<p>Динамический прицел полезен: если он разошёлся, пуля сейчас уйдёт в сторону — остановитесь и только потом стреляйте.</p>

<h2>Как сохранить настройки</h2>
<p>При выходе из игры <code>config.cfg</code> перезаписывается, поэтому свои команды храните отдельно: создайте в папке <code>cstrike</code> файл <code>userconfig.cfg</code> (Блокнотом) и вставьте в него строки выше. Игра загружает его сама. Проверить можно командой <code>exec userconfig.cfg</code>.</p>

<h2>Частые вопросы</h2>
<p><strong>Почему у AWP нет прицела?</strong> У снайперских винтовок прицел виден только в оптике (правая кнопка мыши) — это правило игры, командой не меняется.</p>
<p><strong>А «программы-прицелы» поверх экрана?</strong> Многие серверы считают их читом и банят. Стандартные команды выше безопасны.</p>
<p>Другие полезные команды: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">коды и консольные команды CS 1.6</a> · <a href="/blog/cs-16-fps-oshirish/">как поднять FPS в CS 1.6</a> · <a href="/blog/cs-16-headshot-sozlamalari/">сетевые настройки и мышь для хедшотов</a>.</p>
""",
        },
        "en": {
            "name": "CS 1.6 crosshair settings: color, size and console commands",
            "title": "Commands for crosshair color, size and transparency, ready color codes and how to keep your settings.",
            "body": """
<p>The crosshair is the aiming mark in the middle of the screen. Tuning it to your eyes helps you find targets faster and keeps it visible on bright and dark parts of a map. The commands below work on any CS 1.6 server: they do not need <code>sv_cheats</code> and are not cheats.</p>

<h2>Opening the console</h2>
<p>Press <code>~</code> (the key below Esc). If nothing happens, enable <em>Options → Keyboard → Advanced → Enable developer console</em>. Type a command and press Enter.</p>

<h2>Main crosshair commands</h2>
<table>
  <thead><tr><th>Command</th><th>What it does</th></tr></thead>
  <tbody>
    <tr><td><code>crosshair 1</code></td><td>Turns the crosshair on (<code>0</code> turns it off)</td></tr>
    <tr><td><code>cl_crosshair_color "50 250 50"</code></td><td>Color as red, green, blue (0–255)</td></tr>
    <tr><td><code>cl_crosshair_size small</code></td><td>Size: <code>auto</code>, <code>small</code>, <code>medium</code>, <code>large</code></td></tr>
    <tr><td><code>cl_crosshair_translucent 0</code></td><td><code>1</code> is see-through, <code>0</code> is solid and sharper</td></tr>
    <tr><td><code>cl_dynamiccrosshair 1</code></td><td>The crosshair widens while running and shooting (<code>0</code> keeps it fixed). Available in the current Steam version</td></tr>
  </tbody>
</table>

<h2>Ready color codes</h2>
<ul>
  <li><strong>Green (default):</strong> <code>cl_crosshair_color "50 250 50"</code></li>
  <li><strong>Red:</strong> <code>cl_crosshair_color "250 50 50"</code></li>
  <li><strong>Blue:</strong> <code>cl_crosshair_color "50 50 250"</code></li>
  <li><strong>Yellow:</strong> <code>cl_crosshair_color "250 250 50"</code></li>
  <li><strong>Cyan:</strong> <code>cl_crosshair_color "50 250 250"</code></li>
  <li><strong>Pink:</strong> <code>cl_crosshair_color "250 50 250"</code></li>
</ul>
<p>Most maps (de_dust2, de_inferno) have yellowish walls, so <strong>green</strong> or <strong>cyan</strong> stand out best. Yellow works better on dark maps.</p>

<h2>A setup experienced players use</h2>
<pre><code>crosshair 1
cl_crosshair_size small
cl_crosshair_translucent 0
cl_crosshair_color "50 250 250"
cl_dynamiccrosshair 1</code></pre>
<p>A small solid crosshair does not cover the enemy's head. The dynamic one tells you when your shot will be inaccurate: stop first, then fire.</p>

<h2>Keeping your settings</h2>
<p><code>config.cfg</code> is rewritten when the game closes, so put your own commands in <code>cstrike/userconfig.cfg</code> (create it with Notepad). The game loads it automatically; test with <code>exec userconfig.cfg</code>.</p>

<h2>FAQ</h2>
<p><strong>Why does the AWP have no crosshair?</strong> Sniper rifles show it only when scoped (right mouse button). That is a game rule and no command changes it.</p>
<p><strong>What about on-screen crosshair overlay programs?</strong> Many servers treat them as cheats and ban for them. The built-in commands above are safe.</p>
<p>More: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">CS 1.6 codes and console commands</a> · <a href="/blog/cs-16-fps-oshirish/">How to raise FPS in CS 1.6</a> · <a href="/blog/cs-16-headshot-sozlamalari/">Network and mouse settings for headshots</a>.</p>
""",
        },
    },
    # ==========================================================================
    # 2. FPS
    # ==========================================================================
    {
        "key": "fps",
        "slug": "cs-16-fps-oshirish",
        "image": "post/images/cs16_fps_oshirish.jpg",
        "seo_title": "CS 1.6 da FPS oşiriş — buyruqlar va işga tuşiriş parametrlari",
        "seo_description": "CS 1.6 qotsa yoki FPS past bölsa: fps_max, gl_vsync, net_graph buyruqlari, Steam işga tuşiriş parametrlari va kuçsiz kompyuter uçun grafik sozlamalar.",
        "uz": {
            "name": "CS 1.6 da FPS oşiriş: buyruqlar, işga tuşiriş parametrlari va sozlamalar",
            "title": "Öyin qotsa yoki silliq işlamasa: FPS'ni körsatiş, çegarani oçiş, vertikal sinxronlaşni öçiriş va kuçsiz kompyuter uçun sozlamalar.",
            "body": """
<p>FPS (<em>frames per second</em>) — ekranda bir soniyada neçta kadr çizilişi. CS 1.6 da u past bölsa, öyin "qotadi", siçqonça keçikib javob beradi va nişon oliş qiyinlaşadi. Quyidagi sozlamalar kuçsiz kompyuterda ham öyinni silliqroq qiladi.</p>

<h2>1. Hozirgi FPS'ni köriş</h2>
<ul>
  <li><code>cl_showfps 1</code> — burçakda FPS sonini körsatadi (Steam versiyasi).</li>
  <li><code>net_graph 3</code> — FPS bilan birga ping, paket yöqotiş (loss) va choke'ni körsatadi. Öçiriş: <code>net_graph 0</code>.</li>
</ul>

<h2>2. FPS çegarasi</h2>
<ul>
  <li><code>fps_max 100</code> — standart va köp serverlarda ruxsat etilgan eng yuqori qiymat.</li>
  <li>Steam'dagi yangi versiyada 100 dan yuqori FPS uçun avval <code>fps_override 1</code> kerak. Diqqat: ba'zi serverlar 100 dan yuqori FPS'ni taqiqlaydi, çunki eski dvigatelda bu harakat fizikasini özgartiradi.</li>
</ul>

<h2>3. Vertikal sinxronlaşni öçiriş</h2>
<p><code>gl_vsync 0</code> — kadrlar soni monitor çastotasiga (masalan 60 Hz) bağlanib qolmaydi va siçqonça javobi tezlaşadi. Videokarta sozlamalarida (NVIDIA / AMD panel) ham V-Sync öçiq bölişi kerak.</p>

<h2>4. Kuçsiz kompyuter uçun grafik buyruqlar</h2>
<table>
  <thead><tr><th>Buyruq</th><th>Nima beradi</th></tr></thead>
  <tbody>
    <tr><td><code>r_decals 100</code></td><td>Devordagi öq izlari va qon dağlari kamroq — otişma paytida FPS tuşmaydi</td></tr>
    <tr><td><code>mp_decals 100</code></td><td>Tarmoq öyinidagi izlar soni</td></tr>
    <tr><td><code>max_shells 0</code></td><td>Uçib çiqadigan gilzalar çizilmaydi</td></tr>
    <tr><td><code>max_smokepuffs 0</code></td><td>Öq tekkan joydagi tutun effekti öçadi</td></tr>
    <tr><td><code>cl_weather 0</code></td><td>Yomğir/qor effektlari öçadi (ba'zi xaritalarda)</td></tr>
  </tbody>
</table>
<p>Öyin menyusida: <em>Options → Video</em> — <strong>OpenGL</strong> rejimini tanlang (Software'dan ança tez) va kerak bölsa ekran ölçamini kiçraytiring (masalan 1024×768).</p>

<h2>5. Steam işga tuşiriş parametrlari</h2>
<p>Steam → Kutubxona → Counter-Strike → Xususiyatlar (Properties) → <em>Launch options</em> maydoniga:</p>
<pre><code>-nojoy -noforcemparms -noforcemaccel -freq 75 -console</code></pre>
<ul>
  <li><code>-nojoy</code> — joystik qöllab-quvvatlaşini öçiradi (ortiqça resurs sarflamaydi).</li>
  <li><code>-noforcemparms -noforcemaccel</code> — Windows'ning siçqonça tezlanişi öyinga ta'sir qilmaydi.</li>
  <li><code>-freq 75</code> — monitor çastotasi (60, 75, 144 — monitoringizga qarab yozing).</li>
  <li><code>-console</code> — öyin konsol oçiq holda boşlanadi.</li>
</ul>

<h2>6. Windows tomonidan</h2>
<ul>
  <li>Elektr ta'minoti rejimini <strong>Yuqori unumdorlik</strong> (High performance) qiling.</li>
  <li>Videokarta drayverini yangilang.</li>
  <li>Öyin paytida brauzer, torrent va boşqa ortiqça dasturlarni yoping.</li>
</ul>

<p>Barça buyruqlarni <code>cstrike/userconfig.cfg</code> faylga yozib qöysangiz, har safar qayta kiritiş kerak bölmaydi. Batafsil: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">CS 1.6 kodlari va konsol buyruqlari</a> · <a href="/blog/cs-16-pricel-sozlamalari/">Pricel sozlamalari</a> · <a href="/blog/cs-16-headshot-sozlamalari/">Headshot uçun tarmoq sozlamalari</a>.</p>
""",
        },
        "ru": {
            "name": "Как поднять FPS в CS 1.6: команды, параметры запуска и настройки",
            "title": "Если игра тормозит: как показать FPS, снять ограничение, отключить вертикальную синхронизацию и настроить слабый компьютер.",
            "body": """
<p>FPS (<em>frames per second</em>) — сколько кадров в секунду рисует игра. При низком FPS CS 1.6 «тормозит», мышь отвечает с задержкой и целиться тяжелее. Настройки ниже делают игру плавнее даже на слабом компьютере.</p>

<h2>1. Как увидеть текущий FPS</h2>
<ul>
  <li><code>cl_showfps 1</code> — счётчик FPS в углу экрана (версия Steam).</li>
  <li><code>net_graph 3</code> — FPS, пинг, потеря пакетов (loss) и choke. Выключить: <code>net_graph 0</code>.</li>
</ul>

<h2>2. Ограничение FPS</h2>
<ul>
  <li><code>fps_max 100</code> — стандарт и максимум, разрешённый на большинстве серверов.</li>
  <li>В новой версии Steam для FPS выше 100 сначала нужна команда <code>fps_override 1</code>. Учтите: некоторые серверы запрещают FPS выше 100, потому что на старом движке это меняет физику движения.</li>
</ul>

<h2>3. Отключение вертикальной синхронизации</h2>
<p><code>gl_vsync 0</code> — FPS не привязан к частоте монитора (например, 60 Гц), мышь реагирует быстрее. В панели видеокарты (NVIDIA / AMD) V-Sync тоже должен быть выключен.</p>

<h2>4. Графические команды для слабого ПК</h2>
<table>
  <thead><tr><th>Команда</th><th>Что даёт</th></tr></thead>
  <tbody>
    <tr><td><code>r_decals 100</code></td><td>Меньше следов от пуль и пятен крови — FPS не проседает в перестрелках</td></tr>
    <tr><td><code>mp_decals 100</code></td><td>Количество следов в сетевой игре</td></tr>
    <tr><td><code>max_shells 0</code></td><td>Не рисуются вылетающие гильзы</td></tr>
    <tr><td><code>max_smokepuffs 0</code></td><td>Убирает дымок в месте попадания</td></tr>
    <tr><td><code>cl_weather 0</code></td><td>Отключает дождь/снег (на некоторых картах)</td></tr>
  </tbody>
</table>
<p>В меню игры: <em>Options → Video</em> — выберите режим <strong>OpenGL</strong> (намного быстрее Software) и при необходимости уменьшите разрешение (например, 1024×768).</p>

<h2>5. Параметры запуска в Steam</h2>
<p>Steam → Библиотека → Counter-Strike → Свойства → <em>Параметры запуска</em>:</p>
<pre><code>-nojoy -noforcemparms -noforcemaccel -freq 75 -console</code></pre>
<ul>
  <li><code>-nojoy</code> — отключает поддержку джойстика.</li>
  <li><code>-noforcemparms -noforcemaccel</code> — ускорение мыши Windows не влияет на игру.</li>
  <li><code>-freq 75</code> — частота монитора (60, 75, 144 — по вашему монитору).</li>
  <li><code>-console</code> — игра запускается с открытой консолью.</li>
</ul>

<h2>6. Со стороны Windows</h2>
<ul>
  <li>Включите схему питания <strong>«Высокая производительность»</strong>.</li>
  <li>Обновите драйвер видеокарты.</li>
  <li>Закройте браузер, торрент и другие лишние программы на время игры.</li>
</ul>

<p>Запишите команды в <code>cstrike/userconfig.cfg</code>, чтобы не вводить их каждый раз. Подробнее: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">коды и команды CS 1.6</a> · <a href="/blog/cs-16-pricel-sozlamalari/">настройки прицела</a> · <a href="/blog/cs-16-headshot-sozlamalari/">сетевые настройки для хедшотов</a>.</p>
""",
        },
        "en": {
            "name": "How to raise FPS in CS 1.6: commands, launch options and settings",
            "title": "When the game stutters: show FPS, lift the cap, turn off vertical sync and tune a weak PC.",
            "body": """
<p>FPS (<em>frames per second</em>) is how many frames the game draws each second. With low FPS, CS 1.6 stutters, the mouse lags and aiming gets harder. These settings make the game smoother even on a weak computer.</p>

<h2>1. See your current FPS</h2>
<ul>
  <li><code>cl_showfps 1</code> shows an FPS counter (Steam version).</li>
  <li><code>net_graph 3</code> shows FPS, ping, packet loss and choke. Turn off with <code>net_graph 0</code>.</li>
</ul>

<h2>2. The FPS cap</h2>
<ul>
  <li><code>fps_max 100</code> is the default and the highest value most servers allow.</li>
  <li>In the current Steam version, going above 100 needs <code>fps_override 1</code> first. Some servers forbid more than 100 FPS because on the old engine it changes movement physics.</li>
</ul>

<h2>3. Turn off vertical sync</h2>
<p><code>gl_vsync 0</code> stops FPS from being tied to the monitor refresh rate (for example 60 Hz), so the mouse responds faster. Turn V-Sync off in the NVIDIA / AMD control panel too.</p>

<h2>4. Graphics commands for a weak PC</h2>
<table>
  <thead><tr><th>Command</th><th>Effect</th></tr></thead>
  <tbody>
    <tr><td><code>r_decals 100</code></td><td>Fewer bullet holes and blood decals, so FPS holds up in firefights</td></tr>
    <tr><td><code>mp_decals 100</code></td><td>Decal count in online games</td></tr>
    <tr><td><code>max_shells 0</code></td><td>No ejected shell casings</td></tr>
    <tr><td><code>max_smokepuffs 0</code></td><td>No smoke puffs where bullets hit</td></tr>
    <tr><td><code>cl_weather 0</code></td><td>Turns off rain/snow on maps that have it</td></tr>
  </tbody>
</table>
<p>In <em>Options → Video</em>, choose <strong>OpenGL</strong> (much faster than Software) and lower the resolution if needed (for example 1024×768).</p>

<h2>5. Steam launch options</h2>
<p>Steam → Library → Counter-Strike → Properties → <em>Launch options</em>:</p>
<pre><code>-nojoy -noforcemparms -noforcemaccel -freq 75 -console</code></pre>
<ul>
  <li><code>-nojoy</code> disables joystick support.</li>
  <li><code>-noforcemparms -noforcemaccel</code> keep Windows mouse acceleration out of the game.</li>
  <li><code>-freq 75</code> sets the refresh rate (60, 75, 144 — match your monitor).</li>
  <li><code>-console</code> starts the game with the console open.</li>
</ul>

<h2>6. On the Windows side</h2>
<ul>
  <li>Switch the power plan to <strong>High performance</strong>.</li>
  <li>Update the graphics driver.</li>
  <li>Close the browser, torrents and other heavy programs while playing.</li>
</ul>

<p>Put the commands in <code>cstrike/userconfig.cfg</code> so you do not have to type them each time. More: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">CS 1.6 codes and commands</a> · <a href="/blog/cs-16-pricel-sozlamalari/">Crosshair settings</a> · <a href="/blog/cs-16-headshot-sozlamalari/">Network settings for headshots</a>.</p>
""",
        },
    },
    # ==========================================================================
    # 3. HEADSHOT (TARMOQ VA SIÇQONÇA)
    # ==========================================================================
    {
        "key": "headshot",
        "slug": "cs-16-headshot-sozlamalari",
        "image": "post/images/cs16_headshot_sozlamalari.jpg",
        "seo_title": "CS 1.6 headshot kodlari: haqiqat va işlaydigan sozlamalar",
        "seo_description": "CS 1.6 «headshot kodlari» aslida nima: rate, cl_updaterate, cl_cmdrate, ex_interp tarmoq sozlamalari, siçqonça (m_rawinput) va nişon oliş maslahatlari.",
        "uz": {
            "name": "CS 1.6 headshot kodlari: haqiqat va rostdan işlaydigan sozlamalar",
            "title": "Avtomatik headshot qiladigan kod yöq — lekin tarmoq, siçqonça va pricel sozlamalari hamda töğri odatlar boşga tegişni sezilarli oşiradi.",
            "body": """
<p>Internetda "CS 1.6 headshot kodlari" deb köp röyxatlar tarqalgan. Avval eng muhim haqiqat: <strong>öq özi boşga tegadigan buyruq yöq</strong>. Buni qiladigan har qanday dastur — aimbot, ya'ni çit; serverlar uni aniqlaydi va doimiy ban beradi. "Headshot kodlari" deb tarqatiladigan narsalar aslida <strong>tarmoq va siçqonça sozlamalari</strong>. Ular töğri qöyilsa, öqlar rostdan ham siz nişonga olgan joyga tegadi. Quyida — aynan şu sozlamalar.</p>

<h2>1. Tarmoq sozlamalari (eng muhimi)</h2>
<p>Agar internet sozlamalari past bölsa, siz raqibning eski joyini körasiz va öq "ötib ketadi". Konsolga:</p>
<pre><code>rate 25000
cl_updaterate 101
cl_cmdrate 101
ex_interp 0.01
cl_lc 1
cl_lw 1</code></pre>
<table>
  <thead><tr><th>Buyruq</th><th>Nima qiladi</th></tr></thead>
  <tbody>
    <tr><td><code>rate</code></td><td>Serverdan soniyasiga qabul qilinadigan ma'lumot hajmi. Internet sekin bölsa 15000–20000 qiling</td></tr>
    <tr><td><code>cl_updaterate</code></td><td>Server soniyasiga neçta yangilaniş yuborişi (raqiblar holati)</td></tr>
    <tr><td><code>cl_cmdrate</code></td><td>Siz serverga soniyasiga neçta buyruq (harakat, otiş) yuborasiz</td></tr>
    <tr><td><code>ex_interp</code></td><td>Interpolyatsiya: raqib modeli haqiqiy joyiga qançalik yaqin körinadi</td></tr>
    <tr><td><code>cl_lc</code>, <code>cl_lw</code></td><td>Keçikiş kompensatsiyasi va qurol başorati — öçirmang</td></tr>
  </tbody>
</table>
<p>Natijani <code>net_graph 3</code> bilan tekşiring: <em>loss</em> va <em>choke</em> 0 ga yaqin bölişi kerak. Choke köpaysa, <code>cl_updaterate</code> va <code>rate</code> ni biroz kamaytiring. Ping yuqori bölsa (100 dan ortiq), yaqinroq server tanlang — buni buyruq bilan tuzatib bölmaydi.</p>

<h2>2. Siçqonça</h2>
<ul>
  <li><code>m_rawinput 1</code> — siçqonçadan töğridan-töğri ma'lumot (Windows tezlanişisiz). Steam versiyasida bor.</li>
  <li><code>m_filter 0</code> — harakatni silliqlaş öçiq: nişon aniqroq.</li>
  <li><code>sensitivity 2</code> — sezgirlik. Köp öyinçilar past qiymat (1.5–3) tanlaydi: qöl bilan katta harakat, lekin aniqroq nişon.</li>
  <li><code>zoom_sensitivity_ratio 1</code> — AWP/Scout optikasidagi sezgirlik nisbati.</li>
</ul>

<h2>3. Pricel boş balandligida</h2>
<p>Eng köp headshot beradigan odat — <strong>pricelni doim raqib boşi balandligida uşlab yuriş</strong>. Burçakdan çiqayotganda pricel erga emas, eşik yoki devor çetidagi boş balandligiga qarasin. Şunda raqib çiqqanda siçqonçani deyarli qimirlatmaysiz. Pricelni sozlaş: <a href="/blog/cs-16-pricel-sozlamalari/">CS 1.6 pricel sozlamalari</a>.</p>

<h2>4. Otiş texnikasi</h2>
<ul>
  <li><strong>Töxtab oting.</strong> CS 1.6 da yugurib otilgan öq tarqalib ketadi. Avval töxtang, keyin oting.</li>
  <li><strong>Qisqa seriyalar.</strong> AK-47 va M4A1 da birinçi 2–3 ta öq eng aniq; uzoq masofada tugmani uzoq bosib turmang.</li>
  <li><strong>Engaşiş (Ctrl)</strong> aniqlikni biroz oşiradi, lekin harakatni sekinlaştiradi.</li>
  <li><strong>Deagle</strong> va <strong>USP</strong> bilan boşga bitta aniq öq köpinça yetarli — şoşilmang.</li>
</ul>

<h2>5. Maşq</h2>
<p>Botlar bilan maşq qiling: <code>bot_add</code> bilan bot qöşing, <code>bot_difficulty 3</code> — eng qiyin daraja. Har kuni 10–15 daqiqa faqat boşga otişni maşq qiliş (masalan, faqat Deagle bilan) bir haftada sezilarli natija beradi. Botlar buyruqlari: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">CS 1.6 kodlari va konsol buyruqlari</a>.</p>

<p>Barça sozlamalarni <code>cstrike/userconfig.cfg</code> faylga saqlang. FPS past bölsa, nişon ham "sakraydi" — avval <a href="/blog/cs-16-fps-oshirish/">FPS'ni oşiring</a>.</p>
""",
        },
        "ru": {
            "name": "Коды на хедшот в CS 1.6: правда и настройки, которые действительно работают",
            "title": "Команды, которая сама делает хедшоты, нет — но сетевые настройки, мышь, прицел и правильные привычки заметно увеличивают попадания в голову.",
            "body": """
<p>В интернете много списков «кодов на хедшот для CS 1.6». Сначала главное: <strong>команды, после которой пуля сама летит в голову, не существует</strong>. Любая программа, которая это делает, — аимбот, то есть чит; серверы его определяют и банят навсегда. То, что выдают за «коды на хедшот», на самом деле <strong>сетевые настройки и настройки мыши</strong>. Если выставить их правильно, пули действительно летят туда, куда вы целитесь. Ниже — именно они.</p>

<h2>1. Сетевые настройки (самое важное)</h2>
<p>При слабых сетевых настройках вы видите противника там, где его уже нет, и пули «пролетают сквозь». В консоль:</p>
<pre><code>rate 25000
cl_updaterate 101
cl_cmdrate 101
ex_interp 0.01
cl_lc 1
cl_lw 1</code></pre>
<table>
  <thead><tr><th>Команда</th><th>Что делает</th></tr></thead>
  <tbody>
    <tr><td><code>rate</code></td><td>Сколько данных в секунду принимается от сервера. При медленном интернете — 15000–20000</td></tr>
    <tr><td><code>cl_updaterate</code></td><td>Сколько обновлений (положение противников) сервер присылает в секунду</td></tr>
    <tr><td><code>cl_cmdrate</code></td><td>Сколько команд (движение, выстрелы) вы отправляете серверу в секунду</td></tr>
    <tr><td><code>ex_interp</code></td><td>Интерполяция: насколько модель противника близка к его реальной позиции</td></tr>
    <tr><td><code>cl_lc</code>, <code>cl_lw</code></td><td>Компенсация лагов и предсказание оружия — не выключайте</td></tr>
  </tbody>
</table>
<p>Проверьте через <code>net_graph 3</code>: <em>loss</em> и <em>choke</em> должны быть около 0. Если растёт choke, немного уменьшите <code>cl_updaterate</code> и <code>rate</code>. Если пинг выше 100, выберите сервер поближе — командой это не исправить.</p>

<h2>2. Мышь</h2>
<ul>
  <li><code>m_rawinput 1</code> — данные напрямую от мыши, без ускорения Windows (есть в версии Steam).</li>
  <li><code>m_filter 0</code> — без сглаживания движения: прицеливание точнее.</li>
  <li><code>sensitivity 2</code> — чувствительность. Многие выбирают низкую (1.5–3): движение рукой больше, но точнее.</li>
  <li><code>zoom_sensitivity_ratio 1</code> — чувствительность в прицеле AWP/Scout.</li>
</ul>

<h2>3. Прицел на уровне головы</h2>
<p>Привычка, которая даёт больше всего хедшотов, — <strong>всегда держать прицел на высоте головы противника</strong>. Выходя из-за угла, смотрите не в пол, а на высоту головы у края двери или стены. Тогда при появлении противника мышь почти не нужно двигать. Настройка прицела: <a href="/blog/cs-16-pricel-sozlamalari/">настройки прицела в CS 1.6</a>.</p>

<h2>4. Техника стрельбы</h2>
<ul>
  <li><strong>Стреляйте остановившись.</strong> В CS 1.6 пули на бегу сильно разлетаются.</li>
  <li><strong>Короткие очереди.</strong> У AK-47 и M4A1 точнее всего первые 2–3 пули; на дальней дистанции не зажимайте кнопку.</li>
  <li><strong>Присед (Ctrl)</strong> немного повышает точность, но замедляет.</li>
  <li>С <strong>Deagle</strong> и <strong>USP</strong> часто хватает одного точного выстрела в голову — не торопитесь.</li>
</ul>

<h2>5. Тренировка</h2>
<p>Тренируйтесь с ботами: <code>bot_add</code> добавляет бота, <code>bot_difficulty 3</code> — самый сложный уровень. 10–15 минут в день стрельбы только в голову (например, только с Deagle) дают заметный результат за неделю. Команды для ботов: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">коды и консольные команды CS 1.6</a>.</p>

<p>Сохраните настройки в <code>cstrike/userconfig.cfg</code>. При низком FPS прицел тоже «прыгает» — сначала <a href="/blog/cs-16-fps-oshirish/">поднимите FPS</a>.</p>
""",
        },
        "en": {
            "name": "CS 1.6 headshot codes: the truth and settings that actually work",
            "title": "No command makes headshots for you — but network, mouse and crosshair settings plus good habits raise your headshot rate a lot.",
            "body": """
<p>Many lists of "CS 1.6 headshot codes" circulate online. The key fact first: <strong>no command makes your bullets go to the head by themselves</strong>. Any program that does is an aimbot, i.e. a cheat, and servers detect and permanently ban it. What gets called "headshot codes" are really <strong>network and mouse settings</strong>. Set correctly, they make your bullets land where you actually aim.</p>

<h2>1. Network settings (the most important part)</h2>
<pre><code>rate 25000
cl_updaterate 101
cl_cmdrate 101
ex_interp 0.01
cl_lc 1
cl_lw 1</code></pre>
<table>
  <thead><tr><th>Command</th><th>What it does</th></tr></thead>
  <tbody>
    <tr><td><code>rate</code></td><td>How much data per second you accept from the server. Use 15000–20000 on a slow connection</td></tr>
    <tr><td><code>cl_updaterate</code></td><td>How many updates (enemy positions) the server sends per second</td></tr>
    <tr><td><code>cl_cmdrate</code></td><td>How many commands (movement, shots) you send per second</td></tr>
    <tr><td><code>ex_interp</code></td><td>Interpolation: how close an enemy model is drawn to its real position</td></tr>
    <tr><td><code>cl_lc</code>, <code>cl_lw</code></td><td>Lag compensation and weapon prediction — keep them on</td></tr>
  </tbody>
</table>
<p>Check with <code>net_graph 3</code>: <em>loss</em> and <em>choke</em> should be near 0. If choke grows, lower <code>cl_updaterate</code> and <code>rate</code> a little. If ping is over 100, pick a closer server; no command fixes that.</p>

<h2>2. Mouse</h2>
<ul>
  <li><code>m_rawinput 1</code> reads the mouse directly, without Windows acceleration (Steam version).</li>
  <li><code>m_filter 0</code> turns off smoothing for more precise aim.</li>
  <li><code>sensitivity 2</code>: many players choose a low value (1.5–3) for precision.</li>
  <li><code>zoom_sensitivity_ratio 1</code> sets sensitivity in the AWP/Scout scope.</li>
</ul>

<h2>3. Keep the crosshair at head height</h2>
<p>The habit that gives the most headshots is <strong>always keeping your crosshair where an enemy's head will appear</strong>: at head height on the edge of a door or wall, not on the floor. Then you barely move the mouse when someone peeks. See <a href="/blog/cs-16-pricel-sozlamalari/">CS 1.6 crosshair settings</a>.</p>

<h2>4. Shooting technique</h2>
<ul>
  <li><strong>Stop before you shoot.</strong> Bullets fired while running spread a lot in CS 1.6.</li>
  <li><strong>Short bursts.</strong> The first 2–3 bullets of the AK-47 and M4A1 are the most accurate.</li>
  <li><strong>Crouching (Ctrl)</strong> adds a little accuracy but slows you down.</li>
  <li>With the <strong>Deagle</strong> and <strong>USP</strong> one accurate head shot is often enough — do not rush.</li>
</ul>

<h2>5. Practice</h2>
<p>Practice against bots: <code>bot_add</code> adds one, <code>bot_difficulty 3</code> is the hardest level. 10–15 minutes a day of head-only shooting (for example, Deagle only) shows clear results within a week. Bot commands: <a href="/blog/counter-strike-16-oyinida-ishlatiladigan-kodlar/">CS 1.6 codes and console commands</a>.</p>

<p>Save everything in <code>cstrike/userconfig.cfg</code>. Low FPS makes aim jumpy too, so <a href="/blog/cs-16-fps-oshirish/">raise your FPS</a> first.</p>
""",
        },
    },
]

# Asosiy «CS 1.6 kodlari» maqolasi oxiriga qöşiladigan bağlovçi blok (bir marta: LINKS_MARKER bilan)
MAIN_LINKS = {
    "uz": ("Batafsil qöllanmalar", {
        "pricel": "Pricel sozlamalari: rang, ölçam va tayyor kodlar",
        "fps": "FPS oşiriş: buyruqlar va işga tuşiriş parametrlari",
        "headshot": "Headshot kodlari: haqiqat va işlaydigan tarmoq sozlamalari",
    }),
    "ru": ("Подробные руководства", {
        "pricel": "Настройки прицела: цвет, размер и готовые коды",
        "fps": "Как поднять FPS: команды и параметры запуска",
        "headshot": "Коды на хедшот: правда и рабочие сетевые настройки",
    }),
    "en": ("Detailed guides", {
        "pricel": "Crosshair settings: color, size and ready codes",
        "fps": "Raising FPS: commands and launch options",
        "headshot": "Headshot codes: the truth and network settings that work",
    }),
}

# Kirillga ögirilmaydigan qismlar: kod va inglizça atamalar (öyin menyusi, qurollar, xaritalar)
_ENGLISH = (
    r"[Hh]eadshot|aimbot|choke|loss|Steam|OpenGL|Software|Launch options|Options|Keyboard|Advanced"
    r"|Enable developer console|Video|Properties|Enter|Esc|Ctrl|Deagle|USP|AWP|Scout|FPS|V-Sync|NVIDIA|AMD"
    r"|High performance|frames per second|cyan|Hz|de_dust2|de_inferno|ping"
)
_PROTECTED = re.compile(rf"<pre\b.*?</pre>|<code\b.*?</code>|<em>[A-Za-z →]+</em>|\b(?:{_ENGLISH})\b", re.S)


def to_cyrillic(html):
    """Özbekça matnni kirillga ögiradi, lekin <code>/<pre> içidagi buyruqlar lotinça qoladi."""
    from core.translit import latin_to_cyrillic

    parts, pos = [], 0
    for m in _PROTECTED.finditer(html):
        parts.append(latin_to_cyrillic(html[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(latin_to_cyrillic(html[pos:]))
    # «c» harfi bor söz ögirgiçda xorijiy deb qoladi — özbekça «pricel» kirillda «прицел»
    return re.sub(
        r"(?<![\w/-])([Pp])ricel([a-zşçğö]*)",
        lambda m: ("Прицел" if m.group(1) == "P" else "прицел") + latin_to_cyrillic(m.group(2)),
        "".join(parts),
    )


def links_block(lang, articles):
    heading, names = MAIN_LINKS[lang]
    items = "".join(f'<li><a href="/blog/{a["slug"]}/">{names[a["key"]]}</a></li>' for a in articles)
    return f"\n{LINKS_MARKER}\n<h2>{heading}</h2>\n<ul>{items}</ul>\n"


class Command(BaseCommand):
    help = "CS 1.6 turkumi (pricel, FPS, headshot) maqolalarini naşr qiladi va asosiy maqola bilan bağlaydi."

    def add_arguments(self, parser):
        parser.add_argument("--update", action="store_true", help="Mavjud maqolalarni ham yangilaş")
        parser.add_argument("--draft", action="store_true", help="Qoralama (2099-yil) sifatida saqlaş")
        parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmasdan tekşiriş")
        parser.add_argument("--only", choices=[a["key"] for a in ARTICLES], help="Faqat bitta maqola")

    def handle(self, *args, **opts):
        from django.core.cache import cache
        from django.utils import timezone

        from blog.models import Posts

        articles = [a for a in ARTICLES if not opts["only"] or a["key"] == opts["only"]]
        main = Posts.objects.filter(slug=MAIN_SLUG).first()
        if main is None:
            raise CommandError(f"Asosiy maqola topilmadi: {MAIN_SLUG}")
        publish_time = DRAFT_TIME if opts["draft"] else timezone.now()

        for article in articles:
            fields = {"seo_title": article["seo_title"][:70], "seo_description": article["seo_description"][:200],
                      "image": article.get("image", IMAGE), "source_url": "", "publish_time": publish_time}
            for lang, sfx in (("uz", "uz_uz"), ("ru", "ru_ru"), ("en", "en_us")):
                data = article[lang]
                fields[f"name_{sfx}"] = data["name"].strip()
                fields[f"title_{sfx}"] = data["title"].strip()
                fields[f"body_{sfx}"] = data["body"].strip()
            fields["name_uz_crl"] = to_cyrillic(fields["name_uz_uz"])
            fields["title_uz_crl"] = to_cyrillic(fields["title_uz_uz"])
            fields["body_uz_crl"] = to_cyrillic(fields["body_uz_uz"])

            if opts["dry_run"]:
                sizes = ", ".join(f"{k[-5:]}={len(v)}" for k, v in fields.items() if k.startswith("body_"))
                self.stdout.write(f"[DRY-RUN] {article['slug']}: {fields['name_uz_uz']} ({sizes})")
                continue
            post = Posts.objects.filter(slug=article["slug"]).first()
            if post and not opts["update"]:
                self.stdout.write(self.style.WARNING(f"Mavjud: /blog/{article['slug']}/ (yangilaş: --update)"))
                continue
            created = post is None
            if created:
                post = Posts(slug=article["slug"], created_by=main.created_by, categorie=main.categorie)
            else:
                fields.pop("publish_time")  # yangilaşda naşr sanasi saqlanadi
            for key, value in fields.items():
                setattr(post, key, value)
            post.save()
            self.stdout.write(self.style.SUCCESS(
                f"{'Yaratildi' if created else 'Yangilandi'}: https://complexprogrammer.uz/blog/{article['slug']}/"
            ))

        # Asosiy maqoladan yangi maqolalarga havola (qidiruv robotlari va öquvçilar turkumni topsin)
        if not opts["dry_run"] and not opts["draft"] and LINKS_MARKER not in (main.body_uz_uz or ""):
            for lang, sfx in (("uz", "uz_uz"), ("ru", "ru_ru"), ("en", "en_us")):
                block = links_block(lang, ARTICLES)
                setattr(main, f"body_{sfx}", (getattr(main, f"body_{sfx}") or "").rstrip() + block)
                if lang == "uz":
                    main.body_uz_crl = (main.body_uz_crl or "").rstrip() + to_cyrillic(block)
            main.save(update_fields=["body_uz_uz", "body_uz_crl", "body_ru_ru", "body_en_us", "updated_at"])
            self.stdout.write(self.style.SUCCESS(f"Asosiy maqolaga havolalar qöşildi: /blog/{MAIN_SLUG}/"))

        # Telegram'ga joylaş signal içida alohida oqimda boradi — buyruq tugaguncha kutamiz
        for t in list(threading.enumerate()):
            if t is not threading.main_thread() and t.is_alive() and t.name.startswith("Thread"):
                t.join(timeout=25)
        time.sleep(0.3)
        try:
            cache.clear()
        except Exception:
            pass
