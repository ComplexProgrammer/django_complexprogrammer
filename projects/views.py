from atexit import register
import hashlib
import io
import ipaddress
import json
import re
import os
import shutil
import string
import time
import traceback
import uuid

# import cv2
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from core import downloads
from django.db.models import Max
from comments.pages import page_comments

# import googletrans
# from googletrans import Translator
# from instaloader import Instaloader, Profile
# from decouple import config
# from pysitemap import crawler
# import numpy as np
import requests
from django.core.cache import cache

# import yaml
from django_complexprogrammer.settings import (
    CARTOONIZED_FOLDER,
    MEDIA_URL,
    STATIC_URL,
    WRITE_BOX_CARTOONIZER,
    UPLOAD_FOLDER_VIDEOS,
)

# from gcloud_utils import delete_blob, download_video, generate_signed_url, upload_blob
from projects.models import AvtoTest, IsService, Project

# from static.white_box_cartoonizer.cartoonize import WB_Cartoonize
# import skvideo
# import skvideo.io
from PIL import Image

# import pyttsx3
from django.contrib import messages
from django.core import serializers
from projects import sitemap_crawler, youtube_downloader
from django.views.decorators.csrf import ensure_csrf_cookie
# from projects.cartoonize.video_api import api_request

# skvideo.setFFmpegPath(r'C:\Python310\Lib\site-packages\ffmpeg')
# with open('projects/cartoonize/config.yaml', 'r') as fd:
#     opts = yaml.safe_load(fd)
# if opts['colab-mode']:
#     from flask_ngrok import run_with_ngrok
#     run_with_ngrok(app)

# if not opts['run_local']:
#     if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
#         from gcloud_utils import upload_blob, generate_signed_url, delete_blob, download_video
#     else:
#         raise Exception("GOOGLE_APPLICATION_CREDENTIALS not set in environment variables")
#     from video_api import api_request
#     import Algorithmia


def base(request):
    # if request.device.get('is_mobile'):
    #     is_mobile = True
    # else:
    #     is_mobile = False
    class Status:
        Draft = 0, "Draft"
        Active = 1, "Active"

    services = Project.objects.filter(status=1, is_service=True).values()
    projects = Project.actives.all()
    context = {
        "services": services,
        "projects": projects,
        # 'is_mobile': is_mobile,
    }
    return render(request, "base.html", context=context)


# wb_cartoonizer = WB_Cartoonize(WRITE_BOX_CARTOONIZER+'saved_models/', opts['gpu'])


