"""Bazadagi eski izohlarni tozalaş: havolali/reklama spamni va takroriy izohlarni yaşiriş (öçirmaydi).

Yaşirilgan izohlar admin panelda "Yaşirilgan (spam)" holatida qoladi va kerak bölsa qayta tasdiqlanadi.

Işlatiş:
    python manage.py moderate_comments           # Tekşiriş (bazaga yozmaydi)
    python manage.py moderate_comments --apply   # Saqlaş
"""

from django.core.management.base import BaseCommand

from comments.models import Comment
from comments.moderation import spam_reason


class Command(BaseCommand):
    help = "Eski spam va takroriy izohlarni yaşiriş"

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true")

    def handle(self, *args, **options):
        spam, dupes, seen = [], [], set()
        qs = Comment.objects.filter(status=Comment.Status.APPROVED).order_by("created_at", "id")
        for c in qs.iterator(chunk_size=500):
            if c.is_official:
                continue
            reason = spam_reason(c.text, c.username)
            if reason:
                spam.append((c.pk, reason))
                continue
            key = (c.page_url, c.parent_id, " ".join(c.text.lower().split()))
            if key in seen:
                dupes.append(c.pk)  # birinçisi qoladi, takrorlari yaşiriladi
            else:
                seen.add(key)

        self.stdout.write(f"Spam (havola/reklama): {len(spam)} ta")
        for pk, reason in spam[:10]:
            self.stdout.write(f"  #{pk}: {reason} — {Comment.objects.get(pk=pk).text[:80]!r}")
        self.stdout.write(f"Takroriy izohlar: {len(dupes)} ta")

        if not options["apply"]:
            self.stdout.write(self.style.WARNING("Tekşiruv rejimi. Saqlaş uçun: --apply"))
            return
        for pk, reason in spam:
            Comment.objects.filter(pk=pk).update(status=Comment.Status.HIDDEN, moderation_note=reason)
        Comment.objects.filter(pk__in=dupes).update(status=Comment.Status.HIDDEN, moderation_note="takror")
        self.stdout.write(self.style.SUCCESS(f"Yaşirildi: {len(spam) + len(dupes)} ta izoh"))
