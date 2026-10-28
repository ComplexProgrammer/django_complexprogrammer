"""YouTube'dan video/audio yuklab olish (yt-dlp).

pytube YouTube o'zgarishlaridan keyin ishlamay qoldi (HTTP 400) — yt-dlp faol qo'llab-quvvatlanadi.
YouTube endi ovoz+video birga bo'lgan (progressive) formatni deyarli bermaydi: video va audio alohida
yuklanib, ffmpeg bilan MP4 ga birlashtiriladi. ffmpeg ``imageio-ffmpeg`` paketidan (statik binar,
serverga alohida o'rnatish shart emas) yoki tizimdan olinadi; topilmasa — birlashtirish talab qilmaydigan
formatlar tanlanadi.
"""

import logging
import os
import re
import shutil
import uuid

import yt_dlp
from django.conf import settings

from core import downloads

logger = logging.getLogger(__name__)

# Juda uzun videolar server diski va vaqtini band qilmasin
MAX_DURATION = 3 * 3600
MAX_FILESIZE = 1024 * 1024 * 1024
PLAYLIST_LIMIT = 10
# Sifat nomi -> maksimal balandlik (px); eski mobil ilova nomlari ham qabul qilinadi
QUALITY_HEIGHTS = {
    "low": 360, "360": 360, "360p": 360,
    "medium": 720, "720": 720, "720p": 720, "hd": 720,
    "high": 1080, "1080": 1080, "1080p": 1080, "fullhd": 1080, "full_hd": 1080, "full hd": 1080,
    "very high": 2160, "2160": 2160, "2160p": 2160, "4k": 2160, "4K": 2160,
}

UNAVAILABLE = "YouTube'dan yuklab bo'lmadi, birozdan so'ng urinib ko'ring"


class DownloadError(Exception):
    """Foydalanuvchiga ko'rsatiladigan tushunarli xato; ``detail`` — yt-dlp'ning asl xabari (log va diagnostika uchun)."""

    def __init__(self, message, detail=""):
        super().__init__(message)
        self.detail = detail


def ffmpeg_path():
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # paket yo'q yoki binar topilmadi
        return shutil.which("ffmpeg")


def js_runtimes():
    """YouTube'ning kirilgan (cookie) klientlari imzoni JavaScript bilan hal qilishni talab qiladi.

    yt-dlp sukut bo'yicha faqat tizimdagi deno'ni qidiradi — Passenger PATH'ida u bo'lmasligi mumkin.
    Shuning uchun pip ``deno`` paketining binari (yoki tizimdagi deno/node) yo'li bilan aniq beriladi.
    """
    runtimes = {}
    try:
        import deno

        runtimes["deno"] = {"path": deno.find_deno_bin()}
    except Exception:  # paket yo'q yoki binar topilmadi
        if shutil.which("deno"):
            runtimes["deno"] = {}
    node = getattr(settings, "YTDLP_NODE", "") or shutil.which("node")
    if node:
        runtimes["node"] = {"path": node}
    return runtimes or {"deno": {}}


def _error(exc):
    """yt-dlp xatosini foydalanuvchiga tushunarli DownloadError'ga aylantiradi (asl matn logga yoziladi)."""
    detail = re.sub(r"\x1b\[[0-9;]*m", "", str(exc))  # terminal rang kodlari logni chalkashtirmasin
    logger.warning("yt-dlp: %s", detail)
    return DownloadError(_explain(detail), detail)


def _explain(exc):
    """yt-dlp xatosini foydalanuvchiga tushunarli matnga aylantiradi."""
    text = str(exc).lower()
    if "requested format is not available" in text or "only images are available" in text:
        # JS runtime yo'q yoki YouTube imzosini hal qilib bo'lmadi — video formatlari olinmadi
        return UNAVAILABLE
    if "sign in to confirm" in text or "not a bot" in text:
        return "YouTube hozir serverdan yuklashni cheklab qo'ygan. Birozdan so'ng urinib ko'ring"
    if "private video" in text:
        return "Bu video yopiq (private) — yuklab bo'lmaydi"
    if "age" in text and ("restricted" in text or "confirm your age" in text):
        return "Yosh cheklovi bor video — yuklab bo'lmaydi"
    if "unavailable" in text or "not available" in text or "removed" in text:
        return "Video topilmadi yoki o'chirilgan"
    if "live" in text and "stream" in text:
        return "Jonli efirni yuklab bo'lmaydi"
    if "file is larger than max-filesize" in text:
        return "Fayl juda katta — pastroq sifatni tanlang"
    return UNAVAILABLE


def _options(**extra):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "noplaylist": True,
        "socket_timeout": 20,
        "retries": 3,
    }
    ff = ffmpeg_path()
    if ff:
        opts["ffmpeg_location"] = ff
    opts["js_runtimes"] = js_runtimes()
    # Server IP'si bloklanganda: kirilgan akkaunt cookie'lari va/yoki proksi (settings.YTDLP_*)
    cookies = getattr(settings, "YTDLP_COOKIES", "")
    if cookies and os.path.isfile(cookies):
        opts["cookiefile"] = cookies
    proxy = getattr(settings, "YTDLP_PROXY", "")
    if proxy:
        opts["proxy"] = proxy
    opts.update(extra)
    return opts


def _check(info):
    if info.get("is_live"):
        raise DownloadError("Jonli efirni yuklab bo'lmaydi")
    if (info.get("duration") or 0) > MAX_DURATION:
        raise DownloadError("Video 3 soatdan uzun — yuklab bo'lmaydi")