def convert_bytes_to_image(img_bytes):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """

    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode == "RGBA":
        image = Image.new("RGB", pil_image.size, (255, 255, 255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert("RGB")
    # image = np.array(image)

    return image

    # def cartoonize(request):
    if request.method == "POST":
        try:
            if request.files.get("image"):
                img = request.files["image"].read()

                ## Read Image and convert to PIL (RGB) if RGBA convert appropriately
                image = convert_bytes_to_image(img)

                img_name = str(uuid.uuid4())

                cartoon_image = wb_cartoonizer.infer(image)

                cartoonized_img_name = os.path.join(
                    CARTOONIZED_FOLDER, img_name + ".jpg"
                )
                cv2.imwrite(
                    cartoonized_img_name, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR)
                )

                if not opts["run_local"]:
                    # Upload to bucket
                    output_uri = upload_blob(
                        "cartoonized_images",
                        cartoonized_img_name,
                        img_name + ".jpg",
                        content_type="image/jpg",
                    )
                    print(output_uri)
                    # Delete locally stored cartoonized image
                    os.system("rm " + cartoonized_img_name)
                    cartoonized_img_name = generate_signed_url(output_uri)
                context = {"cartoonized_image": cartoonized_img_name}
                return render(request, "projects/cartoonize.html", context=context)
                print(cartoonized_img_name)
                # return render("projects/cartoonize.html",
                #                        cartoonized_image=cartoonized_img_name)

            if request.files.get("video"):
                filename = str(uuid.uuid4()) + ".mp4"
                video = request.files["video"]
                original_video_path = os.path.join(UPLOAD_FOLDER_VIDEOS, filename)
                video.save(original_video_path)

                modified_video_path = os.path.join(
                    UPLOAD_FOLDER_VIDEOS, filename.split(".")[0] + "_modified.mp4"
                )

                ## Fetch Metadata and set frame rate
                file_metadata = skvideo.io.ffprobe(original_video_path)
                original_frame_rate = None
                if "video" in file_metadata:
                    if "@r_frame_rate" in file_metadata["video"]:
                        original_frame_rate = file_metadata["video"]["@r_frame_rate"]

                if opts["original_frame_rate"]:
                    output_frame_rate = original_frame_rate
                else:
                    output_frame_rate = opts["output_frame_rate"]

                output_frame_rate_number = int(output_frame_rate.split("/")[0])

                # change the size if you want higher resolution :
                ############################
                # Recommnded width_resize  #
                ############################
                # width_resize = 1920 for 1080p: 1920x1080.
                # width_resize = 1280 for 720p: 1280x720.
                # width_resize = 854 for 480p: 854x480.
                # width_resize = 640 for 360p: 640x360.
                # width_resize = 426 for 240p: 426x240.
                width_resize = opts["resize-dim"]

                # Slice, Resize and Convert Video as per settings
                if opts["trim-video"]:
                    # change the variable value to change the time_limit of video (In Seconds)
                    time_limit = opts["trim-video-length"]
                    if opts["original_resolution"]:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path),
                                time_limit,
                                output_frame_rate_number,
                                os.path.abspath(modified_video_path),
                            )
                        )
                    else:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path),
                                time_limit,
                                width_resize,
                                output_frame_rate_number,
                                os.path.abspath(modified_video_path),
                            )
                        )
                else:
                    if opts["original_resolution"]:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path),
                                output_frame_rate_number,
                                os.path.abspath(modified_video_path),
                            )
                        )
                    else:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path),
                                width_resize,
                                output_frame_rate_number,
                                os.path.abspath(modified_video_path),
                            )
                        )

                audio_file_path = os.path.join(
                    UPLOAD_FOLDER_VIDEOS, filename.split(".")[0] + "_audio_modified.mp4"
                )
                os.system(
                    "ffmpeg -hide_banner -loglevel warning -i '{}' -map 0:1 -vn -acodec copy -strict -2  '{}'".format(
                        os.path.abspath(modified_video_path),
                        os.path.abspath(audio_file_path),
                    )
                )

                if opts["run_local"]:
                    cartoon_video_path = wb_cartoonizer.process_video(
                        modified_video_path, output_frame_rate
                    )
                # else:
                #     data_uri = upload_blob("processed_videos_cartoonize", modified_video_path, filename,
                #                            content_type='video/mp4', algo_unique_key='cartoonizeinput')
                #     response = api_request(data_uri)
                #     # Delete the processed video from Cloud storage
                #     delete_blob("processed_videos_cartoonize", filename)
                #     cartoon_video_path = download_video('cartoonized_videos', os.path.basename(response['output_uri']),
                #                                         os.path.join(UPLOAD_FOLDER_VIDEOS,
                #                                                      filename.split(".")[0] + "_cartoon.mp4"))

                ## Add audio to the cartoonized video
                final_cartoon_video_path = os.path.join(
                    UPLOAD_FOLDER_VIDEOS, filename.split(".")[0] + "_cartoon_audio.mp4"
                )
                # os.system("ffmpeg -hide_banner -loglevel warning -i '{}' -i '{}' -codec copy -shortest '{}'".format(
                #     os.path.abspath(cartoon_video_path), os.path.abspath(audio_file_path),
                #     os.path.abspath(final_cartoon_video_path)))

                # # Delete the videos from local disk
                # os.system("rm {} {} {} {}".format(original_video_path, modified_video_path, audio_file_path,
                #                                   cartoon_video_path))

                # return render(request, "projects/cartoonize.html", cartoonized_video=final_cartoon_video_path)
                context = {"cartoonized_video": final_cartoon_video_path}
                return render(request, "projects/cartoonize.html", context=context)

        except Exception:
            print(traceback.print_exc())
            messages.error(
                request, "Our server hiccuped :/ Please upload another file! :)"
            )
            return render(request, "projects/cartoonize.html")
    else:
        return render(request, "projects/cartoonize.html")


INSTAGRAM_UNAVAILABLE = (
    "Instagram yuklab olish xizmati vaqtincha ishlamayapti. "
    "Instagram himoyasi kuchaygani sababli ustida ishlayapmiz."
)


def instagram_downloader_(request):
    if request.method == "POST":
        return JsonResponse({"result": "0", "error": INSTAGRAM_UNAVAILABLE}, status=503)
    context = {"comments": page_comments(request), "unavailable": INSTAGRAM_UNAVAILABLE}
    return render(request, "projects/instagram_downloader.html", context=context)


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

    downloads.cleanup_old()
    try:
        if choice == 3:
            filename = youtube_downloader.download_audio(link)
        elif choice == 2:
            # Pleylist uchun birinchi videoni qaytaramiz, qolganlari ro'yxatda
            filenames = youtube_downloader.download_playlist(link, quality)
            if not filenames:
                return JsonResponse({"result": "0", "error": "Pleylist bo'sh"})
            return JsonResponse({"result": filenames[0], "files": filenames})
        else:
            filename = youtube_downloader.download_video(link, quality)
    except youtube_downloader.DownloadError as exc:
        return JsonResponse({"result": "0", "error": str(exc)})
    return JsonResponse({"result": filename})


def fetch_json(url, cache_key, timeout=5, ttl=600, params=None):
    """Tashqi API'dan JSON oladi: natija keshlanadi, API ishlamasa None qaytaradi."""
    data = cache.get(cache_key)
    if data is not None:
        return data
    try:
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return None
    cache.set(cache_key, data, ttl)
    return data


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
    context = {"comments": comments, "row": range(1, total_bilets), "bilet": bilet}
    return render(request, "projects/avtotest.html", context=context)


