from django.conf import settings
from django.core.management.base import BaseCommand

from core.views import build_sitemap


class Command(BaseCommand):
    help = "static/sitemap.xml faylini /sitemap.xml bilan bir xil qilib qayta yozadi (bazadagi joriy sahifalar asosida)."

    def handle(self, *args, **options):
        path = settings.BASE_DIR / "static" / "sitemap.xml"
        xml = build_sitemap()
        path.write_text(xml, encoding="utf-8", newline="")  # Windows'da ham \n qolsin
        self.stdout.write(self.style.SUCCESS(f"{path} yozildi: {xml.count('<url>')} ta URL"))
