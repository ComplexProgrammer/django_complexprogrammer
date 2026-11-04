"""Avtotest savollari izohlarining AI qoralamasini LOKAL kompyuterda Claude Code orqali yaratiş.

API kaliti (ANTHROPIC_API_KEY) işlatilmaydi: har bir savol uçun ``claude -p`` (Claude Code CLI) çaqiriladi va
sarf şu kompyuterda kirilgan Claude Code hisobi (obuna limiti) dan ketadi. Django kerak emas.

    python scripts/explanations_local.py run --limit 20 [--bilet 5] [--workers 3] [--redo] [--dry-run] [--no-wait]

Natija ``projects/data/explanations/<sana>_claude-code_<vaqt>.json`` ga har bir javobdan keyin yoziladi.

Obuna limiti tugasa (5 soatlik yoki haftalik), skript yangi sörov yubormaydi, limit yangilanadigan vaqtni
Claude Code xabaridan aniqlaydi va şu vaqtgaça kutib, qolgan savollardan avtomatik davom etadi. Vaqt aniqlanmasa,
har ``--retry-minutes`` daqiqada (standart 15) qayta urinadi. ``--no-wait`` bilan kutmasdan tugaydi; keyin qayta
işga tuşirsangiz, tayyor bölgan savollar qayta yuborilmaydi. Kutiş paytida kompyuter uyqu rejimiga ketmasin.

Keyin: git add projects/data/explanations && commit && push → serverdagi git_push.sh faylni
``manage.py import_explanations`` bilan bazaga yozadi (qoralama holatida).

Savollar loyihadagi ``db.sqlite3`` dan faqat ÖQIŞ uçun olinadi. Avval ``git pull`` qiling: serverda izohi
bor savollar qayta yuborilmaydi. Talab: ``claude`` buyruği örnatilgan va hisobga kirilgan (``claude`` → /login).
"""

import argparse
import importlib.util
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
from concurrent.futures import CancelledError, ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db.sqlite3"
IMAGES = ROOT / "static" / "avtotest"
TIMEOUT = 300  # bitta savol uçun (soniya)
RESET_MARGIN = timedelta(minutes=2)  # limit yangilangandan keyin biroz kutib turiş
MAX_CONSECUTIVE_ERRORS = 5  # ketma-ket şunça xato — tanilmagan limit deb hisoblanib, kutiladi
ERROR_LOG = ROOT / "tmp" / "explanations_errors.log"