def GetSavol(request):
    bilet = request.GET.get("bilet", False)
    if bilet == False:
        avtotest = AvtoTest.objects.all().values()
    else:
        avtotest = AvtoTest.objects.filter(bilet=bilet).values()
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


CBU_RATES_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"


def exchangerates(request):
    data = fetch_json(CBU_RATES_URL, "api:cbu", ttl=1800)
    context = {
        "data": data or [],
        "api_error": data is None,
        "comments": page_comments(request),
    }
    return render(request, "projects/exchangerates.html", context=context)


def GetExchangeRates(request):
    data = fetch_json(CBU_RATES_URL, "api:cbu", ttl=1800)
    if data is None:
        return JsonResponse({"data": [], "error": "Markaziy bank sayti javob bermayapti"}, status=503)
    return JsonResponse({"data": data})


def changetext(request):
    comments = page_comments(request)
    context = {"comments": comments}
    if request.method == "POST":
        text = request.POST["text"]
        characters = [
            ["A", "А"],
            ["B", "Б"],
            ["D", "Д"],
            ["E", "Е"],
            ["F", "Ф"],
            ["G", "Г"],
            ["H", "Ҳ"],
            ["I", "И"],
            ["J", "Ж"],
            ["K", "К"],
            ["L", "Л"],
            ["M", "М"],
            ["N", "Н"],
            ["O", "О"],
            ["P", "П"],
            ["Q", "Қ"],
            ["R", "Р"],
            ["S", "С"],
            ["T", "Т"],
            ["U", "У"],
            ["V", "В"],
            ["X", "Х"],
            ["Y", "Й"],
            ["Z", "З"],
            ["a", "а"],
            ["b", "б"],
            ["d", "д"],
            ["e", "е"],
            ["f", "ф"],
            ["g", "г"],
            ["h", "ҳ"],
            ["i", "и"],
            ["j", "ж"],
            ["k", "к"],
            ["l", "л"],
            ["m", "м"],
            ["n", "н"],
            ["o", "о"],
            ["p", "п"],
            ["q", "қ"],
            ["r", "р"],
            ["s", "с"],
            ["t", "т"],
            ["u", "у"],
            ["v", "в"],
            ["x", "х"],
            ["y", "й"],
            ["z", "з"],
            ["А", "A"],
            ["Б", "B"],
            ["С", "C"],
            ["Ч", "Ch"],
            ["Д", "D"],
            ["Е", "E"],
            ["Ф", "F"],
            ["Г", "G"],
            ["Ҳ", "H"],
            ["И", "I"],
            ["Ж", "J"],
            ["К", "K"],
            ["Л", "L"],
            ["М", "M"],
            ["Н", "N"],
            ["О", "O"],
            ["П", "P"],
            ["Қ", "Q"],
            ["Р", "R"],
            ["С", "S"],
            ["Ш", "T"],
            ["Т", "U"],
            ["У", "V"],
            ["В", "X"],
            ["Х", "Y"],
            ["Й", "Z"],
            ["Я", "Ya"],
            ["Ю", "Yu"],
            ["Ё", "Yo"],
            ["З", "Z"],
            ["Ғ", "Gʼ"],
            ["а", "a"],
            ["б", "b"],
            ["с", "c"],
            ["ч", "ch"],
            ["д", "d"],
            ["е", "e"],
            ["ф", "f"],
            ["г", "g"],
            ["ҳ", "h"],
            ["и", "i"],
            ["ж", "j"],
            ["к", "k"],
            ["л", "l"],
            ["м", "m"],
            ["н", "n"],
            ["о", "o"],
            ["п", "p"],
            ["қ", "q"],
            ["р", "r"],
            ["с", "s"],
            ["ш", "sh"],
            ["т", "t"],
            ["у", "u"],
            ["в", "v"],
            ["х", "x"],
            ["й", "y"],
            ["я", "ya"],
            ["ю", "yu"],
            ["ё", "yo"],
            ["з", "z"],
            ["ғ", "gʼ"],
            ["ъ", "`"],
            ["`", "ъ"],
            ["'", "ъ"],
            ["’", "ъ"],
            ["‘", "ъ"],
        ]

        lotin = False
        arr = list(text)
        for ar in arr:
            if 0 < ord(ar) < 1024:
                lotin = True
            for obj in characters:
                if obj[0] == ar:
                    text = text.replace(ar, obj[1])

        if lotin:
            text = text.replace("Оъ", "Ў").replace("оъ", "ў")
            text = (
                text.replace("йа", "я")
                .replace("Йа", "Я")
                .replace("ЙА", "Я")
                .replace("йА", "я")
            )
            text = (
                text.replace("йо", "ё")
                .replace("Йо", "Ё")
                .replace("ЙО", "Ё")
                .replace("йО", "ё")
            )
            text = (
                text.replace("йу", "ю")
                .replace("Йу", "Ю")
                .replace("ЙУ", "Ю")
                .replace("йУ", "ю")
            )
            text = (
                text.replace("сҳ", "ш")
                .replace("Сҳ", "Ш")
                .replace("СҲ", "Ш")
                .replace("сҲ", "ш")
            )
            text = (
                text.replace("cҳ", "ч")
                .replace("Cҳ", "Ч")
                .replace("CҲ", "Ч")
                .replace("cҲ", "ч")
            )
            text = text.replace("Гъ", "Ғ").replace("гъ", "ғ")
        else:
            text = text.replace("Я", "Ya").replace("я", "ya")
            text = text.replace("Ё", "Yo").replace("ё", "yo")
            text = text.replace("Ю", "Yu").replace("ю", "yu")
            text = text.replace("Ш", "Sh").replace("ш", "sh")
            text = text.replace("Ч", "Ch").replace("ч", "ch")
            text = text.replace("Ў", "Oʼ").replace("ў", "oʼ")
            text = text.replace("Ғ", "Gʼ").replace("ғ", "gʼ")
        # return JsonResponse(text, safe=False)
        return HttpResponse(text)
    return render(request, "projects/changetext.html", context=context)


