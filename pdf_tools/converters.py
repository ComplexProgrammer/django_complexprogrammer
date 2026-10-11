"""PDF konvertatsiyalari. Hammasi PyMuPDF/pdf2docx bilan, Java talab qilinmaydi."""

import csv
import os
import zipfile

import fitz  # PyMuPDF

MAX_PAGES = 100


class ConversionError(Exception):
    pass


def _open(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        raise ConversionError("Fayl PDF emas yoki buzilgan") from exc
    if doc.needs_pass:
        raise ConversionError("Parol bilan himoyalangan PDF qo'llab-quvvatlanmaydi")
    if doc.page_count > MAX_PAGES:
        raise ConversionError(f"PDF {MAX_PAGES} sahifadan oshmasligi kerak")
    return doc


def pdf_to_docx(pdf_path, out_path):
    from pdf2docx import Converter

    _open(pdf_path).close()
    cv = Converter(pdf_path)
    try:
        cv.convert(out_path)
    finally:
        cv.close()
    return out_path


def pdf_to_csv(pdf_path, out_path):
    """Barcha sahifalardagi jadvallarni bitta CSV (Excel'da ochiladi) ga yozadi."""
    doc = _open(pdf_path)
    rows_written = 0
    with open(out_path, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        for page in doc:
            for table in page.find_tables().tables:
                for row in table.extract():
                    writer.writerow(["" if cell is None else cell for cell in row])
                    rows_written += 1
                writer.writerow([])
    doc.close()
    if rows_written == 0:
        os.remove(out_path)
        raise ConversionError("PDF ichida jadval topilmadi")
    return out_path


def pdf_to_images(pdf_path, out_path, dpi=150):
    """Har bir sahifani JPG qilib, ZIP arxivga joylaydi."""
    doc = _open(pdf_path)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=dpi)
            zf.writestr(f"page-{i:03d}.jpg", pix.tobytes("jpg"))
    doc.close()
    return out_path


CONVERTERS = {
    "pdf2docx": (pdf_to_docx, ".docx"),
    "pdf2excel": (pdf_to_csv, ".csv"),
    "pdf2image": (pdf_to_images, ".zip"),
}
