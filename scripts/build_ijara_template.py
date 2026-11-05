"""«Uy-joyni ijaraga beriş şartnomasi» DOCX namunasini yaratiş (blog: /blog/uyni-shartnoma-boyicha-ijaraga-berish-tartibi/).

    pip install python-docx
    python scripts/build_ijara_template.py

Natija: media/post/files/ijara-shartnomasi-namunasi{,-lotin-1995,-kirill}.docx — 2026-yilgi alifbo, 1995-yilgi lotin
va kirill yozuvida (rasmiy hujjatlar ko'pincha keyingi ikkitasida tuziladi). Matn maqoladagi qoidalarga mos:
ijara muddati 5 yildan oşmaydi, şartnoma «E-ijara» tizimida röyxatdan ötkaziladi.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

from core.translit import latin2026_to_1995, latin_to_cyrillic  # noqa: E402

OUT = ROOT / "media" / "post" / "files"
L = "________________"

TITLE = "UY-JOYNI IJARAGA BERIŞ ŞARTNOMASI"
HEAD = f"№ _____                  {L} şahri                  «___» ____________ 20__ y."
PARTIES = (
    f"Bir tomondan, {L} (familiyasi, ismi, otasining ismi), pasport / ID-karta: seriya ____ № __________, "
    f"berilgan sana: __________, yaşaş manzili: {L} (bundan buyon — «Ijaraga beruvçi»), ikkinçi tomondan, "
    f"{L} (familiyasi, ismi, otasining ismi), pasport / ID-karta: seriya ____ № __________, berilgan sana: __________, "
    f"yaşaş manzili: {L} (bundan buyon — «Ijaraga oluvçi»), birgalikda «Tomonlar» deb ataluvçilar, "
    "quyidagilar haqida uşbu şartnomani tuzdik:"
)
SECTIONS = [
    ("1. ŞARTNOMA PREDMETI", [
        f"1.1. Ijaraga beruvçi Ijaraga oluvçiga yaşaş uçun vaqtinça foydalanişga quyidagi turar joyni beradi: {L} (manzil), ___ xonali, umumiy maydoni ____ m².",
        f"1.2. Turar joy Ijaraga beruvçiga mulk huquqi asosida tegişli. Huquqni tasdiqlovçi hujjat: {L}.",
        f"1.3. Ijaraga oluvçi bilan birga yaşaydigan şaxslar: {L}.",
        "1.4. Turar joy va undagi mol-mulk topşiriş-qabul qiliş dalolatnomasi (1-ilova) asosida topşiriladi va qaytariladi.",
    ]),
    ("2. ŞARTNOMA MUDDATI", [
        "2.1. Şartnoma «___» ____________ 20__ y.dan «___» ____________ 20__ y.gaça tuziladi.",
        "2.2. Turar joyni ijaraga beriş muddati 5 yildan oşmaydi. Tomonlar kelişuvi bilan muddat tugagaç yangi şartnoma tuzilişi mumkin.",
    ]),
    ("3. IJARA HAQI VA TÖLAŞ TARTIBI", [
        f"3.1. Oylik ijara haqi: {L} söm (yozuv bilan: {L}).",
        "3.2. Ijara haqi har oyning ___-sanasigaça naqd pulda / bank kartasiga / hisob raqamiga (keraklisini qoldiring) tölanadi.",
        f"3.3. Kommunal xizmatlar (elektr energiyasi, gaz, suv, çiqindi, internet) haqini {L} töllaydi.",
        f"3.4. Garov (depozit) puli: {L} söm. Şartnoma tugaganda turar joy va mol-mulkka zarar yetkazilmagan bölsa, garov puli ___ kun içida qaytariladi.",
        "3.5. Ijara haqi miqdori şartnoma muddati davomida faqat Tomonlarning yozma kelişuvi bilan özgartiriladi.",
    ]),
    ("4. TOMONLARNING HUQUQ VA MAJBURIYATLARI", [
        "4.1. Ijaraga beruvçi: turar joyni kelişilgan sanada foydalanişga yaroqli holda topşiradi; Ijaraga oluvçining foydalanişiga asossiz aralaşmaydi; kapital ta'mirni öz hisobidan bajaradi; turar joyga kiriş vaqtini Ijaraga oluvçi bilan oldindan kelişadi.",
        "4.2. Ijaraga oluvçi: turar joydan faqat yaşaş uçun foydalanadi; ijara haqi va kommunal tölovlarni öz vaqtida töllaydi; turar joy va mol-mulkni ehtiyot qiladi; Ijaraga beruvçining yozma roziligisiz turar joyni qayta ijaraga bermaydi va qayta qurmaydi; şartnoma tugaganda turar joyni dalolatnoma böyiça qaytaradi.",
        "4.3. Ijaraga oluvçining aybi bilan yetkazilgan zarar u tomonidan qoplanadi.",
    ]),
    ("5. ŞARTNOMANI BEKOR QILIŞ", [
        "5.1. Şartnoma Tomonlarning kelişuvi bilan istalgan vaqtda bekor qilinişi mumkin.",
        "5.2. Şartnomani muddatidan oldin bekor qilmoqçi bölgan Tomon ikkinçi Tomonni kamida ___ kun oldin yozma ravişda ogohlantiradi.",
        "5.3. Şartnoma amaldagi qonunçilikda nazarda tutilgan boşqa hollarda ham bekor qilinişi mumkin.",
    ]),
    ("6. NIZOLARNI HAL QILIŞ", [
        "6.1. Nizolar muzokaralar yöli bilan, kelişuvga erişilmasa — amaldagi qonunçilikka muvofiq sud tartibida hal qilinadi.",
    ]),
    ("7. YAKUNIY QOIDALAR", [
        "7.1. Şartnoma imzolangan kundan kuçga kiradi va bir xil yuridik kuçga ega ikki nusxada tuziladi.",
        "7.2. Şartnoma qonunçilikda belgilangan tartibda «E-ijara» tizimi orqali soliq organlarida röyxatdan ötkaziladi.",
        "7.3. Ilova: 1-ilova — topşiriş-qabul qiliş dalolatnomasi.",
    ]),
]
SIGN = ["Ijaraga beruvçi", "Ijaraga oluvçi"]
ACT_TITLE = "1-ILOVA. TOPŞIRIŞ-QABUL QILIŞ DALOLATNOMASI"
ACT_INTRO = f"«___» ____________ 20__ y. Ijaraga beruvçi topşirdi, Ijaraga oluvçi qabul qildi: {L} manzildagi turar joy va quyidagi mol-mulk."
ACT_COLS = ["№", "Mol-mulk nomi", "Soni", "Holati"]
ACT_METERS = "Hisoblagiç körsatkiçlari: elektr ________, gaz ________, suv ________. Topşirilgan kalitlar soni: ____."
NOTE = ("Eslatma: bu — namuna. Uni Tomonlarning kelişuviga qarab özgartiring. Muhim bitimlar oldidan huquqşunos bilan "
        "maslahatlaşing. Namuna: complexprogrammer.uz")


def build(convert, path):
    doc = Document()
    for section in doc.sections:
        section.left_margin = section.right_margin = Cm(2)
        section.top_margin = section.bottom_margin = Cm(1.8)
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    def para(text, bold=False, align=None, size=None, space=6):
        p = doc.add_paragraph()
        run = p.add_run(convert(text))
        run.bold = bold
        if size:
            run.font.size = Pt(size)
        if align is not None:
            p.alignment = align
        p.paragraph_format.space_after = Pt(space)
        return p

    para(TITLE, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    para(HEAD, align=WD_ALIGN_PARAGRAPH.CENTER, space=12)
    para(PARTIES, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    for heading, items in SECTIONS:
        para(heading, bold=True, space=4)
        for item in items:
            para(item, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space=3)
    para("TOMONLARNING IMZOLARI", bold=True, space=8)
    table = doc.add_table(rows=1, cols=2)
    for cell, who in zip(table.rows[0].cells, SIGN):
        cell.text = convert(f"{who}:\n\n__________ (imzo)\n{L}\n(F.I.Ş.)\nTel.: ______________")
    doc.add_page_break()
    para(ACT_TITLE, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13)
    para(ACT_INTRO, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    act = doc.add_table(rows=8, cols=4)
    act.style = "Table Grid"
    for cell, col in zip(act.rows[0].cells, ACT_COLS):
        cell.text = convert(col)
    for i in range(1, 8):
        act.rows[i].cells[0].text = str(i)
    para("")
    para(ACT_METERS)
    sign = doc.add_table(rows=1, cols=2)
    for cell, who in zip(sign.rows[0].cells, ["Topşirdi (Ijaraga beruvçi)", "Qabul qildi (Ijaraga oluvçi)"]):
        cell.text = convert(f"{who}:\n\n__________ (imzo)")
    para("")
    para(NOTE, size=9)
    doc.save(path)


def to_cyrillic(text):
    """Kirill: tizim va sayt nomlari, «ID-karta» lotinça qoladi (ögirgiç ularni «ИД», «.уз» qilib yuboradi)."""
    keep = {"E-ijara": "@@E@@", "complexprogrammer.uz": "@@S@@", "ID-karta": "@@I@@"}
    for word, mark in keep.items():
        text = text.replace(word, mark)
    text = latin_to_cyrillic(text)
    for word, mark in keep.items():
        text = text.replace(mark, "ID-карта" if word == "ID-karta" else word)
    return text


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    variants = [
        ("ijara-shartnomasi-namunasi.docx", lambda s: s),
        ("ijara-shartnomasi-namunasi-lotin-1995.docx", latin2026_to_1995),
        ("ijara-shartnomasi-namunasi-kirill.docx", to_cyrillic),
    ]
    for name, convert in variants:
        build(convert, OUT / name)
        print(OUT / name, f"{(OUT / name).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
