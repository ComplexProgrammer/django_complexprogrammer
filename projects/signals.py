"""tests (kitob 49/50) özgarganda AvtoTest nusxasini yangilaş — ``projects/avtotest_sync.py``.

Admin'da bilet, savol yoki javob saqlansa/öçirilsa, tegişli bilet tranzaksiya tugagandan söng
AvtoTest'ga qayta yoziladi. ``QuerySet.update()`` / ``bulk_create`` signal yubormaydi: ulardan keyin
``sync_bilets()`` ni çaqiring yoki ``python manage.py sync_avtotest`` ni işga tuşiring.
"""
import logging

from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch import receiver

from projects.avtotest_sync import SYNCED_BOOK_IDS, bilet_for
from tests.models import Answers, Questions, Topics

log = logging.getLogger(__name__)
CACHE_KEYS = ("avtotest:bilet_sizes", "home:avtotest_stats")


def sync_bilets(*bilets):
    """Berilgan AvtoTest biletlarini tranzaksiya tugagandan söng tests'dan qayta yozadi."""
    bilets = {b for b in bilets if b}
    if not bilets:
        return

    def run():
        from projects.avtotest_sync import builder

        cache.delete_many(CACHE_KEYS)
        try:
            b = builder()
            for bilet in sorted(bilets):
                b.sync_bilet(bilet)
            for bilet, raqam, reason in b.problems:
                log.warning("AvtoTest'ga yozilmadi: %s-bilet %s-savol — %s", bilet, raqam, reason)
        except Exception:  # sinxronlaş xatosi admin'dagi saqlaşni buzmasin
            log.exception("tests -> AvtoTest sinxronlaşda xato (biletlar: %s)", sorted(bilets))

    transaction.on_commit(run)


def topic_bilets(topic_ids):
    rows = Topics.objects.filter(pk__in=[t for t in topic_ids if t], book_id__in=SYNCED_BOOK_IDS)
    return {bilet_for(book_id, number) for book_id, number in rows.values_list("book_id", "number")}


def question_bilets(question_ids):
    topic_ids = Questions.objects.filter(pk__in=[q for q in question_ids if q]).values_list("topic_id", flat=True)
    return topic_bilets(topic_ids)


# --- Topics (bilet) ----------------------------------------------------------------------------
@receiver(post_init, sender=Topics)
def _topic_init(sender, instance, **kwargs):
    instance._sync_orig = (instance.book_id, instance.number) if instance.pk else None


@receiver(post_save, sender=Topics)
@receiver(post_delete, sender=Topics)
def _topic_changed(sender, instance, raw=False, **kwargs):
    if raw:  # loaddata
        return
    sync_bilets(bilet_for(instance.book_id, instance.number), bilet_for(*(instance._sync_orig or (None, None))))
    instance._sync_orig = (instance.book_id, instance.number)


# --- Questions ---------------------------------------------------------------------------------
@receiver(post_init, sender=Questions)
def _question_init(sender, instance, **kwargs):
    instance._sync_orig = instance.topic_id if instance.pk else None


@receiver(post_save, sender=Questions)
@receiver(post_delete, sender=Questions)
def _question_changed(sender, instance, raw=False, **kwargs):
    if raw:
        return
    sync_bilets(*topic_bilets({instance.topic_id, instance._sync_orig}))
    instance._sync_orig = instance.topic_id


# --- Answers -----------------------------------------------------------------------------------
@receiver(post_init, sender=Answers)
def _answer_init(sender, instance, **kwargs):
    instance._sync_orig = instance.question_id if instance.pk else None


@receiver(post_save, sender=Answers)
@receiver(post_delete, sender=Answers)
def _answer_changed(sender, instance, raw=False, **kwargs):
    if raw:
        return
    sync_bilets(*question_bilets({instance.question_id, instance._sync_orig}))
    instance._sync_orig = instance.question_id
