import hashlib
import ipaddress
import json
import logging
import os
from pathlib import Path
import re
import threading
import uuid

import requests
import urllib3
from django.conf import settings
from django.core.cache import cache, caches
from django.db.models import Max
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.text import Truncator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from comments.pages import page_comments
from core import downloads
from core.translit import ALPHABET_2026, convert
from projects import sitemap_crawler, youtube_downloader
from projects.models import AvtoTest, Project

logger = logging.getLogger(__name__)

CBU_RATES_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
CBU_FALLBACK_FILE = settings.BASE_DIR / "projects" / "data" / "cbu_rates_fallback.json"
CBU_CACHE_KEY = "api:cbu:v2"
# Zaxira javoblar alohida keshda: asosiy kesh to'lganda tasodifiy o'chirilmaydi (settings.CACHES)
durable_cache = caches["durable"]

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "uz,ru,en;q=0.9",
}


def _save_disk_fallback(path, data):
    try:
        # Faqat to'liq ro'yxat bo'lsa (kamida 10 ta valyuta) zaxiraga yozamiz
        # Shunda testlar yoki xatolik bilan qisqargan ro'yxat haqiqiy 74 ta valyutani buzmaydi
        if isinstance(data, list) and len(data) < 10:
            return
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(target)
    except Exception as exc:
        logger.warning("Failed to save disk fallback to %s: %s", path, exc)


