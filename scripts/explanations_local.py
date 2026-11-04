"""Avtotest savollari izohlarining AI qoralamasini LOKAL kompyuterda yaratiş (Django kerak emas).

Serverda API kaliti saqlanmaydi: so'rovlar şu kompyuterdan yuboriladi, natija git orqali serverga boradi.

    pip install anthropic                                   # bir marta
    python scripts/explanations_local.py submit --limit 100 [--bilet 5] [--redo] [--dry-run]
    python scripts/explanations_local.py status
    python scripts/explanations_local.py collect            # tayyor batchlarni faylga yozadi

Keyin: git add projects/data/explanations && commit && push → serverdagi git_push.sh yangi faylni
``manage.py import_explanations`` bilan bazaga yozadi (qoralama holatida — admin tasdiqlagandan keyin körinadi).

Savollar loyihadagi ``db.sqlite3`` dan faqat ÖQIŞ uçun olinadi (baza özgartirilmaydi). Avval ``git pull`` qiling,
şunda serverda allaqačon izohi bor savollar qayta yuborilmaydi. Kalit: ANTHROPIC_API_KEY (muhit özgaruvçisi
yoki loyiha .env fayli). Batch API oddiy so'rovdan 50% arzon, natija odatda 1 soat ičida tayyor böladi.
"""

import argparse
import importlib.util
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db.sqlite3"
IMAGES = ROOT / "static" / "avtotest"
STATE_FILE = ROOT / "tmp" / "explanation_batches_local.json"


def _load_prompts():
    """projects/explanation_prompts.py — paket (projects/__init__) orqali emas, fayldan: Django import qilinmasin."""
    spec = importlib.util.spec_from_file_location("explanation_prompts", ROOT / "projects" / "explanation_prompts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = _load_prompts()


def _api_key():
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    env = ROOT / ".env"
    if not key and env.is_file():
        for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
            name, _, value = line.strip().partition("=")
            if name.strip() == "ANTHROPIC_API_KEY":
                key = value.strip().strip("'\"")
    return key


def _client():
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic kutubxonasi örnatilmagan: pip install anthropic")
    key = _api_key()
    return anthropic.Anthropic(api_key=key) if key else anthropic.Anthropic()


def _state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"batches": []}


def _save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _already_done():
    """Hali serverga import qilinmagan natija fayllaridagi va javobi kutilayotgan batchlardagi savollar."""
    ids = {cid for b in _state()["batches"] if not b.get("collected") for cid in b.get("ids", [])}
    for path in P.RESULTS_DIR.glob("*.json"):
        try:
            ids.update(item["id"] for item in json.loads(path.read_text(encoding="utf-8"))["items"])
        except (ValueError, KeyError):
            pass
    return ids


def _questions(args):
    if not DB.is_file():
        sys.exit(f"Baza topilmadi: {DB}")
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    sql = (
        "SELECT bilet, raqam, savol, javob_a, javob_b, javob_c, javob_d, javob, rasm FROM projects_avtotest "
        "WHERE javob IN ('A', 'B', 'C', 'D') AND savol <> '' AND izoh_holati <> 'approved'"
    )
    values = []
    if not args.redo:
        sql += " AND izoh = ''"
    if args.bilet:
        sql += " AND bilet = ?"
        values.append(args.bilet)
    rows = [dict(r) for r in conn.execute(sql + " ORDER BY bilet, raqam", values)]
    conn.close()
    return rows


