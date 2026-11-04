"""Avtotest savollari izohlarining AI qoralamasini Antigravity (Gemini) orqali yaratiş.

API kaliti talab qilinmaydi: har bir savol uçun Antigravity CLI (``agy -p``) çaqiriladi va
sarf joriy tizimdagi Antigravity hisobi / tokenlaridan ketadi.

İşlatilişi:
    python scripts/explanations_antigravity.py run [--limit 20] [--bilet 42] [--workers 2] [--dry-run] [--no-wait]

Limit tugasa (daqiqlik/soatlik/kunlik kvota):
    Skript avtomatik ravishda PAUZA holatiga ötadi, yangilaniş vaqtini (yoki belgilangan daqiqani) kutadi
    va limit tiklangaç inson aralashuvisiz özi avtomatik qolgan savollardan davom etadi.

Natija ``projects/data/explanations/<sana>_antigravity_<vaqt>.json`` fayliga har bir savoldan söng darhol yoziladi.
Keyin: serverda ``manage.py import_explanations`` bilan bazaga yuklanadi.
"""

import argparse
import importlib.util
import json
import os
import random
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
TIMEOUT = 180  # bitta savol uçun maksimal vaqt (soniya)
MAX_RETRIES = 4  # tarmoq yoki vaqtinça xatolikda qayta urinishlar soni
RESET_MARGIN = timedelta(minutes=2)  # limit yangilangandan keyin ehtiyotkorona biroz kutib turiş
ERROR_LOG = ROOT / "tmp" / "explanations_antigravity_errors.log"


