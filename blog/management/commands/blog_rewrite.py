"""Mavjud blog maqolalarini yangilangan matn bilan almashtirish (slug va nashr sanasi o'zgarmaydi).

    python manage.py blog_rewrite games_2026 --dry-run   # nima o'zgarishini ko'rsatadi
    python manage.py blog_rewrite games_2026             # almashtiradi (eski matn zaxiraga saqlanadi)
    python manage.py blog_rewrite --restore tmp/blog_backup/games_2026-20261020-120000.json   # orqaga qaytarish

Matnlar ``blog/rewrites/<modul>.py`` dagi ARTICLES ro'yxatida. Kirillcha (uz_crl) matn lotinchadan avtomatik o'giriladi.
Telegram kanalga qayta yuborilmaydi: avval yuborilgan maqolada ``telegram_posted_at`` to'ldirilgan bo'ladi.
"""

import importlib
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from blog.models import Posts
from core.translit import latin_to_cyrillic

FIELD = {"uz": "uz_uz", "ru": "ru_ru", "en": "en_us"}
TEXT_FIELDS = [f"{kind}_{sfx}" for kind in ("name", "title", "body") for sfx in ("uz_uz", "uz_crl", "ru_ru", "en_us")]
BACKUP_FIELDS = TEXT_FIELDS + ["seo_title", "seo_description"]
BACKUP_DIR = Path(settings.BASE_DIR) / "tmp" / "blog_backup"


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

    def restore(self, path):
        try:
            backup = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise CommandError(f"Zaxira faylini o'qib bo'lmadi: {e}") from e
        for slug, fields in backup.items():
            n = Posts.objects.filter(slug=slug).update(**{k: v for k, v in fields.items() if k in BACKUP_FIELDS})
            self.stdout.write(f"{'✓' if n else '?'} {slug}")
        self.stdout.write(self.style.SUCCESS("Eski matn qaytarildi."))
