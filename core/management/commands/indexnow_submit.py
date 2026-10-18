import html
import re

from django.core.management.base import BaseCommand

from core import indexnow
from core.views import build_sitemap


class Command(BaseCommand):
    help = "Sitemap'dagi barcha manzillarni IndexNow (Yandex, Bing) ga yuboradi. Katta o'zgarishlardan keyin bir marta ishga tushiring."

    def handle(self, *args, **options):
        urls = [html.unescape(u) for u in re.findall(r"<loc>(.*?)</loc>", build_sitemap())]
        sent = indexnow.submit(urls)
        self.stdout.write(self.style.SUCCESS(f"IndexNow: {sent}/{len(urls)} ta manzil yuborildi."))