def video_info(url):
    """Yuklashdan oldin ko'rsatiladigan ma'lumot: nom, rasm, davomiylik, mavjud sifatlar."""
    try:
        with yt_dlp.YoutubeDL(_options(skip_download=True)) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as exc:
        raise _error(exc) from exc
    heights = sorted({f["height"] for f in info.get("formats") or [] if f.get("height") and f.get("vcodec") not in (None, "none")})
    return {
        "id": info.get("id"),
        "title": info.get("title") or "",
        "uploader": info.get("uploader") or info.get("channel") or "",
        "duration": info.get("duration") or 0,
        "thumbnail": info.get("thumbnail") or "",
        "heights": heights,
        "is_live": bool(info.get("is_live")),
        "too_long": (info.get("duration") or 0) > MAX_DURATION,
        "can_merge": bool(ffmpeg_path()),
    }


def _download(url, opts, ext, progress=None):
    """Faylni vaqtinchalik nom bilan yuklaydi va ``downloads`` papkasida xavfsiz nom bilan qaytaradi."""
    folder = downloads.ensure_dir()
    tmp_id = uuid.uuid4().hex
    hooks = []
    if progress:
        def hook(d):
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                if total:
                    progress(min(99, int(d.get("downloaded_bytes", 0) * 100 / total)))
            elif d.get("status") == "finished":
                progress(100)
        hooks.append(hook)
    opts = _options(
        outtmpl=os.path.join(folder, tmp_id + ".%(ext)s"),
        progress_hooks=hooks,
        max_filesize=MAX_FILESIZE,
        **opts,
    )
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            # Avval ma'lumot (davomiylik, jonli efir) tekshiriladi, keyin shu natija bilan yuklanadi
            info = ydl.extract_info(url, download=False)
            _check(info)
            info = ydl.process_ie_result(info, download=True)
    except yt_dlp.utils.DownloadError as exc:
        _cleanup(folder, tmp_id)
        raise _error(exc) from exc
    # Postprocessor (birlashtirish / mp3) yakuniy kengaytmani o'zgartirishi mumkin — tayyor faylni topamiz
    produced = [f for f in os.listdir(folder) if f.startswith(tmp_id + ".") and not f.endswith((".part", ".ytdl"))]
    final = next((f for f in produced if f.endswith("." + ext)), produced[0] if produced else None)
    if not final:
        raise DownloadError(UNAVAILABLE)
    name = downloads.new_name(info.get("title") or "video", os.path.splitext(final)[1])
    os.replace(os.path.join(folder, final), os.path.join(folder, name))
    _cleanup(folder, tmp_id)
    return name


def _cleanup(folder, tmp_id):
    for f in os.listdir(folder):
        if f.startswith(tmp_id):
            try:
                os.remove(os.path.join(folder, f))
            except OSError:
                pass


def download_video(url, resolution, progress=None):
    """Videoni (MP4) media/downloads ga saqlaydi va fayl nomini qaytaradi."""
    height = QUALITY_HEIGHTS.get(str(resolution), 360)
    if ffmpeg_path():
        # Alohida video + audio -> MP4. Avval H.264 (avc1): AV1/VP9 ko'p telefon va pleyerlarda ochilmaydi.
        # YouTube H.264 ni 1080p gacha beradi — 4K uchun keyingi variantlarga (VP9/AV1) o'tiladi.
        fmt = (f"bv*[height<={height}][vcodec^=avc1]+ba[ext=m4a]/bv*[height<={height}][ext=mp4]+ba[ext=m4a]/"
               f"bv*[height<={height}]+ba/b[height<={height}]/bv*+ba/b")
        return _download(url, {"format": fmt, "merge_output_format": "mp4"}, "mp4", progress)
    return _download(url, {"format": f"b[height<={height}][ext=mp4]/b[ext=mp4]/b"}, "mp4", progress)


def download_audio(url, progress=None):
    """Audio: ffmpeg bo'lsa MP3, aks holda konvertatsiyasiz M4A."""
    if ffmpeg_path():
        pp = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
        return _download(url, {"format": "ba[ext=m4a]/ba", "postprocessors": pp}, "mp3", progress)
    return _download(url, {"format": "ba[ext=m4a]/ba"}, "m4a", progress)


def download_videos(urls, resolution):
    return [download_video(url, resolution) for url in urls]


def download_playlist(url, resolution):
    """Pleylistning birinchi PLAYLIST_LIMIT ta videosi."""
    try:
        with yt_dlp.YoutubeDL(_options(noplaylist=False, extract_flat=True, playlistend=PLAYLIST_LIMIT)) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as exc:
        raise _error(exc) from exc
    urls = [e.get("url") or f"https://www.youtube.com/watch?v={e['id']}" for e in info.get("entries") or [] if e.get("id")]
    return download_videos(urls[:PLAYLIST_LIMIT], resolution)


def choose_resolution(resolution):
    """Eski API bilan moslik uchun: sifat nomi -> maksimal balandlik."""
    return QUALITY_HEIGHTS.get(str(resolution), 360)


def is_youtube_url(link):
    return isinstance(link, str) and link.startswith(
        ("https://www.youtube.com/", "https://youtube.com/", "https://youtu.be/", "https://m.youtube.com/",
         "https://music.youtube.com/", "http://www.youtube.com/", "http://youtube.com/", "http://youtu.be/")
    )
