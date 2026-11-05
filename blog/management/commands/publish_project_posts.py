"""/projects/ dagi loyihalar uçun blog maqolalarini naşr qiliş: har bir faol loyihaga kamida bitta maqola.

    python manage.py publish_project_posts --report       # qaysi loyihada maqola yöq — faqat hisobot
    python manage.py publish_project_posts --dry-run      # nima naşr qilinişini körsatadi, bazaga yozmaydi
    python manage.py publish_project_posts                # yangi maqolalarni naşr qiladi (mavjudlariga tegmaydi)
    python manage.py publish_project_posts --update       # mavjud maqolalar matnini ham yangilaydi (sana saqlanadi)
    python manage.py publish_project_posts --only 26      # faqat bitta loyiha (Project.id) yoki slug
    python manage.py publish_project_posts --draft        # qoralama (2099-yil) — saytda körinmaydi
    python manage.py publish_project_posts --telegram     # Telegram kanalga ham yuboriş (standart: yuborilmaydi)

Maqola matnlari: blog/rewrites/project_posts_*.py (ARTICLES). ``[[...]]`` bilan belgilangan nomlar (PDF, IP, Google...)
kirill variantida lotinça qoladi. Rasm sifatida loyihaning öz rasmi (media/projects/images/...) işlatiladi.

Telegram: 12 ta maqola birdan kanalga taşlansa, obunaçilar zerikadi — şuning uçun standart holatda yuborilmaydi
(``telegram_posted_at`` belgilanadi). Kanalga kerakli maqolani admin'dan yoki ``--only <id> --telegram`` bilan yuboring.
"""

import datetime
import importlib
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

MODULES = ("blog.rewrites.project_posts_tests", "blog.rewrites.project_posts_tools")
DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)
LANG_FIELDS = {"uz": "uz_uz", "ru": "ru_ru", "en": "en_us"}

# Ataylab maqola yozilmagan loyihalar (hisobotda sababi bilan körsatiladi)
SKIPPED = {
    10: "YouTube yuklovçi: Google AdSense siyosati YouTube'dan yuklab olişni targ'ib qiluvçi kontentga reklamani "
        "çeklaydi — blogda reklama qilinmaydi.",
    27: "BTC Markets (/cryptomarket/): ma'lumot manbai TradeOgre birjasi 2025-yilda yopilgan, sahifa böş.",
}

_MARK = re.compile(r"\[\[(.+?)\]\]")


def _articles():
    articles = []
    for name in MODULES:
        articles += importlib.import_module(name).ARTICLES
    return articles


def _plain(text):
    return _MARK.sub(r"\1", text).strip()


def _cyr_plain(text):
    """Oddiy matnli maydon (nom, sarlavha): [[...]] qismlar lotinça qoladi, qolgani kirillga ögiriladi."""
    from core.translit import latin_to_cyrillic

    parts, pos = [], 0
    for m in _MARK.finditer(text):
        parts.append(latin_to_cyrillic(text[pos:m.start()]))
        parts.append(m.group(1))
        pos = m.end()
    parts.append(latin_to_cyrillic(text[pos:]))
    return "".join(parts).strip()


def _html(text):
    """HTML matn: [[...]] -> <span translate="no"> (ögirgiç va Google Translate unga tegmaydi)."""
    return _MARK.sub(r'<span translate="no">\1</span>', text).strip()


def build_fields(article):
    from core.translit import latin_to_cyrillic

    fields = {
        "seo_title": _plain(article["seo_title"])[:70],
        "seo_description": _plain(article["seo_description"])[:200],
        "source_url": article["source_url"],
    }
    for kind in ("name", "title"):
        for lang, sfx in LANG_FIELDS.items():
            fields[f"{kind}_{sfx}"] = _plain(article[kind][lang])
        fields[f"{kind}_uz_crl"] = _cyr_plain(article[kind]["uz"])
    for lang, sfx in LANG_FIELDS.items():
        fields[f"body_{sfx}"] = _html(article["body"][lang])
    fields["body_uz_crl"] = latin_to_cyrillic(fields["body_uz_uz"])
    return fields


def project_link(url):
    """Project.url (masalan "tests?topic_id=1") -> maqoladagi havola ("/tests/?topic_id=1")."""
    path, _, query = url.strip("/").partition("?")
    return f"/{path.strip('/')}/" + (f"?{query}" if query else "")


