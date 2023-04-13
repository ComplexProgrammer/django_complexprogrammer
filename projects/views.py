from atexit import register
import io
import json
import os
import random
import shutil
import string
import time
import traceback
import uuid
import cv2
from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
import googletrans
from googletrans import Translator
from instaloader import Instaloader, Profile
# from pysitemap import crawler
import numpy as np
import urllib3
import yaml
from django_complexprogrammer.settings import CARTOONIZED_FOLDER, GET_FILE_FORMATS, MEDIA_URL, STATIC_URL, WRITE_BOX_CARTOONIZER, UPLOAD_FOLDER_VIDEOS
# from gcloud_utils import delete_blob, download_video, generate_signed_url, upload_blob
from projects.models import AvtoTest, Project
# from static.white_box_cartoonizer.cartoonize import WB_Cartoonize
import skvideo
import skvideo.io
from PIL import Image
from django.contrib import messages
from django.core import serializers
from projects import youtube_downloader

# from projects.cartoonize.video_api import api_request

# skvideo.setFFmpegPath(r'C:\Python310\Lib\site-packages\ffmpeg')
with open('projects/cartoonize/config.yaml', 'r') as fd:
    opts = yaml.safe_load(fd)
# if opts['colab-mode']:
#     from flask_ngrok import run_with_ngrok
#     run_with_ngrok(app)

if not opts['run_local']:
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        from gcloud_utils import upload_blob, generate_signed_url, delete_blob, download_video
    else:
        raise Exception("GOOGLE_APPLICATION_CREDENTIALS not set in environment variables")
    from video_api import api_request

