import os

from django.http import JsonResponse
from django.shortcuts import render

from comments.pages import page_comments
from core import downloads
from pdf_tools.converters import CONVERTERS, ConversionError

MAX_PDF_SIZE = 20 * 1024 * 1024


def index(request):
    if request.method != "POST":
        return render(request, "pdf_tools/index.html", {"comments": page_comments(request)})

    upload = request.FILES.get("file")
    conv_type = request.POST.get("type", "pdf2docx")
    if upload is None:
        return JsonResponse({"result": "0", "data": "Fayl tanlanmagan"}, status=400)
    if conv_type not in CONVERTERS:
        return JsonResponse({"result": "0", "data": "Noma'lum konvertatsiya turi"}, status=400)
    if not upload.name.lower().endswith(".pdf"):
        return JsonResponse({"result": "0", "data": "Faqat PDF fayl yuklang"}, status=400)
    if upload.size > MAX_PDF_SIZE:
        return JsonResponse({"result": "0", "data": "Fayl hajmi 20 MB dan oshmasin"}, status=400)

    downloads.cleanup_old()
    folder = downloads.ensure_dir()
    pdf_path = os.path.join(folder, downloads.new_name(upload.name, ".pdf"))
    with open(pdf_path, "wb") as fh:
        for chunk in upload.chunks():
            fh.write(chunk)

    convert, ext = CONVERTERS[conv_type]
    out_name = downloads.new_name(upload.name, ext)
    try:
        convert(pdf_path, os.path.join(folder, out_name))
    except ConversionError as exc:
        return JsonResponse({"result": "0", "data": str(exc)})
    except Exception:
        return JsonResponse({"result": "0", "data": "Konvertatsiyada xatolik yuz berdi"})
    finally:
        try:
            os.remove(pdf_path)
        except OSError:
            pass
    return JsonResponse({"result": out_name, "data": "Tayyor! Fayl yuklanmoqda..."})
