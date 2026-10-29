"""Yangi Özbek alifbosi klaviaturasi mavzusidagi blog maqolasini naşr qiliş yoki yangilaş.

Işlatiş:
    python manage.py publish_keyboard_post           # darhol saytda naşr qiladi
    python manage.py publish_keyboard_post --update  # mavjud maqola matnini yangilaydi
    python manage.py publish_keyboard_post --draft   # qoralama qilib saqlaydi (2099-yil)
    python manage.py publish_keyboard_post --dry-run # bazaga yozmasdan tekşiradi
"""

import datetime
import os
import threading
import time

SLUG = "yangi-ozbek-alifbosi-klaviaturasi"
IMAGE_REL_PATH = "post/images/yangi_ozbek_alifbosi_klaviaturasi.jpg"
SOURCE_URL = "https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM"
DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)

SEO_TITLE = "Yangi Özbek alifbosi klaviaturasi — Ö, Ğ, Ş, Ç harflarini yoziş"
SEO_DESCRIPTION = "Windows, Android va iOS-da yangi özbek alifbosi (Ö, Ğ, Ş, Ç) harflarini klaviaturada qulay yoziş: Microsoft Store ilovasi, Turkish Q va tezkor tugmalar."

ARTICLE_DATA = {
    # ==========================================================================
    # UZ_UZ (2026-yilgi yangi Lotin alifbosi — qat'iy Ş, Ç, Ğ, Ö harflarida)
    # ==========================================================================
    "uz": {
        "name": "Yangi Özbek alifbosi klaviaturasi — Ö, Ğ, Ş, Ç harflarini kompyuter va telefonda oson yoziş qöllanmasi",
        "title": "Microsoft Store ilovasi («O'zbek alifbosi klaviaturasi»), Windows Turkish Q tartibi, tezkor Alt/Ctrl tugmalari, mobil klaviatura va onlayn ögirgiç imkoniyatlari.",
        "body": """
<p>Özbekiston Respublikasida 2026-yilda töliq joriy etilayotgan isloh qilingan yangi lotin alifbosi yozuvimizni yanada ixçam, aniq va xalqaro standartlarga mos holatga keltirdi. Amaldagi 1995-yilgi alifbodagi noqulay ikki belgili birikmalar (<code>sh</code>, <code>ch</code>) hamda teskari vergul bilan yoziladigan harflar (<code>o'</code>, <code>g'</code>) yozuv jarayonini sekinlaştirar, matnlarni qidiruv tizimlarida (SEO) indekslaşda va ma'lumotlar bazalarida chalkaşliklar keltirib chiqarar edi.</p>

<p>Yangi alifboda bu tovuşlar bitta yaxlit harfga aylantirildi: <strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>. Ammo köpçilik foydalanuvçilarda haqli savol tuğiladi: <em>«Standart inglizça QWERTY klaviaturalarida bu harflar yöq-ku, ularni kompyuterda va telefonda qanday qilib tez va qulay yoziş mumkin?»</em></p>

<p>Uşbu maqolada Windows kompyuterlari, noutbuklar hamda smartfonlarda yangi alifbo harflarini heç qanday qiyinçiliksiz yozişning eng sinalgan va samarali 5 ta usulini batafsil körsatib beramiz.</p>

<hr>

<h2>1-usul: Microsoft Store rasmiy ilovasi — «O'zbek alifbosi klaviaturasi» (Tavsiya etiladi)</h2>
<p>Windows 10 va Windows 11 foydalanuvçilari uçun dasturçi <strong>Ryzen_b</strong> tomonidan yaratilgan va Microsoft Store rasmiy dökoniga joylangan <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>«O'zbek alifbosi klaviaturasi»</strong></a> ilovasi ayni muddao.</p>

<div style="background: rgba(14, 165, 233, 0.08); border-left: 4px solid #0ea5e9; padding: 14px 18px; margin: 18px 0; border-radius: 6px;">
  <strong>Ilovaning asosiy qulayliklari:</strong>
  <ul style="margin-bottom: 0;">
    <li><strong>Tezkor tugmalar (Hotkeys):</strong> Klaviaturadagi <code>Alt</code> tugmasini bosib turgan holda harflarni bosiş kifoya:
      <ul>
        <li><code>Alt + O</code> ➔ <strong>ö</strong> (katta harf uçun: <code>Shift + Alt + O</code> ➔ <strong>Ö</strong>)</li>
        <li><code>Alt + G</code> ➔ <strong>ğ</strong> (katta harf uçun: <code>Shift + Alt + G</code> ➔ <strong>Ğ</strong>)</li>
        <li><code>Alt + S</code> ➔ <strong>ş</strong> (katta harf uçun: <code>Shift + Alt + S</code> ➔ <strong>Ş</strong>)</li>
        <li><code>Alt + C</code> ➔ <strong>ç</strong> (katta harf uçun: <code>Shift + Alt + C</code> ➔ <strong>Ç</strong>)</li>
      </ul>
    </li>
    <li><strong>Moslaşuvçan sozlamalar:</strong> Modifikator tugmasini xohişingizga köra <code>Alt</code>, <code>Ctrl</code> yoki <code>Ctrl + Shift</code> kombinatsiyasiga almaştirişingiz mumkin.</li>
    <li><strong>Windows bilan birga işga tuşiş:</strong> Tizim yoqilganda dastur avtomatik fonda (Tray bölimida) ishga tuşadi va kompyuter xotirasini deyarli band qilmaydi.</li>
    <li><strong>Kirill alifbosini aqlli aniqlaş:</strong> Rusça yoki özbekça kirill klaviaturasida yozayotganingizda dastur buni avtomatik sezadi va xalaqit bermaydi.</li>
  </ul>
</div>

<p><strong>Örnatiş tartibi:</strong></p>
<ol>
  <li>Microsoft Store rasmiy sahifasiga öting: <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store — O'zbek alifbosi klaviaturasi</strong></a></li>
  <li><strong>«Get in Store app»</strong> yoki <strong>«Install»</strong> tugmasini bosing.</li>
  <li>Dastur örnatilgach, uni ishga tuşiring. Endi istalgan dasturda (Word, brauzer, Telegram) bemalol <code>Alt+O</code>, <code>Alt+G</code>, <code>Alt+S</code>, <code>Alt+C</code> orqali yangi harflarni yoza olasiz!</li>
</ol>

<p style="text-align: center; margin: 25px 0;">
  <a class="b-btn" href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener" style="display: inline-block; padding: 12px 26px; font-size: 16px; font-weight: bold; background: #0078d4; color: #fff; text-decoration: none; border-radius: 8px;">
    📥 Microsoft Store orqali yuklab oliş
  </a>
</p>

<hr>

<h2>2-usul: Windows sozlamalarida «Turkish Q» tartibini ulab qöyiş (Ilovasiz usul)</h2>
<p>Agar kompyuteringizga qöşimça heç qanday dastur örnatishni istamasangiz, Windows tizimining ichki imkoniyatidan foydalanişingiz mumkin. Turk alifbosida ham ayni şu to'rt harf (<strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>) mavjud bölib, ular jismoniy klaviaturaning chetki qismlariga joylashtirilgan:</p>

<table class="table table-bordered table-striped" style="width: 100%; margin: 16px 0; border-collapse: collapse;">
  <thead>
    <tr style="background: rgba(14, 165, 233, 0.15);">
      <th style="padding: 10px; border: 1px solid #ddd;">Klaviatura tugmasi</th>
      <th style="padding: 10px; border: 1px solid #ddd;">Keltirib chiqaradigan harf</th>
      <th style="padding: 10px; border: 1px solid #ddd;">Shift bilan (Katta harf)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>[ ; ]</code> (Nuqtali vergul tugmasi)</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>ş</strong></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>Ş</strong></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>[ ' ]</code> (Yakka tirnoq tugmasi)</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>ö</strong></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>Ö</strong></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>[ . ]</code> (Nuqta tugmasi / ç)</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>ç</strong></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>Ç</strong></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>[ ] ]</code> (Yopiluvchi burchak qavs)</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>ğ</strong></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><strong>Ğ</strong></td>
    </tr>
  </tbody>
</table>

<p><strong>Windows-da sozlash qadamlari:</strong></p>
<ol>
  <li>Windows <strong>Settings</strong> (Sozlamalar) ➔ <strong>Time &amp; Language</strong> (Vaqt va til) bölimiga kiring.</li>
  <li><strong>Language &amp; Region</strong> (Til va mintaqa) bandini tanlang.</li>
  <li>Özbek tili yonidagi uch nuqtani bosib, <strong>Language options</strong> ➔ <strong>Add a keyboard</strong> (Klaviatura qöşiş) tugmasini bosing va röyxatdan <strong>Turkish Q</strong> ni tanlang (yoki alohida turk tilini qöşimça til qilib qöşing).</li>
  <li>Endi <code>Win + Space</code> yoki <code>Alt + Shift</code> orqali ushbu tartibga ötib, yangi harflarni birgina tugma orqali bemalol terishingiz mumkin.</li>
</ol>

<hr>

<h2>3-usul: MSKLC orqali tayyorlangan maxsus tartiblar (Rahim Sadiy, Tezyechim)</h2>
<p>Klaviatura ishlab chiquvchilari (masalan, Rahim Sadiy va Tezyechim loyihalari) tomonidan Microsoft Keyboard Layout Creator yordamida maxsus <code>.msi</code> installyatorlar tayyorlangan. Ushbu tartiblarda klaviaturadagi öng <strong>AltGr</strong> tugmasi orqali harflar teriladi:</p>
<ul>
  <li><code>AltGr + O</code> ➔ <strong>ö</strong> (yoki <code>Shift + AltGr + O</code> ➔ <strong>Ö</strong>)</li>
  <li><code>AltGr + G</code> ➔ <strong>ğ</strong> (yoki <code>Shift + AltGr + G</code> ➔ <strong>Ğ</strong>)</li>
  <li><code>AltGr + S</code> ➔ <strong>ş</strong> (yoki <code>Shift + AltGr + S</code> ➔ <strong>Ş</strong>)</li>
  <li><code>AltGr + C</code> ➔ <strong>ç</strong> (yoki <code>Shift + AltGr + C</code> ➔ <strong>Ç</strong>)</li>
</ul>
<p>Bu usul standart inglizcha tugmalar joylashuviga mutlaqo teginmaydi, faqat öngdagi Alt tugmasiga qöşimça funksiya yuklaydi.</p>

<hr>

<h2>4-usul: Smartfonlarda yoziş (Android va iOS)</h2>
<p>Smartfonlarda yangi harflarni kiritish yanada oson va heç qanday ilova örnatishni talab etmaydi:</p>

<h3>Android (Google Gboard va Samsung Keyboard):</h3>
<ul>
  <li><strong>Bosib turish (Long-press):</strong> Klaviaturadagi asosiy harf ustiga barmoğingizni 0.5 soniya bosib tursangiz, uning diakritik variantlari menyusi ochiladi:
    <ul>
      <li><code>O</code> ustiga bosib tursangiz ➔ <strong>ö</strong></li>
      <li><code>G</code> ustiga bosib tursangiz ➔ <strong>ğ</strong></li>
      <li><code>S</code> ustiga bosib tursangiz ➔ <strong>ş</strong></li>
      <li><code>C</code> ustiga bosib tursangiz ➔ <strong>ç</strong></li>
    </ul>
  </li>
  <li><strong>Klaviatura sozlamasi:</strong> Gboard sozlamalaridan til bölimiga kirib, «Özbekça (Lotin)» klaviaturasini tanlang va u yerda belgilarni uzoq bosish imkoniyatini yoqib qöying.</li>
</ul>

<h3>iPhone va iPad (Apple iOS):</h3>
<ul>
  <li>iOS klaviaturasida ham xuddi shunday: <code>O</code>, <code>G</code>, <code>S</code>, <code>C</code> harflarini bosib turganda tepasida muqobil harflar paydo böladi.</li>
  <li>Shuningdek, iOS sozlamalarida <em>Turkish</em> (Turkcha) klaviaturasini ulab qöysangiz, pastki qatorda <strong>ş</strong>, <strong>ç</strong>, <strong>ö</strong>, <strong>ğ</strong> harflari alohida tugmaça bölib doimiy körinib turadi.</li>
</ul>

<hr>

<h2>5-usul: Mavjud hujjatlarni yangi alifboga ögirish — Complex Programmer Changetext</h2>
<p>Agar sizda avvaldan yozilgan katta hajmdagi matnlar, maqolalar, referatlar, Word yoki .txt fayllar bölsa, ularni qo'lda bittalab tahrirlab chiquşga aslo hojat yöq!</p>

<p>Bizning saytimizda maxsus ishlab chiqilgan <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Lotin-Kirill matn ögirgiçi</strong></a> orqali birgina harakat bilan butun matnni 2026-yilgi yangi alifboga xatosiz ötkazishingiz mumkin:</p>

<ul>
  <li>Eski lotindagi <code>sh</code>, <code>ch</code>, <code>o'</code>, <code>g'</code> birikmalarini avtomatik <strong>ş, ç, ö, ğ</strong> harflariga almaştiradi;</li>
  <li>Kirilldagi <code>ш</code>, <code>ч</code>, <code>ў</code>, <code>ғ</code> tovuşlarini ham to'g'ri yangi lotin harflariga aylantiradi;</li>
  <li>Havolalar (<code>https://...</code>), <code>@username</code> lar, HTML kodlar va inglizcha dasturlash atamalariga zarar yetkazmaydi;</li>
  <li>Tayyor matnni bir bosişda nusxalab olish yoki <code>.txt</code> formatida yuklab olish mumkin.</li>
</ul>

<p style="text-align: center; margin: 25px 0;">
  <a class="b-btn" href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener" style="display: inline-block; padding: 12px 26px; font-size: 16px; font-weight: bold; background: #059669; color: #fff; text-decoration: none; border-radius: 8px;">
    🚀 Matnni yangi alifboga ögirish (changetext)
  </a>
</p>

<hr>

<h2>Unicode, Alt-kodlar va HTML obyektlar jadvali</h2>
<p>Dasturçilar, matn teruvçilar va veb-ustalar uçun yangi harflarning xalqaro kodlash standartlari:</p>

<table class="table table-bordered table-striped" style="width: 100%; margin: 16px 0; border-collapse: collapse;">
  <thead>
    <tr style="background: rgba(14, 165, 233, 0.15);">
      <th style="padding: 10px; border: 1px solid #ddd;">Harf</th>
      <th style="padding: 10px; border: 1px solid #ddd;">Nomi</th>
      <th style="padding: 10px; border: 1px solid #ddd;">Unicode</th>
      <th style="padding: 10px; border: 1px solid #ddd;">Windows Alt-kod</th>
      <th style="padding: 10px; border: 1px solid #ddd;">HTML kodi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd; font-size: 18px; font-weight: bold;">Ö / ö</td>
      <td style="padding: 8px; border: 1px solid #ddd;">O with diaeresis (umlaüt)</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>U+00D6</code> / <code>U+00F6</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>Alt + 0214</code> / <code>Alt + 0246</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>&amp;Ouml;</code> / <code>&amp;ouml;</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd; font-size: 18px; font-weight: bold;">Ğ / ğ</td>
      <td style="padding: 8px; border: 1px solid #ddd;">G with breve</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>U+011E</code> / <code>U+011F</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>Alt + 0286</code> / <code>Alt + 0287</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>&amp;#286;</code> / <code>&amp;#287;</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd; font-size: 18px; font-weight: bold;">Ş / ş</td>
      <td style="padding: 8px; border: 1px solid #ddd;">S with cedilla</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>U+015E</code> / <code>U+015F</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>Alt + 0350</code> / <code>Alt + 0351</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>&amp;#350;</code> / <code>&amp;#351;</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd; font-size: 18px; font-weight: bold;">Ç / ç</td>
      <td style="padding: 8px; border: 1px solid #ddd;">C with cedilla</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>U+00C7</code> / <code>U+00E7</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>Alt + 0199</code> / <code>Alt + 0231</code></td>
      <td style="padding: 8px; border: 1px solid #ddd;"><code>&amp;Ccedil;</code> / <code>&amp;ccedil;</code></td>
    </tr>
  </tbody>
</table>

<hr>

<h2>Xulosa va tavsiyalar</h2>
<p>Yangi alifboga ötiş yozuv madaniyatimizni yangi bosqichga olib chiqadi. Har kuni kompyuterda matn bilan ishlaydigan mutaxassislar uçun <strong>Microsoft Store ilovasi</strong> eng qulay va tezkor yechimdir. Smartfonda esa uzoq bosish yoki turkcha klaviatura orqali yozish tavsiya etiladi.</p>

<p>Katta hajmdagi eski matnlaringizni bir lahzada yangi alifboga ötkazish uçun esa har doim <a href="https://complexprogrammer.uz/changetext/"><strong>Complex Programmer Changetext</strong></a> xizmatidan bepul foydalanishingiz mumkin!</p>
""",
    },

    # ==========================================================================
    # UZ_CRL (Ўзбек тили — Кирилл алифбосида)
    # ==========================================================================
    "uz_crl": {
        "name": "Янги Ўзбек алифбоси клавиатураси — Ö, Ğ, Ş, Ç ҳарфларини компьютер ва телефонда осон ёзиш қўлланмаси",
        "title": "Microsoft Store иловаси («O'zbek alifbosi klaviaturasi»), Windows Turkish Q тартиби, тезкор Alt/Ctrl тугмалари, мобил клавиатура ва онлайн ўгиргич имкониятлари.",
        "body": """
<p>Ўзбекистон Республикасида 2026 йилда тўлиқ жорий этилаётган ислоҳ қилинган янги лотин алифбоси ёзувимизни янада ихчам, аниқ ва халқаро стандартларга мос ҳолатга келтирди. Амалдаги 1995 йилги алифбодаги ноқулай икки белгили бирикмалар (<code>sh</code>, <code>ch</code>) ҳамда тескари вергул билан ёзиладиган ҳарфлар (<code>o'</code>, <code>g'</code>) ёзув жараёнини секинлаштирар, матнларни қидирув тизимларида (SEO) индексация қилишда чалкашликлар келтириб чиқарар эди.</p>

<p>Янги алифбода бу товушлар битта яхлит ҳарфга айлантирилди: <strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>. Аммо кўпчилик фойдаланувчиларда ҳақли савол туғилади: <em>«Стандарт инглизча QWERTY клавиатураларида бу ҳарфлар йўқ-ку, уларни компьютерда ва телефонда қандай қилиб тез ва қулай ёзиш мумкин?»</em></p>

<p>Ушбу мақолада Windows компьютерлари, ноутбуклар ҳамда смартфонларда янги алифбо ҳарфларини ҳеч қандай қийинчиликсиз ёзишнинг энг синалган ва самарали 5 та усулини батафсил кўрсатиб берамиз.</p>

<hr>

<h2>1-усул: Microsoft Store расмий иловаси — «O'zbek alifbosi klaviaturasi» (Тавсия этилади)</h2>
<p>Windows 10 ва Windows 11 фойдаланувчилари учун дастурчи <strong>Ryzen_b</strong> томонидан яратилган ва Microsoft Store расмий дўконига жойланган <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>«O'zbek alifbosi klaviaturasi»</strong></a> иловаси айни муддао.</p>

<div style="background: rgba(14, 165, 233, 0.08); border-left: 4px solid #0ea5e9; padding: 14px 18px; margin: 18px 0; border-radius: 6px;">
  <strong>Илованинг асосий қулайликлари:</strong>
  <ul style="margin-bottom: 0;">
    <li><strong>Тезкор тугмалар (Hotkeys):</strong> Клавиатурадаги <code>Alt</code> тугмасини босиб турган ҳолда ҳарфларни босиш кифоя:
      <ul>
        <li><code>Alt + O</code> ➔ <strong>ö</strong> (катта ҳарф учун: <code>Shift + Alt + O</code> ➔ <strong>Ö</strong>)</li>
        <li><code>Alt + G</code> ➔ <strong>ğ</strong> (катта ҳарф учун: <code>Shift + Alt + G</code> ➔ <strong>Ğ</strong>)</li>
        <li><code>Alt + S</code> ➔ <strong>ş</strong> (катта ҳарф учун: <code>Shift + Alt + S</code> ➔ <strong>Ş</strong>)</li>
        <li><code>Alt + C</code> ➔ <strong>ç</strong> (катта ҳарф учун: <code>Shift + Alt + C</code> ➔ <strong>Ç</strong>)</li>
      </ul>
    </li>
    <li><strong>Мослашувчан созламалар:</strong> Модификатор тугмасини хоҳишингизга кўра <code>Alt</code>, <code>Ctrl</code> ёки <code>Ctrl + Shift</code> комбинациясига алмаштиришингиз мумкин.</li>
    <li><strong>Windows билан бирга ишга тушиш:</strong> Тизим ёқилганда дастур автоматик фонда ишга тушади ва компьютер хотирасини деярли банд қилмайди.</li>
    <li><strong>Кирилл алифбосини ақлли аниқлаш:</strong> Русча ёки ўзбекча кирилл клавиатурасида ёзаётганингизда дастур буни автоматик сезади ва халақит бермайди.</li>
  </ul>
</div>

<p><strong>Ўрнатиш тартиби:</strong></p>
<ol>
  <li>Microsoft Store расмий саҳифасига ўтинг: <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store — O'zbek alifbosi klaviaturasi</strong></a></li>
  <li><strong>«Get in Store app»</strong> ёки <strong>«Install»</strong> тугмасини босинг.</li>
  <li>Дастур ўрнатилгач, уни ишга туширинг. Энди исталган дастурда (Word, браузер, Telegram) бемалол <code>Alt+O</code>, <code>Alt+G</code>, <code>Alt+S</code>, <code>Alt+C</code> орқали янги ҳарфларни ёза оласиз!</li>
</ol>

<hr>

<h2>2-усул: Windows созламаларида «Turkish Q» тартибини улаб қўйиш (Иловасиз усул)</h2>
<p>Агар компьютерингизга қўшимча ҳеч қандай дастур ўрнатишни истамасангиз, Windows тизимининг ички имкониятидан фойдаланишингиз мумкин. Турк алифбосида ҳам айни шу тўрт ҳарф (<strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>) мавжуд бўлиб, улар клавиатуранинг четки тугмаларига жойлаштирилган:</p>

<ul>
  <li><code>[ ; ]</code> (Нуқтали вергул) ➔ <strong>ş</strong> (Shift билан: <strong>Ş</strong>)</li>
  <li><code>[ ' ]</code> (Якка тирноқ) ➔ <strong>ö</strong> (Shift билан: <strong>Ö</strong>)</li>
  <li><code>[ . ]</code> (Нуқта) ➔ <strong>ç</strong> (Shift билан: <strong>Ç</strong>)</li>
  <li><code>[ ] ]</code> (Ёпилувчи бурчак қавс) ➔ <strong>ğ</strong> (Shift билан: <strong>Ğ</strong>)</li>
</ul>

<p><strong>Windows-да созлаш қадамлари:</strong></p>
<ol>
  <li>Windows <strong>Settings</strong> ➔ <strong>Time &amp; Language</strong> ➔ <strong>Language &amp; Region</strong> бўлимига киринг.</li>
  <li>Ўзбек тили ёнидаги уч нуқтани босиб, <strong>Language options</strong> ➔ <strong>Add a keyboard</strong> тугмасини босинг ва рўйхатдан <strong>Turkish Q</strong> ни танланг.</li>
  <li>Энди <code>Win + Space</code> ёки <code>Alt + Shift</code> орқали ушбу тартибга ўтиб, янги ҳарфларни бемалол теришингиз мумкин.</li>
</ol>

<hr>

<h2>3-усул: Смартфонларда ёзиш (Android ва iOS)</h2>
<p>Смартфонларда янги ҳарфларни киритиш ҳеч қандай илова ўрнатишни талаб этмайди:</p>
<ul>
  <li><strong>Android (Gboard ва Samsung Keyboard):</strong> Клавиатурадаги асосий ҳарф (<code>O</code>, <code>G</code>, <code>S</code>, <code>C</code>) устига бармоғингизни 0.5 сония босиб турсангиз, устида <strong>ö</strong>, <strong>ğ</strong>, <strong>ş</strong>, <strong>ç</strong> ҳарфлари пайдо бўлади.</li>
  <li><strong>iPhone ва iPad (Apple iOS):</strong> Худди шундай, ҳарфни босиб туриш орқали керакли белгини танлашингиз ёки қўшимча <em>Turkish</em> клавиатурасини қўшиб олишингиз мумкин.</li>
</ul>

<hr>

<h2>4-усул: Мавжуд матнларни янги алифбога ўгириш — Changetext онлайн хизмати</h2>
<p>Агар сизда аввалдан ёзилган катта ҳажмдаги ҳужжатлар бўлса, уларни қўлда битталаб таҳрирлаб чиқиш шарт эмас. Saytimizdagi <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Лотин-Кирилл ўгиргичи</strong></a> орқали бир зумда бутун матнни янги 2026 йилги алифбога хатосиз ўтказа оласиз.</p>

<p style="text-align: center; margin: 25px 0;">
  <a class="b-btn" href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener" style="display: inline-block; padding: 12px 26px; font-size: 16px; font-weight: bold; background: #059669; color: #fff; text-decoration: none; border-radius: 8px;">
    🚀 Матнни янги алифбога ўгириш (changetext)
  </a>
</p>
""",
    },

    # ==========================================================================
    # RU_RU (Русский язык)
    # ==========================================================================
    "ru": {
        "name": "Клавиатура нового узбекского алфавита: как легко печатать буквы Ö, Ğ, Ş, Ç на компьютере и смартфоне",
        "title": "Полное руководство: официальное приложение из Microsoft Store («O'zbek alifbosi klaviaturasi»), турецкая раскладка Turkish Q, горячие клавиши Alt/Ctrl, ввод на Android/iOS и онлайн-конвертер.",
        "body": """
<p>В рамках реформы узбекского латинского алфавита 2026 года привычные двухбуквенные сочетания (<code>sh</code>, <code>ch</code>) и буквы с перевернутым апострофом (<code>o'</code>, <code>g'</code>) заменены на удобные монолитные буквы с диакритическими знаками: <strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>.</p>

<p>Это новшество значительно упрощает правила правописания и ускоряет набор текста, однако на стандартных англоязычных клавиатурах QWERTY таких клавиш нет. В этом практическом руководстве мы собрали 5 проверенных способов быстрого и комфортного набора новых букв на Windows, Android и iOS.</p>

<hr>

<h2>Способ 1: Официальное приложение из Microsoft Store — «O'zbek alifbosi klaviaturasi» (Рекомендуется)</h2>
<p>Для пользователей Windows 10 и Windows 11 разработчик <strong>Ryzen_b</strong> создал легкую и удобную утилиту, официально доступную в <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store — O'zbek alifbosi klaviaturasi</strong></a>.</p>

<div style="background: rgba(14, 165, 233, 0.08); border-left: 4px solid #0ea5e9; padding: 14px 18px; margin: 18px 0; border-radius: 6px;">
  <strong>Ключевые преимущества утилиты:</strong>
  <ul style="margin-bottom: 0;">
    <li><strong>Быстрые комбинации (Hotkeys):</strong> Нажатие <code>Alt</code> вместе с базовой буквой мгновенно вставляет нужный символ:
      <ul>
        <li><code>Alt + O</code> ➔ <strong>ö</strong> (заглавная: <code>Shift + Alt + O</code> ➔ <strong>Ö</strong>)</li>
        <li><code>Alt + G</code> ➔ <strong>ğ</strong> (заглавная: <code>Shift + Alt + G</code> ➔ <strong>Ğ</strong>)</li>
        <li><code>Alt + S</code> ➔ <strong>ş</strong> (заглавная: <code>Shift + Alt + S</code> ➔ <strong>Ş</strong>)</li>
        <li><code>Alt + C</code> ➔ <strong>ç</strong> (заглавная: <code>Shift + Alt + C</code> ➔ <strong>Ç</strong>)</li>
      </ul>
    </li>
    <li><strong>Настраиваемые модификаторы:</strong> Вместо <code>Alt</code> можно назначить <code>Ctrl</code> или <code>Ctrl + Shift</code>.</li>
    <li><strong>Автозапуск с Windows:</strong> Программа сворачивается в системный трей и потребляет минимум ресурсов.</li>
    <li><strong>Умная кириллица:</strong> При переключении на русский или узбекский кириллический ввод утилита не мешает набору.</li>
  </ul>
</div>

<p style="text-align: center; margin: 25px 0;">
  <a class="b-btn" href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener" style="display: inline-block; padding: 12px 26px; font-size: 16px; font-weight: bold; background: #0078d4; color: #fff; text-decoration: none; border-radius: 8px;">
    📥 Скачать в Microsoft Store
  </a>
</p>

<hr>

<h2>Способ 2: Раскладка «Turkish Q» в параметрах Windows (Без сторонних программ)</h2>
<p>В турецком алфавите используются ровно те же четыре буквы (<strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>). Включив раскладку <strong>Turkish Q</strong> в настройках Windows, вы получаете прямой доступ к этим буквам на физических клавишах:</p>
<ul>
  <li><code>[ ; ]</code> (Точка с запятой) ➔ <strong>ş</strong> (с Shift: <strong>Ş</strong>)</li>
  <li><code>[ ' ]</code> (Одинарная кавычка) ➔ <strong>ö</strong> (с Shift: <strong>Ö</strong>)</li>
  <li><code>[ . ]</code> (Точка) ➔ <strong>ç</strong> (с Shift: <strong>Ç</strong>)</li>
  <li><code>[ ] ]</code> (Закрывающая квадратная скобка) ➔ <strong>ğ</strong> (с Shift: <strong>Ğ</strong>)</li>
</ul>

<p><strong>Как включить:</strong> Перейдите в <em>Параметры Windows ➔ Время и язык ➔ Язык и регион</em>, выберите параметры языка и добавьте клавиатуру «Turkish Q».</p>

<hr>

<h2>Способ 3: Ввод на смартфонах (Android и iOS)</h2>
<ul>
  <li><strong>Долгое нажатие (Long-press):</strong> Удерживайте пальцем букву <code>O</code>, <code>G</code>, <code>S</code> или <code>C</code> на экранной клавиатуре Gboard, Samsung Keyboard или iOS, чтобы открыть всплывающее меню с символами <strong>ö</strong>, <strong>ğ</strong>, <strong>ş</strong>, <strong>ç</strong>.</li>
  <li><strong>Второй язык:</strong> Можно также добавить турецкую раскладку в настройках клавиатуры телефона для вынесения букв на отдельные клавиши.</li>
</ul>

<hr>

<h2>Способ 4: Быстрая конвертация готовых текстов — Changetext</h2>
<p>Если вам нужно перевести существующие документы, статьи или базы данных на новый алфавит 2026 года, воспользуйтесь бесплатным сервисом <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Changetext</strong></a>. Он автоматически заменяет диграфы, сохраняя ссылки, программный код и форматирование.</p>

<p style="text-align: center; margin: 25px 0;">
  <a class="b-btn" href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener" style="display: inline-block; padding: 12px 26px; font-size: 16px; font-weight: bold; background: #059669; color: #fff; text-decoration: none; border-radius: 8px;">
    🚀 Онлайн-конвертер текста (changetext)
  </a>
</p>
""",
    },

    # ==========================================================================
    # EN_US (English language)
    # ==========================================================================
    "en": {
        "name": "New Uzbek Alphabet Keyboard Guide: How to Type Ö, Ğ, Ş, Ç on Windows, Android, and iOS",
        "title": "Comprehensive tutorial: official Microsoft Store utility («O'zbek alifbosi klaviaturasi»), Windows Turkish Q layout, Alt/Ctrl hotkeys, mobile typing, and online text converter.",
        "body": """
<p>As part of Uzbekistan's 2026 Latin alphabet reform, digraphs and apostrophe-based letters (<code>sh</code>, <code>ch</code>, <code>o'</code>, <code>g'</code>) have been officially replaced by concise diacritical characters: <strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>.</p>

<p>While this streamlines spelling and digital search indexing, standard physical QWERTY keyboards lack dedicated keys for these letters. Below is a practical guide covering the top 5 methods to type the new Uzbek letters effortlessly across all devices.</p>

<hr>

<h2>Method 1: Official Microsoft Store App — «O'zbek alifbosi klaviaturasi» (Recommended)</h2>
<p>For Windows 10 and 11, developer <strong>Ryzen_b</strong> published a dedicated, lightweight utility available in the <a href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener"><strong>Microsoft Store — O'zbek alifbosi klaviaturasi</strong></a>.</p>

<div style="background: rgba(14, 165, 233, 0.08); border-left: 4px solid #0ea5e9; padding: 14px 18px; margin: 18px 0; border-radius: 6px;">
  <strong>Key Features:</strong>
  <ul style="margin-bottom: 0;">
    <li><strong>Fast Hotkeys:</strong> Press and hold <code>Alt</code> and tap the letter:
      <ul>
        <li><code>Alt + O</code> ➔ <strong>ö</strong> (Uppercase: <code>Shift + Alt + O</code> ➔ <strong>Ö</strong>)</li>
        <li><code>Alt + G</code> ➔ <strong>ğ</strong> (Uppercase: <code>Shift + Alt + G</code> ➔ <strong>Ğ</strong>)</li>
        <li><code>Alt + S</code> ➔ <strong>ş</strong> (Uppercase: <code>Shift + Alt + S</code> ➔ <strong>Ş</strong>)</li>
        <li><code>Alt + C</code> ➔ <strong>ç</strong> (Uppercase: <code>Shift + Alt + C</code> ➔ <strong>Ç</strong>)</li>
      </ul>
    </li>
    <li><strong>Customizable Modifiers:</strong> Switch hotkeys to <code>Ctrl</code> or <code>Ctrl + Shift</code> based on personal workflow.</li>
    <li><strong>Auto-start with Windows:</strong> Sits unobtrusively in the system tray with negligible memory footprint.</li>
    <li><strong>Cyrillic Auto-detection:</strong> Recognizes when you are typing in Cyrillic layouts and stays out of the way.</li>
  </ul>
</div>

<p style="text-align: center; margin: 25px 0;">
  <a class="b-btn" href="https://apps.microsoft.com/detail/9pb51j83gqtd?hl=en-US&gl=TM" target="_blank" rel="noopener" style="display: inline-block; padding: 12px 26px; font-size: 16px; font-weight: bold; background: #0078d4; color: #fff; text-decoration: none; border-radius: 8px;">
    📥 Install via Microsoft Store
  </a>
</p>

<hr>

<h2>Method 2: Windows Native «Turkish Q» Layout (No Extra Software)</h2>
<p>The Turkish alphabet features the exact same four characters (<strong>Ö ö, Ğ ğ, Ş ş, Ç ç</strong>). Adding the <strong>Turkish Q</strong> layout in Windows Settings maps them directly to peripheral keys:</p>
<ul>
  <li><code>[ ; ]</code> (Semicolon) ➔ <strong>ş</strong> (with Shift: <strong>Ş</strong>)</li>
  <li><code>[ ' ]</code> (Single Quote) ➔ <strong>ö</strong> (with Shift: <strong>Ö</strong>)</li>
  <li><code>[ . ]</code> (Period) ➔ <strong>ç</strong> (with Shift: <strong>Ç</strong>)</li>
  <li><code>[ ] ]</code> (Closing Bracket) ➔ <strong>ğ</strong> (with Shift: <strong>Ğ</strong>)</li>
</ul>

<p><strong>Setup:</strong> Go to <em>Windows Settings ➔ Time &amp; Language ➔ Language &amp; Region</em>, and add the Turkish Q keyboard layout.</p>

<hr>

<h2>Method 3: Mobile Devices (Android and iOS)</h2>
<ul>
  <li><strong>Long-press:</strong> Simply press and hold the base letters (<code>O</code>, <code>G</code>, <code>S</code>, <code>C</code>) on Gboard, Samsung Keyboard, or Apple iOS to reveal diacritical alternatives (<strong>ö</strong>, <strong>ğ</strong>, <strong>ş</strong>, <strong>ç</strong>).</li>
  <li><strong>Secondary Keyboard:</strong> Adding Turkish as an additional typing language provides dedicated on-screen keys.</li>
</ul>

<hr>

<h2>Method 4: Convert Existing Documents via Changetext</h2>
<p>Instead of manually editing legacy texts, use the free <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Changetext Converter</strong></a>. It converts entire articles, books, and documents into the reformed 2026 Latin alphabet while safeguarding web links, code blocks, and usernames.</p>

<p style="text-align: center; margin: 25px 0;">
  <a class="b-btn" href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener" style="display: inline-block; padding: 12px 26px; font-size: 16px; font-weight: bold; background: #059669; color: #fff; text-decoration: none; border-radius: 8px;">
    🚀 Open Online Text Converter (changetext)
  </a>
</p>
""",
    },
}


