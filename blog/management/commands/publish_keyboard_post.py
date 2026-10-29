"""Yangi Özbek alifbosi klaviaturasi mavzusidagi blog maqolasini naşr qiliş yoki yangilaş.

Uşbu buyruq Microsoft Store'dagi "O'zbek alifbosi klaviaturasi" (Ryzen_b) ilovasi,
Windows tizimidagi "Turkish Q" tartibi, AltGr maketlari va smartfon sozlamalari
asosida tayyorlangan töliq qöllanmani blogga naşr etadi.

Işlatiş:
    python manage.py publish_keyboard_post           # darhol saytda naşr qiladi
    python manage.py publish_keyboard_post --update  # mavjud maqola matnini yangilaydi
    python manage.py publish_keyboard_post --draft   # qoralama qilib saqlaydi (2099-yil)
    python manage.py publish_keyboard_post --dry-run # bazaga yozmasdan tekşiriş
"""

import datetime
import os
import threading
import time

SLUG = "yangi-ozbek-alifbosi-klaviaturasi"
IMAGE_REL_PATH = "post/images/yangi_ozbek_alifbosi_klaviaturasi.jpg"
STORE_URL = "https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM"
DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)

SEO_TITLE = "Yangi Özbek alifbosi klaviaturasi — Windows va smartfonda örnatiş"
SEO_DESCRIPTION = (
    "2026-yilgi yangi özbek alifbosi (Ş, Ç, Ğ, Ö) harflarini kompyuter va telefonda "
    "oson teriş usullari: Microsoft Store ilovasi, Turkish Q tartibi va mobil sozlamalar."
)

