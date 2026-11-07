#!/usr/bin/env python3
"""
Complex Programmer (complexprogrammer.uz) loyihasi uçun generatsiya qilingan
yangi logotiplar, piktogrammalar (PWA 192/512, Apple Touch Icon, multi-size favicon.ico)
hamda OpenGraph brend-bannerlarini joriy qiliş skripti.

Işlatiş:
    python publish_logos.py                  # Standart: "knight" (Cyber-Knight C0mplex) uslubi
    python publish_logos.py --style monogram # Minimalist "<CP>" monogramma uslubi
    python publish_logos.py --dry-run        # Özgarişlarni tekşiriş (fayllarni yozmasdan)
"""

import argparse
import shutil
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


def cleanup_disk_bloat() -> None:
    """Hostingda disk kvotasini (Errno 122: Disk quota exceeded) töldirib qöyadigan
    ortiqça vaqtinçalik/dublikat papkalarni tozalaydi.
    """
    # 1. Eski zaxira papkalarini öçiriş (Git tarixida baribir saqlangan)
    backup_dirs = [
        BASE_DIR / "media" / "projects" / "backups",
        BASE_DIR / "media" / "post" / "backups",
        *STATIC_IMG_DIR.glob("backups_logos_*"),
        *(BASE_DIR / "media" / "projects" / "images").glob("backups_*"),
        *(BASE_DIR / "media" / "post" / "images").glob("backups_*"),
    ]
    for bdir in backup_dirs:
        if bdir.exists():
            shutil.rmtree(bdir, ignore_errors=True)

    # 2. staticfiles/ içidagi ortiqça collectstatic dublikatlarini tozalab, böş papka qoldiriş
    # (WHITENOISE_USE_FINDERS = True bölgani uçun staticfiles/ içida nusxa saqlaş şart emas,
    # lekin papkaning özi mavjud bölsa WhiteNoise UserWarning çiqarmaydi)
    staticfiles_dir = BASE_DIR / "staticfiles"
    if staticfiles_dir.exists():
        shutil.rmtree(staticfiles_dir, ignore_errors=True)
    try:
        staticfiles_dir.mkdir(exist_ok=True)
    except OSError:
        pass

    # 3. Fayl keşini (tmp/django_cache) tozalab joy böşatiş
    cache_dir = BASE_DIR / "tmp" / "django_cache"
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass


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
        "--backup",
        action="store_true",
        help="Alohida backups_logos_<vaqt> papkasiga zaxira nusxa oliş (sukut böyiça disk kvotasini tejaş uçun öçirilgan)",
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

    if not args.dry_run:
        cleanup_disk_bloat()
        print("🧹 Ortiqça vaqtinçalik fayllar (staticfiles, eski keş va zaxiralar) tozalandi.")

    backup_dir = None
    if args.backup and not args.dry_run:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = STATIC_IMG_DIR / f"backups_logos_{timestamp}"
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

        if backup_dir is not None and dst_path.exists():
            shutil.copy2(dst_path, backup_dir / dst_name)

        shutil.copy2(src_path, dst_path)
        print(f"  ✓ static/img/{dst_name:<22} ({size_kb:>6.1f} KB) — {desc}")
        applied += 1

    if args.dry_run:
        print("-" * 72)
        print(f"✅ Tekşiruv yakunlandi: {applied} ta fayl joriy qilişga tayyor.")
        return 0

    restart_txt = BASE_DIR / "tmp" / "restart.txt"
    try:
        restart_txt.parent.mkdir(parents=True, exist_ok=True)
        restart_txt.touch()
        print("🔄 Passenger serveri qayta işga tuşiriş belgisi yangilandi (tmp/restart.txt).")
    except OSError as exc:
        print(f"⚠ Eslatma: tmp/restart.txt yangilanmadi: {exc}")

    print("-" * 72)
    print(f"✅ Muvaffaqiyatli yakunlandi! Jami yangilangan fayllar: {applied} ta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