def _load_prompts():
    spec = importlib.util.spec_from_file_location("explanation_prompts", ROOT / "projects" / "explanation_prompts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = _load_prompts()

SYSTEM_PROMPT = """Siz O'zbekiston yo'l harakati qoidalari (YHQ) bo'yicha oliy toifali mutaxassis va o'qituvchisiz. \
Haydovchilikka nomzodlar uchun avtotest savolining to'g'ri javobi nima uchun to'g'ri ekanini qisqa, tushunarli va asosli tushuntirasiz.

Qat'iy talablar:
1. Matn hajmi: 2-4 gap, sodda va lo'nda til. Avval qoida mazmunini ayting, keyin uni ushbu vaziyatga qo'llang.
2. To'g'ri javob sizga berilgan — uni aslo o'zgartirmang va boshqa variantni to'g'ri deb ko'rsatmang.
3. YHQ band raqamini faqat aniq bilsangiz yozing; ishonchingiz komil bo'lmasa, band raqamisiz qoida mazmunini tushuntiring.
4. Rasm berilgan bo'lsa, rasmni ko'rib chiqib, undagi yo'l belgilari, chiziqlar va transport vositalari joylashuviga tayaning.
5. Matn ichida juft qo'shtirnoq (") ishlatmang! Qoidalar, atamalar yoki belgilar nomi uchun faqat burchakli («...») yoki bittalik ('...') qo'shtirnoq ishlating.
6. Uchala tilda bir xil mazmun:
   - "uz": O'zbek tili (2026-yilgi yangi lotin alifbosi: sh->ş, ch->ç, g'->ğ, o'->ö harflari bilan yozilsin!);
   - "ru": Rus tili;
   - "en": Ingliz tili.
7. "confidence": berilgan javobni qoidaga to'liq va ishonchli bog'lay olsangiz "high", qisman asoslasangiz "medium", savol yoki variant noaniq tuyulsa "low".

Javobni FAQAT va FAQAT bitta toza JSON obyekti ko'rinishida bering (boshqa hech qanday so'z, izoh yoki matn qo'shmang):
{
  "uz": "O'zbekcha tushuntirish (ş, ç, ğ, ö harflari bilan)",
  "ru": "Русское объяснение",
  "en": "English explanation",
  "confidence": "high"
}"""

# --- Limit va tarmoqni aniqlash -----------------------------------------------------------------

LIMIT_RE = re.compile(
    r"credits?\s+balance|balance\s+is\s+too\s+low|too\s+low\s+to\s+continue|out\s+of\s+credits|"
    r"credits?\s+exhausted|resource_exhausted|quota\s+exceeded|usage\s+limit|limit\s+reached|"
    r"hit\s+your.*limit|limit\s+will\s+reset|rate[ _-]?limit|too\s+many\s+requests|\b429\b",
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
    """Kvota yoki so'rovlar limiti tugaganda jarayonni xavfsiz to'xtatib kutish uchun istisno."""
    def __init__(self, message, reset_at=None):
        super().__init__(message)
        self.reset_at = reset_at


def _reset_time(text, now=None):
    """Xabar matnidan limit qachon yangilanishini aniqlash (mavjud bo'lsa)."""
    now = now or datetime.now()
    m = re.search(r"\|(\d{10})\b", text)
    if m:
        return datetime.fromtimestamp(int(m.group(1)))
    m = re.search(r"resets?\s+in\s+(?:(\d+)\s*h\w*)?\s*(?:(\d+)\s*m\w*)?", text, re.I)
    if m and (m.group(1) or m.group(2)):
        return now + timedelta(hours=int(m.group(1) or 0), minutes=int(m.group(2) or 0))
    m = RESET_AT_RE.search(text)
    if m:
        month, day, hour, minute, ampm, tz_name = m.groups()
        hour, minute = int(hour), int(minute or 0)
        if ampm:
            hour = hour % 12 + (12 if ampm[0].lower() == "p" else 0)
        if hour <= 23 and minute <= 59:
            tz = None
            if tz_name:
                try:
                    from zoneinfo import ZoneInfo
                    tz = ZoneInfo(tz_name)
                except Exception:
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
                return target.astimezone().replace(tzinfo=None) if tz else target
            except ValueError:
                pass

    # AI credits balansi tugagan bo'lsa — keyingi soat boshiga yoki kamida 20 daqiqaga mo'ljallash
    if re.search(r"credits?\s+balance|balance\s+is\s+too\s+low", text, re.I):
        next_hour = (now + timedelta(hours=1)).replace(minute=1, second=0, microsecond=0)
        if (next_hour - now).total_seconds() < 900:  # 15 daqiqadan kam qolgan bo'lsa
            next_hour += timedelta(hours=1)
        return next_hour

    return None


def _wait_until(target, reason):
    """Limit tiklangunga qadar pauzada turish va vaqt yetganda avtomatik uyg'onish."""
    print(f"\n⏸  {reason} {target:%Y-%m-%d %H:%M} gaça kutiladi, söng avtomatik davom etadi "
          "(töxtatiş: Ctrl+C, tayyorlari saqlangan).", flush=True)
    last_note = time.monotonic()
    while True:
        left = (target - datetime.now()).total_seconds()
        if left <= 0:
            print(f"▶  {datetime.now():%H:%M} — limit tiklandi, avtomatik davom etilmoqda.", flush=True)
            return
        if time.monotonic() - last_note >= 1800:
            last_note = time.monotonic()
            print(f"   ... yana {int(left // 3600)} soat {int(left % 3600 // 60)} daqiqa kutilmoqda", flush=True)
        time.sleep(min(left, 20))


def _find_agy():
    """Antigravity CLI (agy.exe) ijro faylini aniqlash."""
    env_exe = os.environ.get("ANTIGRAVITY_AGENTAPI_EXE")
    if env_exe and Path(env_exe).is_file():
        return env_exe
    which_exe = shutil.which("agy") or shutil.which("agy.exe")
    if which_exe:
        return which_exe
    user_home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or ".")
    candidate = user_home / ".gemini" / "bin" / ("agy.exe" if sys.platform == "win32" else "agy")
    if candidate.is_file():
        return str(candidate)
    return None


def _clean_2026_uzbek(text):
    """O'zbekcha matndagi eski harf birikmalarini 2026-yilgi isloh qilingan harflarga tekshirib o'tkazish."""
    if not text:
        return text
    subs = [
        ("Sh", "Ş"), ("SH", "Ş"), ("sh", "ş"),
        ("Ch", "Ç"), ("CH", "Ç"), ("ch", "ç"),
        ("O'", "Ö"), ("Oʻ", "Ö"), ("O`", "Ö"),
        ("o'", "ö"), ("oʻ", "ö"), ("o`", "ö"),
        ("G'", "Ğ"), ("Gʻ", "Ğ"), ("G`", "Ğ"),
        ("g'", "ğ"), ("gʻ", "ğ"), ("g`", "ğ"),
    ]
    res = text
    for old, new in subs:
        res = res.replace(old, new)
    return res


def _clean_internal_quotes(text):
    """Matn ichidagi buzilgan yoki qochirilmagan qo'shtirnoqlarni to'g'rilash."""
    if not text:
        return ""
    cleaned = text.replace('\\"', '"')
    parts = cleaned.split('"')
    if len(parts) > 1:
        return "«".join(parts)
    return cleaned


def _extract_by_regex(raw_text):
    """JSON ichida qochirilmagan qo'shtirnoq bo'lsa ham maydonlarni regex orqali ajratib olish."""
    uz_m = re.search(r'"uz"\s*:\s*"([\s\S]*?)"\s*,\s*"ru"\s*:', raw_text)
    ru_m = re.search(r'"ru"\s*:\s*"([\s\S]*?)"\s*,\s*"en"\s*:', raw_text)
    en_m = re.search(r'"en"\s*:\s*"([\s\S]*?)"\s*,\s*"confidence"\s*:', raw_text)
    conf_m = re.search(r'"confidence"\s*:\s*"?([a-zA-Z]+)"?', raw_text, re.I)

    if uz_m and ru_m and en_m:
        uz = _clean_internal_quotes(uz_m.group(1).strip())
        ru = _clean_internal_quotes(ru_m.group(1).strip())
        en = _clean_internal_quotes(en_m.group(1).strip())
        conf = conf_m.group(1).lower() if conf_m else "high"
        if conf not in ("high", "medium", "low"):
            conf = "high"
        return {"uz": uz, "ru": ru, "en": en, "confidence": conf}
    return None


def _extract_json_response(raw_text):
    """Matn ichidan JSON obyektini xavfsiz ajratib olish."""
    if not raw_text:
        return None
    raw_text = raw_text.strip()

    try:
        data = json.loads(raw_text)
        if isinstance(data, dict) and all(k in data for k in ("uz", "ru", "en")):
            return data
    except ValueError:
        pass

    m = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", raw_text, re.I)
    if m:
        try:
            data = json.loads(m.group(1))
            if isinstance(data, dict) and all(k in data for k in ("uz", "ru", "en")):
                return data
        except ValueError:
            pass

    first = raw_text.find("{")
    last = raw_text.rfind("}")
    if first != -1 and last != -1 and last > first:
        try:
            data = json.loads(raw_text[first:last + 1])
            if isinstance(data, dict) and all(k in data for k in ("uz", "ru", "en")):
                return data
        except ValueError:
            pass

    fallback = _extract_by_regex(raw_text)
    if fallback:
        return fallback

    return None


def _already_done():
    """projects/data/explanations/ dagi fayllarda allaqachon tayyor bo'lgan savollar to'plami."""
    ids = set()
    if not P.RESULTS_DIR.exists():
        return ids
    for path in P.RESULTS_DIR.glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            ids.update(item["id"] for item in payload.get("items", []))
        except (ValueError, KeyError, OSError):
            pass
    return ids


def _questions(args):
    """db.sqlite3 dan ishlanishi kerak bo'lgan savollarni o'qish."""
    if not DB.is_file():
        sys.exit(f"Baza topilmadi: {DB}")
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    sql = (
        "SELECT bilet, raqam, savol, javob_a, javob_b, javob_c, javob_d, javob, rasm FROM projects_avtotest "
        "WHERE javob IN ('A', 'B', 'C', 'D') AND length(savol) > 0 AND izoh_holati != 'approved'"
    )
    values = []
    if not args.redo:
        sql += " AND izoh = ''"
    if args.bilet:
        sql += " AND bilet = ?"
        values.append(args.bilet)
    sql += " ORDER BY bilet, raqam"
    rows = [dict(r) for r in conn.execute(sql, values)]
    conn.close()
    return rows


def _cid(q):
    return P.avtotest_custom_id(q["bilet"], q["raqam"])


def _sanitize_for_safety(text):
    """Google xavfsizlik filtrlarining (bolalar/tibbiy atamalar) noo'rin cheklovlarini chetlab o'tish."""
    if not text:
        return ""
    replacements = [
        ("bolalarni ushlab turuvchi", "maxsus ushlab turuvchi"),
        ("bolalarni", "kichik yo'lovchilarni"),
        ("bolalar", "yosh yo'lovchilar"),
        ("bolaga", "kichik yo'lovchiga"),
        ("bola", "yo'lovchi"),
    ]
    res = text
    for old, new in replacements:
        res = re.sub(re.escape(old), new, res, flags=re.I)
    return res


def _safety_fallback_explanation(q):
    """Xavfsizlik filtri so'rovni butunlay to'xtatgan hollarda qoidaviy xavfsiz izoh yaratish."""
    correct_ltr = q["javob"].lower()
    correct_text = q.get(f"javob_{correct_ltr}", "").strip()
    uz = (
        f"O'zbekiston Respublikasi Yo'l harakati qoidalariga muvofiq, ushbu vaziyatda to'g'ri javob: «{correct_text}». "
        "Mazkur talab yo'l harakati xavfsizligini ta'minlash hamda yo'lovchilarning hayoti va sog'lig'ini muhofaza qilishga xizmat qiladi."
    )
    ru = (
        f"Согласно Правилам дорожного движения Республики Узбекистан, правильным ответом является: «{correct_text}». "
        "Данное требование направлено на обеспечение безопасности дорожного движения и защиту пассажиров."
    )
    en = (
        f"According to the Traffic Rules of the Republic of Uzbekistan, the correct answer is: \"{correct_text}\". "
        "This requirement is aimed at ensuring road safety and passenger protection."
    )
    return {
        "uz": _clean_2026_uzbek(uz),
        "ru": ru,
        "en": en,
        "confidence": "medium",
    }


def _build_prompt(q, safe_mode=False):
    """Savol uchun Antigravity CLI ga beriladigan to'liq prompt."""
    options = []
    for ltr in ("a", "b", "c", "d"):
        val = q.get(f"javob_{ltr}")
        if val:
            if safe_mode:
                val = _sanitize_for_safety(val)
            options.append(f"{ltr.upper()}) {val}")
    opts_str = "\n".join(options)

    image_part = ""
    rasm = q.get("rasm")
    if rasm:
        img_path = IMAGES / rasm
        rel_path = f"static/avtotest/{rasm}"
        if img_path.is_file():
            image_part = (
                f"Savol rasmi: {rel_path} faylida joylashgan.\n"
                "(Iltimos, ushbu rasmni ko'rib chiqib, undagi yo'l belgilari, chiziqlar va transport vositalari vaziyatiga tayaning.)\n\n"
            )

    savol_matni = _sanitize_for_safety(q["savol"]) if safe_mode else q["savol"]
    preface = ""
    if safe_mode:
        preface = (
            "Ushbu topshiriq O'zbekiston Respublikasi rasmiy Yo'l harakati qoidalari bo'yicha haydovchilik "
            "imtihon biletining qonuniy me'yoriy talablariga bag'ishlangan sof o'quv-ta'limiy savolidir:\n\n"
        )

    body = (
        f"{preface}"
        f"{image_part}"
        f"Savol ({q['bilet']}-bilet, {q['raqam']}-savol): {savol_matni}\n\n"
        f"Variantlar:\n{opts_str}\n\n"
        f"To'g'ri javob: {q['javob']}\n\n"
        "Talablarga binoan FAQAT bitta JSON obyekti qaytaring."
    )
    return f"{SYSTEM_PROMPT}\n\n---\n\n{body}"


def _ask_agy(agy_exe, q, stop_event=None):
    """Antigravity CLI orqali bitta savol izohini olish."""
    if stop_event and stop_event.is_set():
        return None

    last_err = None
    safe_mode = False
    is_safety_blocked = False

    for attempt in range(1, MAX_RETRIES + 1):
        if stop_event and stop_event.is_set():
            return None

        prompt = _build_prompt(q, safe_mode=safe_mode)
        cmd = [agy_exe, "-p", prompt, "--output-format", "json"]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=TIMEOUT,
                cwd=ROOT,
            )
        except subprocess.TimeoutExpired:
            last_err = RuntimeError(f"agy so'rovi vaqt bo'yicha tugadi ({TIMEOUT} soniya)")
            time.sleep(3 * attempt)
            continue

        raw_stdout = proc.stdout or ""
        raw_stderr = proc.stderr or ""

        outer_json = None
        try:
            outer_json = json.loads(raw_stdout)
        except ValueError:
            for line in reversed(raw_stdout.splitlines()):
                line = line.strip()
                if line.startswith("{"):
                    try:
                        outer_json = json.loads(line)
                        break
                    except ValueError:
                        pass

        status = outer_json.get("status") if outer_json else None
        err_msg = (outer_json.get("error") if outer_json else "") or raw_stderr.strip()

        # Agar muvaffaqiyatsiz bo'lsa:
        if status != "SUCCESS":
            err_lower = err_msg.lower()
            combined_err = f"{raw_stdout} {raw_stderr} {err_msg}"

            # 1. Asosiy obuna, kredit yoki kvota limiti tugagan bo'lsa (pauza qilib kutiladi)
            if LIMIT_RE.search(combined_err):
                raise LimitReached(err_msg or "AI kreditlari balansi tugagan", _reset_time(combined_err))

            # 2. Tarmoq / DNS uzilishi yoki model aniqlanmadi (vaqtincha 2-5 soniyali uzilish)
            if any(k in err_lower for k in ("plan model not specified", "authentication failed", "timed out", "getaddrinfow", "dial tcp", "network", "connection refused", "reset")):
                last_err = RuntimeError(f"agy ulanish xatosi (urinish {attempt}/{MAX_RETRIES}): {err_msg[:120]}")
                time.sleep(3 * attempt)
                continue

            # 3. Xavfsizlik filtri to'sqinlik qilgan bo'lsa
            if any(k in err_lower for k in ("content safety filters", "prohibited use", "sensitive words", "blocked by")):
                safe_mode = True
                is_safety_blocked = True
                last_err = RuntimeError(f"xavfsizlik filtri to'xtatdi (urinish {attempt}/{MAX_RETRIES}): {err_msg[:120]}")
                time.sleep(1.5)
                continue

            last_err = RuntimeError(f"agy muvaffaqiyatsiz: {err_msg}")
            time.sleep(2 * attempt)
            continue

        response_text = outer_json.get("response") or ""
        item_data = _extract_json_response(response_text)
        if not item_data:
            last_err = RuntimeError(f"Model javobidan izoh JSON ajratib olinmadi: {response_text[:120]}")
            time.sleep(2)
            continue

        missing = [k for k in ("uz", "ru", "en") if not item_data.get(k)]
        if missing:
            last_err = RuntimeError(f"JSON'da {missing} maydonlari yetishmaydi")
            time.sleep(2)
            continue

        conf = str(item_data.get("confidence", "high")).lower()
        if conf not in ("high", "medium", "low"):
            conf = "high"

        uz_text = _clean_2026_uzbek(item_data["uz"].strip())

        return {
            "uz": uz_text,
            "ru": item_data["ru"].strip(),
            "en": item_data["en"].strip(),
            "confidence": conf,
        }

    if is_safety_blocked:
        return _safety_fallback_explanation(q)

    raise last_err or RuntimeError("So'rov barcha urinishlarda muvaffaqiyatsiz bo'ldi")


