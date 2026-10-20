"""Test savollariga "nima uchun bu javob to'g'ri" izohining AI qoralamasini yozish (Claude, Message Batches API).

    python manage.py draft_explanations submit [--limit 50] [--bilet 5] [--redo]        # /avtotest/ savollari
    python manage.py draft_explanations submit --source tests [--book 49] [--limit 50]  # /tests/ savollari
    python manage.py draft_explanations status                                          # yuborilgan batchlar holati
    python manage.py draft_explanations collect                                         # tayyor natijalarni bazaga yozish

Batch API oddiy so'rovdan 50% arzon, natija odatda 1 soat ichida tayyor bo'ladi. Qoralamalar ``izoh_holati="draft"``
(/tests/ uchun ``explanation_status="draft"``) bilan saqlanadi — saytda faqat admin panelda "Izohni tasdiqlash"
qilingandan keyin ko'rinadi.
Kalit: ANTHROPIC_API_KEY (.env) yoki `ant auth login` profili.
"""

import base64
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.translit import latin_to_cyrillic
from projects.models import AvtoTest
from tests.models import Answers, Questions

MODEL = "claude-opus-5-5"
LETTERS = ("A", "B", "C", "D")
STATE_FILE = Path(settings.BASE_DIR) / "tmp" / "explanation_batches.json"
IMAGES = Path(settings.BASE_DIR) / "static" / "avtotest"
MEDIA = Path(settings.MEDIA_ROOT)

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


def _state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"batches": []}


def _save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise CommandError("anthropic kutubxonasi o'rnatilmagan: pip install anthropic") from e
    return anthropic.Anthropic()


def _image_block(path):
    media = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media, "data": base64.standard_b64encode(path.read_bytes()).decode()},
    }


def _params(system, content):
    return {
        "model": MODEL,
        "max_tokens": 16000,
        "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        # Barcha so'rovlarda bir xil tizim matni — keshlanadi
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": content}],
    }


def _tests_request(q, answers):
    """/tests/ savoli (tests.Questions): variantlar Answers jadvalida, to'g'risi right=True."""
    options = [a for a in answers if a.name_uz_uz.strip()]
    letters = "ABCDEFGHIJ"
    right = next(letters[i] for i, a in enumerate(options) if a.right)
    book = q.topic.book if q.topic_id else None
    subject = book.book_type.name_uz_uz if book is not None and book.book_type_id else "-"
    lines = [f"Fan / to'plam: {subject}", f"Savol: {q.name_uz_uz}"]
    if q.name_ru_ru:
        lines.append(f"(Ruscha matni: {q.name_ru_ru})")
    lines += ["", "Variantlar:"] + [f"{letters[i]}) {a.name_uz_uz}" for i, a in enumerate(options)]
    lines += ["", f"To'g'ri javob: {right}"]
    content = []
    image = MEDIA / q.image.name if q.image else None
    if image and image.is_file():
        content.append(_image_block(image))
    content.append({"type": "text", "text": "\n".join(lines)})
    return {"custom_id": f"t{q.id}", "params": _params(SYSTEM_TESTS, content)}


def _request(q):
    options = "\n".join(
        f"{letter}) {getattr(q, 'javob_' + letter.lower())}"
        for letter in LETTERS if getattr(q, "javob_" + letter.lower())
    )
    text = (
        f"Savol ({q.bilet}-bilet, {q.raqam}-savol): {q.savol}\n\nVariantlar:\n{options}\n\n"
        f"To'g'ri javob: {q.javob}"
    )
    content = []
    image = IMAGES / q.rasm if q.rasm else None
    if image and image.is_file():
        content.append(_image_block(image))
    content.append({"type": "text", "text": text})
    return {"custom_id": f"q{q.id}", "params": _params(SYSTEM, content)}