def base(request):
    services=Project.services.all()
    projects=Project.actives.all()
    context={
        'services': services,
        'projects': projects
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
        image = pil_image.convert('RGB')
    image = np.array(image)

    return image

# def cartoonize(request):
    if request.method == 'POST':
        try:
            if request.files.get('image'):
                img = request.files["image"].read()

                ## Read Image and convert to PIL (RGB) if RGBA convert appropriately
                image = convert_bytes_to_image(img)

                img_name = str(uuid.uuid4())

                cartoon_image = wb_cartoonizer.infer(image)

                cartoonized_img_name = os.path.join(CARTOONIZED_FOLDER, img_name + ".jpg")
                cv2.imwrite(cartoonized_img_name, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))

                if not opts["run_local"]:
                    # Upload to bucket
                    output_uri = upload_blob("cartoonized_images", cartoonized_img_name, img_name + ".jpg",
                                             content_type='image/jpg')
                    print(output_uri)
                    # Delete locally stored cartoonized image
                    os.system("rm " + cartoonized_img_name)
                    cartoonized_img_name = generate_signed_url(output_uri)
                print(cartoonized_img_name)
                return render("projects/cartoonize.html",
                                       cartoonized_image=cartoonized_img_name)

            if request.files.get('video'):

                filename = str(uuid.uuid4()) + ".mp4"
                video = request.files["video"]
                original_video_path = os.path.join(UPLOAD_FOLDER_VIDEOS, filename)
                video.save(original_video_path)

                modified_video_path = os.path.join(UPLOAD_FOLDER_VIDEOS,
                                                   filename.split(".")[0] + "_modified.mp4")

                ## Fetch Metadata and set frame rate
                file_metadata = skvideo.io.ffprobe(original_video_path)
                original_frame_rate = None
                if 'video' in file_metadata:
                    if '@r_frame_rate' in file_metadata['video']:
                        original_frame_rate = file_metadata['video']['@r_frame_rate']

                if opts['original_frame_rate']:
                    output_frame_rate = original_frame_rate
                else:
                    output_frame_rate = opts['output_frame_rate']

                output_frame_rate_number = int(output_frame_rate.split('/')[0])

                # change the size if you want higher resolution :
                ############################
                # Recommnded width_resize  #
                ############################
                # width_resize = 1920 for 1080p: 1920x1080.
                # width_resize = 1280 for 720p: 1280x720.
                # width_resize = 854 for 480p: 854x480.
                # width_resize = 640 for 360p: 640x360.
                # width_resize = 426 for 240p: 426x240.
                width_resize = opts['resize-dim']

                # Slice, Resize and Convert Video as per settings
                if opts['trim-video']:
                    # change the variable value to change the time_limit of video (In Seconds)
                    time_limit = opts['trim-video-length']
                    if opts['original_resolution']:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), time_limit, output_frame_rate_number,
                                os.path.abspath(modified_video_path)))
                    else:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), time_limit, width_resize,
                                output_frame_rate_number, os.path.abspath(modified_video_path)))
                else:
                    if opts['original_resolution']:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), output_frame_rate_number,
                                os.path.abspath(modified_video_path)))
                    else:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), width_resize, output_frame_rate_number,
                                os.path.abspath(modified_video_path)))

                audio_file_path = os.path.join(UPLOAD_FOLDER_VIDEOS,
                                               filename.split(".")[0] + "_audio_modified.mp4")
                os.system(
                    "ffmpeg -hide_banner -loglevel warning -i '{}' -map 0:1 -vn -acodec copy -strict -2  '{}'".format(
                        os.path.abspath(modified_video_path), os.path.abspath(audio_file_path)))

                if opts["run_local"]:
                    cartoon_video_path = wb_cartoonizer.process_video(modified_video_path, output_frame_rate)
                else:
                    data_uri = upload_blob("processed_videos_cartoonize", modified_video_path, filename,
                                           content_type='video/mp4', algo_unique_key='cartoonizeinput')
                    response = api_request(data_uri)
                    # Delete the processed video from Cloud storage
                    delete_blob("processed_videos_cartoonize", filename)
                    cartoon_video_path = download_video('cartoonized_videos', os.path.basename(response['output_uri']),
                                                        os.path.join(UPLOAD_FOLDER_VIDEOS,
                                                                     filename.split(".")[0] + "_cartoon.mp4"))

                ## Add audio to the cartoonized video
                final_cartoon_video_path = os.path.join(UPLOAD_FOLDER_VIDEOS,
                                                        filename.split(".")[0] + "_cartoon_audio.mp4")
                os.system("ffmpeg -hide_banner -loglevel warning -i '{}' -i '{}' -codec copy -shortest '{}'".format(
                    os.path.abspath(cartoon_video_path), os.path.abspath(audio_file_path),
                    os.path.abspath(final_cartoon_video_path)))

                # Delete the videos from local disk
                os.system("rm {} {} {} {}".format(original_video_path, modified_video_path, audio_file_path,
                                                  cartoon_video_path))

                return render("projects/cartoonize.html", cartoonized_video=final_cartoon_video_path)

        except Exception:
            print(traceback.print_exc())
            messages.error(request, 'Our server hiccuped :/ Please upload another file! :)')
            return render("projects/cartoonize.html")
    else:
        return render(request, "projects/cartoonize.html")
def save_insta_collection(user_name):
    print("start...")
    L = Instaloader(dirname_pattern='media/instagram_downloader/{target}')
    PROFILE = user_name
    profile = Profile.from_username(
        L.context,
        PROFILE
    )
    uploaded_posts = profile.get_posts()
    # if not(os.path.isdir(save_folder)):
    #     os.makedirs(save_folder)

    # Start Saving posts with a count
    count = 1
    for post in uploaded_posts:
        print(count)
        L.download_post(
            post,
            PROFILE
        )
    save_folder = os.path.join(
        'media',
        'instagram_downloader',
        PROFILE
    )
    # profile = Profile.from_username(L.context, PROFILE)
    # posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes, reverse=True)

    # try:
    #     for post in posts_sorted_by_likes:
    #         print(post)
    #         print(post.profile)
    #         print(post.url)
    #         L.download_post(post, target=save_folder)
    # except IndexError:
    #     print("You have no saved posts yet.")
    #     return 'IndexError'
    print("end...")
    return PROFILE
