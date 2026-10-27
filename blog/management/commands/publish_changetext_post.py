"""Lotin-kirill o'girgich (changetext) sahifasi uchun blog maqolasini nashr qilish yoki yangilash.

Ishlatish:
    python manage.py publish_changetext_post           # darhol saytda nashr qiladi
    python manage.py publish_changetext_post --update  # mavjud maqola matnini yangilaydi
    python manage.py publish_changetext_post --draft   # qoralama qilib saqlaydi (2099-yil)
"""

import os
import datetime

SLUG = "lotin-kirill-ogirgich-changetext"
IMAGE_REL_PATH = "post/images/lotin_kirill_ogirgich.jpg"
PAGE_URL = "https://complexprogrammer.uz/changetext/"
DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)

SEO_TITLE = "Lotin-kirill o'girgich — matnlarni xatosiz o'tkazish"
SEO_DESCRIPTION = "O'zbek matnini kirilldan lotinga va 2026-yilgi yangi lotin alifbosiga bepul o'giring. O', G', sh, ch kabi harflar to'g'ri o'tkaziladi."

ARTICLE_DATA = {
    "uz": {
        "name": "Lotin-kirill o‘girgich — o‘zbekcha matnlarni tez, aniq va qulay konvertatsiya qiling",
        "title": "Kirilldan lotinga, amaldagi va yangi 2026-yilgi alifboga bepul o‘tkazish: fonetik qoidalar, texnik atamalar va dasturlash kodlarini saqlash imkoniyatlari.",
        "body": """
<p>Hujjatlar, maqolalar, ilmiy ishlar yoki ijtimoiy tarmoqlardagi postlar bilan ishlaganda o‘zbek tilidagi matnlarni <strong>kirilldan lotinga</strong> yoki <strong>lotindan kirillga</strong> o‘girish zarurati tez-tez uchraydi. Biroq, internetdagi aksariyat oddiy o‘girgichlar matnni shunchaki harfma-harf almashtirib, jiddiy orfografik va ma’noviy xatoliklarga yo‘l qo‘yadi.</p>

<p>Ushbu muammolarni to‘liq bartaraf etish maqsadida yaratilgan <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Lotin-Kirill o‘girgichi</strong></a> o‘zbek tilining fonetik va grammatik xususiyatlarini chuqur inobatga olgan holda ishlaydi. Quyida ushbu vositaning asosiy imkoniyatlari va afzalliklari bilan tanishamiz.</p>

<h2>1. Yangi 2026-yilgi Lotin alifbosi (Ş, Ç, Ğ, Ö) bilan to‘liq moslik</h2>
<p>O‘zbekiston Respublikasida qabul qilingan alifbo islohotiga muvofiq, ko‘p uchraydigan ikki belgili harflar bitta aniq harfga o‘zgartirilgan:</p>
<ul>
  <li><code>Sh</code> ➔ <code>Ş</code> (masalan: <em>shahar</em> ➔ <em>şahar</em>)</li>
  <li><code>Ch</code> ➔ <code>Ç</code> (masalan: <em>choy</em> ➔ <em>çoy</em>)</li>
  <li><code>O‘</code> ➔ <code>Ö</code> (masalan: <em>o‘rganish</em> ➔ <em>örganiç</em>)</li>
  <li><code>G‘</code> ➔ <code>Ğ</code> (masalan: <em>g‘alaba</em> ➔ <em>ğalaba</em>)</li>
</ul>
<p><a href="https://complexprogrammer.uz/changetext/">changetext</a> xizmatida birgina tugma orqali matningizni <strong>Kirill</strong>, <strong>Lotin (1995-yilgi amaldagi alifbo)</strong> yoki <strong>Yangi Lotin (2026)</strong> variantlariga bir zumda o‘tkaza olasiz. Sahifada 28 ta harf va tutuq belgisini qiyosiy ko‘rsatuvchi interaktiv jadval ham mavjud.</p>

<h2>2. Aqlli fonetik tahlil: «E / Ye», «Ts» va tutuq belgisi</h2>
<p>O‘zbek tilida so‘z boshida yoki unlilardan keyin keladigan tovushlar alohida qoidalar asosida yoziladi. Platforma ushbu nozik jihatlarni avtomatik hal qiladi:</p>
<ul>
  <li><strong>E va Ye farqlanishi:</strong> So‘z boshidagi <code>E</code> harfi kirillda to‘g‘ri <code>Э</code> ga, unlilardan keyingi <code>Ye</code> esa <code>Е</code> ga o‘tkaziladi (masalan: <em>Eshik</em> ➔ <em>Эшик</em>, <em>Kiyik</em> ➔ <em>Кийик</em>).</li>
  <li><strong>Ts tovushi:</strong> So‘z o‘rtasida unlilardan keyin kelgan <code>Ц</code> harfi <code>ts</code>, boshqa holatlarda esa <code>s</code> bo‘lib o‘giriladi (masalan: <em>konstitutsiya</em>).</li>
  <li><strong>Sh birikmasi bilan adashmaslik:</strong> <em>Исҳоқ</em> kabi so‘zlar <em>Ishoq</em> emas, ajratuvchi tutuq belgisi bilan <code>Isʼhoq</code> shaklida to‘g‘ri aks ettiriladi.</li>
  <li><strong>«yo‘l» so‘zi:</strong> <code>yo'l</code> so‘zidagi <code>o'</code> alohida tovush bo‘lgani uchun <code>ё</code> ga aylanib ketmaydi va <code>йўл</code> bo‘lib aniq chiqadi.</li>
</ul>

<h2>3. Havolalar, @username va xorijiy so‘zlar daxlsizligi</h2>
<p>Dasturchilar, blogerlar va zamonaviy matn mualliflari uchun eng muhim jihat — matn ichidagi texnik elementlarning buzilmasligidir. Ushbu o‘girgich:</p>
<ul>
  <li>Veb-sayt havolalari (<code>https://...</code>) va elektron pochtalarga tegmaydi;</li>
  <li>Telegram, Instagram va boshqa tarmoqlardagi <code>@username</code> larni o‘zgartirmaydi;</li>
  <li>Dasturlash kodlari (<code>&lt;code&gt;...&lt;/code&gt;</code>) va HTML teglarini toza saqlaydi;</li>
  <li>O‘zbek alifbosida mavjud bo‘lmagan <code>c</code>, <code>w</code> harflari yoki raqamlar qatnashgan xorijiy so‘zlar hamda brendlarni (masalan: <em>CS2</em>, <em>Workshop</em>, <em>VAC</em>, <em>Google Play</em>) lotincha o‘z holicha qoldiradi.</li>
</ul>

<h2>4. Katta hajmli matnlar, tezkor nusxalash va .txt yuklab olish</h2>
<p>Katta maqolalar, hisobotlar yoki kitob boblarini kiritganingizda ham tizim kechikishlarsiz ishlaydi. Natija maydonida bir qator qulayliklar yaratilgan:</p>
<ul>
  <li><strong>Jonli statistika:</strong> Kiritilgan belgilar va so‘zlar soni real vaqtda hisoblab boriladi.</li>
  <li><strong>📥 Qo‘yish va 🗑 Tozalash:</strong> Xotiradan matnni bir zumda joylash yoki tozalash.</li>
  <li><strong>⇄ O‘rin almashtirish (Swap):</strong> Olingan natijani yana teskari yo‘nalishga tezkor aylantirish.</li>
  <li><strong>📋 Bir bosishda nusxalash:</strong> Tayyor natijani clipboardga oson ko‘chirish.</li>
  <li><strong>⬇ .txt fayl qilib yuklab olish:</strong> Katta matnlarni fayl ko‘rinishida qurilmangizga saqlab olish.</li>
</ul>

<h2>5. Qorong‘i rejim va Android mobil ilovasi</h2>
<p>Sayt interfeysi zamonaviy dizaynga ega bo‘lib, tungi vaqtda ko‘zni toliqtirmaydigan <strong>Dark mode</strong> (qorong‘i mavzu) rejimini qo‘llab-quvvatlaydi. Shuningdek, xizmatni brauzerda PWA ilova sifatida kompyuter yoki smartfonga o‘rnatib olishingiz yoki Google Play’dagi rasmiy <a href="https://play.google.com/store/apps/details?id=changetext.complexprogrammer.uz" target="_blank" rel="noopener"><strong>Android ilovasi</strong></a> orqali smartfoningizda cheksiz va qulay ishlatishingiz mumkin.</p>

<h2>Qanday foydalaniladi?</h2>
<ol>
  <li><a href="https://complexprogrammer.uz/changetext/"><strong>https://complexprogrammer.uz/changetext/</strong></a> sahifasiga o‘ting.</li>
  <li>Chap tomondagi maydonga matningizni yozing yoki nusxalab joylashtiring.</li>
  <li>Kerakli yozuvni tanlang: <strong>Avto</strong>, <strong>Kirill</strong>, <strong>Lotin (1995)</strong> yoki <strong>Yangi lotin (2026)</strong>.</li>
  <li>O‘ng tomonda bir soniyada tayyor bo‘lgan natijadan nusxa oling yoki .txt fayl qilib yuklab oling!</li>
</ol>

<p>O‘zbek tilidagi barcha matnlaringizni bepul, aniq va sifatli o‘girish uchun hoziroq sinab ko‘ring: 👉 <a href="https://complexprogrammer.uz/changetext/"><strong>complexprogrammer.uz/changetext</strong></a></p>
""",
    },
    "ru": {
        "name": "Конвертер узбекского текста латиница-кириллица: быстро, точно и без ошибок",
        "title": "Онлайн-перевод узбекского текста с кириллицы на латиницу 1995 года и новый алфавит 2026 года с сохранением ссылок, тегов и кода.",
        "body": """
<p>При работе с документами, статьями и сообщениями на узбекском языке часто требуется перевести текст из <strong>кириллицы в латиницу</strong> или обратно. Обычные онлайн-транслитераторы часто делают побуквенную замену, что приводит к грубым ошибкам в узбекских буквах и искажению терминов.</p>

<p>Сервис <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Changetext</strong></a> учитывает грамматические и фонетические правила узбекского языка, обеспечивая точный результат без ручного редактирования.</p>

<h2>1. Поддержка нового узбекского алфавита 2026 года</h2>
<p>В соответствии с реформой узбекского латинского алфавита привычные двухбуквенные сочетания заменены отдельными символами:</p>
<ul>
  <li><code>Sh</code> ➔ <code>Ş</code></li>
  <li><code>Ch</code> ➔ <code>Ç</code></li>
  <li><code>O‘</code> ➔ <code>Ö</code></li>
  <li><code>G‘</code> ➔ <code>Ğ</code></li>
</ul>
<p>На странице можно в один клик переключаться между <strong>Кириллицей</strong>, <strong>Латиницей 1995 года</strong> и <strong>Новой латиницей 2026 года</strong>, а также сверяться со сравнительной таблицей всех 28 букв.</p>

<h2>2. Умные правила транслитерации</h2>
<ul>
  <li><strong>Буквы Е / Э:</strong> Автоматическое определение позиции звука в начале слова и после гласных.</li>
  <li><strong>Знак тутук (ʼ):</strong> Разделительные знаки в таких именах, как <em>Isʼhoq</em> (Исҳоқ), сохраняются правильно и не сливаются с <em>sh</em>.</li>
  <li><strong>Слово «yo‘l»:</strong> Звук <code>o‘</code> передается как <code>йўл</code>, а не ошибочное <code>ё</code>.</li>
</ul>

<h2>3. Защита ссылок, @username и английских терминов</h2>
<p>Инструмент не портит технические данные:</p>
<ul>
  <li>Ссылки <code>https://...</code> и email остаются нетронутыми;</li>
  <li>Имена пользователей <code>@username</code> не изменяются;</li>
  <li>HTML-теги и блоки <code>&lt;code&gt;...&lt;/code&gt;</code> остаются в исходном виде;</li>
  <li>Слова, содержащие буквы <code>c</code>, <code>w</code> или цифры (например: <em>CS2</em>, <em>Workshop</em>, <em>Google</em>), остаются на латинице.</li>
</ul>

<h2>4. Удобные функции для работы</h2>
<ul>
  <li>Подсчет символов и слов в реальном времени;</li>
  <li>Быстрая вставка из буфера и кнопка очистки;</li>
  <li>Копирование в буфер обмена одним кликом;</li>
  <li>Скачивание готового результата в виде <strong>.txt</strong> файла;</li>
  <li>Смена направления перевода кнопкой <strong>⇄ Swap</strong>.</li>
</ul>

<p>Сервис абсолютно бесплатен и доступен как в браузере (с поддержкой темной темы), так и в виде официального Android-приложения в Google Play: 👉 <a href="https://complexprogrammer.uz/changetext/"><strong>complexprogrammer.uz/changetext</strong></a></p>
""",
    },
    "en": {
        "name": "Uzbek Latin-Cyrillic Text Converter: Accurate, Fast, and Free",
        "title": "Convert Uzbek text between Cyrillic, 1995 Latin, and the new 2026 reformed alphabet with smart preservation of links, codes, and English terms.",
        "body": """
<p>Working with Uzbek text often requires switching between the <strong>Cyrillic script</strong> and the official <strong>Latin script</strong>. Simple character-by-character replacements usually produce orthographic errors. The <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Uzbek Text Converter</strong></a> solves this with intelligent phonetic processing.</p>

<h2>1. Full Support for the New 2026 Latin Alphabet</h2>
<p>In accordance with the Uzbek alphabet reform, digraphs are replaced by single letters with diacritics:</p>
<ul>
  <li><code>Sh</code> ➔ <code>Ş</code></li>
  <li><code>Ch</code> ➔ <code>Ç</code></li>
  <li><code>O‘</code> ➔ <code>Ö</code></li>
  <li><code>G‘</code> ➔ <code>Ğ</code></li>
</ul>
<p>You can seamlessly convert text between Cyrillic, 1995 Latin, and the 2026 Latin alphabet with a single click.</p>

<h2>2. Smart Phonetic and Grammar Rules</h2>
<ul>
  <li>Proper handling of initial vowels (<code>E</code> vs <code>Ye</code> / <code>Э</code>).</li>
  <li>Preservation of the apostrophe/tutuq sign (e.g. <code>Isʼhoq</code> instead of merging into <code>sh</code>).</li>
  <li>Accurate conversion of complex diphthongs like <code>yo‘l</code> into <code>йўл</code>.</li>
</ul>

<h2>3. Safe for Links, Mentions, and Code Snippets</h2>
<ul>
  <li>Web URLs and email addresses are automatically protected;</li>
  <li>Social mentions (<code>@username</code>) remain untouched;</li>
  <li>Programming code blocks (<code>&lt;code&gt;...&lt;/code&gt;</code>) and HTML tags stay intact;</li>
  <li>Foreign terms, brand names, and words containing <code>c</code>, <code>w</code>, or digits (e.g., <em>CS2</em>, <em>Windows</em>, <em>Google Play</em>) are preserved in Latin script.</li>
</ul>

<h2>4. Built for Productivity</h2>
<p>Features include instant character and word counting, one-click clipboard copying, text file download (<code>.txt</code>), dark mode, and an official Android app on Google Play.</p>

<p>Try it online for free: 👉 <a href="https://complexprogrammer.uz/changetext/"><strong>complexprogrammer.uz/changetext</strong></a></p>
""",
    },
}

