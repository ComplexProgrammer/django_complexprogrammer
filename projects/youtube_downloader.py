import pytube

from core import downloads


class DownloadError(Exception):
    """Foydalanuvchiga ko'rsatiladigan tushunarli xato."""


def _youtube(url):
    try:
        return pytube.YouTube(url)
    except Exception as exc:  # pytube har xil ichki xatolar tashlaydi
        raise DownloadError("Video topilmadi yoki havola noto'g'ri") from exc


def _save(stream, title, ext=None):
    if stream is None:
        raise DownloadError("Bu sifatdagi video mavjud emas, boshqa sifatni tanlang")
    name = downloads.new_name(title or "video", ext or "." + stream.subtype)
    try:
        stream.download(output_path=downloads.ensure_dir(), filename=name)
    except Exception as exc:
        raise DownloadError("YouTube'dan yuklab bo'lmadi, birozdan so'ng urinib ko'ring") from exc
    return name


def download_video(url, resolution):
    """Videoni media/downloads ga saqlaydi va fayl nomini qaytaradi."""
    video = _youtube(url)
    stream = video.streams.get_by_itag(choose_resolution(resolution))
    if stream is None:
        # So'ralgan sifat bo'lmasa — ovoz+video birga bo'lgan eng yaxshi oqim
        stream = video.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
    return _save(stream, video.title)


def download_audio(url):
    """Faqat audio oqimini (m4a) yuklaydi — mp3 o'rniga, konvertatsiyasiz."""
    video = _youtube(url)
    stream = video.streams.get_audio_only()
    return _save(stream, video.title, ".m4a")


def download_videos(urls, resolution):
    return [download_video(url, resolution) for url in urls]


def download_playlist(url, resolution):
    playlist = pytube.Playlist(url)
    return download_videos(playlist.video_urls, resolution)


def choose_resolution(resolution):
    if resolution in ["low", "360", "360p"]:
        itag = 18
    elif resolution in ["medium", "720", "720p", "hd"]:
        itag = 22
    elif resolution in ["high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
        itag = 137
    elif resolution in ["very high", "2160", "2160p", "4K", "4k"]:
        itag = 313
    else:
        itag = 18
    return itag


def is_youtube_url(link):
    return isinstance(link, str) and link.startswith(
        ("https://www.youtube.com/", "https://youtube.com/", "https://youtu.be/", "https://m.youtube.com/")
    )

