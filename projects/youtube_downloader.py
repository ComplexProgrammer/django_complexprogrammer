import pytube
from moviepy.editor import VideoFileClip


def download_video(url, resolution):
    itag = choose_resolution(resolution)
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    return stream.default_filename


def download_videos(urls, resolution):
    filenames = []
    for url in urls:
        filename = download_video(url, resolution)
        filenames.append(filename)
    return filenames


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


def input_links():
    print("Videolarning havolalarini kiriting (""STOP"" ni kiritish bilan yakunlang):")

    links = []
    link = ""

    while link != "STOP" and link != "stop":
        link = input()
        links.append(link)

    links.pop()

    return links

def convert_to_mp3(filename):
    clip = VideoFileClip(filename)
    clip.audio.write_audiofile(filename[:-4] + ".mp3")
    clip.close()