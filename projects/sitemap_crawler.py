"""Oddiy sayt xaritasi (sitemap.xml) generatori.

Faqat bitta domen ichida yuradi, sahifalar soni va umumiy vaqt cheklangan.
Ichki tarmoq manzillariga (127.0.0.1, 10.x, 192.168.x ...) so'rov yuborilmaydi.
"""

import ipaddress
import socket
import time
from urllib.parse import urldefrag, urljoin, urlsplit
from xml.sax.saxutils import escape

import requests
from lxml import html as lxml_html

MAX_PAGES = 200
TIME_BUDGET = 25  # soniya
SKIP_EXT = (
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico", ".css", ".js",
    ".pdf", ".zip", ".rar", ".mp3", ".mp4", ".avi", ".doc", ".docx", ".xls", ".xlsx",
)
HEADERS = {"User-Agent": "ComplexProgrammer-SitemapBot/1.0 (+https://complexprogrammer.uz/sitemap/)"}


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


def normalize_start_url(url):
    url = (url or "").strip()
    if not url:
        raise CrawlError("Sayt manzilini kiriting")
    if "://" not in url:
        url = "https://" + url
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise CrawlError("Manzil noto'g'ri")
    if not _is_public_host(parts.hostname):
        raise CrawlError("Bu manzilga ruxsat yo'q")
    return f"{parts.scheme}://{parts.netloc}{parts.path or '/'}"


def crawl(start_url):
    start_url = normalize_start_url(start_url)
    host = urlsplit(start_url).netloc
    seen = {start_url}
    queue = [start_url]
    found = []
    deadline = time.monotonic() + TIME_BUDGET
    session = requests.Session()
    session.headers.update(HEADERS)

    while queue and len(found) < MAX_PAGES and time.monotonic() < deadline:
        url = queue.pop(0)
        try:
            resp = session.get(url, timeout=5, allow_redirects=True)
        except requests.RequestException:
            continue
        # Redirect boshqa domenga olib ketsa — tashlab ketamiz
        if urlsplit(resp.url).netloc != host or resp.status_code != 200:
            continue
        if "text/html" not in resp.headers.get("Content-Type", ""):
            continue
        found.append(resp.url)
        try:
            tree = lxml_html.fromstring(resp.content)
        except (ValueError, lxml_html.etree.ParserError):
            continue
        for href in tree.xpath("//a/@href"):
            link, _ = urldefrag(urljoin(resp.url, href))
            parts = urlsplit(link)
            if parts.scheme not in ("http", "https") or parts.netloc != host:
                continue
            if parts.path.lower().endswith(SKIP_EXT) or link in seen:
                continue
            seen.add(link)
            queue.append(link)

    if not found:
        raise CrawlError("Saytdan birorta ham sahifa olinmadi")
    return found


def build_xml(urls):
    items = "\n".join(
        f"  <url><loc>{escape(u)}</loc><priority>{'1.0' if i == 0 else '0.8'}</priority></url>"
        for i, u in enumerate(urls)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{items}\n</urlset>\n"
    )
