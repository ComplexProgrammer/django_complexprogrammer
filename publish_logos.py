#!/usr/bin/env python3
"""
Complex Programmer (complexprogrammer.uz) loyihasi uçun generatsiya qilingan
yangi logotiplar, piktogrammalar (PWA 192/512, Apple Touch Icon, multi-size favicon.ico)
hamda OpenGraph brend-bannerlarini xavfsiz (zaxira nusxa bilan) joriy qiliş skripti.

Işlatiş:
    python publish_logos.py                  # Standart: "knight" (Cyber-Knight C0mplex) uslubi
    python publish_logos.py --style monogram # Minimalist "<CP>" monogramma uslubi
    python publish_logos.py --dry-run        # O'zgarişlarni tekşiriş (fayllarni yozmasdan)
"""

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_IMG_DIR = BASE_DIR / "static" / "img"
STAGED_DIR = STATIC_IMG_DIR / "staged_logos"


def get_targets(style: str, banner_as_c0mplex: bool) -> list[tuple[str, str, str]]:
    """(staged_filename, target_filename_in_static_img, description) röyxatini qaytaradi."""
    c0mplex_src = f"{style}_banner_686x400.png" if banner_as_c0mplex else f"{style}_icon_192.png"
    c0mplex_desc = (
        "Asosiy brend rasmi (686x400 gorizontal banner)"
        if banner_as_c0mplex
        else "Asosiy brend belgisi (192x192 kvadrat — navbar 28x28, PWA 192x192 va Apple Touch uçun)"
    )
    return [
        (c0mplex_src, "C0mplex.png", c0mplex_desc),
        (f"{style}_icon_512.png", "icon_512.png", "PWA 512x512 yuqori aniqlikdagi ilova piktogrammasi"),
        (f"{style}_favicon.ico", "favicon.ico", "Köpqatlamli (16x16, 32x32, 48x48) brauzer favikoni"),
        (f"{style}_apple_touch_180.png", "apple-touch-icon.png", "iOS / Safari uçun 180x180 piktogramma"),
        (f"{style}_og_banner_1200x630.png", "og_banner.png", "OpenGraph / ijtimoiy tarmoqlar uçun 1200x630 brend-banner"),
        (f"{style}_banner_686x400.png", "C0mplex_banner.png", "Gorizontal brend logotipi (686x400)"),
        ("logo_icon.svg", "logo.svg", "Vektorli (SVG) kvadrat logotip"),
        ("logo_banner.svg", "logo_banner.svg", "Vektorli (SVG) gorizontal brend-banner"),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="complexprogrammer.uz logotiplarini joriy qiliş skripti"
    )
    parser.add_argument(
        "--style",
        choices=["knight", "monogram"],
        default="knight",
        help="Logotip uslubi: 'knight' (Cyber-Knight C0mplex) yoki 'monogram' (<CP> Monogram)",
    )
    parser.add_argument(
        "--banner-as-c0mplex",
        action="store_true",
        help="C0mplex.png sifatida 192x192 kvadrat belgi örniga 686x400 gorizontal bannerni qöllaş",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Heç qanday faylni özgartirmasdan faqat tekşiriş",
    )
    args = parser.parse_args()

    print("=" * 72)
    print(f"🎨 Complex Programmer (complexprogrammer.uz) — Logotiplarni joriy qiliş")
    print(f"📌 Tanlangan uslub: {args.style.upper()}")
    print("=" * 72)

    if not STAGED_DIR.exists():
        print(f"✗ Xatolik: Staged logotiplar papkasi topilmadi: {STAGED_DIR}")
        return 1

    targets = get_targets(args.style, args.banner_as_c0mplex)
    missing = [src for src, _, _ in targets if not (STAGED_DIR / src).exists()]
    if missing:
        print(f"✗ Xatolik: Quyidagi tayyorlangan fayllar topilmadi: {', '.join(missing)}")
        return 1

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = STATIC_IMG_DIR / f"backups_logos_{timestamp}"

    if not args.dry_run:
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"📦 Eski logotiplar zaxira nusxasi: {backup_dir.relative_to(BASE_DIR)}")

    applied = 0
    for src_name, dst_name, desc in targets:
        src_path = STAGED_DIR / src_name
        dst_path = STATIC_IMG_DIR / dst_name
        size_kb = src_path.stat().st_size / 1024.0

        if args.dry_run:
            print(f"  [DRY-RUN] {src_name} ({size_kb:.1f} KB) ➔ static/img/{dst_name} — {desc}")
            applied += 1
            continue

        if dst_path.exists():
            shutil.copy2(dst_path, backup_dir / dst_name)

        shutil.copy2(src_path, dst_path)
        print(f"  ✓ static/img/{dst_name:<22} ({size_kb:>6.1f} KB) — {desc}")
        applied += 1

    if args.dry_run:
        print("-" * 72)
        print(f"✅ Tekşiruv yakunlandi: {applied} ta fayl joriy qilişga tayyor.")
        return 0

    # collectstatic (agar STATIC_ROOT sozlangan bölsa va server muhiti bölsa)
    manage_py = BASE_DIR / "manage.py"
    if manage_py.exists():
        try:
            subprocess.run(
                [sys.executable, str(manage_py), "shell", "-c", "from django.core.cache import cache; cache.clear()"],
                cwd=str(BASE_DIR),
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("🧹 Django keşi tozalandi.")
        except Exception:
            pass

    restart_txt = BASE_DIR / "tmp" / "restart.txt"
    try:
        restart_txt.parent.mkdir(parents=True, exist_ok=True)
        restart_txt.touch()
        print("🔄 Passenger serveri qayta işga tuşiriş belgisi yangilandi (tmp/restart.txt).")
    except Exception:
        pass

    print("-" * 72)
    print(f"✅ Muvaffaqiyatli yakunlandi! Jami yangilangan fayllar: {applied} ta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

