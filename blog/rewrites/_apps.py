"""Google Play ilovalari haqidagi maqolalar uchun umumiy HTML bloklari (blog.css: .b-shots, .b-app, .b-btn)."""

GP = '<span translate="no">Google Play</span>'
SITE = '<a href="/" translate="no">complexprogrammer.uz</a>'
TG_CHANNEL = "https://t.me/complexprogrammeruzchannel"


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def shots(folder, items, lang, width=480, height=1067):
    """Skrinshotlar to'plami: items = [(fayl, {"uz": izoh, ...}), ...]."""
    figs = "".join(
        f'<figure><img src="{folder}{f}" alt="{cap[lang]}" loading="lazy" decoding="async" width="{width}" height="{height}">'
        f"<figcaption>{cap[lang]}</figcaption></figure>"
        for f, cap in items
    )
    return f'<div class="b-shots">{figs}</div>'


def app_box(name_html, icon, play_url, meta, lang):
    """name_html: brend qismi <span translate="no"> ichida bo'lgan ilova nomi."""
    # Ichida <p> yo'q: split_for_ad matnni 3-</p> dan keyin bo'ladi, blok o'rtasidan bo'linib qolmasin
    btn = {"uz": f"{GP}dan yuklab olish", "ru": f"Скачать в {GP}", "en": f"Get it on {GP}"}[lang]
    return (f'<div class="b-app"><img src="{icon}" alt="" width="72" height="72">'
            f'<div><strong>{name_html}</strong><span>{meta[lang]}</span></div>'
            f'<a class="b-btn" href="{play_url}" target="_blank" rel="noopener">{btn}</a></div>')


def youtube(video_id, title):
    return (f'<iframe src="https://www.youtube-nocookie.com/embed/{video_id}" width="560" height="315" '
            f'title="{title}" allowfullscreen></iframe>')
