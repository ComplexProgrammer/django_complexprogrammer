"""Blog uchun yordamchi funksiyalar: til tanlash, HTML tozalash, slug va o'qish vaqti."""

import re
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit

from django.utils.html import strip_tags
from django.utils.text import slugify

# Sayt tili -> model maydonlari qo'shimchasi (birinchisi — afzal, qolganlari — zaxira)
FIELD_ORDER = {
    "uz": ("uz_uz", "en_us", "ru_ru"),
    "ru": ("ru_ru", "uz_uz", "en_us"),
    "en": ("en_us", "uz_uz", "ru_ru"),
    "tr": ("en_us", "uz_uz", "ru_ru"),
}
# Bundan qisqa matn "tarjima qilinmagan" hisoblanadi (admin'da "-" yoki "test" qoldirilgan bo'ladi)
MIN_BODY_CHARS = 50

UI = {
    "uz": {
        "blog": "Blog", "home": "Bosh sahifa", "all": "Barcha maqolalar", "categories": "Kategoriyalar",
        "latest": "So'nggi maqolalar", "popular": "Ko'p o'qilganlar", "related": "O'xshash maqolalar",
        "read_more": "O'qish", "min_read": "daqiqa o'qish", "views": "marta o'qilgan",
        "prev": "Oldingi maqola", "next": "Keyingi maqola", "share": "Ulashish", "copy_link": "Havolani nusxalash",
        "copied": "Havola nusxalandi", "search": "Blogdan qidirish…", "found": "ta maqola topildi",
        "nothing": "Hech narsa topilmadi", "reset": "Filtrni tozalash", "source": "Manba",
        "fallback": "Bu maqola hozircha faqat o'zbek tilida mavjud.", "page": "sahifa",
        "newer": "← Yangiroq", "older": "Eskiroq →", "rss": "RSS obuna",
        "title": "Blog — maqolalar va foydali ma'lumotlar",
        "subtitle": "Avtotest, texnologiya, ta'lim va kundalik hayot uchun foydali maqolalar",
        "articles": "ta maqola", "new": "Yangi", "toc": "Mundarija",
        "tg_title": "Yangi maqolalarni o'tkazib yubormang", "tg_text": "Telegram kanalimizga obuna bo'ling — har bir yangi maqola birinchi bo'lib sizga keladi.",
        "tg_btn": "Kanalga obuna bo'lish",
        "test_title": "Bilimingizni sinab ko'ring", "test_text": "108 ta bilet, imtihon simulyatori (20 savol, 25 daqiqa) va xatolar ustida ishlash — bepul.",
        "test_btn": "Avtotestni boshlash", "exam_btn": "Imtihon simulyatori",
    },
    "ru": {
        "blog": "Блог", "home": "Главная", "all": "Все статьи", "categories": "Категории",
        "latest": "Последние статьи", "popular": "Популярное", "related": "Похожие статьи",
        "read_more": "Читать", "min_read": "мин. чтения", "views": "просмотров",
        "prev": "Предыдущая статья", "next": "Следующая статья", "share": "Поделиться", "copy_link": "Копировать ссылку",
        "copied": "Ссылка скопирована", "search": "Поиск по блогу…", "found": "статей найдено",
        "nothing": "Ничего не найдено", "reset": "Сбросить фильтр", "source": "Источник",
        "fallback": "Эта статья пока доступна только на узбекском языке.", "page": "страница",
        "newer": "← Новее", "older": "Старее →", "rss": "RSS-подписка",
        "title": "Блог — статьи и полезная информация",
        "subtitle": "Полезные статьи об автотесте, технологиях, учёбе и жизни",
        "articles": "статей", "new": "Новое", "toc": "Содержание",
        "tg_title": "Не пропускайте новые статьи", "tg_text": "Подпишитесь на наш Telegram-канал — новые статьи придут к вам первыми.",
        "tg_btn": "Подписаться на канал",
        "test_title": "Проверьте свои знания", "test_text": "108 билетов, симулятор экзамена (20 вопросов, 25 минут) и работа над ошибками — бесплатно.",
        "test_btn": "Начать автотест", "exam_btn": "Симулятор экзамена",
    },
    "en": {
        "blog": "Blog", "home": "Home", "all": "All articles", "categories": "Categories",
        "latest": "Latest articles", "popular": "Most read", "related": "Related articles",
        "read_more": "Read", "min_read": "min read", "views": "views",
        "prev": "Previous article", "next": "Next article", "share": "Share", "copy_link": "Copy link",
        "copied": "Link copied", "search": "Search the blog…", "found": "articles found",
        "nothing": "Nothing found", "reset": "Clear filter", "source": "Source",
        "fallback": "This article is currently available only in Uzbek.", "page": "page",
        "newer": "← Newer", "older": "Older →", "rss": "RSS feed",
        "title": "Blog — articles and useful information",
        "subtitle": "Useful articles on the driving test, technology, learning and everyday life",
        "articles": "articles", "new": "New", "toc": "Contents",
        "tg_title": "Don't miss new articles", "tg_text": "Follow our Telegram channel and get every new article first.",
        "tg_btn": "Join the channel",
        "test_title": "Test your knowledge", "test_text": "108 tickets, an exam simulator (20 questions, 25 minutes) and mistake review — free.",
        "test_btn": "Start the driving test", "exam_btn": "Exam simulator",
    },
}
UI["tr"] = dict(UI["en"], **{
    "home": "Ana sayfa", "all": "Tüm makaleler", "categories": "Kategoriler", "latest": "Son makaleler",
    "popular": "En çok okunanlar", "related": "Benzer makaleler", "read_more": "Oku", "min_read": "dk okuma",
    "views": "görüntülenme", "prev": "Önceki makale", "next": "Sonraki makale", "share": "Paylaş",
    "copy_link": "Bağlantıyı kopyala", "copied": "Bağlantı kopyalandı", "search": "Blogda ara…",
    "found": "makale bulundu", "nothing": "Hiçbir şey bulunamadı", "reset": "Filtreyi temizle", "source": "Kaynak",
    "fallback": "Bu makale şu anda yalnızca Özbekçe mevcuttur.", "page": "sayfa",
    "newer": "← Daha yeni", "older": "Daha eski →", "rss": "RSS aboneliği",
    "title": "Blog — makaleler ve faydalı bilgiler",
    "subtitle": "Ehliyet sınavı, teknoloji, eğitim ve günlük yaşam üzerine faydalı makaleler",
    "articles": "makale", "new": "Yeni", "toc": "İçindekiler",
    "tg_title": "Yeni makaleleri kaçırmayın", "tg_text": "Telegram kanalımıza abone olun, her yeni makale önce size gelsin.",
    "tg_btn": "Kanala abone ol",
    "test_title": "Bilginizi test edin", "test_text": "108 bilet, sınav simülatörü (20 soru, 25 dakika) ve hata tekrarı — ücretsiz.",
    "test_btn": "Teste başla", "exam_btn": "Sınav simülatörü",
})


