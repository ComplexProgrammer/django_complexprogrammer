"""IndexNow: yangi yoki o'zgargan sahifalarni Yandex va Bing'ga darhol xabar qilish (https://www.indexnow.org).

Kalit ochiq ma'lumot — ``/<kalit>.txt`` manzilida turadi va sayt egasi ekanimizni tasdiqlaydi.
Butun saytni yuborish: ``python manage.py indexnow_submit``.
"""

import logging
import threading
from urllib.parse import urlsplit

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from core.seo import SEO_LANGS, SITE_URL, lang_url

log = logging.getLogger(__name__)
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10000  # IndexNow bir so'rovda ko'pi bilan 10 000 manzil qabul qiladi


def key():
    return settings.INDEXNOW_KEY


def submit(urls):
    """Manzillarni yuboradi (bloklaydi). Muvaffaqiyatli yuborilganlar sonini qaytaradi."""
    urls = [u for u in dict.fromkeys(urls) if u.startswith(SITE_URL)]
    sent = 0
    for i in range(0, len(urls), BATCH):
        chunk = urls[i:i + BATCH]
        try:
            r = requests.post(ENDPOINT, json={
                "host": urlsplit(SITE_URL).netloc,
                "key": key(),
                "keyLocation": f"{SITE_URL}/{key()}.txt",
                "urlList": chunk,
            }, timeout=30)
            if r.status_code in (200, 202):
                sent += len(chunk)
            else:
                log.warning("IndexNow: %s %s", r.status_code, r.text[:200])
        except requests.RequestException:
            log.exception("IndexNow yuborilmadi")
    return sent


def submit_paths(paths):
    """Prefikssiz manzillarni (``/blog/slug/``) barcha til versiyalari bilan fonda yuboradi."""
    if settings.DEBUG or not key():
        return
    urls = [lang_url(path, lang) for path in paths for lang in SEO_LANGS]
    threading.Thread(target=submit, args=(urls,), daemon=True).start()


def _connect():
    from blog.models import Posts as BlogPost
    from news.models import Posts as NewsPost
    from tests.models import RoadSigns

    @receiver(post_save, sender=BlogPost, dispatch_uid="indexnow_blog")
    def blog_saved(sender, instance, **kwargs):
        if not instance.is_deleted and instance.publish_time <= timezone.now():
            submit_paths([instance.get_absolute_url(), "/blog/"])

    @receiver(post_save, sender=NewsPost, dispatch_uid="indexnow_news")
    def news_saved(sender, instance, **kwargs):
        if not instance.is_deleted:
            submit_paths([instance.get_absolute_url(), "/news/"])

    @receiver(post_save, sender=RoadSigns, dispatch_uid="indexnow_sign")
    def sign_saved(sender, instance, **kwargs):
        if not instance.is_deleted:
            submit_paths([f"/yol-belgilari/{instance.pk}/", "/yol-belgilari/"])
