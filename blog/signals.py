"""Yangi maqola nashr etilganda Telegram kanalga avtomatik yuborish.

Faqat .env (yoki muhit o'zgaruvchilari)da berilgan bo'lsa ishlaydi:
    TELEGRAM_BOT_TOKEN   — @BotFather bergan token (bot kanalga admin qilingan bo'lishi kerak)
    TELEGRAM_CHANNEL_ID  — masalan ``@complexprogrammer`` yoki ``-100...``
Kelajak sanasi qo'yilgan maqola o'sha sanadan keyingi birinchi saqlashda yuboriladi.
"""

import logging
import threading
from html import escape

import requests
from decouple import config
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from blog.models import Posts
from blog.utils import excerpt

log = logging.getLogger(__name__)
SITE_URL = "https://complexprogrammer.uz"


def _send(post_id, token, chat_id):
    post = Posts.objects.filter(pk=post_id).first()
    if post is None:
        return
    url = f"{SITE_URL}{post.get_absolute_url()}"
    text = f"<b>{escape(post.name_uz_uz)}</b>\n\n{escape(excerpt(post.title_uz_uz, 600))}\n\n👉 {url}"
    try:
        if post.image:
            with post.image.open("rb") as photo:
                r = requests.post(
                    f"https://api.telegram.org/bot{token}/sendPhoto",
                    data={"chat_id": chat_id, "caption": text[:1024], "parse_mode": "HTML"},
                    files={"photo": photo},
                    timeout=20,
                )
        else:
            r = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=20,
            )
        if r.ok:
            Posts.objects.filter(pk=post_id).update(telegram_posted_at=timezone.now())
        else:
            log.warning("Telegram post failed: %s %s", r.status_code, r.text[:200])
    except Exception:  # noqa: BLE001 — admin'dagi saqlashni hech qachon buzmasligi kerak
        log.exception("Telegram post failed")


@receiver(post_save, sender=Posts)
def post_to_telegram(sender, instance, **kwargs):
    token = config("TELEGRAM_BOT_TOKEN", default="")
    chat_id = config("TELEGRAM_CHANNEL_ID", default="")
    if not token or not chat_id:
        return
    if instance.is_deleted or instance.telegram_posted_at or instance.publish_time > timezone.now():
        return
    threading.Thread(target=_send, args=(instance.pk, token, chat_id), daemon=True).start()
