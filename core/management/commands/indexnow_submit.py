import html
import re

from django.core.management.base import BaseCommand, CommandError

from core import indexnow
from core.views import SITEMAP_SLUGS, build_sitemap


class Command(BaseCommand):
    help = (
        "Sitemap'dagi manzillarni IndexNow (Yandex, Bing) ga yuboradi. Katta özgarişlardan keyin bir marta işga tuşiring. "
        "Masalan, izohlar tasdiqlangandan keyin: manage.py indexnow_submit --section savollar"
    )

    def add_arguments(self, parser):
        sections = sorted(set(SITEMAP_SLUGS.values()) | {"sahifalar"})
        parser.add_argument("--section", choices=sections, help="Faqat şu sitemap bölimi (/sitemap-<bölim>.xml)")
        parser.add_argument("--dry-run", action="store_true", help="Yubormasdan sonini körsatiş")

    def handle(self, *args, **options):
        urls = [html.unescape(u) for u in re.findall(r"<loc>(.*?)</loc>", build_sitemap(options["section"]))]
        if not urls:
            raise CommandError("Yuboriladigan manzil topilmadi.")
        if options["dry_run"]:
            self.stdout.write(f"{len(urls)} ta manzil yuboriladi, masalan: {urls[0]}")
            return
        sent = indexnow.submit(urls)
        self.stdout.write(self.style.SUCCESS(f"IndexNow: {sent}/{len(urls)} ta manzil yuborildi."))
