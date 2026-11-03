"""AvtoTest'ni /tests/ dagi 49 va 50-kitoblardan töliq qayta hosil qiliş (yagona manba — tests).

    python manage.py sync_avtotest            # yozadi
    python manage.py sync_avtotest --dry-run  # faqat nima özgarişini körsatadi
    python manage.py sync_avtotest --bilet 136

Odatda kerak emas: admin'dagi har bir özgariş signal orqali avtomatik sinxronlanadi.
``QuerySet.update()`` yoki skript bilan ommaviy özgartirişdan keyin işga tuşiring.
"""
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import transaction

from projects.avtotest_sync import builder
from projects.signals import CACHE_KEYS


class Command(BaseCommand):
    help = "AvtoTest'ni /tests/ dagi 49/50-kitoblardan qayta yozadi (yagona manba — tests)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmaydi, faqat hisobot.")
        parser.add_argument("--bilet", type=int, action="append", help="Faqat şu bilet(lar).")

    def handle(self, *args, dry_run=False, bilet=None, **options):
        b = builder(dry_run=dry_run)
        with transaction.atomic():
            if bilet:
                for number in bilet:
                    b.sync_bilet(number)
            else:
                b.sync_all()
        if not dry_run:
            cache.delete_many(CACHE_KEYS)
        prefix = "[dry-run] " if dry_run else ""
        for key, value in b.stats.items():
            self.stdout.write(f"{prefix}{key}: {value}")
        for number, raqam, reason in b.problems:
            self.stdout.write(self.style.WARNING(
                f"{prefix}{number}-bilet {raqam}-savol AvtoTest'ga yozilmadi: {reason} — Tests → Questions'da tuzating."
            ))
