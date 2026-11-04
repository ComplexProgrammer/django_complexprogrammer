"""Avtotest savollari izohlarining AI qoralamasini LOKAL kompyuterda Claude Code orqali yaratiş.

API kaliti (ANTHROPIC_API_KEY) işlatilmaydi: har bir savol uçun ``claude -p`` (Claude Code CLI) çaqiriladi va
sarf şu kompyuterda kirilgan Claude Code hisobi (obuna limiti) dan ketadi. Django kerak emas.

    python scripts/explanations_local.py run --limit 20 [--bilet 5] [--workers 3] [--redo] [--dry-run]

Natija ``projects/data/explanations/<sana>_claude-code_<vaqt>.json`` ga har bir javobdan keyin yoziladi (to'xtatib
qayta işga tuşirsa, tayyorlari qayta yuborilmaydi). Keyin: git add projects/data/explanations && commit && push →
serverdagi git_push.sh faylni ``manage.py import_explanations`` bilan bazaga yozadi (qoralama holatida).

Savollar loyihadagi ``db.sqlite3`` dan faqat ÖQIŞ uçun olinadi. Avval ``git pull`` qiling — serverda izohi
bor savollar qayta yuborilmaydi. Talab: ``claude`` buyruği örnatilgan va hisobga kirilgan (``claude`` → /login).
"""

import argparse
import importlib.util
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db.sqlite3"
IMAGES = ROOT / "static" / "avtotest"
TIMEOUT = 300  # bitta savol uçun (soniya)


def _load_prompts():
    """projects/explanation_prompts.py — paket (projects/__init__) orqali emas, fayldan: Django import qilinmasin."""
    spec = importlib.util.spec_from_file_location("explanation_prompts", ROOT / "projects" / "explanation_prompts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = _load_prompts()


def _already_done():
    """projects/data/explanations/ dagi fayllarda allaqačon izohi bor savollar."""
    ids = set()
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


def _prompt(q):
    """Savol matni (umumiy modul bilan bir xil) + rasm bölsa, uning yöli — Claude Code uni Read bilan oçadi."""
    text = next(block["text"] for block in P.avtotest_content({**q, "rasm": ""}, IMAGES) if block["type"] == "text")
    image = IMAGES / q["rasm"] if q.get("rasm") else None
    if image and image.is_file():
        text = f"Savol rasmi: {image}\n(Avval şu rasmni Read bilan oçib körib çiqing.)\n\n" + text
    return text


def _env():
    """API kaliti subprocess'ga ötmasin: aks holda claude CLI obuna örniga kalitdan foydalanadi."""
    env = dict(os.environ)
    for name in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
        env.pop(name, None)
    return env


def _ask(claude, q):
    cmd = [
        claude, "-p", _prompt(q),
        "--model", P.MODEL, "--effort", "medium",
        "--system-prompt", P.SYSTEM + "\n\nFaqat berilgan JSON sxemasi böyiça javob bering.",
        "--json-schema", json.dumps(P.SCHEMA),
        "--output-format", "json",
        "--tools", "Read", "--allowedTools", "Read", "--add-dir", str(IMAGES),
        "--strict-mcp-config", "--no-session-persistence",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=TIMEOUT, env=_env(), cwd=ROOT)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip()[:300])
    out = json.loads(proc.stdout)
    if out.get("is_error"):
        raise RuntimeError(str(out.get("result"))[:300])
    data = out.get("structured_output") or json.loads(out.get("result") or "{}")
    if not all(data.get(k) for k in ("uz", "ru", "en", "confidence")):
        raise RuntimeError(f"to'liq bölmagan javob: {list(data)}")
    return {k: data[k] for k in ("uz", "ru", "en", "confidence")}


def run(args):
    done = _already_done()
    todo = [q for q in _questions(args) if P.avtotest_custom_id(q["bilet"], q["raqam"]) not in done]
    if args.limit:
        todo = todo[: args.limit]
    if not todo:
        print("Yuboriladigan savol yöq (hammasida izoh bor yoki natija faylida turibdi).")
        return
    print(f"{len(todo)} ta savol, {args.workers} ta parallel (Claude Code, model: {P.MODEL}).")
    if args.dry_run:
        print("Birinči so'rov namunasi:\n" + _prompt(todo[0]))
        return
    claude = shutil.which("claude")
    if not claude:
        sys.exit("claude buyruği topilmadi: Claude Code örnatilganini va PATH'da ekanini tekşiring.")

    P.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = P.RESULTS_DIR / f"{datetime.now():%Y-%m-%d}_claude-code_{datetime.now():%H%M%S}.json"
    payload = {"source": "claude-code", "model": P.MODEL, "started": datetime.now().isoformat(timespec="seconds"), "items": []}
    lock = threading.Lock()
    failed = 0

    def save(item):
        with lock:
            payload["items"].append(item)
            payload["items"].sort(key=lambda i: P.parse_custom_id(i["id"])[1])
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(_ask, claude, q): q for q in todo}
        for n, future in enumerate(as_completed(futures), 1):
            q = futures[future]
            cid = P.avtotest_custom_id(q["bilet"], q["raqam"])
            try:
                save({"id": cid, **future.result()})
                print(f"[{n}/{len(todo)}] {q['bilet']}-bilet {q['raqam']}-savol ✓")
            except KeyboardInterrupt:
                raise
            except Exception as e:  # bitta savol xatosi butun jarayonni to'xtatmasin — keyingi işga tuşirişda qayta yuboriladi
                failed += 1
                print(f"[{n}/{len(todo)}] {q['bilet']}-bilet {q['raqam']}-savol ✗ {e}")

    items = payload["items"]
    if not items:
        path.unlink(missing_ok=True)
        sys.exit("Birorta ham izoh olinmadi.")
    low = sum(1 for i in items if i["confidence"] == "low")
    print(f"\n{path.relative_to(ROOT)}: {len(items)} ta izoh ({low} tasi past ishonçli), {failed} tasi xato.")
    print("Keyingi qadam: git add projects/data/explanations && git commit -m \"izohlar\" && git push\n"
          "Server (git_push.sh) faylni import_explanations bilan bazaga yozadi. Admin → Tests → Questions → «Qoralama».")


def main():
    parser = argparse.ArgumentParser(description="Avtotest izohlari AI qoralamasi (lokal, Claude Code orqali).")
    parser.add_argument("action", choices=["run"])
    parser.add_argument("--limit", type=int, default=0, help="Nečta savol (0 — barçasi)")
    parser.add_argument("--bilet", type=int, help="Faqat şu bilet")
    parser.add_argument("--workers", type=int, default=3, help="Bir vaqtda nečta so'rov (obuna limitiga qarab 1–4)")
    parser.add_argument("--redo", action="store_true", help="Izohi borlarini ham qayta yozish (tasdiqlanganlar tegilmaydi)")
    parser.add_argument("--dry-run", action="store_true", help="Yubormasdan savollar sonini va namunani körsatiş")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