def instagram_downloader_(request):
    if request.method == 'GET':
        return render(request, 'projects/instagram_downloader.html')
    if request.method == 'POST':
        user_name = request.POST['user_name']
        if user_name is None:
            context={
                        'result': '0'
                    }
        else:
            result = save_insta_collection(user_name)
            file_path = os.path.join(settings.MEDIA_ROOT, 'instagram_downloader') 
            file_path = str(settings.BASE_DIR)
            print(file_path)
            if result == user_name and os.path.exists(file_path):
                shutil.make_archive(result, 'zip', base_dir=file_path)
                now = time.time()
                future = now + 3
                while True:
                    print(future)
                    if time.time() > future:
                        context={
                            'result': file_path+'\\'+result + '.zip'
                        }
                        # send_file_(file_path+'\\'+result + '.zip')
                        # time.sleep(3)
                        # remove_file_(file_path+'\\'+result + '.zip')
                        return FileResponse(open(file_path+'\\'+result + '.zip', 'rb'), as_attachment=True)
                        # return render(request, 'projects/instagram_downloader.html', context=context)
            else:
                context={
                            'result': '0'
                        }
        return render(request, 'projects/instagram_downloader.html', context=context)
def youtube_downloader_(request):
    if request.method == 'GET':
        return render(request, 'projects/youtube_downloader.html')
    if request.method == 'POST':
        json_data = request.json
        choice = json_data['choice']
        quality = json_data['quality']  # low, medium, high, very high
        link = json_data['link']
        if link[0:23] == "https://www.youtube.com" or link[0:19] == "https://youtube.com" or link[
                                                                                             0:16] == "https://youtu.be":
            if choice == 1 or choice == 2:
                if choice == 2:
                    print("Pleylist yuklab olinmoqda...")
                    filenames = youtube_downloader.download_playlist(link, quality)
                    print("Yuklab olish tugadi!")
                    print(filenames)
                if choice == 1:
                    filename = youtube_downloader.download_video(link, quality)
                    # result = app.root_path.replace('website', '') + filename
                    # print(result)
                    return {"result": filename}
            elif choice == 3:
                print("Yuklab olinmoqda...")
                filename = youtube_downloader.download_video(link, 'low')
                print("Oʻzgartirilmoqda...")
                youtube_downloader.convert_to_mp3(filename)
                # result = app.root_path.replace('website', '') + filename.replace('.mp4', '.mp3')
                return {"result": filename}
            else:
                print("Yaroqsiz kiritish! Tugatilmoqda...")
        else:
            return {"result": "0"}

def coins(request):
    url = "https://api.minerstat.com/v2/coins"
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    htmlSource = r.data
    context={
        "data": json.loads(htmlSource)
    }
    return render(request, 'projects/coins.html', context=context)

def hash(h, key):
    return h[key]

def C0mplexTranslate(request):
    context={
        'data': googletrans.LANGUAGES
    }
    if request.method=='POST':
        text = request.POST['text']
        src = request.POST['src']
        dest = request.POST['dest']
        print(src)
        print(dest)
        print(text)
        translator = Translator()
        print(context.get('data').get(src))
        print(context.get('data').get(dest))
        # result = translator.translate(text)
        result = translator.translate(text, src=context.get('data').get(src), dest=context.get('data').get(dest)) # type: ignore
        print(result.src)
        print(result.dest)
        print(result.origin)
        print(result.text)
        print(result.pronunciation)
        context={
            'data': result.text
        }
        return render(request, 'projects/translate.html', context=context)
    
    print(context.get('data'))
    return render(request, 'projects/translate.html', context=context)

def ImageCompare(request):
    if request.method == 'GET':
        return render(request, 'projects/imagecompare.html')
    if request.method == 'POST':
        if 'img1' not in request.files or 'img2' not in request.files:
            print('No file part')
            context = {"data": ''}
        else:
            img1_model = request.files['img1']
            img2_model = request.files['img2']
            print(img1_model)
            print(img2_model)
            image1 = np.asarray(bytearray(img1_model.read()), dtype="uint8")
            image1 = cv2.imdecode(image1, cv2.IMREAD_COLOR)
            image2 = np.asarray(bytearray(img2_model.read()), dtype="uint8")
            image2 = cv2.imdecode(image2, cv2.IMREAD_COLOR)
            # grayA = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            # grayB = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            grayA = cv2.cvtColor(image1, cv2.COLOR_BGRA2GRAY)
            grayB = cv2.cvtColor(image2, cv2.COLOR_BGRA2GRAY)
            height1, width1, channels1 = image1.shape
            height2, width2, channels2 = image2.shape
            print(height1, width1, channels1)
            print(height2, width2, channels2)
            if width1 == width2 and height1 == height2:
                context = GetImageCompareResult(image1, image2, grayA, grayB)
            else:
                dim = (512, 512)
                resized_image1 = cv2.resize(grayA, dim, interpolation=cv2.INTER_AREA)
                resized_image2 = cv2.resize(grayB, dim, interpolation=cv2.INTER_AREA)
                context = GetImageCompareResult(image1, image2, grayA, resized_image1)
                # ImageFile.LOAD_TRUNCATED_IMAGES = True
                # img1 = Image.open(img1_model)
                # img2 = Image.open(img2_model)
                #
                # diff = ImageChops.difference(img1, img2)
                # print(diff.getbbox())
                # with io.BytesIO() as output:
                #     diff.save(output, format="png")
                #     contents = output.getvalue()
                #     result = "data:image/png;base64," + base64.b64encode(contents).decode('utf-8')
                #     # print(result)
                #     return {"data": result}
            return render(request, 'projects/imagecompare.html', context=context)