# Kirillcha versiya uchun qo'shimcha matn
CYR_DATA = {
    "name": "Лотин-кирилл ўгиргич — ўзбекча матнларни тез, аниқ ва қулай конвертация қилинг",
    "title": "Кириллдан лотинга, амалдаги ва янги 2026 йилги алифбога бепул ўтказиш: фонетик қоидалар, техник атамалар ва дастурлаш кодларини сақлаш имкониятлари.",
    "body": """
<p>Ҳужжатлар, мақолалар, илмий ишлар ёки ижтимоий тармоқлардаги постлар билан ишлаганда ўзбек тилидаги матнларни <strong>кириллдан лотинга</strong> ёки <strong>лотиндан кириллга</strong> ўгириш зарурати тез-тез учрайди. Бироқ, интернетдаги аксарият оддий ўгиргичлар матнни шунчаки ҳарфма-ҳарф алмаштириб, жиддий орфографик ва маъновий хатоликларга йўл қўяди.</p>

<p>Ушбу муаммоларни тўлиқ бартараф этиш мақсадида яратилган <a href="https://complexprogrammer.uz/changetext/" target="_blank" rel="noopener"><strong>Complex Programmer Лотин-Кирилл ўгиргичи</strong></a> ўзбек тилининг фонетик ва грамматик хусусиятларини чуқур инобатга олган ҳолда ишлайди.</p>

<h2>1. Янги 2026 йилги Лотин алифбоси (Ş, Ç, Ğ, Ö) билан тўлиқ мослик</h2>
<p>Ўзбекистон Республикасида қабул қилинган алифбо ислоҳотига мувофиқ, кўп учрайдиган икки белгили ҳарфлар битта аниқ ҳарфга ўзгартирилган:</p>
<ul>
  <li><code>Sh</code> ➔ <code>Ş</code> (масалан: <em>шаҳар</em> ➔ <em>şahar</em>)</li>
  <li><code>Ch</code> ➔ <code>Ç</code> (масалан: <em>чой</em> ➔ <em>çoy</em>)</li>
  <li><code>O‘</code> ➔ <code>Ö</code> (масалан: <em>ўрганиш</em> ➔ <em>örganiç</em>)</li>
  <li><code>G‘</code> ➔ <code>Ğ</code> (масалан: <em>ғалаба</em> ➔ <em>ğalaba</em>)</li>
</ul>
<p><a href="https://complexprogrammer.uz/changetext/">changetext</a> хизматида биргина тугма орқали матнингизни <strong>Кирилл</strong>, <strong>Лотин (1995 йилги амалдаги алифбо)</strong> ёки <strong>Янги Лотин (2026)</strong> вариантларига бир зумда ўтказа оласиз.</p>

<h2>2. Ақлли фонетик таҳлил: «Э / Е», «Ц» ва тутуқ белгиси</h2>
<ul>
  <li><strong>Э ва Е фарқланиши:</strong> Сўз бошидаги <code>E</code> ҳарфи кириллда тўғри <code>Э</code> га, унлилардан кейинги <code>Ye</code> эса <code>Е</code> га ўтказилади (масалан: <em>Эшик</em>, <em>Кийик</em>).</li>
  <li><strong>Ц товуши:</strong> Сўз ўртасида унлилардан кейин келган <code>Ц</code> ҳарфи <code>ts</code>, бошқа ҳолатларда эса <code>s</code> бўлиб ўгирилади.</li>
  <li><strong>Sh бирикмаси билан адашмаслик:</strong> <em>Исҳоқ</em> каби сўзлар <em>Ишоқ</em> эмас, ажратувчи тутуқ белгиси билан <code>Isʼhoq</code> шаклида тўғри акс эттирилади.</li>
  <li><strong>«йўл» сўзи:</strong> <code>yo'l</code> сўзидаги <code>o'</code> алоҳида товуш бўлгани учун <code>ё</code> га айланиб кетмайди ва <code>йўл</code> бўлиб чиқади.</li>
</ul>

<h2>3. Ҳаволалар, @username ва хорижий сўзлар дахлсизлиги</h2>
<ul>
  <li>Веб-сайт ҳаволалари (<code>https://...</code>) ва электрон почталар ўзгармайди;</li>
  <li>Ижтимоий тармоқлардаги <code>@username</code> ларга тегилмайди;</li>
  <li>Дастурлаш кодлари (<code>&lt;code&gt;...&lt;/code&gt;</code>) ва HTML теглари тоза сақланади;</li>
  <li>Ўзбек алифбосида мавжуд бўлмаган <code>c</code>, <code>w</code> ҳарфлари ёки рақамлар қатнашган сўзлар (масалан: <em>CS2</em>, <em>Workshop</em>, <em>Google Play</em>) лотинча ўз ҳолича қолади.</li>
</ul>

<h2>4. Қандай фойдаланилади?</h2>
<ol>
  <li><a href="https://complexprogrammer.uz/changetext/"><strong>https://complexprogrammer.uz/changetext/</strong></a> саҳифасига ўтинг.</li>
  <li>Чап томондаги майдонга матнни киритинг ёки жойлаштиринг.</li>
  <li>Керакли алифбони танланг (Авто, Кирилл, Лотин 1995, Янги лотин 2026).</li>
  <li>Ўнг томондаги тайёр натижадан нусха олинг ёки .txt файл кўринишида юклаб олинг!</li>
</ol>

<p>Батафсил синаб кўриш: 👉 <a href="https://complexprogrammer.uz/changetext/"><strong>complexprogrammer.uz/changetext</strong></a></p>
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
    help = "Lotin-kirill o'girgich (changetext) blog maqolasini rasmlari bilan birga nashr qilish yoki yangilash."

    def add_arguments(self, parser):
        parser.add_argument("--update", action="store_true", help="Mavjud maqola matnini yangilash")
        parser.add_argument("--draft", action="store_true", help="Saytda ko'rsatmasdan qoralama (2099-yil) sifatida saqlash")
        parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmasdan tekshirish")

    def handle(self, *args, **opts):
        from django.conf import settings
        from django.contrib.auth.models import User
        from django.utils import timezone
        from blog.models import Categories, Posts

        author = User.objects.filter(is_superuser=True).order_by("id").first()
        if not author:
            author = User.objects.order_by("id").first()
        if not author:
            raise CommandError("Muallif uchun birorta ham User topilmadi.")

        category = (
            Categories.objects.filter(name_uz_uz__icontains="ilm", is_deleted=False).first()
            or Categories.objects.filter(name_uz_uz__icontains="test", is_deleted=False).first()
            or Categories.objects.filter(is_deleted=False).first()
        )

        publish_time = DRAFT_TIME if opts["draft"] else timezone.now()

        # Rasm tekshiruvi
        image_full_path = os.path.join(settings.MEDIA_ROOT, IMAGE_REL_PATH)
        has_image = os.path.exists(image_full_path)
        if not has_image:
            self.stdout.write(self.style.WARNING(f"Ogohlantirish: Rasm fayli topilmadi: {image_full_path}"))
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
            "source_url": PAGE_URL,
            "publish_time": publish_time,
            "image": IMAGE_REL_PATH if has_image else "",
        }

        post = Posts.objects.filter(slug=SLUG).first()
        if post and not opts["update"]:
            self.stdout.write(self.style.WARNING(f"Maqola allaqachon mavjud ({SLUG}). Yangilash uchun --update parametrini bering."))
            self.stdout.write(f"Havola: https://complexprogrammer.uz/blog/{SLUG}/")
            return

        if opts["dry_run"]:
            self.stdout.write(self.style.SUCCESS(f"[DRY-RUN] Maqola tayyor: {fields['name_uz_uz']}"))
            return

        if not post:
            post = Posts(slug=SLUG, created_by=author, categorie=category)
            action = "yaratildi va nashr qilindi"
        else:
            action = "yangilandi"

        for k, v in fields.items():
            setattr(post, k, v)
        if category and not post.categorie:
            post.categorie = category

        post.save()

        status_text = "Qoralama (2099-yil)" if opts["draft"] else "Nashr qilindi (jonli efirda)"
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS(f"✅ Maqola muvaffaqiyatli {action}!"))
        self.stdout.write(self.style.SUCCESS(f"📌 Holati: {status_text}"))
        self.stdout.write(self.style.SUCCESS(f"🖼 Rasm: {IMAGE_REL_PATH}"))
        self.stdout.write(self.style.SUCCESS(f"🔗 Saytdagi havola: https://complexprogrammer.uz/blog/{SLUG}/"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
