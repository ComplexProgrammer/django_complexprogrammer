"""Telegram Login Widget ma'lumotlarini tekshirish: https://core.telegram.org/widgets/login#checking-authorization"""

import hashlib
import hmac
import time

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
