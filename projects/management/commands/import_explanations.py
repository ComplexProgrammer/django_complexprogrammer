"""Lokalda yaratilgan AI izoh qoralamalarini bazaga yoziş.

    python manage.py import_explanations            # projects/data/explanations/ dagi yangi fayllar
    python manage.py import_explanations --force    # import qilinganlarini ham qayta yozish
    python manage.py import_explanations --file projects/data/explanations/2026-11-04_msgbatch_x.json

Fayllar ``scripts/explanations_local.py collect`` bilan lokal kompyuterda yaratiladi va git orqali keladi —
serverda API kaliti kerak emas. ``git_push.sh`` GitHub'dan yangi fayl kelganda buni avtomatik çaqiradi.
Qaysi fayl import qilingani ``tmp/explanations_imported.json`` da saqlanadi (admin qöl bilan tahrirlagan qoralama
keyingi deploy'da qayta yozilib ketmasin). Tasdiqlangan izohlarga hečqačon tegilmaydi.
"""

import hashlib
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from projects.explanation_prompts import RESULTS_DIR, parse_custom_id
from projects.explanation_store import save_draft, sync_avtotest

DONE_FILE = Path(settings.BASE_DIR) / "tmp" / "explanations_imported.json"


def _done():
    try:
        return json.loads(DONE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


class Command(BaseCommand):
    help = "projects/data/explanations/*.json dagi AI izoh qoralamalarini bazaga yozadi (draft holatida)."

    def add_arguments(self, parser):
        parser.add_argument("--file", help="Faqat şu fayl")
        parser.add_argument("--force", action="store_true", help="Oldin import qilingan fayllarni ham qayta yozish")

    def handle(self, *args, **opts):
        if opts["file"]:
            files = [Path(opts["file"])]
            if not files[0].is_file():
                raise CommandError(f"Fayl topilmadi: {files[0]}")
        else:
            files = sorted(RESULTS_DIR.glob("*.json"))
        done = _done()
        saved = skipped = imported = 0
        for path in files:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if not opts["force"] and done.get(path.name) == digest:
                continue
            try:
                items = json.loads(path.read_text(encoding="utf-8"))["items"]
            except (ValueError, KeyError) as e:
                self.stderr.write(f"{path.name}: öqib bölmadi ({e}) — ötkazib yuborildi.")
                continue
            file_saved = 0
            for item in items:
                try:
                    kind, key = parse_custom_id(item["id"])
                except (KeyError, ValueError):
                    skipped += 1
                    continue
                if save_draft(kind, key, item):
                    file_saved += 1
                else:
                    skipped += 1  # savol topilmadi, izoh böş yoki admin allaqačon tasdiqlagan
            saved += file_saved
            imported += 1
            done[path.name] = digest
            self.stdout.write(f"{path.name}: {file_saved}/{len(items)} ta qoralama saqlandi.")
        if not imported:
            self.stdout.write("Yangi izoh fayli yöq.")
            return
        sync_avtotest()
        DONE_FILE.parent.mkdir(parents=True, exist_ok=True)
        DONE_FILE.write_text(json.dumps(done, indent=1), encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(
            f"{imported} ta fayl: {saved} ta qoralama saqlandi, {skipped} tasi ötkazib yuborildi. "
            "Admin → Tests → Questions → filtr «Qoralama» orqali tekşirib, tasdiqlang."
        ))
