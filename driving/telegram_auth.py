"""Telegram Login Widget va Mini App ma'lumotlarini tekşiriş:
https://core.telegram.org/widgets/login#checking-authorization
https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""

import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from django.conf import settings

# Bizning manzil parametrlarimiz — Telegram imzosiga kirmaydi
OWN_PARAMS = {"hash", "next", "welcome", "login"}
# Telegram Login Widget imzolaydigan standart maydonlar (URL'ga begona utm/yclid/gclid qöşilib qolsa ham işlaşi uçun)
WIDGET_KNOWN_KEYS = {"id", "first_name", "last_name", "username", "photo_url", "auth_date"}


def _iter_tokens(bot_token):
    """Berilgan bot_token va settings.TELEGRAM_BOT_TOKENS içidan barça toza tokenlarni qaytaradi."""
    raw = []
    if isinstance(bot_token, (list, tuple, set)):
        raw.extend(bot_token)
    elif bot_token:
        raw.append(bot_token)
    raw.extend(getattr(settings, "TELEGRAM_BOT_TOKENS", ()))
    seen = set()
    for t in raw:
        cleaned = (t or "").strip().strip("'\"")
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            yield cleaned


def verify(params, bot_token):
    """Töğri imzolangan bölsa Telegram ma'lumotlari (dict), aks holda ``None``."""
    if not params:
        return None
    received = (params.get("hash") or "").strip()
    user_id = str(params.get("id", "")).strip()
    if not received or not user_id.isdigit():
        return None

    try:
        if int(params.get("auth_date", 0)) <= 0:
            return None
    except (ValueError, TypeError):
        return None

    # 1-variant: OWN_PARAMS dan taşqari barça parametrlar
    data_primary = {k: str(v) for k, v in params.items() if k not in OWN_PARAMS}
    # 2-variant: faqat Telegram Login Widget'ning öz maydonlari (agar URL'da begona query parametr bölsa)
    data_strict = {k: str(v) for k, v in params.items() if k in WIDGET_KNOWN_KEYS}

    for candidate_data in (data_primary, data_strict):
        check_string = "\n".join(f"{k}={candidate_data[k]}" for k in sorted(candidate_data))
        for token in _iter_tokens(bot_token):
            secret = hashlib.sha256(token.encode()).digest()
            expected = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(expected, received):
                return candidate_data

    return None


def verify_webapp(init_data, bot_token):
    """Telegram Mini App ``initData`` imzosini tekşiradi.

    Töğri bölsa foydalanuvçi ma'lumotlari (id, first_name, ...), aks holda ``None``.
    """
    if not init_data or not isinstance(init_data, str):
        return None

    raw = init_data.strip().lstrip("#?")
    # Agar location.hash töliq yuborilgan bölsa (tgWebAppData=...), içki qiymatni ajratib olamiz
    if "tgWebAppData=" in raw:
        outer = dict(parse_qsl(raw, keep_blank_values=True))
        if outer.get("tgWebAppData"):
            raw = outer["tgWebAppData"]

    params = dict(parse_qsl(raw, keep_blank_values=True))
    received = (params.pop("hash", "") or "").strip()
    if not received:
        return None

    check_string = "\n".join(f"{k}={params[k]}" for k in sorted(params))
    matched = False
    for token in _iter_tokens(bot_token):
        secret = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
        expected = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, received):
            matched = True
            break

    if not matched:
        return None

    try:
        if int(params.get("auth_date", 0)) <= 0:
            return None
        user = json.loads(params.get("user", "{}"))
    except (ValueError, TypeError):
        return None

    if not isinstance(user, dict) or not str(user.get("id", "")).isdigit():
        return None
    return {k: str(v) for k, v in user.items() if k in ("id", "first_name", "last_name", "username", "photo_url")}