def GetImageCompareResult(image1, image2, grayA, grayB):
    (score, diff0) = compare_ssim(grayA, grayB, full=True)
    diff0 = (diff0 * 255).astype("uint8")
    print("SSIM: {}".format(score))
    thresh = cv2.threshold(diff0, 0, 255,
                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)
    im_arr = cv2.imencode('.jpg', thresh)[1].tostring()  # im_arr: image in Numpy one-dim array format.
    base64_str = "data:image/png;base64," + base64.b64encode(im_arr).decode('utf-8')
    # im_bytes = im_arr.tobytes()
    # im_b64 = base64.b64encode(im_bytes)
    context={
        'data': base64_str
    }
    return context

def avtotest(request):
    context={
        'row': range(1, 109),
        'bilet': 0
    }
    return render(request, 'projects/avtotest.html', context=context)

def avtotest_item(request, bilet):
    context={
        'row': range(1, 109),
        'bilet': bilet
    }
    return render(request, 'projects/avtotest.html', context=context)



def GetSavol(request):
    bilet=request.GET['bilet']
    avtotest=AvtoTest.objects.filter(bilet=bilet).values()
    return JsonResponse(list(avtotest), safe=False) 
    # qs = AvtoTest.objects.filter(bilet=bilet)
    # qs_json = serializers.serialize('json', qs)
    # return HttpResponse(qs_json, content_type='application/json')

def exchangerates(request):
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    print(r.status)
    # r = urllib3.request.urlopen(url)
    # data = r.read()
    context={
        "data": json.loads(r.data)
    }
    return render(request, 'projects/exchangerates.html', context=context)

def changetext(request):
    if request.method == 'POST':
        text = request.POST['text']
        characters = [["A", "А"], ["B", "Б"], ["D", "Д"], ["E", "Е"], ["F", "Ф"], ["G", "Г"], ["H", "Ҳ"], ["I", "И"],
                    ["J", "Ж"], ["K", "К"], ["L", "Л"], ["M", "М"], ["N", "Н"], ["O", "О"], ["P", "П"], ["Q", "Қ"],
                    ["R", "Р"], ["S", "С"], ["T", "Т"], ["U", "У"], ["V", "В"], ["X", "Х"], ["Y", "Й"], ["Z", "З"],
                    ["a", "а"], ["b", "б"], ["d", "д"], ["e", "е"], ["f", "ф"], ["g", "г"], ["h", "ҳ"], ["i", "и"],
                    ["j", "ж"], ["k", "к"], ["l", "л"], ["m", "м"], ["n", "н"], ["o", "о"], ["p", "п"], ["q", "қ"],
                    ["r", "р"], ["s", "с"], ["t", "т"], ["u", "у"], ["v", "в"], ["x", "х"], ["y", "й"], ["z", "з"],
                    ["А", "A"], ["Б", "B"], ["С", "C"], ["Ч", "Ch"], ["Д", "D"], ["Е", "E"], ["Ф", "F"], ["Г", "G"],
                    ["Ҳ", "H"], ["И", "I"], ["Ж", "J"], ["К", "K"], ["Л", "L"], ["М", "M"], ["Н", "N"], ["О", "O"],
                    ["П", "P"], ["Қ", "Q"], ["Р", "R"], ["С", "S"], ["Ш", "Sh"], ["Т", "T"], ["У", "U"], ["В", "V"],
                    ["Х", "X"], ["Й", "Y"], ["Я", "Ya"], ["Ю", "Yu"], ["Ё", "Yo"], ["З", "Z"], ["Ғ", "Gʼ"], ["а", "a"],
                    ["б", "b"], ["с", "c"], ["ч", "ch"], ["д", "d"], ["е", "e"], ["ф", "f"], ["г", "g"], ["ҳ", "h"],
                    ["и", "i"], ["ж", "j"], ["к", "k"], ["л", "l"], ["м", "m"], ["н", "n"], ["о", "o"], ["п", "p"],
                    ["қ", "q"], ["р", "r"], ["с", "s"], ["ш", "sh"], ["т", "t"], ["у", "u"], ["в", "v"], ["х", "x"],
                    ["й", "y"], ["я", "ya"], ["ю", "yu"], ["ё", "yo"], ["з", "z"], ["ғ", "gʼ"], ["ъ", "`"], ["`", "ъ"],
                    ["'", "ъ"]]

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
            text = text.replace("йа", "я").replace("Йа", "Я").replace("ЙА", "Я").replace("йА", "я")
            text = text.replace("йо", "ё").replace("Йо", "Ё").replace("ЙО", "Ё").replace("йО", "ё")
            text = text.replace("йу", "ю").replace("Йу", "Ю").replace("ЙУ", "Ю").replace("йУ", "ю")
            text = text.replace("сҳ", "ш").replace("Сҳ", "Ш").replace("СҲ", "Ш").replace("сҲ", "ш")
            text = text.replace("cҳ", "ч").replace("Cҳ", "Ч").replace("CҲ", "Ч").replace("cҲ", "ч")
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
    return render(request, 'projects/changetext.html')