try:
    from django.core.management.base import BaseCommand, CommandError
except ImportError:
    class BaseCommand:
        pass
    class CommandError(Exception):
        pass


class Command(BaseCommand):
    help = "Yangi Özbek alifbosi klaviaturasi haqidagi blog maqolasini naşr qiliş yoki yangilaş."

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
                Categories.objects.filter(name_uz_uz__icontains="texno", is_deleted=False).first()
                or Categories.objects.filter(name_uz_uz__icontains="ilm", is_deleted=False).first()
                or Categories.objects.filter(name_uz_uz__icontains="foydali", is_deleted=False).first()
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

            "name_uz_crl": ARTICLE_DATA["uz_crl"]["name"].strip(),
            "title_uz_crl": ARTICLE_DATA["uz_crl"]["title"].strip(),
            "body_uz_crl": ARTICLE_DATA["uz_crl"]["body"].strip(),

            "name_ru_ru": ARTICLE_DATA["ru"]["name"].strip(),
            "title_ru_ru": ARTICLE_DATA["ru"]["title"].strip(),
            "body_ru_ru": ARTICLE_DATA["ru"]["body"].strip(),

            "name_en_us": ARTICLE_DATA["en"]["name"].strip(),
            "title_en_us": ARTICLE_DATA["en"]["title"].strip(),
            "body_en_us": ARTICLE_DATA["en"]["body"].strip(),

            "seo_title": SEO_TITLE[:70],
            "seo_description": SEO_DESCRIPTION[:200],
            "source_url": SOURCE_URL,
            "publish_time": publish_time,
            "image": IMAGE_REL_PATH if has_image else "",
        }

        if opts["dry_run"]:
            self.stdout.write(self.style.SUCCESS("=" * 68))
            self.stdout.write(self.style.SUCCESS(f"[DRY-RUN] Maqola tayyor: {fields['name_uz_uz']}"))
            self.stdout.write(self.style.SUCCESS(f"         Slug: {SLUG} | Rasm: {IMAGE_REL_PATH} (mavjud={has_image})"))
            self.stdout.write(self.style.SUCCESS("=" * 68))
            return

        post = Posts.objects.filter(slug=SLUG).first()
        if post and not opts["update"]:
            self.stdout.write(self.style.WARNING(f"Maqola allaqaçon mavjud ({SLUG}). Yangilaş uçun --update parametrini bering."))
            self.stdout.write(f"Havola: https://complexprogrammer.uz/blog/{SLUG}/")
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
        self.stdout.write(self.style.SUCCESS("=" * 68))
        self.stdout.write(self.style.SUCCESS(f"✅ Maqola muvaffaqiyatli {action}!"))
        self.stdout.write(self.style.SUCCESS(f"📌 Holati: {status_text}"))
        self.stdout.write(self.style.SUCCESS(f"🖼 Rasm: {IMAGE_REL_PATH}"))
        self.stdout.write(self.style.SUCCESS(f"🔗 Saytdagi havola: https://complexprogrammer.uz/blog/{SLUG}/"))
        self.stdout.write(self.style.SUCCESS("=" * 68))
