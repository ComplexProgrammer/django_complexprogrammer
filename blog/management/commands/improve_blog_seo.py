"""Search Console asosida blog maqolalarini yaxşilaş: SEO sarlavha/tavsif va ijara şartnomasi DOCX namunasi.

    python manage.py improve_blog_seo --dry-run   # nima özgarişini körsatadi
    python manage.py improve_blog_seo             # yozadi
    python manage.py improve_blog_seo --force     # admin kiritgan SEO sarlavhalarni ham almaştiradi

Sabab (Search Console, 2026-11): quyidagi maqolalar 3–10-örinda körsatiladi, lekin SEO sarlavha/tavsifi böş edi —
qidiruv natijasida tasodifiy matn çiqib, CTR 0,5–1,7% bölgan. «ijara shartnomasi namunasi» sörovida maqola 2,4-örinda,
lekin namuna boşqa saytdan olingan rasm edi — endi tahrirlanadigan Word fayl (scripts/build_ijara_template.py).
"""

import re

from django.core.management.base import BaseCommand

SEO = {
    "kozning-lazer-operatsiyasi-qancha-turadi": (
        "Köz lazer operatsiyasi narxi va usullari: kimga mos, asoratlar",
        "Közning lazer korreksiyasi: usullari, kimga zarur, narxi nimaga bağliq, operatsiya jarayoni, keyingi tekşiruvlar va mumkin bölgan asoratlar.",
    ),
    "sizga-glyutensiz-mahsulotlar-kerakmi-va-ularning-narxi-qancha": (
        "Glyuten nima, kimga zarar va glyutensiz non qayerda sotiladi",
        "Glyuten nima va qaysi mahsulotlarda bor, seliakiya va glyutenni hazm qila olmaslik alomatlari, glyutensiz non foydasi va uni Özbekistonda qayerdan oliş mumkin.",
    ),
    "uy-sharoitida-koz-atrofidagi-ajinlarni-kamaytirish": (
        "Köz atrofidagi ajinlarni uy şaroitida kamaytiriş: maşq va massaj",
        "Köz atrofidagi ajinlarni ketkaziş: terini namlantiriş, malhamlar, köz muşaklari uçun maşqlar va massaj — uyda qilsa böladigan usullar.",
    ),
    "tishga-breket-qoyish-qancha-turadi": (
        "Breket turlari va narxi: metall, keramik, sapfir, lingval",
        "Tişga breket qöyiş: tayyorgarlik, materialiga (metall, keramik, sapfir, plastik) va örnatiliş usuliga köra breket turlari, ortodont qabuli va reteynerlar.",
    ),
    "quruq-yuz-terisini-parvarish-qilish-sirlari": (
        "Quruq yuz terisi parvarişi: belgilari va bosqiçma-bosqiç sxema",
        "Quruq yuz terisi belgilari, parvarişning asosiy tamoyillari, kunlik bosqiçma-bosqiç sxema hamda yoz va qişda teri parvarişining öziga xos jihatlari.",
    ),
}

IJARA_SLUG = "uyni-shartnoma-boyicha-ijaraga-berish-tartibi"
IJARA_MARK = "<!-- ijara-docx -->"
FILES = "/media/post/files/ijara-shartnomasi-namunasi"
IJARA_BLOCK = {
    "uz": ("📄 Tahrirlanadigan namuna — Word (DOCX)", [
        ("", "Yangi alifboda"), ("-lotin-1995", "Lotin yozuvida (1995)"), ("-kirill", "Kirill yozuvida"),
    ], "Namunada: taraflar, turar joy, muddat (5 yilgaça), ijara haqi va garov puli, huquq va majburiyatlar, bekor qiliş tartibi, "
       "imzolar hamda topşiriş-qabul qiliş dalolatnomasi. Faylni yuklab oling, böş joylarni töldiring va kerak bölsa şartlarni özgartiring."),
    "ru": ("📄 Редактируемый образец — Word (DOCX, на узбекском)", [
        ("-kirill", "Кириллица"), ("-lotin-1995", "Латиница (1995)"), ("", "Новый алфавит"),
    ], "В образце: стороны, жильё, срок (до 5 лет), арендная плата и залог, права и обязанности, порядок расторжения, "
       "подписи и акт приёма-передачи. Скачайте файл, заполните пустые поля и при необходимости измените условия."),
    "en": ("📄 Editable template — Word (DOCX, in Uzbek)", [
        ("-lotin-1995", "Latin script (1995)"), ("-kirill", "Cyrillic"), ("", "New alphabet"),
    ], "Includes the parties, the property, term (up to 5 years), rent and deposit, rights and duties, termination, "
       "signatures and a handover act. Download it, fill in the blanks and adjust the terms as needed."),
}