def _load_prompts():
    """projects/explanation_prompts.py — paket (projects/__init__) orqali emas, fayldan: Django import qilinmasin."""
    spec = importlib.util.spec_from_file_location("explanation_prompts", ROOT / "projects" / "explanation_prompts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = _load_prompts()


# --- Obuna limiti ---------------------------------------------------------------------------------------------

LIMIT_RE = re.compile(
    r"usage limit|limit reached|hit your (?:\w+ )?limit|limit will reset|out of (?:extra )?usage|rate[ _-]?limit"
    r"|too many requests",
    re.I,
)
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
RESET_AT_RE = re.compile(
    r"resets?\s+(?:at\s+|on\s+)?"
    r"(?:(" + "|".join(MONTHS) + r")[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(?:at\s+)?)?"
    r"(\d{1,2})(?::(\d{2}))?\s*([ap]\.?m\.?)?"
    r"(?:\s*\(([A-Za-z_]+(?:/[A-Za-z_+-]+)+)\))?",
    re.I,
)


class LimitReached(Exception):
    def __init__(self, message, reset_at):
        super().__init__(message)
        self.reset_at = reset_at


def _reset_time(text, now=None):
    """Claude Code xabaridan limit yangilanadigan vaqt (lokal, naive datetime) yoki None.

    Formatlar: «…limit reached|1762264800», «resets in 2h 30m», «resets 5pm (Asia/Tashkent)», «resets Nov 7, 9am».
    """
    now = now or datetime.now()
    m = re.search(r"\|(\d{10})\b", text)
    if m:
        return datetime.fromtimestamp(int(m.group(1)))
    m = re.search(r"resets?\s+in\s+(?:(\d+)\s*h\w*)?\s*(?:(\d+)\s*m\w*)?", text, re.I)
    if m and (m.group(1) or m.group(2)):
        return now + timedelta(hours=int(m.group(1) or 0), minutes=int(m.group(2) or 0))
    m = RESET_AT_RE.search(text)
    if not m:
        return None
    month, day, hour, minute, ampm, tz_name = m.groups()
    hour, minute = int(hour), int(minute or 0)
    if ampm:
        hour = hour % 12 + (12 if ampm[0].lower() == "p" else 0)
    if hour > 23 or minute > 59:
        return None
    tz = None
    if tz_name:
        try:
            from zoneinfo import ZoneInfo

            tz = ZoneInfo(tz_name)
        except Exception:  # noma'lum zona / tzdata yöq — lokal vaqt deb olinadi
            tz = None
    base = datetime.now(tz) if tz else now
    try:
        target = base.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if month:
            target = target.replace(month=MONTHS.index(month[:3].lower()) + 1, day=int(day))
            if target < base - timedelta(days=1):
                target = target.replace(year=target.year + 1)
        elif target <= base:
            target += timedelta(days=1)
    except ValueError:
        return None
    return target.astimezone().replace(tzinfo=None) if tz else target


def _parse_output(stdout):
    """``claude -p --output-format json`` natijasi; oldida/ortida boşqa qator bölsa ham oxirgi JSON obyekt olinadi."""
    try:
        return json.loads(stdout)
    except ValueError:
        pass
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except ValueError:
                continue
    return None


def _message(proc, out):
    """Qisqa matn: modelning javobi / xato xabari (JSON'dagi ``result``), bölmasa stderr."""
    parts = [str(out.get("result") or "") if out else "", proc.stderr or ""]
    if not out:
        parts.append(proc.stdout or "")
    return "\n".join(p.strip() for p in parts if p and p.strip())


def _brief(proc, out):
    return (_message(proc, out) or f"exit code {proc.returncode}").replace("\n", " ")[:300]


def _log_error(q, proc):
    """Töliq çiqişni tmp/explanations_errors.log ga yozadi (konsolda faqat qisqasi körinadi)."""
    try:
        ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
        with ERROR_LOG.open("a", encoding="utf-8") as f:
            f.write(f"--- {datetime.now():%Y-%m-%d %H:%M:%S} {q['bilet']}-bilet {q['raqam']}-savol, exit={proc.returncode}\n"
                    f"stdout: {proc.stdout}\nstderr: {proc.stderr}\n")
    except OSError:
        pass


def _synthetic(out):
    """API'ga umuman sörov ketmagan javob (limitda Claude Code şunday qaytaradi): 0 ms, 0 token."""
    if not out:
        return False
    usage = out.get("usage") or {}
    return out.get("duration_api_ms") == 0 and not usage.get("output_tokens") and not usage.get("input_tokens")


def _check_limit(proc, out):
    text = _message(proc, out)
    if (out and out.get("api_error_status") == 429) or LIMIT_RE.search(text) or _synthetic(out):
        raise LimitReached(_brief(proc, out), _reset_time(text))


def _wait_until(target):
    """Uyqu rejimidan keyin ham töğri işlaşi uçun soat bilan tekşirib kutadi."""
    print(f"\n⏸  Limit tugadi. {target:%Y-%m-%d %H:%M} gaça kutiladi, keyin avtomatik davom etadi "
          "(töxtatiş: Ctrl+C, tayyorlari saqlangan).", flush=True)
    last_note = time.monotonic()
    while True:
        left = (target - datetime.now()).total_seconds()
        if left <= 0:
            print(f"▶  {datetime.now():%H:%M} — davom etilmoqda.", flush=True)
            return
        if time.monotonic() - last_note >= 1800:
            last_note = time.monotonic()
            print(f"   ... yana {int(left // 3600)} soat {int(left % 3600 // 60)} daqiqa", flush=True)
        time.sleep(min(left, 30))


# --- Savollar va sörovlar -------------------------------------------------------------------------------------

def _already_done():
    """projects/data/explanations/ dagi fayllarda allaqaçon izohi bor savollar."""
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


def _cid(q):
    return P.avtotest_custom_id(q["bilet"], q["raqam"])


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


def _ask(claude, q, stop):
    if stop.is_set():  # boşqa sörov limitga urildi — bu savol keyingi bosqiçda yuboriladi
        return None
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
    out = _parse_output(proc.stdout or "")
    data = None
    if proc.returncode == 0 and out and not out.get("is_error"):
        data = out.get("structured_output")
        if not data:
            try:
                data = json.loads(out.get("result") or "")
            except ValueError:
                data = None
    if isinstance(data, dict) and all(data.get(k) for k in ("uz", "ru", "en", "confidence")):
        return {k: data[k] for k in ("uz", "ru", "en", "confidence")}
    _log_error(q, proc)
    _check_limit(proc, out)
    if isinstance(data, dict):
        raise RuntimeError(f"töliq bölmagan javob: {list(data)}")
    raise RuntimeError(_brief(proc, out))


def _task(claude, q, stop):
    """Limitga urilgan zahoti boşqa oqimlar ham yangi sörov boşlamasin (asosiy oqimni kutmasdan)."""
    try:
        return _ask(claude, q, stop)
    except LimitReached:
        stop.set()
        raise


def _round(claude, todo, workers, save, progress):
    """Bir bosqiç: limitga urilsa, yangi sörovlar yuborilmaydi va LimitReached qaytariladi."""
    stop = threading.Event()
    limit = None
    streak = []  # ketma-ket xato bergan savollar
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_task, claude, q, stop): q for q in todo}
        for future in as_completed(futures):
            q = futures[future]
            label = f"{q['bilet']}-bilet {q['raqam']}-savol"
            try:
                item = future.result()
            except CancelledError:
                continue
            except LimitReached as e:
                if limit is None:
                    for f in futures:
                        f.cancel()
                    print(f"⛔ {label}: obuna limiti — {e}", flush=True)
                if limit is None or (e.reset_at and (not limit.reset_at or e.reset_at > limit.reset_at)):
                    limit = e
                continue
            except KeyboardInterrupt:
                raise
            except Exception as e:  # bitta savol xatosi butun jarayonni töxtatmasin — keyingi işga tuşirişda qayta yuboriladi
                if limit is not None:  # limitdan keyin tugagan sörov — qayta yuboriladi
                    continue
                streak.append(_cid(q))
                progress["failed"].add(_cid(q))
                progress["n"] += 1
                print(f"[{progress['n']}/{progress['total']}] {label} ✗ {e}", flush=True)
                if len(streak) >= MAX_CONSECUTIVE_ERRORS:
                    stop.set()
                    for f in futures:
                        f.cancel()
                    progress["failed"].difference_update(streak)  # bular ham kutişdan keyin qayta yuboriladi
                    progress["n"] -= len(streak)
                    limit = LimitReached(f"ketma-ket {len(streak)} ta xato (töliq matn: {ERROR_LOG.relative_to(ROOT)})", None)
                    print(f"⛔ {limit} — limit deb hisoblanadi.", flush=True)
                continue
            if item is None:
                continue
            streak.clear()
            save({"id": _cid(q), **item})
            progress["n"] += 1
            print(f"[{progress['n']}/{progress['total']}] {label} ✓", flush=True)
    return limit


