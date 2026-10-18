"""Asosiy sahifalar ishlayotganini tekshirish: ``python manage.py smoke_check``.

2026-10-10..12 da sayt bir necha kun xato berib, Google'dan trafik nolga tushgan (Search Console). Deploy'dan keyin
shu buyruq bilan tekshirilsa, bunday holat darhol ko'rinadi. Xato bo'lsa chiqish kodi 1.
"""

from django.core.management.base import BaseCommand
from django.test import Client
from django.test.utils import override_settings

from blog.models import Posts

PATHS = [
    "/", "/avtotest/", "/avtotest/1/", "/avtotest/1/1/", "/avtotest/imtihon/", "/avtotest/mavzular/",
    "/avtotest/pdf/", "/avtotest/kun-savoli/", "/yol-belgilari/", "/tests/", "/blog/", "/news/", "/projects/",
    "/translate/", "/search/?q=avto", "/sitemap.xml", "/robots.txt", "/ru/avtotest/", "/en/",
]


class Command(BaseCommand):
    help = "Asosiy sahifalarni (va eng ko'p o'qilgan maqolalarni) ochib, 200 qaytarayotganini tekshiradi."

    def handle(self, *args, **options):
        paths = list(PATHS)
        # Trafikning asosiy qismi bloglardan keladi — eng ko'p o'qilgan 5 ta maqola ham tekshiriladi
        paths += [p.get_absolute_url() for p in Posts.published().order_by("-view_count")[:5]]
        client = Client(HTTP_HOST="complexprogrammer.uz", HTTP_USER_AGENT="smoke-check")
        failed = 0
        with override_settings(SECURE_SSL_REDIRECT=False):
            for path in paths:
                try:
                    status = client.get(path, secure=True).status_code
                except Exception as e:  # noqa: BLE001 — har qanday xato ro'yxatga tushsin
                    status = f"{type(e).__name__}: {e}"[:120]
                ok = status == 200
                failed += not ok
                self.stdout.write(f"{'OK ' if ok else 'XATO'} {status}  {path}")
        if failed:
            self.stderr.write(self.style.ERROR(f"{failed} ta sahifa ishlamayapti!"))
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS(f"Hammasi joyida: {len(paths)} ta sahifa."))
