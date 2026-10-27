import os

from django.http import JsonResponse
from django.shortcuts import render

from comments.pages import page_comments
from core import downloads
from pdf_tools.converters import CONVERTERS, ConversionError

MAX_PDF_SIZE = 20 * 1024 * 1024
MAX_PDF_MB = MAX_PDF_SIZE // (1024 * 1024)

TEXT = {
    "uz": {
        "badge_free": "Bepul, ro'yxatdan o'tmasdan", "badge_limit": "{mb} MB gacha, {pages} sahifagacha",
        "badge_private": "Fayllar 1 soatda o'chiriladi", "choose": "1. Formatni tanlang", "upload": "2. PDF faylni yuklang",
        "to_word": "Word", "to_word_d": "Tahrirlanadigan DOCX hujjat", "to_excel": "Excel", "to_excel_d": "Jadvallar CSV ko'rinishida (Excel ochadi)",
        "to_image": "Rasm", "to_image_d": "Har bir sahifa JPG, ZIP arxivda",
        "drop": "PDF faylni shu yerga tashlang", "or": "yoki", "browse": "Faylni tanlang", "change": "Boshqa fayl",
        "convert": "Konvertatsiya qilish", "uploading": "Yuklanmoqda", "converting": "Konvertatsiya qilinmoqda — katta fayllarda bir daqiqagacha vaqt oladi",
        "ready": "Tayyor!", "download": "Yuklab olish", "again": "Yana fayl", "error": "Xatolik yuz berdi",
        "only_pdf": "Faqat PDF fayl tanlang", "too_big": "Fayl hajmi {mb} MB dan oshmasin", "network": "Internet aloqasini tekshirib, qayta urinib ko'ring",
        "how": "Qanday ishlaydi?", "step1": "Natija formatini tanlang", "step2": "PDF faylni yuklang", "step3": "Tayyor faylni yuklab oling",
        "app": "Android ilovalar",
    },
    "ru": {
        "badge_free": "Бесплатно, без регистрации", "badge_limit": "До {mb} МБ, до {pages} страниц",
        "badge_private": "Файлы удаляются через 1 час", "choose": "1. Выберите формат", "upload": "2. Загрузите PDF",
        "to_word": "Word", "to_word_d": "Редактируемый документ DOCX", "to_excel": "Excel", "to_excel_d": "Таблицы в CSV (открывается в Excel)",
        "to_image": "Картинки", "to_image_d": "Каждая страница в JPG, архив ZIP",
        "drop": "Перетащите PDF сюда", "or": "или", "browse": "Выберите файл", "change": "Другой файл",
        "convert": "Конвертировать", "uploading": "Загрузка", "converting": "Конвертация — для больших файлов до минуты",
        "ready": "Готово!", "download": "Скачать", "again": "Ещё файл", "error": "Произошла ошибка",
        "only_pdf": "Выберите PDF файл", "too_big": "Размер файла не должен превышать {mb} МБ", "network": "Проверьте подключение к интернету и попробуйте снова",
        "how": "Как это работает?", "step1": "Выберите формат результата", "step2": "Загрузите PDF файл", "step3": "Скачайте готовый файл",
        "app": "Приложения Android",
    },
    "en": {
        "badge_free": "Free, no sign-up", "badge_limit": "Up to {mb} MB, {pages} pages",
        "badge_private": "Files are deleted after 1 hour", "choose": "1. Choose a format", "upload": "2. Upload a PDF",
        "to_word": "Word", "to_word_d": "Editable DOCX document", "to_excel": "Excel", "to_excel_d": "Tables as CSV (opens in Excel)",
        "to_image": "Images", "to_image_d": "Every page as JPG in a ZIP",
        "drop": "Drop your PDF here", "or": "or", "browse": "Choose file", "change": "Another file",
        "convert": "Convert", "uploading": "Uploading", "converting": "Converting — large files can take up to a minute",
        "ready": "Done!", "download": "Download", "again": "Convert another", "error": "Something went wrong",
        "only_pdf": "Please choose a PDF file", "too_big": "The file must not exceed {mb} MB", "network": "Check your internet connection and try again",
        "how": "How it works", "step1": "Choose the output format", "step2": "Upload your PDF", "step3": "Download the result",
        "app": "Android apps",
    },
    "tr": {
        "badge_free": "Ücretsiz, kayıt gerekmez", "badge_limit": "{mb} MB'a, {pages} sayfaya kadar",
        "badge_private": "Dosyalar 1 saat sonra silinir", "choose": "1. Biçim seçin", "upload": "2. PDF yükleyin",
        "to_word": "Word", "to_word_d": "Düzenlenebilir DOCX belgesi", "to_excel": "Excel", "to_excel_d": "Tablolar CSV olarak (Excel açar)",
        "to_image": "Resim", "to_image_d": "Her sayfa JPG, ZIP arşivinde",
        "drop": "PDF dosyasını buraya bırakın", "or": "veya", "browse": "Dosya seçin", "change": "Başka dosya",
        "convert": "Dönüştür", "uploading": "Yükleniyor", "converting": "Dönüştürülüyor — büyük dosyalar bir dakika sürebilir",
        "ready": "Hazır!", "download": "İndir", "again": "Başka dosya", "error": "Bir hata oluştu",
        "only_pdf": "Lütfen bir PDF dosyası seçin", "too_big": "Dosya {mb} MB'ı geçmemelidir", "network": "İnternet bağlantınızı kontrol edip tekrar deneyin",
        "how": "Nasıl çalışır?", "step1": "Çıktı biçimini seçin", "step2": "PDF dosyanızı yükleyin", "step3": "Sonucu indirin",
        "app": "Android uygulamaları",
    },
}


def index(request):
    if request.method != "POST":
        from django.utils import translation

        from pdf_tools.converters import MAX_PAGES

        t = dict(TEXT.get((translation.get_language() or "uz")[:2], TEXT["en"]))
        t["badge_limit"] = t["badge_limit"].format(mb=MAX_PDF_MB, pages=MAX_PAGES)
        t["too_big"] = t["too_big"].format(mb=MAX_PDF_MB)
        context = {"comments": page_comments(request), "t": t, "max_size": MAX_PDF_SIZE}
        return render(request, "pdf_tools/index.html", context)

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
