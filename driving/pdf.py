"""Avtotest savollari va to'g'ri javoblari — bitta PDF (PyMuPDF Story: HTML -> sahifalar).

Search Console'da "avto test 1000 savol javoblar pdf", "avto test 1000 скачать" so'rovlari ko'p — shu fayl uchun.
Yaratish: ``python manage.py build_avtotest_pdf`` (natija media/avtotest/ ga yoziladi).
"""

import os
import tempfile
from html import escape
from pathlib import Path

import fitz
from django.conf import settings
from PIL import Image
from django.utils import timezone

from projects.models import AvtoTest

FONT = Path(__file__).resolve().parent / "fonts" / "NotoSans.ttf"
IMAGES = Path(settings.BASE_DIR) / "static" / "avtotest"
OUT_DIR = Path(settings.MEDIA_ROOT) / "avtotest"
LETTERS = ("A", "B", "C", "D")

TEXT = {
    "uz": {"title": "Avto test savollari va javoblari", "sub": "{n} ta savol, {b} ta bilet · to'g'ri javoblar belgilangan",
           "bilet": "{n}-bilet", "site": "Onlayn yechish va imtihon simulyatori: complexprogrammer.uz/avtotest", "sfx": ""},
    "ru": {"title": "Вопросы и ответы автотеста", "sub": "{n} вопросов, {b} билетов · правильные ответы отмечены",
           "bilet": "Билет {n}", "site": "Решать онлайн и симулятор экзамена: complexprogrammer.uz/ru/avtotest", "sfx": "_ru"},
}

CSS = """
@font-face { font-family: noto; src: url(NotoSans.ttf); }
* { font-family: noto; }
body { font-size: 10pt; line-height: 1.35; }
h1 { font-size: 22pt; text-align: center; margin: 120pt 0 8pt 0; }
h2 { font-size: 14pt; color: #4f46e5; margin: 14pt 0 6pt 0; border-bottom: 1px solid #c7d2fe; }
p.sub, p.site { text-align: center; color: #555555; }
div.q { margin: 0 0 10pt 0; page-break-inside: avoid; }
p.qt { font-weight: bold; margin: 0 0 4pt 0; }
p.a { margin: 0 0 1pt 12pt; color: #333333; }
p.ok { margin: 0 0 1pt 12pt; color: #15803d; font-weight: bold; }
img { width: 190pt; }
"""


def pdf_path(lang):
    return OUT_DIR / f"avtotest-savollar-javoblar-{lang}.pdf"


def _html(lang):
    t = TEXT[lang]
    sfx = t["sfx"]
    rows = list(AvtoTest.objects.filter(javob__in=LETTERS).order_by("bilet", "raqam"))
    bilets = sorted({q.bilet for q in rows})
    parts = [
        f"<h1>{escape(t['title'])}</h1>",
        f"<p class='sub'>{escape(t['sub'].format(n=len(rows), b=len(bilets)))}</p>",
        f"<p class='site'>{escape(t['site'])}</p>",
        f"<p class='site'>{timezone.localdate():%d.%m.%Y}</p>",
    ]
    current = None
    for q in rows:
        if q.bilet != current:
            current = q.bilet
            parts.append(f"<h2 style='page-break-before: always'>{escape(t['bilet'].format(n=q.bilet))}</h2>")
        text = getattr(q, "savol" + sfx) or q.savol
        block = [f"<div class='q'><p class='qt'>{q.raqam}. {escape(text)}</p>"]
        if q.rasm and (IMAGES / q.rasm).is_file():
            block.append(f"<img src='{escape(q.rasm)}'/>")
        for letter in LETTERS:
            answer = getattr(q, f"javob_{letter.lower()}{sfx}") or getattr(q, f"javob_{letter.lower()}")
            if not answer:
                continue
            if letter == q.javob:
                block.append(f"<p class='ok'>✔ {letter}) {escape(answer)}</p>")
            else:
                block.append(f"<p class='a'>{letter}) {escape(answer)}</p>")
        block.append("</div>")
        parts.append("".join(block))
    return "<body>" + "".join(parts) + "</body>"


def _compressed_images(folder):
    """Rasmlarning PDF uchun kichraytirilgan nusxalari (asl fayllar ~80 MB — PDF ham shuncha bo'lib qolardi)."""
    for src in IMAGES.iterdir():
        if src.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        try:
            with Image.open(src) as img:
                img = img.convert("RGB")
                img.thumbnail((520, 520))
                img.save(Path(folder) / src.name, "JPEG", quality=62, optimize=True)
        except OSError:
            continue


def build(lang="uz", images_dir=None):
    """PDF faylni yaratadi va yo'lini qaytaradi."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_images:
        if images_dir is None:
            _compressed_images(tmp_images)
            images_dir = tmp_images
        return _build(lang, images_dir)


def _build(lang, images_dir):
    archive = fitz.Archive()
    archive.add(str(images_dir))
    archive.add(str(FONT.parent))
    story = fitz.Story(html=_html(lang), user_css=CSS, archive=archive)
    target = pdf_path(lang)
    fd, tmp = tempfile.mkstemp(suffix=".pdf")  # oraliq fayl loyiha papkasidan tashqarida (sinxronlash dasturlari band qilmasin)
    os.close(fd)
    writer = fitz.DocumentWriter(tmp)
    page = fitz.paper_rect("a4")
    where = page + (42, 42, -42, -42)
    more = True
    while more:
        device = writer.begin_page(page)
        more, _ = story.place(where)
        story.draw(device)
        writer.end_page()
    writer.close()

    # Sahifa raqami va sayt manzili har bir sahifa pastida; rasmlar siqiladi (fayl hajmi kichikroq)
    doc = fitz.open(tmp)
    doc.set_metadata({"title": TEXT[lang]["title"], "author": "Complex Programmer", "subject": "complexprogrammer.uz/avtotest"})
    for number, pg in enumerate(doc, start=1):
        pg.insert_text((42, page.height - 20), f"complexprogrammer.uz/avtotest   ·   {number}", fontsize=8, color=(0.45, 0.45, 0.45))
    doc.save(str(target), garbage=4, deflate=True)
    doc.close()
    try:
        os.unlink(tmp)
    except OSError:
        pass
    return target