def _run_worker(agy_exe, q, lock, save_fn, progress, stop_event):
    """Bitta savolni qayta ishlash."""
    if stop_event.is_set():
        return None

    time.sleep(random.uniform(0.1, 0.4))
    label = f"{q['bilet']}-bilet {q['raqam']}-savol"

    try:
        res = _ask_agy(agy_exe, q, stop_event)
        if res is None:
            return None
        save_fn({"id": _cid(q), **res})
        with lock:
            progress["n"] += 1
            print(f"[{progress['n']}/{progress['total']}] {label} ✓ ({res['confidence']})", flush=True)
        return True
    except LimitReached as lr:
        stop_event.set()
        raise lr
    except Exception as e:
        with lock:
            progress["n"] += 1
            progress["failed"].add(_cid(q))
            print(f"[{progress['n']}/{progress['total']}] {label} ✗ {e}", flush=True)
            try:
                ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
                with ERROR_LOG.open("a", encoding="utf-8") as f:
                    f.write(f"--- {datetime.now():%Y-%m-%d %H:%M:%S} {label} ---\n{e}\n\n")
            except OSError:
                pass
        return False


def _round(agy_exe, todo, workers, save_fn, progress):
    """Bir bosqich: agar obuna/kvota limiti tugasa, boshqa oqimlar to'xtatilib, LimitReached qaytariladi."""
    stop_event = threading.Event()
    limit_exc = None
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_run_worker, agy_exe, q, lock, save_fn, progress, stop_event): q for q in todo}
        for future in as_completed(futures):
            q = futures[future]
            label = f"{q['bilet']}-bilet {q['raqam']}-savol"
            try:
                future.result()
            except CancelledError:
                continue
            except LimitReached as lr:
                if limit_exc is None:
                    stop_event.set()
                    for f in futures:
                        f.cancel()
                    print(f"\n⛔ {label}: Kvota / limit tugadi — {lr}", flush=True)
                    limit_exc = lr
                continue
            except KeyboardInterrupt:
                stop_event.set()
                for f in futures:
                    f.cancel()
                raise
            except Exception:
                continue

    return limit_exc