class Command(BaseCommand):
    help = "/projects/ dagi loyihalar uçun blog maqolalarini naşr qiladi (har bir loyihaga kamida bitta)."

    def add_arguments(self, parser):
        parser.add_argument("--report", action="store_true", help="Faqat hisobot: qaysi loyihada maqola yöq")
        parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmasdan körsatiş")
        parser.add_argument("--update", action="store_true", help="Mavjud maqolalar matnini ham yangilaş")
        parser.add_argument("--only", help="Faqat şu loyiha (Project.id) yoki maqola slug'i")
        parser.add_argument("--draft", action="store_true", help="Qoralama (2099-yil) sifatida saqlaş")
        parser.add_argument("--telegram", action="store_true", help="Naşr qilinganda Telegram kanalga ham yuboriş")

    def handle(self, *args, **opts):
        from blog.models import Posts
        from projects.models import Project

        if opts["report"]:
            return self.report()

        articles = _articles()
        if opts["only"]:
            articles = [a for a in articles if opts["only"] in (str(a["project_id"]), a["slug"])]
            if not articles:
                raise CommandError(f"Maqola topilmadi: {opts['only']}")

        active = set(Project.actives.values_list("id", flat=True))
        superuser = None
        created = updated = 0
        for article in articles:
            slug = article["slug"]
            if article["project_id"] not in active:
                self.stdout.write(self.style.WARNING(f"- {slug}: loyiha #{article['project_id']} faol emas — ötkazildi."))
                continue
            fields = build_fields(article)
            post = Posts.objects.filter(slug=slug).first()
            if post and not opts["update"]:
                self.stdout.write(f"= {slug}: mavjud (yangilaş: --update)")
                continue
            action = "~ yangilanadi" if post else "+ yaratiladi"
            self.stdout.write(f"{action}: /blog/{slug}/ — {fields['name_uz_uz']}")
            if opts["dry_run"]:
                continue

            image = article.get("image") or ""
            if image and not (Path(settings.MEDIA_ROOT) / image).exists():
                self.stdout.write(self.style.WARNING(f"  rasm topilmadi: media/{image} — rasmsiz saqlanadi."))
                image = ""
            if post is None:
                if superuser is None:
                    from django.contrib.auth.models import User

                    superuser = User.objects.filter(is_superuser=True).order_by("id").first()
                    if superuser is None:
                        raise CommandError("Superuser topilmadi (maqola muallifi uçun kerak).")
                post = Posts(slug=slug, created_by=superuser, categorie_id=article["categorie_id"],
                             publish_time=DRAFT_TIME if opts["draft"] else timezone.now())
                if not opts["telegram"]:
                    post.telegram_posted_at = timezone.now()  # blog signali kanalga yubormasin
                created += 1
            else:
                updated += 1
            for name, value in fields.items():
                setattr(post, name, value)
            if image:
                post.image = image
            post.save()

        if not opts["dry_run"]:
            try:
                from django.core.cache import cache

                cache.clear()
            except Exception:
                pass
            self.stdout.write(self.style.SUCCESS(f"Yaratildi: {created}, yangilandi: {updated}."))
        self.report()

    def report(self):
        """Har bir faol loyiha uçun: maqolada uning sahifasiga havola bormi."""
        from blog.models import Posts
        from projects.models import Project

        posts = list(Posts.objects.filter(is_deleted=False).values_list("slug", "body_uz_uz", "source_url"))
        self.stdout.write("\n/projects/ loyihalari va blog maqolalari:")
        missing = 0
        for project in Project.actives.order_by("order"):
            link = project_link(project.url)
            slugs = [s for s, body, src in posts if link in (body or "") or link in (src or "")]
            if slugs:
                self.stdout.write(f"  ✓ #{project.id} {project.title[:40]:40} {link:22} → {', '.join(slugs[:2])}")
            elif project.id in SKIPPED:
                self.stdout.write(self.style.WARNING(f"  · #{project.id} {project.title[:40]:40} {link:22} ataylab yozilmagan: {SKIPPED[project.id]}"))
            else:
                missing += 1
                self.stdout.write(self.style.ERROR(f"  ✗ #{project.id} {project.title[:40]:40} {link:22} maqola yöq"))
        self.stdout.write(self.style.SUCCESS("Barça loyihalarda maqola bor.") if not missing
                          else self.style.WARNING(f"{missing} ta loyihada maqola yöq."))
