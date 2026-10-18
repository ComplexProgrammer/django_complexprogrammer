import tempfile

from django.core.management.base import BaseCommand

from driving import pdf


class Command(BaseCommand):
    help = "Avtotest savollari va javoblari PDF fayllarini (uz, ru) media/avtotest/ ga qayta yaratadi."

    def handle(self, *args, **options):
        with tempfile.TemporaryDirectory() as images:
            pdf._compressed_images(images)  # ikkala til uchun bir marta
            for lang in pdf.TEXT:
                path = pdf.build(lang, images_dir=images)
                self.stdout.write(self.style.SUCCESS(f"{path} — {path.stat().st_size / 1024 / 1024:.1f} MB"))
