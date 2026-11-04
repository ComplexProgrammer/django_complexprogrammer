"""Barça AI izoh qoralamalarini tasdiqlaş (saytda körsatiş) — admin'dagi «Izohni tasdiqlaş» amalining ommaviy varianti.

    python manage.py approve_explanations --dry-run       # nečtasi tasdiqlanişini körsatadi, hečnarsa özgarmaydi
    python manage.py approve_explanations                 # barça qoralamalar
    python manage.py approve_explanations --skip-low      # past ishonçli (low) qoralamalar qoladi — qöl bilan tekşiriş uçun
    python manage.py approve_explanations --book 49       # faqat şu kitob (49 — Avto Test, 50 — e-avtomaktab)

Faqat izoh matni bor qoralamalar tasdiqlanadi. Qaytariş: admin → Tests → Questions → «Izohni qoralamaga qaytariş».
"""

from collections import Counter

from django.core.management.base import BaseCommand
from django.db import transaction

from projects.signals import sync_bilets, topic_bilets
from tests.models import Questions


class Command(BaseCommand):
    help = "Barça izoh qoralamalarini (explanation_status='draft') tasdiqlaydi va /avtotest/ ga sinxronlaydi."

    def add_arguments(self, parser):
        parser.add_argument("--skip-low", action="store_true", help="Past ishonçli (low) qoralamalarni tasdiqlamaslik")
        parser.add_argument("--book", type=int, help="Faqat şu kitob savollari")
        parser.add_argument("--dry-run", action="store_true", help="Hečnarsani özgartirmasdan sonini körsatiş")

    def handle(self, *args, **opts):
        qs = Questions.objects.filter(explanation_status="draft", is_deleted=False).exclude(explanation_uz_uz="")
        if opts["book"]:
            qs = qs.filter(topic__book_id=opts["book"])
        by_confidence = Counter(qs.values_list("explanation_confidence", flat=True))
        if opts["skip_low"]:
            qs = qs.exclude(explanation_confidence="low")
        total = qs.count()
        summary = ", ".join(f"{k or '—'}: {v}" for k, v in sorted(by_confidence.items())) or "yöq"
        self.stdout.write(f"Qoralamalar (ishonç böyiça): {summary}")
        if not total:
            self.stdout.write("Tasdiqlanadigan qoralama yöq.")
            return
        if opts["dry_run"]:
            self.stdout.write(f"{total} ta qoralama tasdiqlanadi (--dry-run: hečnarsa özgarmadi).")
            return
        topic_ids = set(qs.values_list("topic_id", flat=True))
        with transaction.atomic():
            n = qs.update(explanation_status="approved")
        sync_bilets(*topic_bilets(topic_ids))  # update() signal yubormaydi — /avtotest/ sahifalari ham yangilansin
        left = by_confidence.get("low", 0) if opts["skip_low"] else 0
        self.stdout.write(self.style.SUCCESS(
            f"{n} ta izoh tasdiqlandi va saytda körinadi."
            + (f" {left} ta past ishonçli qoralama qoldi (admin → «Qoralama» filtri)." if left else "")
        ))