ARTICLE_DATA = {
    "uz": {
        "name": "Yangi Özbek alifbosi klaviaturasi: Windows, macOS va telefonlarda Ş, Ç, Ğ, Ö harflarini qulay teriş",
        "title": (
            "Kompyuter va smartfonlarda 2026-yilgi yangi özbek alifbosida xatosiz va tez yozış uçun "
            "eng yaxşi klaviatura dasturlari, qisqa klavişlar va amaliy sozlamalar qöllanmasi."
        ),
        "body": """
<p>Özbekiston Respublikasida 2026-yilgi isloh qilingan lotin alifbosiga bölgan ehtiyoj va qiziqiş tobora oşib bormoqda. Yangi alifboda avvalgi ikki belgili birikmalar örniga bitta yaxlit harflar joriy etildi: <strong>Ş ş</strong> (avvalgi <em>sh</em>), <strong>Ç ç</strong> (avvalgi <em>ch</em>), <strong>Ğ ğ</strong> (avvalgi <em>g‘</em>) va <strong>Ö ö</strong> (avvalgi <em>o‘</em>). Bu islohot matnlarni ixçamlaştiriş, xatoliklarni kamaytiriş va dasturiy ta’minotlarda qidiruv tizimini osonlaştirişda ulkan yutuq böldi.</p>

<p>Biroq köpçilik foydalanuvçilarda tabiiy savol tuğilmoqda: <em>«Kompyuter klaviaturasida yoki smartfonda bu harflarni qanday qilib oson va tez teriş mumkin?»</em> Standart inglizça QWERTY klaviaturasida uşbu harflar alohida klaviş sifatida mavjud emas. Quyidagi batafsil qöllanmada Windows, macOS, Android va iOS tizimlarida yangi harflarni heç qanday qiyinçiliksiz terişning <strong>eng samarali 5 ta usulini</strong> körsatib beramiz.</p>

<hr />

<h2>1-usul: Microsoft Store’dagi «Özbek alifbosi klaviaturasi» dasturi (Tavsiya etiladi)</h2>

<p>Windows 10 va Windows 11 foydalanuvçilari uçun eng qulay va zamonaviy yeçimlardan biri — dasturçi <strong>Ryzen_b</strong> tomonidan yaratilgan va rasmiy Microsoft Store dökoniga joylaştirilgan <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>«Özbek alifbosi klaviaturasi»</strong></a> yordamçi dasturidir.</p>

<p>Uşbu yengil dastur tizimda orqa fonda işlaydi va odatiy inglizça (yoki özbekça lotin) klaviatura tartibiga maxsus qisqa klavişlar (hotkeys) kombinatsiyasini qöşadi:</p>

<ul>
  <li><code>Alt + O</code> (yoki <code>Ctrl + O</code>) ➔ <strong>ö</strong> (katta harf: <code>Alt + Shift + O</code> ➔ <strong>Ö</strong>)</li>
  <li><code>Alt + G</code> (yoki <code>Ctrl + G</code>) ➔ <strong>ğ</strong> (katta harf: <code>Alt + Shift + G</code> ➔ <strong>Ğ</strong>)</li>
  <li><code>Alt + S</code> (yoki <code>Ctrl + S</code>) ➔ <strong>ş</strong> (katta harf: <code>Alt + Shift + S</code> ➔ <strong>Ş</strong>)</li>
  <li><code>Alt + C</code> (yoki <code>Ctrl + C</code>) ➔ <strong>ç</strong> (katta harf: <code>Alt + Shift + C</code> ➔ <strong>Ç</strong>)</li>
</ul>

<h3>Dasturning asosiy afzalliklari:</h3>
<ol>
  <li><strong>Avtomatik işga tuşiş:</strong> Kompyuter yoqilişi bilan Windows bilan birga fonda yuklanadi va bildirişlar maydoni (system tray)da qulay belgi bilan turadi.</li>
  <li><strong>Aqlli til nazorati:</strong> Agar siz klaviatura tilini Rusça (kirill) ga almaştirsangiz, dastur buni avtomatik aniqlaydi va qisqa klavişlarni vaqtinça öçirib turadi. Lotinçaga qaytganingizda esa yana darhol faollaşadi.</li>
  <li><strong>Xavfsiz va tizimga daxlsiz:</strong> Registr fayllarini yoki tizim drayverlarini özgartirmaydi, kompyuter tezligiga mutlaqo ta’sir qilmaydi.</li>
  <li><strong>Rasmiy dökon kafolati:</strong> Microsoft Store xavfsizlik tekşiruvidan ötganligi sababli virus yoki zararli kodlardan mutlaqo xoli.</li>
</ol>

<p>👉 <strong>Yuklab oliş havolasi:</strong> <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store — Özbek alifbosi klaviaturasi</strong></a></p>

<hr />

<h2>2-usul: Qöşimça dastursiz — Windows’da «Turkish Q» klaviaturasi</h2>

<p>Agar sizda begona, işxona yoki öquv markazi kompyuteri bölib, unga qöşimça dastur örnatiş huquqi (administrator paroli) bölmasa, ajoyib sodda yeçim mavjud: <strong>Turkça Q (Turkish Q)</strong> klaviatura tartibini qöşiş.</p>

<p>Çunki turk alifbosida ham ayni şu harflar (<strong>Ş, Ç, Ö, Ğ</strong>) mavjud bölib, ular klaviaturaning öng tomonidagi tiniş belgilari örnida joylaşgan:</p>

<ul>
  <li><code>;</code> (nuqtali vergul) klavişi ➔ <strong>Ş ş</strong></li>
  <li><code>.</code> (nuqta) klavişi ➔ <strong>Ç ç</strong></li>
  <li><code>,</code> (vergul) klavişi ➔ <strong>Ö ö</strong></li>
  <li><code>[</code> (kvadrat qavs) klavişi ➔ <strong>Ğ ğ</strong></li>
</ul>

<h3>Qanday qöşiladi?</h3>
<ol>
  <li>Windows <strong>Settings</strong> (Sozlamalar: <code>Win + I</code>) menyusiga kiring.</li>
  <li><strong>Time &amp; Language</strong> ➔ <strong>Language &amp; Region</strong> (Til va mintaqa) bölimiga öting.</li>
  <li>Özbek yoki ingliz tili qatoridagi üç nuqtani bosib, <strong>Language options</strong> ni tanlang.</li>
  <li><strong>Add a keyboard</strong> (Klaviatura qöşiş) tugmasini bosing va röyxatdan <strong>Turkish Q</strong> ni tanlang.</li>
</ol>
<p>Endi <code>Alt + Shift</code> yoki <code>Win + Space</code> orqali uşbu klaviaturaga ötib, barmoğingiz ostidagi bitta tugma orqali bemalol yangi harflarni tera olasiz.</p>

<hr />

<h2>3-usul: AltGr tizimi va mustaqil klaviatura maketlari (MSKLC)</h2>

<p>Klaviaturaning öng tomonidagi <code>Alt</code> (ba’zi klaviaturalarda <code>AltGr</code> deb yozilgan) tugmasi xalqaro me’yorda qöşimça belgilarni teriş uçun möljallangan. Dasturçilar tomonidan Microsoft Keyboard Layout Creator (MSKLC) asosida tayyorlangan özbekça maketlarda:</p>
<ul>
  <li><code>AltGr + S</code> ➔ <strong>ş</strong></li>
  <li><code>AltGr + C</code> ➔ <strong>ç</strong></li>
  <li><code>AltGr + G</code> ➔ <strong>ğ</strong></li>
  <li><code>AltGr + O</code> ➔ <strong>ö</strong></li>
</ul>
<p>Bu usul qidiruv va matn muharrirlaridagi <code>Ctrl + S</code> (saqlaş) yoki <code>Ctrl + C</code> (nusxalaş) kabi tizim buyruqlari bilan heç qaçon töqnaşmaydi.</p>

<hr />

<h2>4-usul: Smartfonlarda (Android va iOS / iPhone) yangi harflarni teriş</h2>

<p>Zamonaviy mobil telefonlarda qöşimça dastur örnatiş şart emas. Ikki xil juda qulay yöl bor:</p>

<h3>1. Bosib turiş (Long-press) usuli:</h3>
<p>Standart Google Gboard, Samsung Keyboard yoki Apple iOS klaviaturasida asosiy harfni barmoğingiz bilan 1 soniya bosib tursangiz, qöşimça variantlar menyusi oçiladi:</p>
<ul>
  <li><strong>S</strong> harfini bosib tursangiz ➔ <strong>Ş ş</strong> çiqadi.</li>
  <li><strong>C</strong> harfini bosib tursangiz ➔ <strong>Ç ç</strong> çiqadi.</li>
  <li><strong>G</strong> harfini bosib tursangiz ➔ <strong>Ğ ğ</strong> çiqadi.</li>
  <li><strong>O</strong> harfini bosib tursangiz ➔ <strong>Ö ö</strong> çiqadi.</li>
</ul>

<h3>2. Klaviatura sozlamalariga Turkça til qöşiş:</h3>
<p>Agar harflarni bosib turiş vaqtni olsa, telefon sozlamalaridan klaviaturaga <strong>Turkça (Türkçe)</strong> tilini qöşib qöyişingiz mumkin. Natijada ekran klaviaturangizning öng tomonida <strong>Ş, Ç, Ğ, Ö</strong> harflari alohida tölaqonli tugmalar sifatida doimiy körinib turadi.</p>

<hr />

<h2>5-usul: Katta matnlarni bir zumda ötkaziş — Onlayn Changetext ögirgiç</h2>

<p>Agar sizda allaqaçon eski 1995-yilgi lotin alifbosida (<em>sh, ch, o‘, g‘</em> birikmalari bilan) yoki kirill yozuvida yozilgan katta maqolalar, kurs işlari, kitoblar yoki rasmiy hujjatlar mavjud bölsa, ularni qölda qayta terib çiqişga hojat yöq.</p>

<p>Bizning saytimizda maxsus işlab çiqilgan <a href="https://complexprogrammer.uz/changetext/"><strong>Complex Programmer Lotin-Kirill va Yangi Lotin ögirgiçi</strong></a> orqali birgina tugma bilan minglab sahifali matnlarni 2026-yilgi yangi alifboga soniyalar içida xatosiz aylantirib olişingiz mumkin. Ögirgiç veb-manzillarni, dasturlaş kodlarini va inglizça atamalarni toza saqlaydi.</p>

<hr />

<h2>Yangi harflarning Unicode va klaviatura kodlari jadvali</h2>

<p>Dasturçilar, dizaynerlar va qisqa klavişlardan foydalanuvçilar uçun yangi harflarning rasmiy xalqaro parametrlari:</p>

<table class="table table-bordered table-striped" style="width: 100%; margin-top: 15px;">
  <thead>
    <tr style="background-color: #2c3e50; color: #ffffff;">
      <th style="padding: 10px;">Harf (Katta / Kiçik)</th>
      <th style="padding: 10px;">Unicode kodi</th>
      <th style="padding: 10px;">Microsoft Store App</th>
      <th style="padding: 10px;">Turkish Q tartibi</th>
      <th style="padding: 10px;">AltGr kombinatsiyasi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px;"><strong>Ş / ş</strong></td>
      <td style="padding: 10px;"><code>U+015E</code> / <code>U+015F</code></td>
      <td style="padding: 10px;"><code>Alt + S</code></td>
      <td style="padding: 10px;"><code>;</code> (nuqtali vergul)</td>
      <td style="padding: 10px;"><code>AltGr + S</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ç / ç</strong></td>
      <td style="padding: 10px;"><code>U+00C7</code> / <code>U+00E7</code></td>
      <td style="padding: 10px;"><code>Alt + C</code></td>
      <td style="padding: 10px;"><code>.</code> (nuqta)</td>
      <td style="padding: 10px;"><code>AltGr + C</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ğ / ğ</strong></td>
      <td style="padding: 10px;"><code>U+011E</code> / <code>U+011F</code></td>
      <td style="padding: 10px;"><code>Alt + G</code></td>
      <td style="padding: 10px;"><code>[</code> (kvadrat qavs)</td>
      <td style="padding: 10px;"><code>AltGr + G</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ö / ö</strong></td>
      <td style="padding: 10px;"><code>U+00D6</code> / <code>U+00F6</code></td>
      <td style="padding: 10px;"><code>Alt + O</code></td>
      <td style="padding: 10px;"><code>,</code> (vergul)</td>
      <td style="padding: 10px;"><code>AltGr + O</code></td>
    </tr>
  </tbody>
</table>

<hr />

<h2>Xulosa</h2>
<p>2026-yilgi islohot özbek tili yozuvini zamonaviy axborot texnologiyalariga töliq moslaştiriş yönalişidagi eng muhim qadamdir. Kompyuteringizga Microsoft Store’dagi yengil <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>«Özbek alifbosi klaviaturasi»</strong></a> ilovasini örnatib oliş yoki Windows’da <strong>Turkish Q</strong> tartibini yoqiş orqali siz har kuni yuzlab sözlarni bir zumda, xatosiz va çarçoqsiz yoza olasiz!</p>
""",
    },
    "ru": {
        "name": "Клавиатура нового узбекского алфавита: как легко печатать Ş, Ç, Ğ, Ö на Windows, macOS и смартфонах",
        "title": (
            "Полное практическое руководство по настройке узбекской клавиатуры реформы 2026 года: "
            "утилита из Microsoft Store, горячие клавиши, турецкая раскладка и мобильные клавиатуры."
        ),
        "body": """
<p>В рамках реформы узбекского алфавита 2026 года привычные двухбуквенные сочетания заменены отдельными символами с диакритическими знаками: <strong>Ş ş</strong> (вместо <em>sh</em>), <strong>Ç ç</strong> (вместо <em>ch</em>), <strong>Ğ ğ</strong> (вместо <em>g‘</em>) и <strong>Ö ö</strong> (вместо <em>o‘</em>). Это нововведение упрощает поиск, морфологический анализ и набор текста.</p>

<p>Однако на стандартной клавиатуре QWERTY отдельных клавиш для этих букв нет. В данном руководстве рассмотрены <strong>5 лучших способов</strong> быстрой и комфортной печати на новом узбекском алфавите в Windows, macOS, Android и iOS.</p>

<hr />

<h2>Способ 1: Приложение «O‘zbek alifbosi klaviaturasi» из Microsoft Store (Рекомендуется)</h2>

<p>Для пользователей Windows 10 и Windows 11 разработчик <strong>Ryzen_b</strong> создал легкую и удобную фоновую утилиту, доступную официально в магазине <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store</strong></a>.</p>

<p>Приложение добавляет глобальные горячие клавиши:</p>
<ul>
  <li><code>Alt + O</code> (или <code>Ctrl + O</code>) ➔ <strong>ö</strong> (заглавная: <code>Alt + Shift + O</code> ➔ <strong>Ö</strong>)</li>
  <li><code>Alt + G</code> (или <code>Ctrl + G</code>) ➔ <strong>ğ</strong> (заглавная: <code>Alt + Shift + G</code> ➔ <strong>Ğ</strong>)</li>
  <li><code>Alt + S</code> (или <code>Ctrl + S</code>) ➔ <strong>ş</strong> (заглавная: <code>Alt + Shift + S</code> ➔ <strong>Ş</strong>)</li>
  <li><code>Alt + C</code> (или <code>Ctrl + C</code>) ➔ <strong>ç</strong> (заглавная: <code>Alt + Shift + C</code> ➔ <strong>Ç</strong>)</li>
</ul>

<h3>Преимущества утилиты:</h3>
<ol>
  <li><strong>Автозапуск с Windows:</strong> запускается автоматически и тихо работает в системном трее.</li>
  <li><strong>Умное переключение:</strong> при включении русской раскладки перехват сочетаний автоматически отключается, не мешая привычным действиям.</li>
  <li><strong>Безопасность:</strong> не требует сторонних драйверов, проверено модерацией Microsoft Store.</li>
</ol>

<p>👉 <strong>Скачать из Microsoft Store:</strong> <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>«O‘zbek alifbosi klaviaturasi» (Ryzen_b)</strong></a></p>

<hr />

<h2>Способ 2: Без сторонних программ — Турецкая раскладка (Turkish Q) в Windows</h2>

<p>Если на рабочем или учебном компьютере нет прав администратора для установки приложений, самым простым решением является добавление раскладки <strong>Turkish Q</strong>.</p>
<p>В турецком алфавите используются в точности те же буквы:</p>
<ul>
  <li>Клавиша <code>;</code> ➔ <strong>Ş ş</strong></li>
  <li>Клавиша <code>.</code> ➔ <strong>Ç ç</strong></li>
  <li>Клавиша <code>,</code> ➔ <strong>Ö ö</strong></li>
  <li>Клавиша <code>[</code> ➔ <strong>Ğ ğ</strong></li>
</ul>

<p>Чтобы включить: откройте <em>Параметры Windows ➔ Время и язык ➔ Язык и регион ➔ Параметры языка ➔ Добавить клавиатуру ➔ Турецкая (Q)</em>.</p>

<hr />

<h2>Способ 3: Раскладки на базе AltGr (MSKLC)</h2>
<p>При использовании правой клавиши <code>AltGr</code> сочетания <code>AltGr + S</code>, <code>AltGr + C</code>, <code>AltGr + G</code>, <code>AltGr + O</code> не конфликтуют с привычными комбинациями типа <code>Ctrl + C</code> / <code>Ctrl + S</code>.</p>

<hr />

<h2>Способ 4: Смартфоны (Android и iPhone / iOS)</h2>
<ol>
  <li><strong>Долгое нажатие (Long-press):</strong> в клавиатурах Gboard и iOS удерживайте клавиши <code>S</code>, <code>C</code>, <code>G</code>, <code>O</code> для выбора букв <strong>Ş, Ç, Ğ, Ö</strong>.</li>
  <li><strong>Добавление турецкой раскладки:</strong> в настройках клавиатуры включите турецкий язык — буквы появятся в качестве отдельных кнопок в правой части клавиатуры.</li>
</ol>

<hr />

<h2>Способ 5: Мгновенный перевод больших текстов — онлайн-конвертер Changetext</h2>
<p>Большие готовые документы, написанные по правилам 1995 года или на кириллице, можно за одну секунду перевести в новый алфавит 2026 года с помощью сервиса <a href="https://complexprogrammer.uz/changetext/"><strong>Complex Programmer Changetext</strong></a>.</p>

<hr />

<h2>Сводная таблица кодов Unicode</h2>
<table class="table table-bordered table-striped" style="width: 100%;">
  <thead>
    <tr style="background-color: #2c3e50; color: #ffffff;">
      <th style="padding: 10px;">Буква</th>
      <th style="padding: 10px;">Unicode</th>
      <th style="padding: 10px;">Microsoft Store App</th>
      <th style="padding: 10px;">Turkish Q</th>
      <th style="padding: 10px;">AltGr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px;"><strong>Ş / ş</strong></td>
      <td style="padding: 10px;"><code>U+015E</code> / <code>U+015F</code></td>
      <td style="padding: 10px;"><code>Alt + S</code></td>
      <td style="padding: 10px;"><code>;</code></td>
      <td style="padding: 10px;"><code>AltGr + S</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ç / ç</strong></td>
      <td style="padding: 10px;"><code>U+00C7</code> / <code>U+00E7</code></td>
      <td style="padding: 10px;"><code>Alt + C</code></td>
      <td style="padding: 10px;"><code>.</code></td>
      <td style="padding: 10px;"><code>AltGr + C</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ğ / ğ</strong></td>
      <td style="padding: 10px;"><code>U+011E</code> / <code>U+011F</code></td>
      <td style="padding: 10px;"><code>Alt + G</code></td>
      <td style="padding: 10px;"><code>[</code></td>
      <td style="padding: 10px;"><code>AltGr + G</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ö / ö</strong></td>
      <td style="padding: 10px;"><code>U+00D6</code> / <code>U+00F6</code></td>
      <td style="padding: 10px;"><code>Alt + O</code></td>
      <td style="padding: 10px;"><code>,</code></td>
      <td style="padding: 10px;"><code>AltGr + O</code></td>
    </tr>
  </tbody>
</table>
""",
    },
    "en": {
        "name": "New Uzbek Alphabet Keyboard Layout: How to Type Ş, Ç, Ğ, Ö on Windows, macOS, and Mobile",
        "title": (
            "A comprehensive practical guide to setting up the reformed 2026 Uzbek Latin keyboard layout: "
            "Microsoft Store utility, shortcuts, Turkish Q layout, and smartphone settings."
        ),
        "body": """
<p>The 2026 reform of the Uzbek Latin alphabet replaces cumbersome digraphs with single letters equipped with diacritics: <strong>Ş ş</strong> (formerly <em>sh</em>), <strong>Ç ç</strong> (formerly <em>ch</em>), <strong>Ğ ğ</strong> (formerly <em>g‘</em>), and <strong>Ö ö</strong> (formerly <em>o‘</em>). This streamlined standard significantly improves digital typography, indexing, and typing speed.</p>

<p>Because these characters are not present on standard US QWERTY keyboards, users need efficient input methods. Here are the <strong>top 5 practical ways</strong> to type the new Uzbek characters effortlessly on PC and mobile devices.</p>

<hr />

<h2>Method 1: "O‘zbek alifbosi klaviaturasi" from Microsoft Store (Recommended)</h2>

<p>For Windows 10 and 11 users, developer <strong>Ryzen_b</strong> has published a lightweight utility in the official <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store</strong></a>.</p>

<p>It adds convenient system-wide hotkeys:</p>
<ul>
  <li><code>Alt + O</code> (or <code>Ctrl + O</code>) ➔ <strong>ö</strong> (uppercase: <code>Alt + Shift + O</code> ➔ <strong>Ö</strong>)</li>
  <li><code>Alt + G</code> (or <code>Ctrl + G</code>) ➔ <strong>ğ</strong> (uppercase: <code>Alt + Shift + G</code> ➔ <strong>Ğ</strong>)</li>
  <li><code>Alt + S</code> (or <code>Ctrl + S</code>) ➔ <strong>ş</strong> (uppercase: <code>Alt + Shift + S</code> ➔ <strong>Ş</strong>)</li>
  <li><code>Alt + C</code> (or <code>Ctrl + C</code>) ➔ <strong>ç</strong> (uppercase: <code>Alt + Shift + C</code> ➔ <strong>Ç</strong>)</li>
</ul>

<h3>Key Features:</h3>
<ol>
  <li><strong>Autorun:</strong> Starts silently with Windows and rests in the system tray.</li>
  <li><strong>Intelligent Layout Detection:</strong> Automatically suspends hotkeys when Cyrillic layouts are active.</li>
  <li><strong>Safe &amp; Clean:</strong> Requires no administrative system hooks or kernel-level drivers.</li>
</ol>

<p>👉 <strong>Download from Microsoft Store:</strong> <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>O‘zbek alifbosi klaviaturasi (Ryzen_b)</strong></a></p>

<hr />

<h2>Method 2: Built-in Windows Solution — Turkish Q Layout</h2>

<p>If you cannot install third-party software on a school or work computer, you can use the built-in <strong>Turkish Q</strong> layout:</p>
<ul>
  <li>Key <code>;</code> ➔ <strong>Ş ş</strong></li>
  <li>Key <code>.</code> ➔ <strong>Ç ç</strong></li>
  <li>Key <code>,</code> ➔ <strong>Ö ö</strong></li>
  <li>Key <code>[</code> ➔ <strong>Ğ ğ</strong></li>
</ul>

<p>Add it via <em>Windows Settings ➔ Time &amp; Language ➔ Language &amp; Region ➔ Language options ➔ Add a keyboard ➔ Turkish Q</em>.</p>

<hr />

<h2>Method 3: AltGr Keyboard Layouts (MSKLC)</h2>
<p>Layouts based on the Microsoft Keyboard Layout Creator map the right <code>AltGr</code> key to the special characters (e.g. <code>AltGr + S</code> ➔ <strong>ş</strong>), preventing collisions with standard editor shortcuts.</p>

<hr />

<h2>Method 4: Mobile Devices (Android and iOS / iPhone)</h2>
<ul>
  <li><strong>Long-press:</strong> On Gboard or iOS, hold down <code>S</code>, <code>C</code>, <code>G</code>, or <code>O</code> to access <strong>Ş, Ç, Ğ, Ö</strong>.</li>
  <li><strong>Turkish Keyboard:</strong> Add Turkish in your keyboard settings to place dedicated keys right on the on-screen layout.</li>
</ul>

<hr />

<h2>Method 5: Batch Converting Existing Documents — Online Changetext Tool</h2>
<p>For existing files written under the 1995 standard or in Cyrillic, use the free <a href="https://complexprogrammer.uz/changetext/"><strong>Complex Programmer Changetext Converter</strong></a> to convert entire articles in seconds while preserving links, usernames, and code snippets.</p>

<hr />

<h2>Unicode Reference Chart</h2>
<table class="table table-bordered table-striped" style="width: 100%;">
  <thead>
    <tr style="background-color: #2c3e50; color: #ffffff;">
      <th style="padding: 10px;">Letter</th>
      <th style="padding: 10px;">Unicode</th>
      <th style="padding: 10px;">Microsoft Store App</th>
      <th style="padding: 10px;">Turkish Q</th>
      <th style="padding: 10px;">AltGr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px;"><strong>Ş / ş</strong></td>
      <td style="padding: 10px;"><code>U+015E</code> / <code>U+015F</code></td>
      <td style="padding: 10px;"><code>Alt + S</code></td>
      <td style="padding: 10px;"><code>;</code></td>
      <td style="padding: 10px;"><code>AltGr + S</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ç / ç</strong></td>
      <td style="padding: 10px;"><code>U+00C7</code> / <code>U+00E7</code></td>
      <td style="padding: 10px;"><code>Alt + C</code></td>
      <td style="padding: 10px;"><code>.</code></td>
      <td style="padding: 10px;"><code>AltGr + C</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ğ / ğ</strong></td>
      <td style="padding: 10px;"><code>U+011E</code> / <code>U+011F</code></td>
      <td style="padding: 10px;"><code>Alt + G</code></td>
      <td style="padding: 10px;"><code>[</code></td>
      <td style="padding: 10px;"><code>AltGr + G</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ö / ö</strong></td>
      <td style="padding: 10px;"><code>U+00D6</code> / <code>U+00F6</code></td>
      <td style="padding: 10px;"><code>Alt + O</code></td>
      <td style="padding: 10px;"><code>,</code></td>
      <td style="padding: 10px;"><code>AltGr + O</code></td>
    </tr>
  </tbody>
</table>
""",
    },
}