def lang_key(code):
    code = (code or "uz")[:2]
    return code if code in FIELD_ORDER else "uz"


def pick(obj, field, lang, min_len=3):
    """Joriy tildagi matnni qaytaradi; bo'sh bo'lsa keyingi tilga o'tadi. -> (matn, asosiy_tilmi)"""
    get = obj.get if isinstance(obj, dict) else (lambda name: getattr(obj, name, ""))
    original = get(f"{field}_uz_uz") or ""
    for i, sfx in enumerate(FIELD_ORDER[lang]):
        value = get(f"{field}_{sfx}") or ""
        # Admin'da ko'pincha o'zbekcha matn boshqa til maydoniga shunchaki nusxalangan — bu tarjima emas
        if sfx != "uz_uz" and value == original:
            continue
        plain = strip_tags(value).strip() if field == "body" else value.strip()
        if len(plain) >= min_len:
            return value, i == 0
    return "", True


def reading_minutes(html):
    words = len(strip_tags(html).split())
    return max(1, round(words / 200))


def excerpt(text, limit=160):
    text = re.sub(r"\s+", " ", strip_tags(text or "")).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",.;:—-") + "…"


_APOSTROPHES = re.compile(r"[ʻʼ‘’`'´]")


def make_slug(text, max_length=80):
    slug = slugify(_APOSTROPHES.sub("", text or ""))
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit("-", 1)[0]
    return slug


