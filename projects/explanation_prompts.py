"""Savol izohlari AI qoralamasi uçun umumiy qism: model, tizim matni, javob sxemasi va so'rov yasaş.

Django'ga böğliq emas — uni ham server buyruği (``manage.py draft_explanations``), ham lokal skript
(``scripts/explanations_local.py``, Django örnatilmagan kompyuterda) işlatadi. Prompt şu bitta joyda.
"""

import base64
from pathlib import Path

MODEL = "claude-opus-5-5"
LETTERS = ("A", "B", "C", "D")

# Natija fayllari (lokalda yaratiladi, git orqali serverga boradi, serverda import_explanations bazaga yozadi)
RESULTS_DIR = Path(__file__).resolve().parent / "data" / "explanations"

SYSTEM = """Siz O'zbekiston yo'l harakati qoidalari (YHQ) bo'yicha tajribali o'qituvchisiz. Haydovchilikka nomzodlar uchun \
avtotest savolining to'g'ri javobi nima uchun to'g'ri ekanini qisqa tushuntirasiz.

Talablar:
- 2-4 gap, sodda til. Avval qoida mazmunini ayting, keyin uni shu vaziyatga qo'llang.
- To'g'ri javob sizga berilgan — uni o'zgartirmang va boshqa variantni to'g'ri demang.
- YHQ band raqamini faqat aniq bilsangiz yozing; ishonchingiz komil bo'lmasa, raqamsiz qoida mazmunini ayting.
- Rasm berilgan bo'lsa, undagi vaziyatga (belgilar, transport vositalari joylashuvi) tayaning.
- Uchala tilda bir xil mazmun: o'zbekcha (lotin), ruscha, inglizcha.
- confidence: berilgan javobni qoidaga ishonchli bog'lay olsangiz "high", qisman "medium", \
savol yoki javob noaniq/xato tuyulsa "low"."""

# /tests/ da haydovchilik testlaridan tashqari maktab fanlari (matematika, tarix, ingliz tili...) ham bor
SYSTEM_TESTS = """Siz tajribali o'qituvchisiz. O'quvchiga test savolining to'g'ri javobi nima uchun to'g'ri ekanini \
qisqa tushuntirasiz. Fan (to'plam nomi) savol bilan birga beriladi.

Talablar:
- 2-4 gap, sodda til. Avval qoida, ta'rif yoki faktni ayting, keyin uni shu savolga qo'llang.
- Hisoblash savolida asosiy qadamlarni qisqa ko'rsating.
- To'g'ri javob sizga berilgan — uni o'zgartirmang va boshqa variantni to'g'ri demang.
- Haydovchilik testi bo'lsa: O'zbekiston YHQ (to'plam AQSh CDL bo'lsa — o'sha qoidalar) asosida tushuntiring; \
band raqamini faqat aniq bilsangiz yozing.
- Rasm berilgan bo'lsa, undagi vaziyatga tayaning.
- Uchala tilda bir xil mazmun: o'zbekcha (lotin), ruscha, inglizcha.
- confidence: berilgan javobni ishonchli asoslay olsangiz "high", qisman "medium", \
savol yoki javob noaniq/xato tuyulsa "low"."""

SCHEMA = {
    "type": "object",
    "properties": {
        "uz": {"type": "string"},
        "ru": {"type": "string"},
        "en": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    },
    "required": ["uz", "ru", "en", "confidence"],
    "additionalProperties": False,
}


def image_block(path):
    media = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media, "data": base64.standard_b64encode(path.read_bytes()).decode()},
    }


def params(system, content):
    return {
        "model": MODEL,
        "max_tokens": 16000,
        "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        # Barcha so'rovlarda bir xil tizim matni — keshlanadi
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": content}],
    }


def avtotest_content(q, images_dir):
    """``q`` — AvtoTest obyekti yoki bazadan öqilgan dict (savol, javob_a..d, javob, bilet, raqam, rasm)."""
    get = q.get if isinstance(q, dict) else lambda k, d="": getattr(q, k, d)
    options = "\n".join(
        f"{letter}) {get('javob_' + letter.lower())}" for letter in LETTERS if get("javob_" + letter.lower())
    )
    text = (
        f"Savol ({get('bilet')}-bilet, {get('raqam')}-savol): {get('savol')}\n\nVariantlar:\n{options}\n\n"
        f"To'g'ri javob: {get('javob')}"
    )
    content = []
    rasm = get("rasm")
    image = Path(images_dir) / rasm if rasm else None
    if image and image.is_file():
        content.append(image_block(image))
    content.append({"type": "text", "text": text})
    return content


def avtotest_custom_id(bilet, raqam):
    """Bazadagi ID emas, (bilet, raqam) — lokal va server bazasida ID'lar farq qilsa ham natija töğri savolga tuşadi."""
    return f"a{int(bilet)}_{int(raqam)}"


def parse_custom_id(custom_id):
    """'a5_12' -> ("avtotest", (5, 12)); 'q123' -> ("avtotest_id", 123); 't45' -> ("tests", 45)."""
    if custom_id.startswith("a"):
        bilet, raqam = custom_id[1:].split("_")
        return "avtotest", (int(bilet), int(raqam))
    return ("tests" if custom_id[0] == "t" else "avtotest_id"), int(custom_id[1:])
