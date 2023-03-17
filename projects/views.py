import io
import os
import traceback
import uuid
import cv2
from django.shortcuts import render, get_object_or_404
import numpy as np
import yaml
from django_complexprogrammer.settings import CARTOONIZED_FOLDER, WRITE_BOX_CARTOONIZER, UPLOAD_FOLDER_VIDEOS
# from gcloud_utils import delete_blob, download_video, generate_signed_url, upload_blob
from projects.models import Project
from static.white_box_cartoonizer.cartoonize import WB_Cartoonize
import skvideo
import skvideo.io
from PIL import Image
from django.contrib import messages

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
    if projects.get(id=1).application_id is not "":
        print(projects.get(id=1).application_id)
    return render(request, "base.html", context=context)

wb_cartoonizer = WB_Cartoonize(WRITE_BOX_CARTOONIZER+'saved_models/', opts['gpu'])


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

def cartoonize(request):
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
def projects(request):
    projects=Project.actives.all()
    context={
        'projects': projects
    }
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