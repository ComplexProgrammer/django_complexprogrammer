"""SEO yordamchilari: sahifa meta'si, til versiyalari (hreflang) va strukturalangan ma'lumot (JSON-LD).

Til versiyalari: o'zbekcha — prefikssiz (``/avtotest/``), ruscha — ``/ru/avtotest/``,
inglizcha — ``/en/avtotest/``. Prefiksni ``core.middleware.LanguagePrefixMiddleware`` qayta ishlaydi.
"""

import json
import re

from core.seo_pages import BILET, LABELS, PAGES

SITE_URL = "https://complexprogrammer.uz"
DEFAULT_LANG = "uz"
# Qidiruv tizimlari alohida indekslaydigan tillar (tr matnlari asosan inglizcha — dublikat bo'lmasin)
SEO_LANGS = ("uz", "ru", "en")
PREFIX_LANGS = ("ru", "en")
OG_LOCALES = {"uz": "uz_UZ", "ru": "ru_RU", "en": "en_US", "tr": "tr_TR"}
# Indekslanmaydigan sahifalar (shaxsiy natijalar, qidiruv)
NOINDEX_PATHS = {"/search/", "/avtotest/xatolar/", "/tests/xatolar/", "/offline/", "/profil/", "/auth/telegram/", "/avtotest/imtihon/natija/"}
# canonical/hreflang'da saqlanadigan (sahifa mazmunini o'zgartiradigan) parametrlar
CANONICAL_PARAMS = ("id", "book_id", "categorie_id", "page")

ORG_SAME_AS = [
    "https://t.me/complexprogrammeruzchannel",
    "https://www.instagram.com/complexprogrammer",
    "https://www.facebook.com/complexprogrammer",
    "https://twitter.com/c0mplexprog",
    "https://github.com/complexprogrammer",
]

_BILET_RE = re.compile(r"/avtotest/(\d+)/")


def meta_lang(lang):
    return lang if lang in SEO_LANGS else "en"


def page_meta(path, lang):
    """Sahifa meta'si (title, desc, h1, lead, text, faq, kind) yoki ``None``."""
    ml = meta_lang(lang)
    page = PAGES.get(path)
    if page:
        meta = dict(page.get(ml) or page[DEFAULT_LANG])
        meta["kind"] = page["kind"]
        return meta
    match = _BILET_RE.fullmatch(path)
    if match:
        meta = {k: v.format(n=match.group(1)) for k, v in BILET[ml].items()}
        meta.update(kind="bilet", parent="/avtotest/")
        return meta
    return None


def canonical_query(params):
    pairs = [f"{k}={params[k]}" for k in CANONICAL_PARAMS if params.get(k)]
    return "?" + "&".join(pairs) if pairs else ""


def lang_url(path, lang):
    """``path`` (prefikssiz, query bilan) ning ``lang`` tilidagi to'liq manzili."""
    return SITE_URL + ("" if lang == DEFAULT_LANG else f"/{lang}") + path


def alternates(path):
    links = [(code, lang_url(path, code)) for code in SEO_LANGS]
    links.append(("x-default", lang_url(path, DEFAULT_LANG)))
    return links


def _crumb(position, name, url):
    return {"@type": "ListItem", "position": position, "name": name, "item": url}


def json_ld(lang, meta, canonical, url_lang=DEFAULT_LANG):
    """Sahifa uchun JSON-LD (``@graph``) — ``<script type="application/ld+json">`` ichiga.

    ``url_lang`` — joriy manzilning tili (prefiksdan), havolalar shu til versiyasiga qaratiladi.
    """
    ml = meta_lang(lang)
    kind = meta.get("kind")
    name = meta.get("h1") or meta.get("title", "")
    home_url = lang_url("/", url_lang)
    graph = []

    if kind == "home":
        graph.append({
            "@type": "Organization",
            "@id": SITE_URL + "/#organization",
            "name": "Complex Programmer",
            "url": SITE_URL + "/",
            "logo": SITE_URL + "/static/img/C0mplex.png",
            "sameAs": ORG_SAME_AS,
        })
        graph.append({
            "@type": "WebSite",
            "@id": SITE_URL + "/#website",
            "name": "Complex Programmer",
            "url": home_url,
            "inLanguage": ml,
            "publisher": {"@id": SITE_URL + "/#organization"},
            "potentialAction": {
                "@type": "SearchAction",
                "target": {"@type": "EntryPoint", "urlTemplate": SITE_URL + "/search/?q={search_term_string}"},
                "query-input": "required name=search_term_string",
            },
        })
    else:
        crumbs = [_crumb(1, LABELS[ml]["home"], home_url)]
        parent = meta.get("parent")
        if parent:
            parent_meta = page_meta(parent, lang)
            crumbs.append(_crumb(2, parent_meta.get("h1") or parent_meta["title"], lang_url(parent, url_lang)))
        crumbs.append(_crumb(len(crumbs) + 1, name, canonical))
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})

    if kind in ("tool", "game"):
        graph.append({
            "@type": "WebApplication",
            "name": name,
            "url": canonical,
            "description": meta.get("desc", ""),
            "inLanguage": ml,
            "applicationCategory": "GameApplication" if kind == "game" else "UtilitiesApplication",
            "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "UZS"},
            "publisher": {"@type": "Organization", "name": "Complex Programmer", "url": SITE_URL + "/"},
        })

    if meta.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in meta["faq"]
            ],
        })

    return json_ld_dump(graph)


def json_ld_dump(graph):
    if not graph:
        return ""
    data = {"@context": "https://schema.org", "@graph": graph}
    # "</script>" matn ichida bo'lsa ham skript yopilib qolmasin
    return json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