# ----------------------------------------------------------------------------------------
# HTML tozalash. Maqolalar boshqa saytlardan inline style/tailwind klasslari bilan ko'chirilgan —
# ular sahifa dizaynini buzadi (tungi rejimda oq fon, ulkan shriftlar). Faqat ruxsat etilgan
# teglar va atributlar qoldiriladi; <script>/<style> butunlay olib tashlanadi.
# ----------------------------------------------------------------------------------------
ALLOWED_TAGS = {
    "p", "br", "h2", "h3", "h4", "h5", "h6", "strong", "b", "em", "i", "u", "s", "sub", "sup",
    "ul", "ol", "li", "a", "img", "blockquote", "pre", "code", "table", "thead", "tbody", "tfoot",
    "tr", "th", "td", "figure", "figcaption", "hr", "div", "span", "iframe", "caption",
}
RENAME_TAGS = {"h1": "h2"}  # sahifada bitta <h1> bo'lishi kerak — maqola sarlavhasi
VOID_TAGS = {"br", "img", "hr"}
DROP_WITH_CONTENT = {"script", "style", "noscript", "template", "svg", "button", "form", "input", "select"}
ALLOWED_ATTRS = {
    "a": {"href", "title"},
    "img": {"src", "alt", "width", "height"},
    "iframe": {"src", "width", "height", "allowfullscreen", "title"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan"},
}
IFRAME_HOSTS = ("www.youtube.com", "youtube.com", "www.youtube-nocookie.com", "player.vimeo.com")


def _safe_url(url, *, image=False):
    url = (url or "").strip()
    scheme = urlsplit(url).scheme.lower()
    if scheme in ("http", "https", "") and not url.lower().startswith(("javascript:", "vbscript:")):
        return url
    if image and url.startswith("data:image/"):
        return url
    return None


class _Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0  # DROP_WITH_CONTENT ichida bo'lsak > 0
        self.open_tags = []

    def handle_starttag(self, tag, attrs):
        if tag in DROP_WITH_CONTENT:
            if tag not in VOID_TAGS:
                self.skip += 1
            return
        if self.skip:
            return
        tag = RENAME_TAGS.get(tag, tag)
        if tag not in ALLOWED_TAGS:
            return
        allowed = ALLOWED_ATTRS.get(tag, set())
        kept = {}
        for name, value in attrs:
            if name in allowed:
                kept[name] = value if value is not None else ""
        if tag == "a":
            href = _safe_url(kept.get("href"))
            if href is None:
                kept.pop("href", None)
            else:
                kept["href"] = href
                if href.startswith("http") and "complexprogrammer.uz" not in href:
                    kept["target"] = "_blank"
                    kept["rel"] = "noopener nofollow"
        elif tag == "img":
            src = _safe_url(kept.get("src"), image=True)
            if not src:
                return
            kept["src"] = src
            kept["loading"] = "lazy"
            kept["decoding"] = "async"
            kept.setdefault("alt", "")
        elif tag == "iframe":
            if urlsplit(kept.get("src", "")).hostname not in IFRAME_HOSTS:
                self.skip += 1  # yopilish tegigacha hammasini tashlaymiz
                self.open_tags.append("__skipped_iframe__")
                return
            kept["loading"] = "lazy"
            kept["allowfullscreen"] = ""
        attr_html = "".join(
            f' {k}="{escape(v, quote=True)}"' if v != "" else f" {k}" for k, v in kept.items()
        )
        self.out.append(f"<{tag}{attr_html}>")
        if tag not in VOID_TAGS:
            self.open_tags.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if RENAME_TAGS.get(tag, tag) not in VOID_TAGS and tag not in DROP_WITH_CONTENT:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "iframe" and self.open_tags and self.open_tags[-1] == "__skipped_iframe__":
            self.open_tags.pop()
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        tag = RENAME_TAGS.get(tag, tag)
        if tag in VOID_TAGS or tag not in self.open_tags:
            return
        # Noto'g'ri yopilgan teglarni ham to'g'ri tartibda yopamiz
        while self.open_tags:
            current = self.open_tags.pop()
            self.out.append(f"</{current}>")
            if current == tag:
                break

    def handle_data(self, data):
        if not self.skip:
            self.out.append(escape(data, quote=False))

    def result(self):
        while self.open_tags:
            tag = self.open_tags.pop()
            if tag != "__skipped_iframe__":
                self.out.append(f"</{tag}>")
        html = "".join(self.out)
        # Bo'sh paragraflar va ortiqcha bo'sh qatorlarni olib tashlaymiz
        empty = re.compile(r"<(p|div|span|strong|b|em|i)>(\s|&nbsp;|\xa0|<br>)*</\1>")
        while True:
            html, n = empty.subn("", html)
            if not n:
                return html.strip()


def clean_html(html):
    cleaner = _Cleaner()
    cleaner.feed(html or "")
    cleaner.close()
    return cleaner.result()


_H2 = re.compile(r"<h2>(.*?)</h2>", re.S)


def add_toc(html, min_items=3):
    """Maqoladagi <h2> sarlavhalariga id qo'yadi va mundarija ro'yxatini qaytaradi: (html, [(id, matn), ...]).

    Sarlavhalar min_items tadan kam bo'lsa mundarija bo'sh qaytadi (qisqa maqolada keraksiz).
    """
    toc = []

    def anchor(match):
        # shablon matnni o'zi escape qiladi — "&amp;" ikki marta escape bo'lmasin
        text = re.sub(r"\s+", " ", unescape(strip_tags(match.group(1)))).strip()
        if not text:
            return match.group(0)
        anchor_id = f"s{len(toc) + 1}"
        toc.append((anchor_id, text))
        return f'<h2 id="{anchor_id}">{match.group(1)}</h2>'

    html = _H2.sub(anchor, html)
    return html, (toc if len(toc) >= min_items else [])


def split_for_ad(html, after_paragraphs=3):
    """Reklamani matn o'rtasiga (3-paragrafdan keyin) qo'yish uchun HTML'ni ikkiga bo'ladi."""
    pos = -1
    for _ in range(after_paragraphs):
        pos = html.find("</p>", pos + 1)
        if pos == -1:
            return html, ""
    pos += len("</p>")
    return html[:pos], html[pos:]