def block(lang):
    heading, files, note = IJARA_BLOCK[lang]
    links = "".join(f'<li><a href="{FILES}{sfx}.docx" download>{label}</a></li>' for sfx, label in files)
    return f"{IJARA_MARK}<div class=\"b-download\"><p><strong>{heading}</strong></p><ul>{links}</ul><p>{note}</p></div>"


def insert_after_heading(body, needle, html):
    """``needle`` matnli sarlavhadan keyin (namuna rasmi örniga ustidan) qöyadi; topilmasa — oxiriga."""
    m = re.search(re.escape(needle) + r".*?</h[23]>", body, re.S)
    if m:
        return body[:m.end()] + html + body[m.end():]
    return body.rstrip() + html


class Command(BaseCommand):
    help = "Blog: böş SEO sarlavha/tavsiflarni töldiriş va ijara maqolasiga DOCX namuna qöşiş."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--force", action="store_true", help="Mavjud SEO sarlavha/tavsifni ham almaştiriş")

    def handle(self, *args, **opts):
        from django.conf import settings

        from blog.models import Posts
        from core.translit import latin_to_cyrillic

        changed = 0
        for slug, (title, desc) in SEO.items():
            post = Posts.objects.filter(slug=slug).first()
            if post is None:
                self.stdout.write(self.style.WARNING(f"? {slug}: topilmadi"))
                continue
            if post.seo_title and not opts["force"]:
                self.stdout.write(f"= {slug}: SEO sarlavha bor — tegilmadi")
                continue
            self.stdout.write(f"~ {slug}: «{title}»")
            if not opts["dry_run"]:
                Posts.objects.filter(pk=post.pk).update(seo_title=title[:70], seo_description=desc[:200])
                changed += 1

        post = Posts.objects.filter(slug=IJARA_SLUG).first()
        missing = [s for s in ("", "-lotin-1995", "-kirill")
                   if not (settings.BASE_DIR / "media" / "post" / "files" / f"ijara-shartnomasi-namunasi{s}.docx").exists()]
        if post is None:
            self.stdout.write(self.style.WARNING(f"? {IJARA_SLUG}: topilmadi"))
        elif missing:
            self.stdout.write(self.style.ERROR(f"DOCX fayllar yöq ({missing}) — avval: python scripts/build_ijara_template.py"))
        elif IJARA_MARK in (post.body_uz_uz or ""):
            self.stdout.write(f"= {IJARA_SLUG}: DOCX namuna allaqaçon qöşilgan")
        else:
            self.stdout.write(f"+ {IJARA_SLUG}: DOCX namuna bloki")
            if not opts["dry_run"]:
                uz = block("uz")
                fields = {
                    "body_uz_uz": insert_after_heading(post.body_uz_uz or "", "namunasi:", uz),
                    "body_uz_crl": insert_after_heading(post.body_uz_crl or "", "намунаси:", latin_to_cyrillic(uz)),
                    "body_ru_ru": (post.body_ru_ru or "").rstrip() + block("ru") if post.body_ru_ru else post.body_ru_ru,
                    "body_en_us": (post.body_en_us or "").rstrip() + block("en") if post.body_en_us else post.body_en_us,
                }
                # update(): signal yöq — Telegram'ga qayta yuborilmaydi, sana özgarmaydi
                Posts.objects.filter(pk=post.pk).update(**fields)
                changed += 1

        if not opts["dry_run"]:
            try:
                from django.core.cache import cache

                cache.clear()
            except Exception:
                pass
        self.stdout.write(self.style.SUCCESS(f"Tayyor: {changed} ta maqola yangilandi." if not opts["dry_run"] else "--dry-run: heçnarsa yozilmadi."))
