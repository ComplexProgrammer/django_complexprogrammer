"""Telegram Login Widget ma'lumotlarini tekshirish: https://core.telegram.org/widgets/login#checking-authorization"""

import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

MAX_AGE = 24 * 3600
# Bizning manzil parametrlarimiz — Telegram imzosiga kirmaydi
OWN_PARAMS = {"hash", "next"}


def verify(params, bot_token):
    """To'g'ri imzolangan bo'lsa Telegram ma'lumotlari (dict), aks holda ``None``."""
    received = params.get("hash", "")
    if not bot_token or not received or not params.get("id", "").isdigit():
        return None
    data = {k: v for k, v in params.items() if k not in OWN_PARAMS}
    check_string = "\n".join(f"{k}={data[k]}" for k in sorted(data))
    secret = hashlib.sha256(bot_token.encode()).digest()
    expected = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, received):
        return None
    try:
        if time.time() - int(data.get("auth_date", 0)) > MAX_AGE:
            return None
    except ValueError:
        return None
    return data


def verify_webapp(init_data, bot_token):
    """Telegram Mini App ``initData`` (https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app).

    To'g'ri bo'lsa foydalanuvchi ma'lumotlari (id, first_name, ...), aks holda ``None``.
    """
    if not bot_token or not init_data:
        return None
    params = dict(parse_qsl(init_data, keep_blank_values=True))
    received = params.pop("hash", "")
    check_string = "\n".join(f"{k}={params[k]}" for k in sorted(params))
    secret = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    expected = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
    if not received or not hmac.compare_digest(expected, received):
        return None
    try:
        if time.time() - int(params.get("auth_date", 0)) > MAX_AGE:
            return None
        user = json.loads(params.get("user", "{}"))
    except ValueError:
        return None
    if not isinstance(user, dict) or not str(user.get("id", "")).isdigit():
        return None
    return {k: str(v) for k, v in user.items() if k in ("id", "first_name", "last_name", "username", "photo_url")}