CYR_DATA = {
    "name": "Янги Ўзбек алифбоси клавиатураси: Windows, macOS ва телефонларда Ш, Ч, Ғ, Ў ҳарфларини қулай териш",
    "title": (
        "Компьютер ва смартфонларда 2026 йилги янги ўзбек алифбосида хатосиз ва тез ёзиш учун "
        "энг яхши клавиатура дастурлари, қисқа клавишлар ва амалий созламалар қўлланмаси."
    ),
    "body": """
<p>Ўзбекистон Республикасида 2026 йилги ислоҳ қилинган лотин алифбосига бўлган эҳтиёж ва қизиқиш тобора ошиб бормоқда. Янги алифбода аввалги икки белгили бирикмалар ўрнига битта яхлит ҳарфлар жорий этилди: <strong>Ş ş</strong> (аввалги <em>sh</em>), <strong>Ç ç</strong> (аввалги <em>ch</em>), <strong>Ğ ğ</strong> (аввалги <em>g‘</em>) ва <strong>Ö ö</strong> (аввалги <em>o‘</em>). Бу ислоҳот матнларни ихчамлаштириш, хатоликларни камайтириш ва дастурий таъминотларда қидирув тизимини осонлаштиришда улкан ютуқ бўлди.</p>

<p>Бироқ кўпчилик фойдаланувчиларда табиий савол туғилмоқда: <em>«Компьютер клавиатурасида ёки смартфонда бу ҳарфларни қандай қилиб осон ва тез териш мумкин?»</em> Стандарт инглизча QWERTY клавиатурасида ушбу ҳарфлар алоҳида клавиш сифатида мавжуд эмас. Қуйидаги батафсил қўлланмада Windows, macOS, Android ва iOS тизимларида янги ҳарфларни ҳеч қандай қийинчиликсиз теришнинг <strong>энг самарали 5 та усулини</strong> кўрсатиб берамиз.</p>

<hr />

<h2>1-усул: Microsoft Store’даги «O‘zbek alifbosi klaviaturasi» дастури (Тавсия этилади)</h2>

<p>Windows 10 ва Windows 11 фойдаланувчилари учун энг қулай ва замонавий ечимлардан бири — дастурчи <strong>Ryzen_b</strong> томонидан яратилган ва расмий Microsoft Store дўконига жойлаштирилган <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>«O‘zbek alifbosi klaviaturasi»</strong></a> ёрдамчи дастуридир.</p>

<p>Ушбу енгил дастур тизимда орқа фонда ишлайди ва одатий инглизча (ёки ўзбекча лотин) клавиатура тартибига махсус қисқа клавишлар (hotkeys) комбинациясини қўшади:</p>

<ul>
  <li><code>Alt + O</code> (ёки <code>Ctrl + O</code>) ➔ <strong>ö</strong> (катта ҳарф: <code>Alt + Shift + O</code> ➔ <strong>Ö</strong>)</li>
  <li><code>Alt + G</code> (ёки <code>Ctrl + G</code>) ➔ <strong>ğ</strong> (катта ҳарф: <code>Alt + Shift + G</code> ➔ <strong>Ğ</strong>)</li>
  <li><code>Alt + S</code> (ёки <code>Ctrl + S</code>) ➔ <strong>ş</strong> (катта ҳарф: <code>Alt + Shift + S</code> ➔ <strong>Ş</strong>)</li>
  <li><code>Alt + C</code> (ёки <code>Ctrl + C</code>) ➔ <strong>ç</strong> (катта ҳарф: <code>Alt + Shift + C</code> ➔ <strong>Ç</strong>)</li>
</ul>

<h3>Дастурнинг асосий афзалликлари:</h3>
<ol>
  <li><strong>Автоматик ишга тушиш:</strong> Компьютер ёқилиши билан Windows билан бирга фонда юкланади ва билдиришлар майдони (system tray)да қулай белги билан туради.</li>
  <li><strong>Ақлли тил назорати:</strong> Агар сиз клавиатура тилини Русча (кирилл) га алмаштирсангиз, дастур буни автоматик аниқлайди ва қисқа клавишларни вақтинча ўчириб туради. Лотинчага қайтганингизда эса яна дарҳол фаоллашади.</li>
  <li><strong>Хавфсиз ва тизимга дахлсиз:</strong> Регистр файлларини ёки тизим драйверларини ўзгартирмайди, компьютер тезлигига мутлақо таъсир қилмайди.</li>
  <li><strong>Расмий дўкон кафолати:</strong> Microsoft Store хавфсизлик текширувидан ўтганлиги сабабли вирус ёки зарарли кодлардан мутлақо холи.</li>
</ol>

<p>👉 <strong>Юклаб олиш ҳаволаси:</strong> <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store — O‘zbek alifbosi klaviaturasi</strong></a></p>

<hr />

<h2>2-усул: Қўшимча дастурсиз — Windows’да «Turkish Q» клавиатураси</h2>

<p>Агар сизда бегона, ишхона ёки ўқув маркази компьютери бўлиб, унга қўшимча дастур ўрнатиш ҳуқуқи (администратор пароли) бўлмаса, ажойиб содда ечим мавжуд: <strong>Туркча Q (Turkish Q)</strong> клавиатура тартибини қўшиш.</p>

<p>Чунки турк алифбосида ҳам айни шу ҳарфлар (<strong>Ş, Ç, Ö, Ğ</strong>) мавжуд бўлиб, улар клавиатуранинг ўнг томонидаги тиниш белгилари ўрнида жойлашган:</p>

<ul>
  <li><code>;</code> (нуқтали вергул) клавиши ➔ <strong>Ş ş</strong></li>
  <li><code>.</code> (нуқта) клавиши ➔ <strong>Ç ç</strong></li>
  <li><code>,</code> (вергул) клавиши ➔ <strong>Ö ö</strong></li>
  <li><code>[</code> (квадрат қавс) клавиши ➔ <strong>Ğ ğ</strong></li>
</ul>

<p>Қўшиш учун: Windows <em>Settings ➔ Time &amp; Language ➔ Language &amp; Region ➔ Language options ➔ Add a keyboard ➔ Turkish Q</em>.</p>

<hr />

<h2>3-усул: AltGr тизими ва мустақил клавиатура макетлари (MSKLC)</h2>
<p>Ўнгдаги <code>AltGr</code> тугмаси орқали <code>AltGr + S</code>, <code>AltGr + C</code>, <code>AltGr + G</code>, <code>AltGr + O</code> комбинациялари тизим буйруқларига халақит бермайди.</p>

<hr />

<h2>4-усул: Смартфонларда (Android ва iOS / iPhone) янги ҳарфларни териш</h2>
<ul>
  <li><strong>Босиб туриш (Long-press):</strong> Gboard ёки iOS клавиатурасида <code>S</code>, <code>C</code>, <code>G</code>, <code>O</code> ҳарфларини босиб турсангиз, <strong>Ş, Ç, Ğ, Ö</strong> ҳарфлари чиқади.</li>
  <li><strong>Туркча тил қўшиш:</strong> Телефон созламаларидан туркча тилни қўшиб қўйсангиз, ҳарфлар алоҳида тугма бўлиб кўриниб туради.</li>
</ul>

<hr />

<h2>5-усул: Катта матнларни бир зумда ўтказиш — Changetext ўгиргич</h2>
<p>Эски алифбода ёки кириллда ёзилган матнларни қўлда қайта териб чиқмасдан, <a href="https://complexprogrammer.uz/changetext/"><strong>Complex Programmer Changetext</strong></a> саҳифасида бир сонияда янги алифбога ўтказиб олишингиз мумкин.</p>

<hr />

<h2>Unicode кодлари жадвали</h2>
<table class="table table-bordered table-striped" style="width: 100%;">
  <thead>
    <tr style="background-color: #2c3e50; color: #ffffff;">
      <th style="padding: 10px;">Ҳарф</th>
      <th style="padding: 10px;">Unicode</th>
      <th style="padding: 10px;">Microsoft Store App</th>
      <th style="padding: 10px;">Turkish Q</th>
      <th style="padding: 10px;">AltGr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px;"><strong>Ş / ş</strong></td>
      <td style="padding: 10px;"><code>U+015E</code> / <code>U+015F</code></td>
      <td style="padding: 10px;"><code>Alt + S</code></td>
      <td style="padding: 10px;"><code>;</code></td>
      <td style="padding: 10px;"><code>AltGr + S</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ç / ç</strong></td>
      <td style="padding: 10px;"><code>U+00C7</code> / <code>U+00E7</code></td>
      <td style="padding: 10px;"><code>Alt + C</code></td>
      <td style="padding: 10px;"><code>.</code></td>
      <td style="padding: 10px;"><code>AltGr + C</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ğ / ğ</strong></td>
      <td style="padding: 10px;"><code>U+011E</code> / <code>U+011F</code></td>
      <td style="padding: 10px;"><code>Alt + G</code></td>
      <td style="padding: 10px;"><code>[</code></td>
      <td style="padding: 10px;"><code>AltGr + G</code></td>
    </tr>
    <tr>
      <td style="padding: 10px;"><strong>Ö / ö</strong></td>
      <td style="padding: 10px;"><code>U+00D6</code> / <code>U+00F6</code></td>
      <td style="padding: 10px;"><code>Alt + O</code></td>
      <td style="padding: 10px;"><code>,</code></td>
      <td style="padding: 10px;"><code>AltGr + O</code></td>
    </tr>
  </tbody>
</table>
""",
}