def GetChangeTextData(request, text):
    if text is None:
        return ''
    characters = [["A", "А"], ["B", "Б"], ["D", "Д"], ["E", "Е"], ["F", "Ф"], ["G", "Г"], ["H", "Ҳ"], ["I", "И"],
                ["J", "Ж"], ["K", "К"], ["L", "Л"], ["M", "М"], ["N", "Н"], ["O", "О"], ["P", "П"], ["Q", "Қ"],
                ["R", "Р"], ["S", "С"], ["T", "Т"], ["U", "У"], ["V", "В"], ["X", "Х"], ["Y", "Й"], ["Z", "З"],
                ["a", "а"], ["b", "б"], ["d", "д"], ["e", "е"], ["f", "ф"], ["g", "г"], ["h", "ҳ"], ["i", "и"],
                ["j", "ж"], ["k", "к"], ["l", "л"], ["m", "м"], ["n", "н"], ["o", "о"], ["p", "п"], ["q", "қ"],
                ["r", "р"], ["s", "с"], ["t", "т"], ["u", "у"], ["v", "в"], ["x", "х"], ["y", "й"], ["z", "з"],
                ["А", "A"], ["Б", "B"], ["С", "C"], ["Ч", "Ch"], ["Д", "D"], ["Е", "E"], ["Ф", "F"], ["Г", "G"],
                ["Ҳ", "H"], ["И", "I"], ["Ж", "J"], ["К", "K"], ["Л", "L"], ["М", "M"], ["Н", "N"], ["О", "O"],
                ["П", "P"], ["Қ", "Q"], ["Р", "R"], ["С", "S"], ["Ш", "Sh"], ["Т", "T"], ["У", "U"], ["В", "V"],
                ["Х", "X"], ["Й", "Y"], ["Я", "Ya"], ["Ю", "Yu"], ["Ё", "Yo"], ["З", "Z"], ["Ғ", "Gʼ"], ["а", "a"],
                ["б", "b"], ["с", "c"], ["ч", "ch"], ["д", "d"], ["е", "e"], ["ф", "f"], ["г", "g"], ["ҳ", "h"],
                ["и", "i"], ["ж", "j"], ["к", "k"], ["л", "l"], ["м", "m"], ["н", "n"], ["о", "o"], ["п", "p"],
                ["қ", "q"], ["р", "r"], ["с", "s"], ["ш", "sh"], ["т", "t"], ["у", "u"], ["в", "v"], ["х", "x"],
                ["й", "y"], ["я", "ya"], ["ю", "yu"], ["ё", "yo"], ["з", "z"], ["ғ", "gʼ"], ["ъ", "`"], ["`", "ъ"],
                ["'", "ъ"]]

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
        text = text.replace("йа", "я").replace("Йа", "Я").replace("ЙА", "Я").replace("йА", "я")
        text = text.replace("йо", "ё").replace("Йо", "Ё").replace("ЙО", "Ё").replace("йО", "ё")
        text = text.replace("йу", "ю").replace("Йу", "Ю").replace("ЙУ", "Ю").replace("йУ", "ю")
        text = text.replace("сҳ", "ш").replace("Сҳ", "Ш").replace("СҲ", "Ш").replace("сҲ", "ш")
        text = text.replace("cҳ", "ч").replace("Cҳ", "Ч").replace("CҲ", "Ч").replace("cҲ", "ч")
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