def run(args):
    done = _already_done()
    queue = [q for q in _questions(args) if _cid(q) not in done]
    if args.limit:
        queue = queue[: args.limit]
    if not queue:
        print("Yuboriladigan savol yöq (hammasida izoh bor yoki natija faylida turibdi).")
        return
    print(f"{len(queue)} ta savol, {args.workers} ta parallel (Claude Code, model: {P.MODEL}).")
    if args.dry_run:
        print("Birinçi sörov namunasi:\n" + _prompt(queue[0]))
        return
    claude = shutil.which("claude")
    if not claude:
        sys.exit("claude buyruği topilmadi: Claude Code örnatilganini va PATH'da ekanini tekşiring.")

    P.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = P.RESULTS_DIR / f"{datetime.now():%Y-%m-%d}_claude-code_{datetime.now():%H%M%S}.json"
    payload = {"source": "claude-code", "model": P.MODEL, "started": datetime.now().isoformat(timespec="seconds"), "items": []}
    lock = threading.Lock()
    progress = {"n": 0, "total": len(queue), "failed": set()}

    def save(item):
        with lock:
            done.add(item["id"])
            payload["items"].append(item)
            payload["items"].sort(key=lambda i: P.parse_custom_id(i["id"])[1])
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    remaining = []
    try:
        while True:
            remaining = [q for q in queue if _cid(q) not in done and _cid(q) not in progress["failed"]]
            if not remaining:
                break
            limit = _round(claude, remaining, args.workers, save, progress)
            if limit is None:
                remaining = []
                break
            remaining = [q for q in queue if _cid(q) not in done and _cid(q) not in progress["failed"]]
            if not remaining:
                break
            now = datetime.now()
            if limit.reset_at and limit.reset_at > now:
                resume = limit.reset_at + RESET_MARGIN
            else:  # vaqt aniqlanmadi — birozdan keyin qayta urinib köriladi
                resume = now + timedelta(minutes=args.retry_minutes)
            if args.no_wait:
                print(f"\n--no-wait: {len(remaining)} ta savol qoldi. Limit ~{resume:%Y-%m-%d %H:%M} da yangilanadi, "
                      "keyin skriptni qayta işga tuşiring.")
                break
            _wait_until(resume)
    except KeyboardInterrupt:
        print("\nTöxtatildi (Ctrl+C). Tayyor izohlar saqlangan, qayta işga tuşirsangiz qolganidan davom etadi.")

    items = payload["items"]
    if not items:
        path.unlink(missing_ok=True)
        sys.exit("Birorta ham izoh olinmadi.")
    low = sum(1 for i in items if i["confidence"] == "low")
    shown = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    print(f"\n{shown}: {len(items)} ta izoh ({low} tasi past ishonçli), "
          f"{len(progress['failed'])} tasi xato" + (f", {len(remaining)} tasi qoldi." if remaining else "."))
    print("Keyingi qadam: git add projects/data/explanations && git commit -m \"izohlar\" && git push\n"
          "Server (git_push.sh) faylni import_explanations bilan bazaga yozadi. Admin → Tests → Questions → «Qoralama».")


def main():
    parser = argparse.ArgumentParser(description="Avtotest izohlari AI qoralamasi (lokal, Claude Code orqali).")
    parser.add_argument("action", choices=["run"])
    parser.add_argument("--limit", type=int, default=0, help="Neçta savol (0 — barçasi)")
    parser.add_argument("--bilet", type=int, help="Faqat şu bilet")
    parser.add_argument("--workers", type=int, default=3, help="Bir vaqtda neçta sörov (obuna limitiga qarab 1–4)")
    parser.add_argument("--redo", action="store_true", help="Izohi borlarini ham qayta yoziş (tasdiqlanganlar tegilmaydi)")
    parser.add_argument("--dry-run", action="store_true", help="Yubormasdan savollar sonini va namunani körsatiş")
    parser.add_argument("--no-wait", action="store_true", help="Limit tugasa kutmasdan çiqiş")
    parser.add_argument("--retry-minutes", type=int, default=15,
                        help="Limit yangilaniş vaqti aniqlanmasa, neçta daqiqadan keyin qayta urinilsin")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
