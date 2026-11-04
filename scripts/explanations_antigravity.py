"""Avtotest savollari izohlarining AI qoralamasini Antigravity (Gemini) orqali yaratiş.

API kaliti talab qilinmaydi: har bir savol uçun Antigravity CLI (``agy -p``) çaqiriladi va
sarf joriy tizimdagi Antigravity hisobi / tokenlaridan ketadi.

İşlatilişi:
    python scripts/explanations_antigravity.py run [--limit 20] [--bilet 42] [--workers 2] [--dry-run]

Natija ``projects/data/explanations/<sana>_antigravity_<vaqt>.json`` fayliga yozib boriladi.
Keyin: serverda ``manage.py import_explanations`` bilan bazaga yuklanadi.
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
TIMEOUT = 180  # bitta savol uçun maksimal vaqt (soniya)
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
5. Uchala tilda bir xil mazmun:
   - "uz": O'zbek tili (2026-yilgi yangi lotin alifbosi: sh->ş, ch->ç, g'->ğ, o'->ö harflari bilan yozilsin!);
   - "ru": Rus tili;
   - "en": Ingliz tili.
6. "confidence": berilgan javobni qoidaga to'liq va ishonchli bog'lay olsangiz "high", qisman asoslasangiz "medium", savol yoki variant noaniq tuyulsa "low".

Javobni FAQAT va FAQAT bitta toza JSON obyekti ko'rinishida bering (boshqa hech qanday so'z, izoh yoki matn qo'shmang):
{
  "uz": "O'zbekcha tushuntirish (ş, ç, ğ, ö harflari bilan)",
  "ru": "Русское объяснение",
  "en": "English explanation",
  "confidence": "high"
}"""


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


def _extract_json_response(raw_text):
    """Matn ichidan JSON obyektini xavfsiz ajratib olish."""
    if not raw_text:
        return None
    raw_text = raw_text.strip()
    # 1. To'g'ridan-to'g'ri JSON bo'lsa
    try:
        data = json.loads(raw_text)
        if isinstance(data, dict):
            return data
    except ValueError:
        pass

    # 2. ```json ... ``` blokidan izlash
    m = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", raw_text, re.I)
    if m:
        try:
            data = json.loads(m.group(1))
            if isinstance(data, dict):
                return data
        except ValueError:
            pass

    # 3. Eng birinchi { va eng oxirgi } orasidan izlash
    first = raw_text.find("{")
    last = raw_text.rfind("}")
    if first != -1 and last != -1 and last > first:
        try:
            data = json.loads(raw_text[first:last + 1])
            if isinstance(data, dict):
                return data
        except ValueError:
            pass
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


def _build_prompt(q):
    """Savol uchun Antigravity CLI ga beriladigan to'liq prompt."""
    options = []
    for ltr in ("a", "b", "c", "d"):
        val = q.get(f"javob_{ltr}")
        if val:
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

    body = (
        f"{image_part}"
        f"Savol ({q['bilet']}-bilet, {q['raqam']}-savol): {q['savol']}\n\n"
        f"Variantlar:\n{opts_str}\n\n"
        f"To'g'ri javob: {q['javob']}\n\n"
        "Talablarga binoan FAQAT bitta JSON obyekti qaytaring."
    )
    return f"{SYSTEM_PROMPT}\n\n---\n\n{body}"


def _ask_agy(agy_exe, q):
    """Antigravity CLI orqali bitta savol izohini olish."""
    prompt = _build_prompt(q)
    cmd = [agy_exe, "-p", prompt, "--output-format", "json"]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=TIMEOUT,
        cwd=ROOT,
    )

    if proc.returncode != 0 and not proc.stdout:
        err = proc.stderr.strip() or f"exit code {proc.returncode}"
        raise RuntimeError(f"agy xatosi: {err}")

    # agy natijasi: {"status": "SUCCESS", "response": "..."}
    outer_json = None
    try:
        outer_json = json.loads(proc.stdout)
    except ValueError:
        # Boshqa matn bo'lsa, oxirgi qatorlardan izlash
        for line in reversed(proc.stdout.splitlines()):
            line = line.strip()
            if line.startswith("{"):
                try:
                    outer_json = json.loads(line)
                    break
                except ValueError:
                    pass

    if not outer_json:
        raise RuntimeError("agy javobida JSON topilmadi")

    if outer_json.get("status") != "SUCCESS":
        err_msg = outer_json.get("error") or proc.stderr.strip() or "noma'lum xato"
        raise RuntimeError(f"agy muvaffaqiyatsiz: {err_msg}")

    response_text = outer_json.get("response") or ""
    item_data = _extract_json_response(response_text)
    if not item_data:
        raise RuntimeError(f"Model javobidan izoh JSON ajratib olinmadi: {response_text[:150]}")

    for k in ("uz", "ru", "en"):
        if not item_data.get(k):
            raise RuntimeError(f"JSON'da '{k}' maydoni yetishmaydi")

    conf = str(item_data.get("confidence", "high")).lower()
    if conf not in ("high", "medium", "low"):
        conf = "high"

    # 2026-yilgi imlo qoidasini kafolatlash
    uz_text = _clean_2026_uzbek(item_data["uz"].strip())

    return {
        "uz": uz_text,
        "ru": item_data["ru"].strip(),
        "en": item_data["en"].strip(),
        "confidence": conf,
    }


def _run_worker(agy_exe, q, lock, save_fn, progress):
    """Bitta savolni qayta ishlash va xatolik yuz bersa yozib qo'yish."""
    label = f"{q['bilet']}-bilet {q['raqam']}-savol"
    try:
        res = _ask_agy(agy_exe, q)
        save_fn({"id": _cid(q), **res})
        with lock:
            progress["n"] += 1
            print(f"[{progress['n']}/{progress['total']}] {label} ✓ ({res['confidence']})", flush=True)
        return True
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

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(_run_worker, agy_exe, q, lock, save, progress) for q in queue]
            for future in as_completed(futures):
                try:
                    future.result()
                except CancelledError:
                    pass
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
        print("\n⚠️ Hech qanday izoh olinmadi.")


def main():
    parser = argparse.ArgumentParser(description="Avtotest izohlari AI qoralamasi (Antigravity tokenlari orqali).")
    parser.add_argument("action", nargs="?", default="run", choices=["run"], help="Harakat (standart: run)")
    parser.add_argument("--limit", type=int, default=0, help="Nechta savol ishlanishi (0 — barchasi)")
    parser.add_argument("--bilet", type=int, help="Faqat ko'rsatilgan bilet savollari")
    parser.add_argument("--workers", type=int, default=2, help="Bir vaqtda ishlaydigan so'rovlar soni (standart: 2)")
    parser.add_argument("--redo", action="store_true", help="Izohi bor savollarni ham qayta ishlash")
    parser.add_argument("--dry-run", action="store_true", help="Haqiqiy so'rov yubormasdan savol va promptni ko'rish")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()