def GetChangeTextData(request):
    text = request.GET.get("text", None)
    if text is None:
        return ""
    characters = [
        ["A", "А"],
        ["B", "Б"],
        ["D", "Д"],
        ["E", "Е"],
        ["F", "Ф"],
        ["G", "Г"],
        ["H", "Ҳ"],
        ["I", "И"],
        ["J", "Ж"],
        ["K", "К"],
        ["L", "Л"],
        ["M", "М"],
        ["N", "Н"],
        ["O", "О"],
        ["P", "П"],
        ["Q", "Қ"],
        ["R", "Р"],
        ["S", "С"],
        ["T", "Т"],
        ["U", "У"],
        ["V", "В"],
        ["X", "Х"],
        ["Y", "Й"],
        ["Z", "З"],
        ["a", "а"],
        ["b", "б"],
        ["d", "д"],
        ["e", "е"],
        ["f", "ф"],
        ["g", "г"],
        ["h", "ҳ"],
        ["i", "и"],
        ["j", "ж"],
        ["k", "к"],
        ["l", "л"],
        ["m", "м"],
        ["n", "н"],
        ["o", "о"],
        ["p", "п"],
        ["q", "қ"],
        ["r", "р"],
        ["s", "с"],
        ["t", "т"],
        ["u", "у"],
        ["v", "в"],
        ["x", "х"],
        ["y", "й"],
        ["z", "з"],
        ["А", "A"],
        ["Б", "B"],
        ["С", "C"],
        ["Ч", "Ch"],
        ["Д", "D"],
        ["Е", "E"],
        ["Ф", "F"],
        ["Г", "G"],
        ["Ҳ", "H"],
        ["И", "I"],
        ["Ж", "J"],
        ["К", "K"],
        ["Л", "L"],
        ["М", "M"],
        ["Н", "N"],
        ["О", "O"],
        ["П", "P"],
        ["Қ", "Q"],
        ["Р", "R"],
        ["С", "S"],
        ["Ш", "T"],
        ["Т", "U"],
        ["У", "V"],
        ["В", "X"],
        ["Х", "Y"],
        ["Й", "Z"],
        ["Я", "Ya"],
        ["Ю", "Yu"],
        ["Ё", "Yo"],
        ["З", "Z"],
        ["Ғ", "Gʼ"],
        ["а", "a"],
        ["б", "b"],
        ["с", "c"],
        ["ч", "ch"],
        ["д", "d"],
        ["е", "e"],
        ["ф", "f"],
        ["г", "g"],
        ["ҳ", "h"],
        ["и", "i"],
        ["ж", "j"],
        ["к", "k"],
        ["л", "l"],
        ["м", "m"],
        ["н", "n"],
        ["о", "o"],
        ["п", "p"],
        ["қ", "q"],
        ["р", "r"],
        ["с", "s"],
        ["ш", "sh"],
        ["т", "t"],
        ["у", "u"],
        ["в", "v"],
        ["х", "x"],
        ["й", "y"],
        ["я", "ya"],
        ["ю", "yu"],
        ["ё", "yo"],
        ["з", "z"],
        ["ғ", "gʼ"],
        ["ъ", "`"],
        ["`", "ъ"],
        ["'", "ъ"],
    ]

    lotin = False
    arr = list(text)
    for ar in arr:
        if 0 < ord(ar) < 1024:
            lotin = True
        for obj in characters:
            if obj[0] == ar:
                text = text.replace(ar, obj[1])

    if lotin:
        text = text.replace("Оъ", "Ў").replace("оъ", "ў")
        text = (
            text.replace("йа", "я")
            .replace("Йа", "Я")
            .replace("ЙА", "Я")
            .replace("йА", "я")
        )
        text = (
            text.replace("йо", "ё")
            .replace("Йо", "Ё")
            .replace("ЙО", "Ё")
            .replace("йО", "ё")
        )
        text = (
            text.replace("йу", "ю")
            .replace("Йу", "Ю")
            .replace("ЙУ", "Ю")
            .replace("йУ", "ю")
        )
        text = (
            text.replace("сҳ", "ш")
            .replace("Сҳ", "Ш")
            .replace("СҲ", "Ш")
            .replace("сҲ", "ш")
        )
        text = (
            text.replace("cҳ", "ч")
            .replace("Cҳ", "Ч")
            .replace("CҲ", "Ч")
            .replace("cҲ", "ч")
        )
        text = text.replace("Гъ", "Ғ").replace("гъ", "ғ")
    else:
        text = text.replace("Я", "Ya").replace("я", "ya")
        text = text.replace("Ё", "Yo").replace("ё", "yo")
        text = text.replace("Ю", "Yu").replace("ю", "yu")
        text = text.replace("Ш", "Sh").replace("ш", "sh")
        text = text.replace("Ч", "Ch").replace("ч", "ch")
        text = text.replace("Ў", "Oʼ").replace("ў", "oʼ")
        text = text.replace("Ғ", "Gʼ").replace("ғ", "gʼ")
    return HttpResponse(text)


def client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def ip(request):
    comments = page_comments(request)
    # Parametr berilmasa — serverning emas, foydalanuvchining o'z IP manzili
    raw_ip = request.GET.get("ip") or client_ip(request)
    try:
        ip_obj = ipaddress.ip_address(raw_ip.strip())
    except ValueError:
        return render(
            request,
            "projects/ip.html",
            {"data": {"error": True, "reason": "Noto'g'ri IP manzil"}, "comments": comments},
        )
    if ip_obj.is_private or ip_obj.is_loopback:
        data = {"ip": str(ip_obj), "error": True, "reason": "Lokal (xususiy) IP manzil"}
    else:
        data = fetch_json(f"https://ipapi.co/{ip_obj}/json/", f"api:ip:{ip_obj}", ttl=3600)
        if data is None:
            data = {"ip": str(ip_obj), "error": True, "reason": "Xizmat vaqtincha ishlamayapti"}
    return render(request, "projects/ip.html", {"data": data, "comments": comments})


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
    try:
        urls = sitemap_crawler.crawl(url)
    except sitemap_crawler.CrawlError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
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