def submit(args):
    done = _already_done()
    requests = []
    for q in _questions(args):
        cid = P.avtotest_custom_id(q["bilet"], q["raqam"])
        if cid in done:
            continue
        requests.append({"custom_id": cid, "params": P.params(P.SYSTEM, P.avtotest_content(q, IMAGES))})
        if args.limit and len(requests) >= args.limit:
            break
    if not requests:
        print("Yuboriladigan savol yöq (hammasida izoh bor yoki natijasi kutilmoqda).")
        return
    size_mb = len(json.dumps(requests)) / 1024 / 1024
    print(f"{len(requests)} ta savol, ~{size_mb:.1f} MB (model: {P.MODEL}).")
    if args.dry_run:
        return
    if size_mb > 200:
        sys.exit("Batch 256 MB chegarasiga yaqin — --limit bilan bölib yuboring.")
    batch = _client().messages.batches.create(requests=requests)
    state = _state()
    state["batches"].append({"id": batch.id, "ids": [r["custom_id"] for r in requests], "collected": False,
                             "created": datetime.now().isoformat(timespec="seconds")})
    _save_state(state)
    print(f"Batch yuborildi: {batch.id}. Natijani 'collect' bilan oling (odatda 1 soatgaça).")


def status(args):
    client = _client()
    pending = [b for b in _state()["batches"] if not b.get("collected")]
    if not pending:
        print("Kutilayotgan batch yöq.")
    for b in pending:
        batch = client.messages.batches.retrieve(b["id"])
        c = batch.request_counts
        print(f"{b['id']}: {batch.processing_status} — tayyor {c.succeeded}, xato {c.errored}, jarayonda {c.processing}")


def collect(args):
    client = _client()
    state = _state()
    written = []
    for b in state["batches"]:
        if b.get("collected"):
            continue
        if client.messages.batches.retrieve(b["id"]).processing_status != "ended":
            print(f"{b['id']}: hali tugamagan.")
            continue
        items, skipped = [], []
        for result in client.messages.batches.results(b["id"]):
            if result.result.type != "succeeded":
                skipped.append(result.custom_id)  # keyingi 'submit' da qayta yuboriladi
                continue
            message = result.result.message
            if message.stop_reason != "end_turn":  # refusal / max_tokens — qoralama saqlanmaydi
                skipped.append(result.custom_id)
                continue
            text = next((block.text for block in message.content if block.type == "text"), "")
            try:
                data = json.loads(text)
            except ValueError:
                skipped.append(result.custom_id)
                continue
            items.append({"id": result.custom_id, **{k: data.get(k, "") for k in ("uz", "ru", "en", "confidence")}})
        P.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        path = P.RESULTS_DIR / f"{datetime.now():%Y-%m-%d}_{b['id']}.json"
        payload = {"batch": b["id"], "model": P.MODEL, "collected": datetime.now().isoformat(timespec="seconds"),
                   "items": sorted(items, key=lambda i: P.parse_custom_id(i["id"])[1])}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        b["collected"] = True
        written.append(path)
        low = sum(1 for i in items if i["confidence"] == "low")
        print(f"{path.relative_to(ROOT)}: {len(items)} ta izoh ({low} tasi past ishonçli), {len(skipped)} tasi ötkazib yuborildi.")
    _save_state(state)
    if written:
        print("\nKeyingi qadam: git add projects/data/explanations && git commit -m \"izohlar\" && git push\n"
              "Server (git_push.sh) faylni import_explanations bilan bazaga yozadi. Admin → Tests → Questions → «Qoralama».")


def main():
    parser = argparse.ArgumentParser(description="Avtotest izohlari AI qoralamasi (lokal, Django'siz).")
    parser.add_argument("action", choices=["submit", "status", "collect"])
    parser.add_argument("--limit", type=int, default=0, help="Nečta savol (0 — barçasi)")
    parser.add_argument("--bilet", type=int, help="Faqat şu bilet")
    parser.add_argument("--redo", action="store_true", help="Izohi borlarini ham qayta yozish (tasdiqlanganlar tegilmaydi)")
    parser.add_argument("--dry-run", action="store_true", help="Yubormasdan so'rovlar sonini va hajmini körsatiş")
    args = parser.parse_args()
    {"submit": submit, "status": status, "collect": collect}[args.action](args)


if __name__ == "__main__":
    main()