def _load_disk_fallback(path):
    try:
        target = Path(path)
        if target.is_file():
            with open(target, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as exc:
        logger.warning("Failed to load disk fallback from %s: %s", path, exc)
    return None


def base(request):
    # if request.device.get('is_mobile'):
    #     is_mobile = True
    # else:
    #     is_mobile = False
    class Status:
        Draft = 0, "Draft"
        Active = 1, "Active"

    services = Project.actives.filter(is_service=True).values()
    projects = Project.actives.all()
    context = {
        "services": services,
        "projects": projects,
        "today": home_today(request),
        # 'is_mobile': is_mobile,
    }
    return render(request, "base.html", context=context)


def home_today(request):
    """Bosh sahifadagi "Bugun" bloki: dollar kursi va eng yangi maqola (har kuni yangilanadigan narsa)."""
    from django.utils import translation

    from blog.models import Posts
    from blog.utils import lang_key, pick

    usd = cache.get("home:usd")
    if usd is None:
        # Bosh sahifa CBU'ni kutib qolmasin: qisqa timeout, xato ham 10 daqiqaga keshlanadi
        rates = fetch_json(CBU_RATES_URL, CBU_CACHE_KEY, timeout=3, ttl=1800)
        row = next((r for r in rates or [] if r.get("Ccy") == "USD"), None)
        usd = {"rate": row.get("Rate"), "diff": row.get("Diff", ""), "date": row.get("Date", "")} if row else False
        cache.set("home:usd", usd, 1800 if usd else 600)

    post = cache.get("home:post")
    if post is None:
        latest = Posts.published().order_by("-publish_time").first()
        post = False
        if latest:
            post = {f: getattr(latest, f) for f in ("name_uz_uz", "name_uz_crl", "name_ru_ru", "name_en_us")}
            post["url"] = latest.get_absolute_url()
        cache.set("home:post", post, 600)
    post_title = ""
    if post:
        post_title = pick(post, "name", lang_key(translation.get_language()))[0]

    return {
        "usd": usd or None,
        "usd_up": bool(usd) and not str(usd.get("diff", "")).startswith("-"),
        "post": post or None,
        "post_title": post_title,
    }


INSTAGRAM_UNAVAILABLE = (
    "Instagram yuklab olish xizmati vaqtincha ishlamayapti. "
    "Instagram himoyasi kuchaygani sababli ustida ishlayapmiz."
)


def instagram_downloader_(request):
    if request.method == "POST":
        return JsonResponse({"result": "0", "error": INSTAGRAM_UNAVAILABLE}, status=503)
    context = {"comments": page_comments(request), "unavailable": INSTAGRAM_UNAVAILABLE}
    return render(request, "projects/instagram_downloader.html", context=context)


# Bir jarayonda bir vaqtda ko'pi bilan shuncha yuklash (hosting thread/NPROC limiti); qolganlari navbatda kutadi
YT_SLOTS = threading.BoundedSemaphore(2)
YT_JOB_TTL = 2 * 3600


def _youtube_download(choice, quality, link):
    """Yuklab olish natijasi: {"result": fayl, "files": [...]} yoki {"result": "0", "error": ...}."""
    downloads.cleanup_old()
    try:
        if choice == 3:
            return {"result": youtube_downloader.download_audio(link)}
        if choice == 2:
            # Pleylist uchun birinchi videoni qaytaramiz, qolganlari ro'yxatda
            filenames = youtube_downloader.download_playlist(link, quality)
            if not filenames:
                return {"result": "0", "error": "Pleylist bo'sh"}
            return {"result": filenames[0], "files": filenames}
        return {"result": youtube_downloader.download_video(link, quality)}
    except youtube_downloader.DownloadError as exc:
        return {"result": "0", "error": str(exc)}


def _youtube_job(job_id, *args):
    key = f"ytjob:{job_id}"
    with YT_SLOTS:
        cache.set(key, {"status": "running"}, YT_JOB_TTL)
        try:
            data = _youtube_download(*args)
        except Exception:  # fon oqimida kutilmagan xato — foydalanuvchi cheksiz kutib qolmasin
            logger.exception("YouTube job %s failed", job_id)
            data = {"result": "0", "error": "Xatolik yuz berdi, birozdan so'ng urinib ko'ring"}
        cache.set(key, {"status": "done", **data}, YT_JOB_TTL)


def youtube_downloader_(request):
    comments = page_comments(request)
    context = {"comments": comments}
    if request.method != "POST":
        return render(request, "projects/youtube_downloader.html", context=context)

    try:
        json_data = json.loads(request.body)
        choice = int(json_data.get("choice", 1))
        quality = json_data.get("quality", "low")  # low, medium, high, very high
        link = (json_data.get("link") or "").strip()
    except (ValueError, TypeError):
        return JsonResponse({"result": "0", "error": "Noto'g'ri so'rov"}, status=400)

    if not youtube_downloader.is_youtube_url(link):
        return JsonResponse({"result": "0", "error": "YouTube havolasini kiriting"})

    if not json_data.get("async"):
        # Mobil ilova javobni shu so'rovning o'zida kutadi (eski format)
        return JsonResponse(_youtube_download(choice, quality, link))

    # Sayt: yuklash fonda bajariladi, sahifa holatni /youtube_downloader/status/ orqali so'rab turadi
    job_id = uuid.uuid4().hex
    cache.set(f"ytjob:{job_id}", {"status": "queued"}, YT_JOB_TTL)
    threading.Thread(target=_youtube_job, args=(job_id, choice, quality, link), daemon=True).start()
    return JsonResponse({"job": job_id})


def youtube_job_status(request):
    job_id = request.GET.get("job", "")
    data = cache.get(f"ytjob:{job_id}") if job_id.isalnum() else None
    if data is None:
        return JsonResponse({"status": "done", "result": "0", "error": "Vazifa topilmadi, qaytadan urinib ko'ring"}, status=404)
    return JsonResponse(data)


def fetch_json(
    url,
    cache_key,
    timeout=8,
    ttl=600,
    params=None,
    headers=None,
    fallback=True,
    disk_fallback_path=None,
):
    """Tashqi API'dan JSON oladi: natija keshlanadi, API ishlamasa kesh fallback yoki diskdan qaytaradi.

    Kesh muddati tugaganda eski (fallback) ma'lumot bo'lsa, u darhol qaytariladi va API fonda yangilanadi
    (stale-while-revalidate) — foydalanuvchi tashqi API'ni (CBU, CoinGecko) kutib qolmaydi.
    """
    # 1. Asosiy yangi keshni tekshiramiz
    data = cache.get(cache_key)
    if data is not None:
        return data

    if disk_fallback_path is None and cache_key in ("api:cbu", CBU_CACHE_KEY):
        disk_fallback_path = CBU_FALLBACK_FILE

    args = (url, cache_key, timeout, ttl, params, headers, fallback, disk_fallback_path)
    if fallback:
        # Diskdagi zaxira bu yerda ishlatilmaydi: u kunlab eski bo'lishi mumkin (faqat API ishlamasa beriladi)
        stale = durable_cache.get(f"{cache_key}:fallback")
        if stale:
            # Bir vaqtda faqat bitta jarayon yangilaydi; qolganlar eski ma'lumotni olib ketaveradi
            if cache.add(f"{cache_key}:refreshing", 1, timeout + 10):
                threading.Thread(target=_refresh_json, args=args, daemon=True).start()
            return stale

    return _fetch_json_now(*args)


def _refresh_json(*args):
    try:
        _fetch_json_now(*args)
    except Exception as exc:  # fon oqimida xato jarayonni yiqitmasin
        logger.warning("Background refresh failed for %s: %s", args[0], exc)
    finally:
        cache.delete(f"{args[1]}:refreshing")


def _fetch_json_now(url, cache_key, timeout, ttl, params, headers, fallback, disk_fallback_path):
    req_headers = DEFAULT_REQUEST_HEADERS.copy()
    # Ulanish uchun alohida qisqa chegara: server javob bermasa, timeout*2 (SSL qayta urinish bilan *4) kutilmasin
    timeout = (min(3, timeout), timeout)
    if headers:
        req_headers.update(headers)

    data = None
    try:
        resp = requests.get(url, params=params, headers=req_headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.SSLError as ssl_err:
        logger.warning("SSL error fetching %s: %s. Retrying without SSL verification...", url, ssl_err)
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            resp = requests.get(url, params=params, headers=req_headers, timeout=timeout, verify=False)
            resp.raise_for_status()
            data = resp.json()
        except Exception as retry_err:
            logger.warning("Retry without verify also failed for %s: %s", url, retry_err)
    except (requests.RequestException, ValueError) as exc:
        logger.warning("fetch_json network error for %s: %s", url, exc)

    # 2. Agar API muvaffaqiyatli ma'lumot qaytargan bo'lsa
    if data:
        cache.set(cache_key, data, ttl)
        if fallback:
            # CBU uchun qisqargan ro'yxat (10 tadan kam) bo'lsa, mavjud 74 ta valyutalik zaxirani buzmaymiz
            is_cbu_truncated = cache_key in ("api:cbu", CBU_CACHE_KEY) and isinstance(data, list) and len(data) < 10
            if not is_cbu_truncated:
                durable_cache.set(f"{cache_key}:fallback", data, 86400 * 30)  # 30 kun saqlanadi
                if disk_fallback_path:
                    _save_disk_fallback(disk_fallback_path, data)
        return data

    # 3. Agar API xatolik bergan bo'lsa, fallback keshdan olamiz
    if fallback:
        fallback_data = durable_cache.get(f"{cache_key}:fallback")
        if fallback_data:
            logger.info("Using cached fallback for key '%s'", cache_key)
            cache.set(cache_key, fallback_data, 300)  # Keyingi so'rovlar kutib qolmasligi uchun 5 daqiqa
            return fallback_data

        if disk_fallback_path:
            disk_data = _load_disk_fallback(disk_fallback_path)
            if disk_data:
                logger.info("Using disk fallback for key '%s' from %s", cache_key, disk_fallback_path)
                cache.set(cache_key, disk_data, 300)
                durable_cache.set(f"{cache_key}:fallback", disk_data, 86400 * 30)
                return disk_data

    return None


def coins(request):
    # Ma'lumot sahifa ochilgach /GetCoins/ orqali yuklanadi — sahifa tez ochiladi
    return render(request, "projects/coins.html", {"comments": page_comments(request)})


def GetCoins(request):
    # minerstat endi API kalit talab qiladi — CoinGecko'ning bepul API'si ishlatiladi
    data = fetch_json(
        "https://api.coingecko.com/api/v3/coins/markets",
        "api:coingecko",
        ttl=300,
        params={"vs_currency": "usd", "order": "market_cap_desc", "per_page": 250, "page": 1},
    )
    if data is None:
        return JsonResponse({"data": [], "error": "Kripto narxlar xizmati javob bermayapti"}, status=503)
    coins = [
        {
            "type": "coin",
            "rank": c.get("market_cap_rank"),
            "name": c.get("name"),
            "coin": (c.get("symbol") or "").upper(),
            "image": c.get("image"),
            "price": c.get("current_price"),
            "change24h": c.get("price_change_percentage_24h"),
            "market_cap": c.get("market_cap"),
        }
        for c in data
    ]
    return JsonResponse({"data": coins})


TRANSLATE_LANGUAGES = {
    "auto": "Auto", "uz": "O'zbek", "ru": "Русский", "en": "English", "tr": "Türkçe",
    "kk": "Қазақ", "ky": "Кыргыз", "tg": "Тоҷикӣ", "tk": "Türkmen", "az": "Azərbaycan",
    "de": "Deutsch", "fr": "Français", "es": "Español", "it": "Italiano", "ar": "العربية",
    "fa": "فارسی", "zh-CN": "中文", "ja": "日本語", "ko": "한국어", "hi": "हिन्दी",
    "uk": "Українська", "pl": "Polski", "pt": "Português",
}
MAX_TRANSLATE_CHARS = 5000


def GetTranslateLanguages(request):
    return JsonResponse({"data": TRANSLATE_LANGUAGES})


def TextToSpeech(request):
    # Ovozli o'qish brauzerning speechSynthesis API'si orqali bajariladi
    return HttpResponse(request.GET.get("text", ""))


def GetTranslateResult(request):
    text = (request.GET.get("text") or request.POST.get("text") or "").strip()
    src = request.GET.get("src") or request.POST.get("src") or "auto"
    dest = request.GET.get("dest") or request.POST.get("dest") or "uz"
    if not text:
        return JsonResponse({"data": ""})
    if len(text) > MAX_TRANSLATE_CHARS:
        return JsonResponse({"data": "", "error": f"Matn {MAX_TRANSLATE_CHARS} belgidan oshmasin"}, status=400)
    if src not in TRANSLATE_LANGUAGES or dest not in TRANSLATE_LANGUAGES or dest == "auto":
        return JsonResponse({"data": "", "error": "Noto'g'ri til"}, status=400)

    cache_key = "tr:" + hashlib.sha1(f"{src}|{dest}|{text}".encode()).hexdigest()
    result = cache.get(cache_key)
    if result is None:
        result = _translate_google(text, src, dest) or _translate_mymemory(text, src, dest)
        if result is None:
            return JsonResponse({"data": "", "error": "Tarjima xizmati vaqtincha ishlamayapti"}, status=503)
        cache.set(cache_key, result, 60 * 60 * 24)
    return JsonResponse({"data": result})


def _translate_google(text, src, dest):
    try:
        resp = requests.post(
            "https://translate.googleapis.com/translate_a/single",
            params={"client": "gtx", "sl": src, "tl": dest, "dt": "t"},
            data={"q": text},
            timeout=6,
        )
        resp.raise_for_status()
        return "".join(part[0] for part in resp.json()[0] if part and part[0])
    except (requests.RequestException, ValueError, TypeError, IndexError):
        return None


def _split_chunks(text, size=450):
    """MyMemory 500 belgidan uzun matnni qabul qilmaydi — gaplar bo'yicha bo'lamiz."""
    chunks, current = [], ""
    for sentence in re.split(r"(?<=[.!?\n])\s*", text):
        while len(sentence) > size:
            chunks.append(sentence[:size])
            sentence = sentence[size:]
        if len(current) + len(sentence) + 1 > size and current:
            chunks.append(current)
            current = ""
        current = (current + " " + sentence).strip() if current else sentence
    if current:
        chunks.append(current)
    return chunks


def _translate_mymemory(text, src, dest):
    pair = f"{'Autodetect' if src == 'auto' else src}|{dest}"
    parts = []
    try:
        for chunk in _split_chunks(text):
            resp = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": chunk, "langpair": pair, "de": settings.DEFAULT_FROM_EMAIL},
                timeout=6,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("responseStatus") != 200:
                return None
            parts.append(data["responseData"]["translatedText"])
    except (requests.RequestException, ValueError, KeyError):
        return None
    return " ".join(parts)


@ensure_csrf_cookie
def C0mplexTranslate(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/translate.html", context=context)


def ImageCompare(request):
    # Solishtirish brauzerda (canvas) bajariladi, server faqat sahifani beradi
    return render(request, "projects/imagecompare.html", {"comments": page_comments(request)})


def avtotest(request):
    comments = page_comments(request)

    # Get max bilet value and add 1
    max_bilet = AvtoTest.objects.aggregate(Max("bilet"))["bilet__max"]
    total_bilets = max_bilet + 1 if max_bilet else 1

    context = {"comments": comments, "row": range(1, total_bilets), "bilet": 0}
    return render(request, "projects/avtotest.html", context=context)


def avtotest_item(request, bilet):
    comments = page_comments(request)
    max_bilet = AvtoTest.objects.aggregate(Max("bilet"))["bilet__max"]
    total_bilets = max_bilet + 1 if max_bilet else 1
    # Har bir savolning alohida sahifasiga havolalar (/avtotest/<bilet>/<raqam>/)
    field = {"uz": "savol", "ru": "savol_ru"}.get((request.LANGUAGE_CODE or "uz")[:2], "savol_en")
    questions = [
        {"raqam": q["raqam"], "text": Truncator(q[field] or q["savol"]).chars(120)}
        for q in AvtoTest.objects.filter(bilet=bilet).order_by("raqam").values("raqam", "savol", field)
    ]
    context = {"comments": comments, "row": range(1, total_bilets), "bilet": bilet, "questions": questions}
    return render(request, "projects/avtotest.html", context=context)


def avtotest_mistakes(request):
    """Foydalanuvchi xato qilgan savollar (ro'yxat brauzer localStorage'idan olinadi)."""
    return render(request, "projects/avtotest_mistakes.html", {"comments": page_comments(request)})


def GetSavol(request):
    bilet = request.GET.get("bilet")
    ids = request.GET.get("ids")
    if ids:
        # Xatolar rejimi uchun: ?ids=1,5,17 (ko'pi bilan 200 ta)
        id_list = [int(i) for i in ids.split(",")[:200] if i.strip().isdigit()]
        avtotest = AvtoTest.objects.filter(id__in=id_list).values()
    elif bilet:
        if not str(bilet).isdigit():
            return JsonResponse([], safe=False)
        avtotest = AvtoTest.objects.filter(bilet=bilet).values()
    else:
        # Parametrsiz — barcha savollar (mobil ilova shu formatdan foydalanishi mumkin)
        avtotest = AvtoTest.objects.all().values()
    return JsonResponse(list(avtotest), safe=False)
    # qs = AvtoTest.objects.filter(bilet=bilet)
    # qs_json = serializers.serialize('json', qs)
    # return HttpResponse(qs_json, content_type='application/json')


def GetBilet(request):
    arr = []
    max_bilet = AvtoTest.objects.aggregate(Max("bilet"))["bilet__max"]
    total_bilets = max_bilet + 1 if max_bilet else 1
    for i in range(1, total_bilets):
        context = {"bilet": i}
        arr.append(context)
    return JsonResponse(list(arr), safe=False)


# Sahifa tepasida kartochka bo'lib chiqadigan valyutalar
RATES_FEATURED = ("USD", "EUR", "RUB", "KZT")
RATES_TEXT = {
    "uz": {
        "date": "Kurs sanasi", "featured": "Asosiy valyutalar", "all": "Barcha valyutalar", "search": "Valyuta qidirish: dollar, EUR, 840...",
        "converter": "Valyuta kalkulyatori", "amount": "Miqdor", "currency": "Valyuta", "swap": "Almashtirish", "sum": "so'm",
        "rate": "Kurs", "change": "O'zgarish", "code": "Kod", "per": "{} uchun", "none": "Hech narsa topilmadi",
        "error": "Markaziy bank sayti hozir javob bermayapti. Birozdan so'ng sahifani yangilang.",
        "note": "Markaziy bankning rasmiy kursi. Banklardagi sotib olish va sotish kurslari farq qilishi mumkin.", "app": "Android ilova",
    },
    "ru": {
        "date": "Курс на", "featured": "Основные валюты", "all": "Все валюты", "search": "Поиск валюты: доллар, EUR, 840...",
        "converter": "Конвертер валют", "amount": "Сумма", "currency": "Валюта", "swap": "Поменять", "sum": "сум",
        "rate": "Курс", "change": "Изменение", "code": "Код", "per": "за {}", "none": "Ничего не найдено",
        "error": "Сайт Центрального банка сейчас не отвечает. Обновите страницу чуть позже.",
        "note": "Официальный курс ЦБ. Курсы покупки и продажи в банках могут отличаться.", "app": "Приложение Android",
    },
    "en": {
        "date": "Rates as of", "featured": "Major currencies", "all": "All currencies", "search": "Search currency: dollar, EUR, 840...",
        "converter": "Currency converter", "amount": "Amount", "currency": "Currency", "swap": "Swap", "sum": "UZS",
        "rate": "Rate", "change": "Change", "code": "Code", "per": "per {}", "none": "Nothing found",
        "error": "The Central Bank website is not responding right now. Please refresh the page a little later.",
        "note": "Official Central Bank rate. Buy and sell rates at banks may differ.", "app": "Android app",
    },
    "tr": {
        "date": "Kur tarihi", "featured": "Ana para birimleri", "all": "Tüm para birimleri", "search": "Para birimi ara: dolar, EUR, 840...",
        "converter": "Döviz çevirici", "amount": "Miktar", "currency": "Para birimi", "swap": "Değiştir", "sum": "som",
        "rate": "Kur", "change": "Değişim", "code": "Kod", "per": "{} için", "none": "Sonuç bulunamadı",
        "error": "Merkez Bankası sitesi şu anda yanıt vermiyor. Lütfen sayfayı biraz sonra yenileyin.",
        "note": "Merkez Bankası resmi kuru. Bankalardaki alış ve satış kurları farklı olabilir.", "app": "Android uygulaması",
    },
}


def _num(value, digits=2, sign=False):
    """12345.6 -> "12 345.60" (minglar bo'sh joy bilan ajratiladi)."""
    return format(value, f"{'+' if sign else ''},.{digits}f").replace(",", "\u00a0")


def _rate_rows(data, lang):
    """CBU javobini jadval uchun tayyorlaydi: Diff satr emas, son sifatida solishtiriladi."""
    name_key = {"ru": "CcyNm_RU", "en": "CcyNm_EN", "tr": "CcyNm_EN"}.get(lang, "CcyNm_UZ")
    rows = []
    for item in data or []:
        try:
            rate = float(item["Rate"])
            diff = float(item.get("Diff") or 0)
            nominal = int(item.get("Nominal") or 1)
        except (KeyError, TypeError, ValueError):
            continue
        prev = rate - diff
        rows.append({
            "ccy": item.get("Ccy", ""),
            "code": item.get("Code", ""),
            "name": item.get(name_key) or item.get("CcyNm_EN") or item.get("Ccy", ""),
            "nominal": nominal,
            "rate": rate,
            "rate_fmt": _num(rate),
            "diff_fmt": _num(diff, sign=True),
            "pct_fmt": _num(diff / prev * 100 if prev else 0, sign=True) + "%",
            "trend": "up" if diff > 0 else "down" if diff < 0 else "flat",
            # Qidiruv barcha tillardagi nom bo'yicha: ruscha sahifada ham "dollar" topilsin
            "search": " ".join(
                str(item.get(k) or "") for k in ("Ccy", "Code", "CcyNm_UZ", "CcyNm_UZC", "CcyNm_RU", "CcyNm_EN")
            ).lower(),
        })
    return rows


def exchangerates(request):
    from django.utils import translation

    data = fetch_json(CBU_RATES_URL, CBU_CACHE_KEY, ttl=1800, timeout=8)
    lang = (translation.get_language() or "uz")[:2]
    t = RATES_TEXT.get(lang, RATES_TEXT["en"])
    rows = _rate_rows(data, lang)
    for r in rows:
        # Kurs bir necha birlik uchun berilgan valyutalar (masalan, 10 JPY) — "10 JPY uchun"
        r["per"] = t["per"].format(f"{r['nominal']} {r['ccy']}") if r["nominal"] > 1 else ""
    by_ccy = {r["ccy"]: r for r in rows}
    context = {
        "rows": rows,
        "featured": [by_ccy[c] for c in RATES_FEATURED if c in by_ccy],
        "rate_date": (data or [{}])[0].get("Date", "") if data else "",
        # Kalkulyator uchun: 1 birlik valyuta necha so'm
        "converter_rates": {r["ccy"]: r["rate"] / r["nominal"] for r in rows},
        "t": t,
        "api_error": not rows,
        "comments": page_comments(request),
    }
    return render(request, "projects/exchangerates.html", context=context)


def GetExchangeRates(request):
    data = fetch_json(CBU_RATES_URL, CBU_CACHE_KEY, ttl=1800, timeout=8)
    if not data:
        return JsonResponse({"data": [], "error": "Markaziy bank sayti javob bermayapti"}, status=503)
    return JsonResponse({"data": data})


CHANGETEXT_TEXT = {
    "uz": {
        "badge_auto": "Yozuvni o'zi aniqlaydi", "badge_scripts": "Kirill · Lotin 1995 · Lotin 2026", "badge_free": "Bepul, cheklovsiz",
        "auto": "Avto", "cyr": "Kirill", "lat1995": "Lotin (1995)", "lat2026": "Yangi lotin (2026)",
        "source": "Matn", "result": "Natija", "placeholder": "Matnni shu yerga yozing yoki qo'ying...", "result_placeholder": "Natija shu yerda chiqadi",
        "chars": "belgi", "words": "so'z", "paste": "Qo'yish", "clear": "Tozalash", "copy": "Nusxalash", "copied": "Nusxalandi",
        "download": "Yuklab olish (.txt)", "swap": "Natijani matnga o'tkazish", "error": "Xatolik yuz berdi, qayta urinib ko'ring",
        "alphabet": "O'zbek lotin alifbosi (2026): 28 harf va tutuq belgisi (ʼ)",
        "alphabet_note": "1995-yilgi alifboda 26 harf va 3 ta harf birikmasi (sh, ch, ng) bor edi. Islohot sh, ch, gʻ va oʻ ni bitta harfga — ş, ç, ğ va ö ga aylantirdi, ng esa alohida harf sifatida sanalmaydi. Tutuq belgisi (ʼ) harf emas, belgi.",
        "changed": "o'zgargan harflar", "app": "Android ilova",
        "tip": "Inglizcha so'zlar, havolalar va @username o'zgarmaydi. Natijani tekshirib oling.",
    },
    "ru": {
        "badge_auto": "Сам определяет алфавит", "badge_scripts": "Кириллица · Латиница 1995 · Латиница 2026", "badge_free": "Бесплатно, без ограничений",
        "auto": "Авто", "cyr": "Кириллица", "lat1995": "Латиница (1995)", "lat2026": "Новая латиница (2026)",
        "source": "Текст", "result": "Результат", "placeholder": "Введите или вставьте текст...", "result_placeholder": "Здесь появится результат",
        "chars": "симв.", "words": "слов", "paste": "Вставить", "clear": "Очистить", "copy": "Копировать", "copied": "Скопировано",
        "download": "Скачать (.txt)", "swap": "Перенести результат в текст", "error": "Произошла ошибка, попробуйте ещё раз",
        "alphabet": "Узбекский латинский алфавит (2026): 28 букв и знак тутук (ʼ)",
        "alphabet_note": "В алфавите 1995 года было 26 букв и 3 буквосочетания (sh, ch, ng). Реформа заменила sh, ch, gʻ и oʻ одиночными буквами ş, ç, ğ и ö, а ng больше не считается отдельной буквой. Тутук (ʼ) — знак, а не буква.",
        "changed": "изменённые буквы", "app": "Приложение Android",
        "tip": "Английские слова, ссылки и @username не меняются. Проверьте результат.",
    },
    "en": {
        "badge_auto": "Detects the script itself", "badge_scripts": "Cyrillic · Latin 1995 · Latin 2026", "badge_free": "Free, no limits",
        "auto": "Auto", "cyr": "Cyrillic", "lat1995": "Latin (1995)", "lat2026": "New Latin (2026)",
        "source": "Text", "result": "Result", "placeholder": "Type or paste your text here...", "result_placeholder": "The result will appear here",
        "chars": "chars", "words": "words", "paste": "Paste", "clear": "Clear", "copy": "Copy", "copied": "Copied",
        "download": "Download (.txt)", "swap": "Use result as input", "error": "Something went wrong, please try again",
        "alphabet": "Uzbek Latin alphabet (2026): 28 letters and the tutuq sign (ʼ)",
        "alphabet_note": "The 1995 alphabet had 26 letters and 3 digraphs (sh, ch, ng). The reform replaced sh, ch, gʻ and oʻ with the single letters ş, ç, ğ and ö, and ng is no longer counted as a separate letter. The tutuq (ʼ) is a sign, not a letter.",
        "changed": "changed letters", "app": "Android app",
        "tip": "English words, links and @usernames are kept as is. Please check the result.",
    },
    "tr": {
        "badge_auto": "Alfabeyi kendisi algılar", "badge_scripts": "Kiril · Latin 1995 · Latin 2026", "badge_free": "Ücretsiz, sınırsız",
        "auto": "Otomatik", "cyr": "Kiril", "lat1995": "Latin (1995)", "lat2026": "Yeni Latin (2026)",
        "source": "Metin", "result": "Sonuç", "placeholder": "Metni buraya yazın veya yapıştırın...", "result_placeholder": "Sonuç burada görünecek",
        "chars": "karakter", "words": "kelime", "paste": "Yapıştır", "clear": "Temizle", "copy": "Kopyala", "copied": "Kopyalandı",
        "download": "İndir (.txt)", "swap": "Sonucu metne aktar", "error": "Bir hata oluştu, tekrar deneyin",
        "alphabet": "Özbek Latin alfabesi (2026): 28 harf ve tutuk işareti (ʼ)",
        "alphabet_note": "1995 alfabesinde 26 harf ve 3 harf birleşimi (sh, ch, ng) vardı. Reform sh, ch, gʻ ve oʻ'yu tek harflere — ş, ç, ğ ve ö'ye dönüştürdü; ng artık ayrı bir harf sayılmıyor. Tutuk (ʼ) bir harf değil, işarettir.",
        "changed": "değişen harfler", "app": "Android uygulaması",
        "tip": "İngilizce kelimeler, bağlantılar ve @kullanıcı adları değişmez. Sonucu kontrol edin.",
    },
}


@ensure_csrf_cookie
def changetext(request):
    from django.utils import translation

    if request.method == "POST":
        # Sahifa matnni POST bilan yuboradi: uzun matn URL (GET) chegarasiga sig'maydi
        return HttpResponse(convert(request.POST.get("text", ""), request.POST.get("to")))
    lang = (translation.get_language() or "uz")[:2]
    context = {
        "comments": page_comments(request),
        "alphabet": ALPHABET_2026,
        "t": CHANGETEXT_TEXT.get(lang, CHANGETEXT_TEXT["en"]),
    }
    return render(request, "projects/changetext.html", context=context)


def GetChangeTextData(request):
    # to: "cyr", "lat1995" yoki "lat2026"; berilmasa — kirill lotinga, lotin kirillga
    text = request.GET.get("text", "")
    return HttpResponse(convert(text, request.GET.get("to")))


def client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


IP_TEXT = {
    "uz": {
        "your_ip": "Sizning IP manzilingiz", "checked_ip": "Tekshirilgan IP manzil", "copy": "Nusxalash", "copied": "Nusxalandi",
        "placeholder": "IP manzil kiriting, masalan 8.8.8.8", "search": "Tekshirish", "my_ip": "Mening IP", "invalid": "IP manzil noto'g'ri yozilgan",
        "loading": "Ma'lumot yuklanmoqda...", "location": "Joylashuv", "network": "Tarmoq", "time": "Vaqt", "country": "Mamlakat haqida",
        "country_name": "Mamlakat", "region": "Viloyat", "city": "Shahar", "postal": "Pochta indeksi", "coords": "Koordinatalar", "map": "Xaritada ochish",
        "ip": "IP manzil", "version": "Versiya", "org": "Provayder", "asn": "ASN", "net": "Tarmoq bloki", "hostname": "Host nomi",
        "timezone": "Vaqt mintaqasi", "utc": "UTC farqi", "local_time": "Hozirgi vaqt",
        "capital": "Poytaxt", "calling": "Telefon kodi", "currency": "Valyuta", "languages": "Tillar", "tld": "Domen", "population": "Aholi",
        "area": "Maydoni, km²", "eu": "Yevropa Ittifoqi", "yes": "Ha", "no": "Yo'q", "error": "Xizmat vaqtincha ishlamayapti",
        "private": "Lokal (xususiy) IP manzil — internetda joylashuvi yo'q",
        "note": "Joylashuv IP manzil bo'yicha taxminiy aniqlanadi: odatda provayder joylashgan shahar ko'rsatiladi.", "app": "Android ilova",
    },
    "ru": {
        "your_ip": "Ваш IP-адрес", "checked_ip": "Проверяемый IP-адрес", "copy": "Копировать", "copied": "Скопировано",
        "placeholder": "Введите IP-адрес, например 8.8.8.8", "search": "Проверить", "my_ip": "Мой IP", "invalid": "Неверный IP-адрес",
        "loading": "Загрузка данных...", "location": "Местоположение", "network": "Сеть", "time": "Время", "country": "О стране",
        "country_name": "Страна", "region": "Регион", "city": "Город", "postal": "Почтовый индекс", "coords": "Координаты", "map": "Открыть на карте",
        "ip": "IP-адрес", "version": "Версия", "org": "Провайдер", "asn": "ASN", "net": "Сеть", "hostname": "Имя хоста",
        "timezone": "Часовой пояс", "utc": "Смещение UTC", "local_time": "Текущее время",
        "capital": "Столица", "calling": "Телефонный код", "currency": "Валюта", "languages": "Языки", "tld": "Домен", "population": "Население",
        "area": "Площадь, км²", "eu": "Евросоюз", "yes": "Да", "no": "Нет", "error": "Сервис временно недоступен",
        "private": "Локальный (частный) IP-адрес — у него нет местоположения в интернете",
        "note": "Местоположение по IP определяется приблизительно: обычно это город провайдера.", "app": "Приложение Android",
    },
    "en": {
        "your_ip": "Your IP address", "checked_ip": "IP address checked", "copy": "Copy", "copied": "Copied",
        "placeholder": "Enter an IP address, e.g. 8.8.8.8", "search": "Look up", "my_ip": "My IP", "invalid": "Invalid IP address",
        "loading": "Loading details...", "location": "Location", "network": "Network", "time": "Time", "country": "About the country",
        "country_name": "Country", "region": "Region", "city": "City", "postal": "Postal code", "coords": "Coordinates", "map": "Open map",
        "ip": "IP address", "version": "Version", "org": "Provider", "asn": "ASN", "net": "Network", "hostname": "Hostname",
        "timezone": "Time zone", "utc": "UTC offset", "local_time": "Local time",
        "capital": "Capital", "calling": "Calling code", "currency": "Currency", "languages": "Languages", "tld": "Domain", "population": "Population",
        "area": "Area, km²", "eu": "European Union", "yes": "Yes", "no": "No", "error": "The service is temporarily unavailable",
        "private": "Local (private) IP address — it has no location on the internet",
        "note": "IP location is approximate: it usually shows the city of the internet provider.", "app": "Android app",
    },
    "tr": {
        "your_ip": "IP adresiniz", "checked_ip": "Sorgulanan IP adresi", "copy": "Kopyala", "copied": "Kopyalandı",
        "placeholder": "IP adresi girin, ör. 8.8.8.8", "search": "Sorgula", "my_ip": "IP'm", "invalid": "Geçersiz IP adresi",
        "loading": "Bilgiler yükleniyor...", "location": "Konum", "network": "Ağ", "time": "Saat", "country": "Ülke hakkında",
        "country_name": "Ülke", "region": "Bölge", "city": "Şehir", "postal": "Posta kodu", "coords": "Koordinatlar", "map": "Haritada aç",
        "ip": "IP adresi", "version": "Sürüm", "org": "Sağlayıcı", "asn": "ASN", "net": "Ağ bloğu", "hostname": "Ana bilgisayar adı",
        "timezone": "Saat dilimi", "utc": "UTC farkı", "local_time": "Yerel saat",
        "capital": "Başkent", "calling": "Telefon kodu", "currency": "Para birimi", "languages": "Diller", "tld": "Alan adı", "population": "Nüfus",
        "area": "Yüzölçümü, km²", "eu": "Avrupa Birliği", "yes": "Evet", "no": "Hayır", "error": "Hizmet geçici olarak kullanılamıyor",
        "private": "Yerel (özel) IP adresi — internette konumu yok",
        "note": "IP konumu yaklaşıktır: genellikle internet sağlayıcısının şehrini gösterir.", "app": "Android uygulaması",
    },
}


def _ip_lookup(raw_ip, wait=True):
    """IP ma'lumoti. ``wait=False`` bo'lsa ipapi.co'ga so'rov yuborilmaydi — faqat kesh (yo'q bo'lsa None)."""
    try:
        ip_obj = ipaddress.ip_address((raw_ip or "").strip())
    except ValueError:
        return {"error": True, "code": "invalid", "reason": "Noto'g'ri IP manzil"}
    if ip_obj.is_private or ip_obj.is_loopback:
        return {"ip": str(ip_obj), "error": True, "code": "private", "reason": "Lokal (xususiy) IP manzil"}
    cache_key = f"api:ip:{ip_obj}"
    if not wait:
        return cache.get(cache_key)
    data = fetch_json(f"https://ipapi.co/{ip_obj}/json/", cache_key, ttl=3600, timeout=4, fallback=False)
    return data or {"ip": str(ip_obj), "error": True, "code": "error", "reason": "Xizmat vaqtincha ishlamayapti"}


def ip(request):
    from django.utils import translation

    # Parametr berilmasa — serverning emas, foydalanuvchining o'z IP manzili
    raw_ip = request.GET.get("ip") or client_ip(request)
    # Sahifa ipapi.co'ni kutmaydi: keshda bo'lmasa, jadval brauzerda /GetIpData/ orqali to'ldiriladi
    data = _ip_lookup(raw_ip, wait=False)
    pending = data is None
    if pending:
        data = {"ip": raw_ip.strip()}
    lang = (translation.get_language() or "uz")[:2]
    context = {
        "data": data,
        "pending": pending,
        # O'z IP'ini ko'ryaptimi yoki boshqa manzilni tekshiryaptimi — sarlavha shunga qarab
        "own_ip": not request.GET.get("ip"),
        "t": IP_TEXT.get(lang, IP_TEXT["en"]),
        "comments": page_comments(request),
    }
    return render(request, "projects/ip.html", context)


def GetIpData(request):
    data = _ip_lookup(request.GET.get("ip") or client_ip(request))
    return JsonResponse(data, status=503 if data.get("code") == "error" else 200)


def map(request):
    comments = page_comments(request)
    # key = config('GOOGLE_MAP_API_KEY')
    # eligable_locations = Locations.objects.filter(place_id__isnull=False)
    locations = []

    # for a in eligable_locations:
    #     data = {
    #         'lat': float(a.lat),
    #         'lng': float(a.lng),
    #         'name': a.name
    #     }

    #     locations.append(data)

    data = {"lat": float(50.4777), "lng": float(12.3649), "name": "Saxony"}

    locations.append(data)
    context = {"key": "key", "locations": locations, "comments": comments}
    return render(request, "projects/map.html", context)


def password_generator(request):
    # Parol brauzerda (crypto.getRandomValues) yaratiladi va serverga umuman yuborilmaydi
    return render(request, "projects/password_generator.html", {"comments": page_comments(request)})


@ensure_csrf_cookie
def sitemap(request):
    if request.method != "POST":
        return render(request, "projects/sitemap.html", {"comments": page_comments(request)})
    try:
        url = json.loads(request.body or b"{}").get("url", "")
    except ValueError:
        url = ""
    # Bir sayt qayta-qayta so'ralsa, 25 soniyalik aylanib chiqish takrorlanmasin
    cache_key = "sitemap_crawl:" + hashlib.sha1(url.strip().lower().encode()).hexdigest()
    urls = cache.get(cache_key)
    if urls is None:
        try:
            urls = sitemap_crawler.crawl(url)
        except sitemap_crawler.CrawlError as exc:
            return JsonResponse({"error": str(exc)}, status=400)
        cache.set(cache_key, urls, 3600)
    return JsonResponse({"xml": sitemap_crawler.build_xml(urls), "count": len(urls), "urls": urls})


def snake(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/snake.html", context=context)


def snake2(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/snake2.html", context=context)


def car(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/car.html", context=context)


def duckhunt(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/duckhunt.html", context=context)


def motorcycle(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/motorcycle.html", context=context)


def bubbleshooter(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/bubbleshooter.html", context=context)


def pingpong(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/pingpong.html", context=context)


def tictactoe(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/tictactoe.html", context=context)


def tetris(request):
    comments = page_comments(request)
    context = {"comments": comments}
    return render(request, "projects/tetris.html", context=context)


def terms(request):
    return render(request, "terms.html")


def privacy(request):
    return render(request, "privacy.html")


def send_yandex_verification(request):
    temp = open("templates/yandex_6bd5e2cc7d84e7b1.html", "rb")
    response = FileResponse(temp)
    return response


def send_google_verification(request):
    temp = open("templates/googleed00602540a61448.html", "rb")
    response = FileResponse(temp)
    return response


def send_zen_verification(request):
    temp = open(
        "templates/zen_7l9bCOKi66HKyY4ilLYmulKUQTlrZLJrS3HSjTiMhq0GoD4ap8COxE7Bjw1oYf26.html",
        "rb",
    )
    response = FileResponse(temp)
    return response


def send_sitemap(request):
    temp = open("static/sitemap.xml", "rb")
    response = FileResponse(temp)
    return response


def send_bing_site_auth(request):
    temp = open("static/BingSiteAuth.xml", "rb")
    response = FileResponse(temp)
    return response


def send_rss(request):
    temp = open("static/rss.xml", "rb")
    response = FileResponse(temp)
    return response


def send_app_adstxt(request):
    temp = open("static/app-ads.txt", "rb")
    response = FileResponse(temp)
    return response


def send_adstxt(request):
    temp = open("static/ads.txt", "rb")
    response = FileResponse(temp)
    return response


def send_robots(request):
    temp = open("static/robots.txt", "rb")
    response = FileResponse(temp)
    return response


def assetlinks(request):
    temp = open("static/assetlinks.json", "rb")
    response = FileResponse(temp)
    return response


def projects(request):
    comments = page_comments(request)
    context = {"comments": comments}

    projects = Project.actives.all()
    context = {"projects": projects, "comments": comments}
    return render(request, "projects/home.html", context=context)


def services(request):
    services = Project.services.all()
    context = {"services": services}
    return render(request, "base.html", context=context)


def project_item(request, id):
    comments = page_comments(request)
    context = {"comments": comments}

    item = get_object_or_404(Project, id=id)
    context = {
        "item": item,
        "comments": comments,
        "seo_title": f"{item.title} — Complex Programmer",
        "seo_description": item.sub_title or item.title,
    }
    return render(request, "projects/item.html", context=context)


def send_file(request):
    """Faqat media/downloads ichidagi faylni nomi bo'yicha beradi."""
    downloads.cleanup_old()
    path = downloads.resolve(request.GET.get("filename"))
    if path is None:
        raise Http404("Fayl topilmadi yoki muddati o'tgan")
    # Fayl nomidagi uuid prefiksini foydalanuvchiga ko'rsatmaymiz
    nice_name = os.path.basename(path).split("_", 1)[-1]
    return FileResponse(open(path, "rb"), as_attachment=True, filename=nice_name)


@require_POST
def remove_file(request):
    path = downloads.resolve(request.GET.get("filename"))
    if path is not None:
        try:
            os.remove(path)
        except OSError:
            # Windows'da fayl hali uzatilayotgan bo'lishi mumkin — cleanup_old keyin o'chiradi
            pass
    return JsonResponse({"ok": True})