try:
    from django.core.management.base import BaseCommand, CommandError
except ImportError:
    class BaseCommand:
        pass
    class CommandError(Exception):
        pass


class Command(BaseCommand):
    help = "Yangi Özbek alifbosi klaviaturasi blog maqolasini naşr qiliş yoki yangilaş."

    def add_arguments(self, parser):
        parser.add_argument("--update", action="store_true", help="Mavjud maqola matnini yangilaş")
        parser.add_argument("--draft", action="store_true", help="Saytda körsatmasdan qoralama (2099-yil) sifatida saqlaş")
        parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmasdan tekşiriş")

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

        if not opts["dry_run"]:
            author = User.objects.filter(is_superuser=True).order_by("id").first()
            if not author:
                author = User.objects.order_by("id").first()
            if not author:
                raise CommandError("Muallif uçun birorta ham User topilmadi.")

            category = (
                Categories.objects.filter(name_uz_uz__icontains="texnolog", is_deleted=False).first()
                or Categories.objects.filter(name_uz_uz__icontains="dastur", is_deleted=False).first()
                or Categories.objects.filter(name_uz_uz__icontains="ilm", is_deleted=False).first()
                or Categories.objects.filter(is_deleted=False).first()
            )
        else:
            author = None
            category = None

        publish_time = DRAFT_TIME if opts["draft"] else timezone.now()

        image_full_path = os.path.join(settings.MEDIA_ROOT, IMAGE_REL_PATH)
        has_image = os.path.exists(image_full_path)
        if not has_image:
            self.stdout.write(self.style.WARNING(f"Ogohlantiriş: Rasm fayli topilmadi: {image_full_path}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Rasm biriktirildi: {IMAGE_REL_PATH}"))

        fields = {
            "name_uz_uz": ARTICLE_DATA["uz"]["name"].strip(),
            "title_uz_uz": ARTICLE_DATA["uz"]["title"].strip(),
            "body_uz_uz": ARTICLE_DATA["uz"]["body"].strip(),

            "name_uz_crl": CYR_DATA["name"].strip(),
            "title_uz_crl": CYR_DATA["title"].strip(),
            "body_uz_crl": CYR_DATA["body"].strip(),

            "name_ru_ru": ARTICLE_DATA["ru"]["name"].strip(),
            "title_ru_ru": ARTICLE_DATA["ru"]["title"].strip(),
            "body_ru_ru": ARTICLE_DATA["ru"]["body"].strip(),

            "name_en_us": ARTICLE_DATA["en"]["name"].strip(),
            "title_en_us": ARTICLE_DATA["en"]["title"].strip(),
            "body_en_us": ARTICLE_DATA["en"]["body"].strip(),

            "seo_title": SEO_TITLE[:70],
            "seo_description": SEO_DESCRIPTION[:200],
            "source_url": STORE_URL,
            "publish_time": publish_time,
            "image": IMAGE_REL_PATH if has_image else "",
        }

        post = Posts.objects.filter(slug=SLUG).first() if not opts["dry_run"] else None
        if post and not opts["update"]:
            self.stdout.write(self.style.WARNING(f"Maqola allaqaçon mavjud ({SLUG}). Yangilaş uçun --update parametrini bering."))
            self.stdout.write(f"Havola: https://complexprogrammer.uz/blog/{SLUG}/")
            return

        if opts["dry_run"]:
            self.stdout.write(self.style.SUCCESS(f"[DRY-RUN] Maqola tayyor: {fields['name_uz_uz']}"))
            self.stdout.write(f"Slug: {SLUG}")
            self.stdout.write(f"Rasm: {IMAGE_REL_PATH} (mavjud={has_image})")
            return

        if not post:
            post = Posts(slug=SLUG, created_by=author, categorie=category)
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

        try:
            cache.clear()
        except Exception:
            pass

        status_text = "Qoralama (2099-yil)" if opts["draft"] else "Naşr qilindi (jonli efirda)"
        self.stdout.write(self.style.SUCCESS("=" * 64))
        self.stdout.write(self.style.SUCCESS(f"✅ Maqola muvaffaqiyatli {action}!"))
        self.stdout.write(self.style.SUCCESS(f"📌 Holati: {status_text}"))
        self.stdout.write(self.style.SUCCESS(f"🖼 Rasm: {IMAGE_REL_PATH}"))
        self.stdout.write(self.style.SUCCESS(f"🔗 Saytdagi havola: https://complexprogrammer.uz/blog/{SLUG}/"))
        self.stdout.write(self.style.SUCCESS("=" * 64))
