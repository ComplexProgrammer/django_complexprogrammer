"""Sayt xaritasi (sitemap.xml) generatori.

Faqat bitta sayt ichida yuradi (``www.`` bilan va usiz bir xil sayt hisoblanadi), sahifalar soni va umumiy
vaqt cheklangan. Ichki tarmoq manzillariga (127.0.0.1, 10.x, 192.168.x ...) so'rov yuborilmaydi.
robots.txt taqiqlagan, ``noindex`` belgilangan va HTML bo'lmagan sahifalar xaritaga kirmaydi;
``rel=canonical`` bo'lsa — kanonik manzil yoziladi, ``utm_*`` kabi kuzatuv parametrlari olib tashlanadi.
"""

import ipaddress
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from email.utils import parsedate_to_datetime
from urllib import robotparser
from urllib.parse import parse_qsl, urldefrag, urlencode, urljoin, urlsplit, urlunsplit
from xml.sax.saxutils import escape

import requests
from lxml import html as lxml_html

MAX_PAGES = 300
TIME_BUDGET = 60  # soniya — fonda ishlaydi, sahifa holatni so'rab turadi
WORKERS = 4  # hosting thread limiti (NPROC) sababli ko'p emas
SKIP_EXT = (
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico", ".css", ".js", ".json", ".xml", ".txt",
    ".pdf", ".zip", ".rar", ".7z", ".mp3", ".mp4", ".avi", ".mov", ".webm", ".doc", ".docx", ".xls", ".xlsx",
    ".ppt", ".pptx", ".exe", ".apk", ".dmg",
)
TRACKING_PARAMS = ("utm_", "fbclid", "gclid", "yclid", "ysclid", "_ga", "mc_cid", "mc_eid")
# Ba'zi saytlar (Cloudflare, WAF) "bot" User-Agent'ni bloklaydi — brauzerga o'xshash, lekin o'zini tanishtiradi
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
    "ComplexProgrammer-SitemapBot/2.0 (+https://complexprogrammer.uz/sitemap/)"
)
HTML_TYPES = ("text/html", "application/xhtml+xml")


class CrawlError(Exception):
    pass


def _is_public_host(host):
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            return False
    return True


def _site(netloc):
    """``www.example.com:443`` -> ``example.com`` — bir saytning turli ko'rinishlarini tenglashtirish uchun."""
    host = netloc.lower().split("@")[-1].split(":")[0]
    return host[4:] if host.startswith("www.") else host


def normalize_start_url(url):
    url = (url or "").strip()
    if not url:
        raise CrawlError("Sayt manzilini kiriting")
    if "://" not in url:
        url = "https://" + url
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname or "." not in parts.hostname:
        raise CrawlError("Manzil noto'g'ri")
    if not _is_public_host(parts.hostname):
        raise CrawlError("Sayt topilmadi yoki bu manzilga ruxsat yo'q")
    return f"{parts.scheme}://{parts.netloc.lower()}{parts.path or '/'}"