def ip(request):
    ip = request.GET.get('ip', False);
    if ip == False:
        url = "https://ipapi.co/json"
    else:
        url = "https://ipapi.co/" + ip + "/json"
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    context={
        'data':json.loads(r.data)
    }
    return render(request, 'projects/ip.html', context=context)

def password_generator(request):
    if request.method == 'POST':
        characterList = ""
        json_data = json.loads(request.body)
        PasswordLength = int(json_data['PasswordLength'])
        Uppercase = json_data['Uppercase']
        Lowercase = json_data['Lowercase']
        Numbers = json_data['Numbers']
        Symbols = json_data['Symbols']
        if Uppercase:
            characterList += string.ascii_uppercase
        if Lowercase:
            characterList += string.ascii_lowercase
        if Numbers:
            characterList += string.digits
        if Symbols:
            characterList += string.punctuation
        password = []

        for i in range(PasswordLength):
            # Picking a random character from our
            # character list
            randomchar = random.choice(characterList)

            # appending a random character to password
            password.append(randomchar)
        return HttpResponse({"".join(password)})
    return render(request, 'projects/password_generator.html')


def sitemap(request):
    if request.method == 'POST':
        url = request.args.get('url')
        from asyncio import events, windows_events
        el = windows_events.ProactorEventLoop()
        events.set_event_loop(el)
        crawler(url, out_file='sitemap.xml', exclude_urls=[".ico", ".css", ".pdf", ".jpg", ".zip", ".png", ".svg"])
        basedir = os.path.abspath(os.path.dirname(__file__))
        time.sleep(10)
        send_file_(str(settings.BASE_DIR)+'\\sitemap.xml')
        time.sleep(3)
        remove_file_(str(settings.BASE_DIR)+'\\sitemap.xml')
    return render(request, 'projects/sitemap.html')

def projects(request):
    projects=Project.actives.all()
    context={
        'projects': projects
    }
    print(context)
    return render(request, "projects/home.html", context=context)
def services(request):
    services=Project.services.all()
    context={
        'services': services
    }
    return render(request, "base.html", context=context)
def project_item(request, id):
    item=get_object_or_404(Project, id=id)
    context={
        'item': item
    }
    return render(request, "projects/item.html", context=context)
def send_file_(request):
    if request[-4:] in GET_FILE_FORMATS:
        # global data
        # headers = open("C:\\Users\\sazug\\OneDrive\\Desktop\\DDOS\\hammer\\headers\\headers.txt", "r")
        # headers = open(request, 'rb')
        # data = headers.read()
        # headers.close
        return FileResponse(open(request, 'rb'), as_attachment=True)
    else:
        return FileResponse(STATIC_URL+'img/fuck.jpg',
                         as_attachment=True)
def remove_file_(request):
    if os.path.exists(request) and request[-4:] in GET_FILE_FORMATS:
        if request[-4:] == ".mp3":
            filename_ = request[:-4] + ".mp4"
            if os.path.exists(filename_):
                os.remove(filename_)
        if request[-4:] == ".zip":
            filename_ = request[:-4]
            path = filename_
            shutil.rmtree(path, ignore_errors=True)
            # for file_name in os.listdir(path):
            #     print(file_name)
            #     file = path + file_name
            #     print(file)
            #     if os.path.isfile(file):
            #         print('Deleting file:', file)
            #         os.remove(file)
        os.remove(request)
        return "1"
    else:
        return "0"