import json
import urllib.request

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from driving import yhq


class Command(BaseCommand):
    help = "Yöl harakati qoidalari matnini lex.uz'dan olib, driving/data/yhq_<til>.json ga yozadi (qoidalar özgarganda)."

    def add_arguments(self, parser):
        parser.add_argument("--lang", default="uz", choices=yhq.LANGS, help="Matn tili: uz (asosiy) yoki ru")
        parser.add_argument("--file", help="lex.uz sahifasi oldindan yuklab olingan bo'lsa — HTML fayl yo'li")

    def handle(self, *args, **opts):
        if opts["file"]:
            page = open(opts["file"], encoding="utf-8", errors="ignore").read()
        else:
            request = urllib.request.Request(yhq.SOURCE_URLS[opts["lang"]], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=90) as response:
                page = response.read().decode("utf-8", errors="ignore")
        data = yhq.parse(page)
        points = sum(len(c["points"]) for c in data["chapters"])
        if len(data["chapters"]) < 25 or points < 150:
            raise CommandError(f"Sahifa tuzilishi o'zgargan ko'rinadi: {len(data['chapters'])} bob, {points} band — fayl yozilmadi.")
        data.update(source=yhq.SOURCE_URLS[opts["lang"]], fetched=timezone.localdate().isoformat())
        yhq.DATA_DIR.mkdir(exist_ok=True)
        path = yhq.DATA_DIR / f"yhq_{opts['lang']}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"{path}: {len(data['chapters'])} bob, {points} band, {len(data['signs'])} belgi."))
