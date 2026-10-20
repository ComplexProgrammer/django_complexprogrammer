import re

from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.utils import translation

from core.seo import DEFAULT_LANG, PREFIX_LANGS

# Qidiruv robotlari — ularga prefikssiz manzillar doim o'zbekcha ko'rsatiladi
# (Accept-Language'ga qarab boshqa tilga o'tib ketmasin: hreflang="uz" deb belgilangan)
BOT_RE = re.compile(r"bot|crawl|spider|slurp|mediapartners|facebookexternalhit", re.I)


class PrivateStaticMiddleware:
    """``media/`` papkasi STATICFILES_DIRS'da ham bor, shuning uchun arxiv hujjatlari
    ``/static/arxiv/...`` orqali ham ochiq bo'lib qolardi — himoyani chetlab o'tadi.
    Ular faqat ``/media/arxiv/documents/`` (huquq tekshiriladi) orqali beriladi.
    WhiteNoiseMiddleware'dan oldin turishi shart.
    """

    PREFIX = settings.STATIC_URL + "arxiv/"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(self.PREFIX):
            raise Http404
        return self.get_response(request)


class FrameAncestorsMiddleware:
    """Saytni boshqa saytlar iframe ichiga joylashini (clickjacking) taqiqlaydi.

    X-Frame-Options faqat DENY/SAMEORIGIN biladi, Telegram WebApp esa saytni
    web.telegram.org iframe'ida ochadi — shuning uchun CSP ``frame-ancestors`` ishlatiladi.
    """

    POLICY = "frame-ancestors " + " ".join(settings.FRAME_ANCESTORS)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = self.POLICY
        return response


class LanguagePrefixMiddleware:
    """``/ru/...`` va ``/en/...`` — tilga xos manzillar (qidiruv tizimlari har bir tilni alohida indekslashi uchun).

    Prefiks ``path_info``dan olib tashlanadi (URL'lar o'zgarmaydi) va sahifa o'sha tilda ko'rsatiladi.
    Prefikssiz manzillar avvalgidek cookie / Accept-Language bo'yicha ishlaydi.
    ``i18n_patterns`` ataylab ishlatilmagan: u prefikssiz sahifalarda cookie'ni e'tiborsiz qoldiradi.
    LocaleMiddleware'dan keyin turishi kerak.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        parts = request.path_info.split("/", 2)
        lang = parts[1] if len(parts) > 1 and parts[1] in PREFIX_LANGS else None
        request.lang_prefix = ""

        if lang:
            if len(parts) == 2:  # "/ru" -> "/ru/"
                return HttpResponsePermanentRedirect(request.path + "/")
            request.lang_prefix = "/" + lang
            request.path_info = "/" + parts[2]
        elif settings.LANGUAGE_COOKIE_NAME not in request.COOKIES and BOT_RE.search(
            request.META.get("HTTP_USER_AGENT", "")
        ):
            lang = DEFAULT_LANG

        if lang:
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

        response = self.get_response(request)

        # /ru/ sahifadan boshqa (prefikssiz) sahifaga o'tganda ham til saqlansin
        if request.lang_prefix and request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) != lang:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                lang,
                max_age=settings.LANGUAGE_COOKIE_AGE or 365 * 24 * 3600,
                samesite="Lax",
            )
        return response
