"""2026-yilgi alifboga xato ögirilgan inglizça sözlarni tiklaş: Sçool -> School, Şe -> She, ÇANGE -> CHANGE.

``migrate_db_to_2026`` barça matnni özbekça deb hisoblagan: loyihalar sarlavhalari (inglizça), ingliz tili testlari
(savol, javob, mavzu) va inglizça izohlardagi sh/ch ham ş/ç ga aylanib qolgan. Bu buyruq faqat
``core.translit.ENGLISH_SH_CH_WORDS`` dagi sözlarni qaytaradi, özbekça sözlarga (çap, çoy, toş, şe’r) tegmaydi.

Işlatiş:
    python manage.py restore_english_2026            # Tekşiriş (bazaga yozmaydi)
    python manage.py restore_english_2026 --apply    # Bazaga saqlaş
"""

from django.apps import apps
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import transaction

from core.management.commands.migrate_db_to_2026 import MODEL_TARGETS
from core.translit import restore_english_2026

TARGETS = [(label, fields) for label, _path, fields in MODEL_TARGETS] + [
    ("projects.Project", ["title", "sub_title", "category"]),
]


class Command(BaseCommand):
    help = "2026-yilgi alifboga xato ögirilgan inglizça sözlarni (Sçool, Şooter) tiklaş."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Özgarişlarni bazaga saqlaş")
        parser.add_argument("--verbose-all", action="store_true", help="Barça özgarişlarni körsatiş")

    def handle(self, *args, **options):
        apply = options["apply"]
        show_all = options["verbose_all"]
        total = 0
        for label, fields in TARGETS:
            try:
                model = apps.get_model(label)
            except LookupError:
                continue
            fields = [f for f in fields if f in {x.name for x in model._meta.fields}]
            changed = []
            for obj in model.objects.only("pk", *fields).iterator(chunk_size=500):
                dirty = []
                for f in fields:
                    old = getattr(obj, f)
                    if isinstance(old, str):
                        new = restore_english_2026(old)
                        if new != old:
                            setattr(obj, f, new)
                            dirty.append((f, old, new))
                if dirty:
                    changed.append(obj)
                    if show_all or len(changed) <= 3:
                        for f, old, new in dirty:
                            self.stdout.write(f"  [{label} #{obj.pk} {f}] {old[:70]!r} -> {new[:70]!r}")
            if changed:
                self.stdout.write(self.style.SUCCESS(f"{label}: {len(changed)} ta yozuv"))
                total += len(changed)
                if apply:
                    with transaction.atomic():
                        model.objects.bulk_update(changed, fields, batch_size=200)
        if apply:
            cache.clear()
            self.stdout.write(self.style.SUCCESS(f"Tayyor: {total} ta yozuv tiklandi."))
        else:
            self.stdout.write(self.style.WARNING(f"Tekşiruv: {total} ta yozuv tiklanadi. Saqlaş uçun: --apply"))