def clean_url(url):
    """Fragment va kuzatuv parametrlarini olib tashlaydi, host'ni kichik harfga o'tkazadi."""
    url, _ = urldefrag(url)
    p = urlsplit(url)
    query = urlencode([(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                       if not k.lower().startswith(TRACKING_PARAMS)])
    return urlunsplit((p.scheme, p.netloc.lower(), p.path or "/", query, ""))


def _lastmod(resp):
    try:
        return parsedate_to_datetime(resp.headers["Last-Modified"]).date().isoformat()
    except (KeyError, TypeError, ValueError, IndexError):
        return None


def _robots(session, start_url):
    """robots.txt (topilmasa yoki o'qib bo'lmasa — hamma narsa ruxsat)."""
    rp = robotparser.RobotFileParser()
    p = urlsplit(start_url)
    try:
        resp = session.get(f"{p.scheme}://{p.netloc}/robots.txt", timeout=5)
        rp.parse(resp.text.splitlines() if resp.status_code == 200 else [])
    except requests.RequestException:
        rp.parse([])
    return rp


def _fetch(session, url, site):
    """Sahifani yuklaydi: {"url", "lastmod", "links", "index"} yoki None."""
    try:
        resp = session.get(url, timeout=8, allow_redirects=True)
    except requests.RequestException:
        return None
    # Redirect boshqa saytga olib ketsa yoki sahifa HTML bo'lmasa — tashlab ketamiz
    if _site(urlsplit(resp.url).netloc) != site or resp.status_code != 200:
        return None
    if not resp.headers.get("Content-Type", "").lower().startswith(HTML_TYPES):
        return None
    page = {"url": clean_url(resp.url), "lastmod": _lastmod(resp), "links": [], "index": True}
    if "noindex" in resp.headers.get("X-Robots-Tag", "").lower():
        page["index"] = False
    try:
        tree = lxml_html.fromstring(resp.content)
    except (ValueError, lxml_html.etree.ParserError):
        return page
    robots = " ".join(tree.xpath("//meta[translate(@name,'ROBOTS','robots')='robots']/@content")).lower()
    if "noindex" in robots:
        page["index"] = False
    canonical = tree.xpath("//link[translate(@rel,'CANONICL','canonicl')='canonical']/@href")
    if canonical:
        target = clean_url(urljoin(resp.url, canonical[0].strip()))
        if _site(urlsplit(target).netloc) == site:
            page["url"] = target
    if "nofollow" in robots:
        return page
    for a in tree.xpath("//a[@href]"):
        if "nofollow" in (a.get("rel") or "").lower():
            continue
        link = clean_url(urljoin(resp.url, a.get("href").strip()))
        p = urlsplit(link)
        if p.scheme in ("http", "https") and _site(p.netloc) == site and not p.path.lower().endswith(SKIP_EXT):
            page["links"].append(link)
    return page


def crawl(start_url, progress=None, max_pages=MAX_PAGES):
    """Saytni aylanib chiqadi va [{"url", "lastmod", "depth"}] ro'yxatini qaytaradi (bosh sahifa birinchi).

    ``progress(found, checked)`` — har bir to'plamdan keyin chaqiriladi (sahifada jarayonni ko'rsatish uchun).
    """
    start_url = normalize_start_url(start_url)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5"})

    # Bosh sahifa: redirect (example.com -> www.example.com, http -> https) shu yerda aniqlanadi
    first = _fetch(session, start_url, _site(urlsplit(start_url).netloc))
    if first is None:
        raise CrawlError("Sayt ochilmadi: manzilni tekshiring yoki sayt botlarni bloklagan bo'lishi mumkin")
    site = _site(urlsplit(first["url"]).netloc)
    robots = _robots(session, first["url"])
    allowed = lambda u: robots.can_fetch(USER_AGENT, u)  # noqa: E731

    pages, found_urls = [], set()
    seen = {start_url, first["url"]}
    deadline = time.monotonic() + TIME_BUDGET
    checked = 1

    def add(page, depth):
        if page["index"] and page["url"] not in found_urls and allowed(page["url"]):
            found_urls.add(page["url"])
            pages.append({"url": page["url"], "lastmod": page["lastmod"], "depth": depth})

    def enqueue(page, depth, queue):
        for link in page["links"]:
            if link not in seen and allowed(link):
                seen.add(link)
                queue.append((link, depth + 1))

    add(first, 0)
    queue = []
    enqueue(first, 0, queue)
    if progress:
        progress(len(pages), checked)

    # Sahifalar WORKERS tadan parallel yuklanadi
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        while queue and len(pages) < max_pages and time.monotonic() < deadline:
            batch, queue = queue[:WORKERS * 2], queue[WORKERS * 2:]
            results = pool.map(lambda item: (_fetch(session, item[0], site), item[1]), batch)
            for page, depth in results:
                checked += 1
                if page is None or len(pages) >= max_pages:
                    continue
                add(page, depth)
                enqueue(page, depth, queue)
            if progress:
                progress(len(pages), checked)

    if not pages:
        raise CrawlError("Saytda indekslanadigan sahifa topilmadi (noindex yoki robots.txt taqiqlagan)")
    return pages


def build_xml(pages):
    """sitemap.xml matni. ``pages`` — crawl() natijasi yoki oddiy URL'lar ro'yxati (eski format)."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in pages:
        if isinstance(page, str):
            page = {"url": page, "depth": 0 if not lines[2:] else 1}
        # Bosh sahifa 1.0, chuqurlashgan sari kamayadi (0.8, 0.6, ... eng kami 0.4)
        priority = max(0.4, 1.0 - 0.2 * page.get("depth", 1))
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(page['url'])}</loc>")
        if page.get("lastmod"):
            lines.append(f"    <lastmod>{page['lastmod']}</lastmod>")
        lines.append(f"    <priority>{priority:.1f}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"