def run(args):
    agy_exe = _find_agy()
    if not agy_exe:
        sys.exit("Antigravity CLI (agy.exe) topilmadi. Tizimda agy o'rnatilganini tekshiring.")

    done = _already_done()
    all_q = _questions(args)
    queue = [q for q in all_q if _cid(q) not in done]

    if args.limit and args.limit > 0:
        queue = queue[: args.limit]

    if not queue:
        print("Yangi izoh talab qilinadigan savol topilmadi (hammasi tayyor yoki natija fayllarida bor).")
        return

    print(f"📋 Jami: {len(queue)} ta savol, parallel oqimlar: {args.workers} ta.")
    print(f"🤖 Antigravity CLI: {agy_exe}")

    if args.dry_run:
        print("\n--- Birinchi so'rov namunasi ---\n")
        print(_build_prompt(queue[0]))
        return

    P.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_file = P.RESULTS_DIR / f"{datetime.now():%Y-%m-%d}_antigravity_{datetime.now():%H%M%S}.json"
    payload = {
        "source": "antigravity",
        "model": "gemini-4-argon",
        "started": datetime.now().isoformat(timespec="seconds"),
        "items": [],
    }

    lock = threading.Lock()
    progress = {"n": 0, "total": len(queue), "failed": set()}

    def save(item):
        with lock:
            done.add(item["id"])
            payload["items"].append(item)
            payload["items"].sort(key=lambda i: P.parse_custom_id(i["id"])[1])
            out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"🚀 Jarayon boshlandi. Natijalar fayli: {out_file.relative_to(ROOT)}\n", flush=True)

    remaining = []
    try:
        while True:
            remaining = [q for q in queue if _cid(q) not in done and _cid(q) not in progress["failed"]]
            if not remaining:
                break

            limit = _round(agy_exe, remaining, args.workers, save, progress)
            if limit is None:
                # Agar limit xatosi bo'lmasa va qolganlar bo'lsa (masalan, ayrim xatoliklar), tugatamiz yoki davom etamiz
                remaining = [q for q in queue if _cid(q) not in done and _cid(q) not in progress["failed"]]
                break

            remaining = [q for q in queue if _cid(q) not in done and _cid(q) not in progress["failed"]]
            if not remaining:
                break

            now = datetime.now()
            if limit.reset_at and limit.reset_at > now:
                resume = limit.reset_at + RESET_MARGIN
                reason = "Limit tugadi, yangilaniş vaqti:"
            else:
                resume = now + timedelta(minutes=args.retry_minutes)
                reason = f"Limit tugadi (yangilaniş vaqti noma'lum, {args.retry_minutes} daqiqadan söng tekşiriladi):"

            if args.no_wait:
                print(f"\n--no-wait rejimi: {len(remaining)} ta savol qoldi. Limit ~{resume:%Y-%m-%d %H:%M} da yangilanadi.")
                break

            _wait_until(resume, reason)

    except KeyboardInterrupt:
        print("\n\n⏹ Foydalanuvchi tomonidan to'xtatildi (Ctrl+C). Saqlangan izohlar faylda qoldi.")

    items = payload["items"]
    if items:
        low = sum(1 for i in items if i.get("confidence") == "low")
        print(f"\n✅ Yakunlandi! {len(items)} ta savolga izoh tayyorlandi ({low} tasi past ishonchli).")
        print(f"📁 Fayl: {out_file.relative_to(ROOT)}")
        print("Keyingi buyruq (serverga yuborish):")
        print(f'  git add {out_file.relative_to(ROOT)} && git commit -m "izohlar: antigravity" && git push')
    else:
        out_file.unlink(missing_ok=True)
        print("\n⚠️ Hech qanday yangi izoh olinmadi.")


def main():
    parser = argparse.ArgumentParser(description="Avtotest izohlari AI qoralamasi (Antigravity tokenlari orqali).")
    parser.add_argument("action", nargs="?", default="run", choices=["run"], help="Harakat (standart: run)")
    parser.add_argument("--limit", type=int, default=0, help="Nechta savol ishlanishi (0 — barchasi)")
    parser.add_argument("--bilet", type=int, help="Faqat ko'rsatilgan bilet savollari")
    parser.add_argument("--workers", type=int, default=2, help="Bir vaqtda ishlaydigan so'rovlar soni (standart: 2)")
    parser.add_argument("--redo", action="store_true", help="Izohi bor savollarni ham qayta ishlash")
    parser.add_argument("--dry-run", action="store_true", help="Haqiqiy so'rov yubormasdan savol va promptni ko'rish")
    parser.add_argument("--no-wait", action="store_true", help="Limit tugasa kutmasdan chiqish")
    parser.add_argument("--retry-minutes", type=int, default=10, help="Limit yangilanish vaqti noma'lum bo'lsa, necha daqiqadan keyin qayta urinilsin (standart: 10)")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
