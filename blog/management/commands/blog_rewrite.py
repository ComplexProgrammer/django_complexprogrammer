"""Blog maqolalarini yangilangan matn bilan almashtirish (slug va nashr sanasi o'zgarmaydi) yoki yangisini yaratish.

    python manage.py blog_rewrite games_2026 --dry-run   # nima o'zgarishini ko'rsatadi
    python manage.py blog_rewrite games_2026             # almashtiradi (eski matn zaxiraga saqlanadi)
    python manage.py blog_rewrite sudoku_app             # bazada yo'q maqolani qoralama sifatida yaratadi
    python manage.py blog_rewrite --restore tmp/blog_backup/games_2026-20261020-120000.json   # orqaga qaytarish

Matnlar ``blog/rewrites/<modul>.py`` dagi ARTICLES ro'yxatida. Kirillcha (uz_crl) matn lotinchadan avtomatik o'giriladi.
Telegram kanalga qayta yuborilmaydi: avval yuborilgan maqolada ``telegram_posted_at`` to'ldirilgan bo'ladi.

Maqolada ``"create": {"categorie_id": ..., "image": ...}`` bo'lsa va u bazada topilmasa, yangi maqola yaratiladi.
U saytda ko'rinmaydi (nashr sanasi 2099-yil): admin'da tekshirib, «Publish time»ni bugungi sanaga o'zgartiring —
shunda saytda chiqadi va Telegram kanalga yuboriladi. ``--publish`` bilan darhol nashr qilinadi.
"""

import datetime
import importlib
import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from blog.models import Posts
from core.translit import latin_to_cyrillic

FIELD = {"uz": "uz_uz", "ru": "ru_ru", "en": "en_us"}
TEXT_FIELDS = [f"{kind}_{sfx}" for kind in ("name", "title", "body") for sfx in ("uz_uz", "uz_crl", "ru_ru", "en_us")]
BACKUP_FIELDS = TEXT_FIELDS + ["seo_title", "seo_description"]
BACKUP_DIR = Path(settings.BASE_DIR) / "tmp" / "blog_backup"
DRAFT_TIME = datetime.datetime(2099, 1, 1, tzinfo=datetime.timezone.utc)


def _fields(article):
    data = {"seo_title": article["seo_title"][:70], "seo_description": article["seo_description"][:200]}
    for kind in ("name", "title", "body"):
        for lang, sfx in FIELD.items():
            data[f"{kind}_{sfx}"] = article[kind][lang]
        data[f"{kind}_uz_crl"] = latin_to_cyrillic(article[kind]["uz"])
    return data


class Command(BaseCommand):
    help = "Blog maqolalarini blog/rewrites/<modul>.py dagi yangi matn bilan almashtirish (zaxira bilan)."

    def add_arguments(self, parser):
        parser.add_argument("module", nargs="?", help="blog/rewrites ichidagi modul nomi, masalan games_2026")
        parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmasdan ko'rsatish")
        parser.add_argument("--restore", help="Zaxira JSON faylidan eski matnni qaytarish")
        parser.add_argument("--publish", action="store_true", help="Yangi yaratilgan maqolani qoralama emas, darhol nashr qilish")

    def handle(self, *args, **opts):
        if opts["restore"]:
            return self.restore(Path(opts["restore"]))
        if not opts["module"]:
            raise CommandError("Modul nomini bering, masalan: manage.py blog_rewrite games_2026")
        try:
            module = importlib.import_module(f"blog.rewrites.{opts['module']}")
        except ImportError as e:
            raise CommandError(f"blog/rewrites/{opts['module']}.py topilmadi") from e

        backup, changed = {}, []
        for article in module.ARTICLES:
            post = Posts.objects.filter(slug=article["slug"]).first()
            if post is None and "create" in article:
                self.create(article, opts)
                continue
            if post is None:
                self.stdout.write(self.style.WARNING(f"? {article['slug']}: maqola topilmadi — o'tkazib yuborildi."))
                continue
            new = _fields(article)
            self.stdout.write(f"~ {article['slug']}: «{post.name_uz_uz}» → «{new['name_uz_uz']}»")
            if opts["dry_run"]:
                continue
            backup[article["slug"]] = {f: getattr(post, f) for f in BACKUP_FIELDS}
            for name, value in new.items():
                setattr(post, name, value)
            changed.append(post)

        if opts["dry_run"] or not changed:
            return
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        path = BACKUP_DIR / f"{opts['module']}-{timezone.now():%Y%m%d-%H%M%S}.json"
        path.write_text(json.dumps(backup, ensure_ascii=False, indent=1), encoding="utf-8")
        for post in changed:
            post.save()
        self.stdout.write(self.style.SUCCESS(f"{len(changed)} ta maqola yangilandi. Eski matn: {path}"))

    def create(self, article, opts):
        new = _fields(article)
        self.stdout.write(f"+ {article['slug']}: «{new['name_uz_uz']}» (yangi maqola)")
        if opts["dry_run"]:
            return
        author = User.objects.filter(is_superuser=True).order_by("id").first()
        if author is None:
            raise CommandError("Superuser topilmadi (maqola muallifi uchun kerak).")
        spec = article["create"]
        post = Posts(slug=article["slug"], created_by=author, categorie_id=spec["categorie_id"],
                     publish_time=timezone.now() if opts["publish"] else DRAFT_TIME, **new)
        image = spec.get("image")
        if image and (Path(settings.MEDIA_ROOT) / image).exists():
            post.image = image
        elif image:
            self.stdout.write(self.style.WARNING(f"  rasm topilmadi: media/{image} — admin'da qo'shing."))
        post.save()
        if opts["publish"]:
            self.stdout.write(self.style.SUCCESS(f"  Nashr qilindi: {post.get_absolute_url()}"))
        else:
            self.stdout.write(self.style.SUCCESS("  Qoralama yaratildi. Admin → Blog → Posts: matnni tekshirib, "
                                                 "«Publish time»ni bugungi sanaga o'zgartiring."))

    def restore(self, path):
        try:
            backup = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise CommandError(f"Zaxira faylini o'qib bo'lmadi: {e}") from e
        for slug, fields in backup.items():
            n = Posts.objects.filter(slug=slug).update(**{k: v for k, v in fields.items() if k in BACKUP_FIELDS})
            self.stdout.write(f"{'✓' if n else '?'} {slug}")
        self.stdout.write(self.style.SUCCESS("Eski matn qaytarildi."))