class Command(BaseCommand):
    help = "Avtotest izohlarining AI qoralamasi: submit / status / collect."

    def add_arguments(self, parser):
        parser.add_argument("action", choices=["submit", "status", "collect"])
        parser.add_argument("--source", choices=["avtotest", "tests"], default="avtotest",
                            help="avtotest — /avtotest/ savollari, tests — /tests/ savollari")
        parser.add_argument("--book", type=int, help="--source tests: faqat shu kitob (49 — Avto Test, 50 — e-avtomaktab)")
        parser.add_argument("--limit", type=int, default=0, help="Nechta savol (0 — barchasi)")
        parser.add_argument("--bilet", type=int, help="Faqat shu bilet")
        parser.add_argument("--redo", action="store_true", help="Qoralamasi borlarini ham qayta yozish (tasdiqlanganlar tegilmaydi)")
        parser.add_argument("--dry-run", action="store_true", help="Yubormasdan so'rovlar sonini va hajmini ko'rsatish")

    def handle(self, *args, **opts):
        getattr(self, opts["action"])(opts)

    def submit(self, opts):
        requests = self._tests_requests(opts) if opts["source"] == "tests" else self._avtotest_requests(opts)
        if not requests:
            self.stdout.write("Yuboriladigan savol yo'q.")
            return
        size_mb = len(json.dumps(requests)) / 1024 / 1024
        self.stdout.write(f"{len(requests)} ta savol, ~{size_mb:.1f} MB (model: {MODEL}).")
        if opts["dry_run"]:
            return
        if size_mb > 200:
            raise CommandError("Batch 256 MB chegarasiga yaqin — --limit bilan bo'lib yuboring.")
        batch = _client().messages.batches.create(requests=requests)
        state = _state()
        state["batches"].append({"id": batch.id, "ids": [r["custom_id"] for r in requests], "collected": False})
        _save_state(state)
        self.stdout.write(self.style.SUCCESS(f"Batch yuborildi: {batch.id}. Natijani 'collect' bilan oling (odatda 1 soatgacha)."))

    def _pending(self):
        return {cid for b in _state()["batches"] if not b.get("collected") for cid in b.get("ids", [])}

    def _tests_requests(self, opts):
        qs = (
            Questions.objects.filter(is_deleted=False).exclude(explanation_status="approved")
            .select_related("topic__book__book_type").order_by("topic__book_id", "topic__number", "number")
        )
        if not opts["redo"]:
            qs = qs.filter(explanation_uz_uz="")
        if opts["book"]:
            qs = qs.filter(topic__book_id=opts["book"])
        answers = {}
        for a in Answers.objects.filter(is_deleted=False, question__in=qs).order_by("sort_order", "number"):
            answers.setdefault(a.question_id, []).append(a)
        pending = self._pending()
        requests = []
        for q in qs:
            options = answers.get(q.id, [])
            if f"t{q.id}" in pending or sum(1 for a in options if a.right and a.name_uz_uz.strip()) != 1:
                continue  # yuborilgan yoki to'g'ri javobi aniq bitta bo'lmagan savol
            requests.append(_tests_request(q, options))
            if opts["limit"] and len(requests) >= opts["limit"]:
                break
        return requests

    def _avtotest_requests(self, opts):
        qs = AvtoTest.objects.filter(javob__in=LETTERS).exclude(izoh_holati="approved").order_by("bilet", "raqam")
        if not opts["redo"]:
            qs = qs.filter(izoh="")
        if opts["bilet"]:
            qs = qs.filter(bilet=opts["bilet"])
        pending = self._pending()
        questions = [q for q in qs if f"q{q.id}" not in pending]
        if opts["limit"]:
            questions = questions[: opts["limit"]]
        return [_request(q) for q in questions]

    def status(self, opts):
        client = _client()
        for b in _state()["batches"]:
            if b.get("collected"):
                continue
            batch = client.messages.batches.retrieve(b["id"])
            c = batch.request_counts
            self.stdout.write(f"{b['id']}: {batch.processing_status} — tayyor {c.succeeded}, xato {c.errored}, jarayonda {c.processing}")

    def collect(self, opts):
        client = _client()
        state = _state()
        saved = skipped = 0
        for b in state["batches"]:
            if b.get("collected"):
                continue
            if client.messages.batches.retrieve(b["id"]).processing_status != "ended":
                self.stdout.write(f"{b['id']}: hali tugamagan.")
                continue
            for result in client.messages.batches.results(b["id"]):
                kind, pk = result.custom_id[0], int(result.custom_id[1:])
                if result.result.type != "succeeded":
                    skipped += 1  # keyingi 'submit' da qayta yuboriladi
                    continue
                message = result.result.message
                if message.stop_reason != "end_turn":  # refusal / max_tokens — qoralama saqlanmaydi
                    skipped += 1
                    continue
                text = next((block.text for block in message.content if block.type == "text"), "")
                try:
                    data = json.loads(text)
                except ValueError:
                    skipped += 1
                    continue
                if kind == "t":
                    uz = data["uz"].strip()
                    saved += Questions.objects.filter(pk=pk).exclude(explanation_status="approved").update(
                        explanation_uz_uz=uz, explanation_uz_crl=latin_to_cyrillic(uz),
                        explanation_ru_ru=data["ru"].strip(), explanation_en_us=data["en"].strip(),
                        explanation_confidence=data["confidence"], explanation_status="draft",
                    )
                    continue
                saved += AvtoTest.objects.filter(pk=pk).exclude(izoh_holati="approved").update(
                    izoh=data["uz"].strip(), izoh_ru=data["ru"].strip(), izoh_en=data["en"].strip(),
                    izoh_ishonch=data["confidence"], izoh_holati="draft",
                )
            b["collected"] = True
        _save_state(state)
        self.stdout.write(self.style.SUCCESS(
            f"{saved} ta qoralama saqlandi, {skipped} tasi o'tkazib yuborildi. "
            "Admin → AvtoTest (yoki Tests → Questions) → filtr 'Qoralama' orqali tekshirib, tasdiqlang."
        ))
