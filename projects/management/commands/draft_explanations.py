"""Avtotest savollariga "nima uchun bu javob to'g'ri" izohining AI qoralamasini yozish (Claude, Message Batches API).

    python manage.py draft_explanations submit [--limit 50] [--bilet 5] [--redo]   # batch yuborish
    python manage.py draft_explanations status                                     # yuborilgan batchlar holati
    python manage.py draft_explanations collect                                    # tayyor natijalarni bazaga yozish

Batch API oddiy so'rovdan 50% arzon, natija odatda 1 soat ichida tayyor bo'ladi. Qoralamalar ``izoh_holati="draft"``
bilan saqlanadi — saytda faqat admin panelda "Izohni tasdiqlash" qilingandan keyin ko'rinadi.
Kalit: ANTHROPIC_API_KEY (.env) yoki `ant auth login` profili.
"""

import base64
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from projects.models import AvtoTest

MODEL = "claude-opus-5-5"
LETTERS = ("A", "B", "C", "D")
STATE_FILE = Path(settings.BASE_DIR) / "tmp" / "explanation_batches.json"
IMAGES = Path(settings.BASE_DIR) / "static" / "avtotest"

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
        media = "image/png" if image.suffix.lower() == ".png" else "image/jpeg"
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": media, "data": base64.standard_b64encode(image.read_bytes()).decode()},
        })
    content.append({"type": "text", "text": text})
    return {
        "custom_id": f"q{q.id}",
        "params": {
            "model": MODEL,
            "max_tokens": 16000,
            "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
            # Barcha so'rovlarda bir xil tizim matni — keshlanadi
            "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": content}],
        },
    }


class Command(BaseCommand):
    help = "Avtotest izohlarining AI qoralamasi: submit / status / collect."

    def add_arguments(self, parser):
        parser.add_argument("action", choices=["submit", "status", "collect"])
        parser.add_argument("--limit", type=int, default=0, help="Nechta savol (0 — barchasi)")
        parser.add_argument("--bilet", type=int, help="Faqat shu bilet")
        parser.add_argument("--redo", action="store_true", help="Qoralamasi borlarini ham qayta yozish (tasdiqlanganlar tegilmaydi)")
        parser.add_argument("--dry-run", action="store_true", help="Yubormasdan so'rovlar sonini va hajmini ko'rsatish")

    def handle(self, *args, **opts):
        getattr(self, opts["action"])(opts)

    def submit(self, opts):
        qs = AvtoTest.objects.filter(javob__in=LETTERS).exclude(izoh_holati="approved").order_by("bilet", "raqam")
        if not opts["redo"]:
            qs = qs.filter(izoh="")
        if opts["bilet"]:
            qs = qs.filter(bilet=opts["bilet"])
        pending = {cid for b in _state()["batches"] if not b.get("collected") for cid in b.get("ids", [])}
        questions = [q for q in qs if f"q{q.id}" not in pending]
        if opts["limit"]:
            questions = questions[: opts["limit"]]
        if not questions:
            self.stdout.write("Yuboriladigan savol yo'q.")
            return
        requests = [_request(q) for q in questions]
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
                pk = int(result.custom_id[1:])
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
                saved += AvtoTest.objects.filter(pk=pk).exclude(izoh_holati="approved").update(
                    izoh=data["uz"].strip(), izoh_ru=data["ru"].strip(), izoh_en=data["en"].strip(),
                    izoh_ishonch=data["confidence"], izoh_holati="draft",
                )
            b["collected"] = True
        _save_state(state)
        self.stdout.write(self.style.SUCCESS(
            f"{saved} ta qoralama saqlandi, {skipped} tasi o'tkazib yuborildi. "
            "Admin → AvtoTest → filtr 'Qoralama' orqali tekshirib, tasdiqlang."
        ))
