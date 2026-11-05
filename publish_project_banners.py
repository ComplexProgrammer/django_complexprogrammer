#!/usr/bin/env python
"""Loyihalar (/projects/) va ularga mos blog maqolalari bannerlarini serverda
fayl tizimi orqali xavfsiz almashtiriş skripti.

DIQQAT (TALAB): BAZAGA HEÇ QANDAY ÖZGARİŞ KIRITILMAYDI (Zero-DB change)!
Ma'lumotlar bazasidagi rasm yöllari özgarmagan holda, fayllarning özi diskda
(media/projects/images va media/post/images papkalarida) yangilanadi.

Loyiha bannerlari (16 ta faol loyiha):
  1. tests                -> media/projects/images/test.png
  2. avtotest             -> media/projects/images/avtotest.png
  3. tests?topic_id=1     -> media/projects/images/maxresdefault.jpg
  4. tests/?type_id=2     -> media/projects/images/img.png
  5. tests/?type_id=3     -> media/projects/images/img.jpg
  6. password_generator   -> media/projects/images/password-generator.png
  7. pdf_tools            -> media/projects/images/0b0040d43c285926eb01.png
  8. market               -> media/projects/images/photo_5388719227059423968_y.jpg
  9. ip                   -> media/projects/images/ipfinder.png
  10. changetext          -> media/projects/images/changetext.jpg
  11. exchangerates       -> media/projects/images/exchangerates.png
  12. imagecompare        -> media/projects/images/imagecompare.png
  13. translate           -> media/projects/images/translate.jpg
  14. coins               -> media/projects/images/btc.png
  15. youtube_downloader  -> media/projects/images/youtube.png
  16. sitemap             -> media/projects/images/sitemap.png

Mos blog maqolalari (post/images/):
  - avtotest maqolasi (PNG) -> media/post/images/avtotest.png
  - avtotest maqolasi (JPG) -> media/post/images/avtotest.jpg
  - changetext maqolasi     -> media/post/images/lotin_kirill_ogirgich.jpg

Işlatiş:
    python publish_project_banners.py             # Rasmlarni yangilaş (avtomatik zaxira olinadi)
    python publish_project_banners.py --dry-run   # Amallarni sinovdan ötkaziş (fayllarga tegilmaydi)
    python publish_project_banners.py --status    # Hozirgi fayllar va holatni tekşiriş
    python publish_project_banners.py --backup    # Faqat mavjud fayllardan zaxira oliş
    python publish_project_banners.py --restore <TIMESTAMP> # Zaxiradan qaytariş
"""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sqlite3
import sys

# Server (CloudLinux / cPanel) resurs va thread limitlari
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

ROOT_DIR = Path(__file__).resolve().parent
MEDIA_DIR = ROOT_DIR / "media"
STAGED_DIR = MEDIA_DIR / "projects" / "staged_banners"
PROJECTS_IMG_DIR = MEDIA_DIR / "projects" / "images"
POST_IMG_DIR = MEDIA_DIR / "post" / "images"
BACKUP_BASE_DIR = MEDIA_DIR / "projects" / "backups"
DB_PATH = ROOT_DIR / "db.sqlite3"

# 16 ta faol loyihaning rasm xaritasi
PROJECT_BANNERS = [
    {
        "url": "tests",
        "title": "Barça testlar (Universal test platformasi)",
        "source": "test.png",
        "target_rel": "projects/images/test.png",
    },
    {
        "url": "avtotest",
        "title": "Avtotest 2026 (Haydovçilik guvohnomasi)",
        "source": "avtotest.png",
        "target_rel": "projects/images/avtotest.png",
    },
    {
        "url": "tests?topic_id=1",
        "title": "Umumiy bilim (Intellektual viktorina)",
        "source": "maxresdefault.jpg",
        "target_rel": "projects/images/maxresdefault.jpg",
    },
    {
        "url": "tests/?type_id=2",
        "title": "Maktab testlari (DTM va maktab fanlari)",
        "source": "img.png",
        "target_rel": "projects/images/img.png",
    },
    {
        "url": "tests/?type_id=3",
        "title": "Avtotest: qöşimça savollar (Amaliy vaziyatlar)",
        "source": "img.jpg",
        "target_rel": "projects/images/img.jpg",
    },
    {
        "url": "password_generator",
        "title": "Parol generatori (Kiberxavfsizlik)",
        "source": "password-generator.png",
        "target_rel": "projects/images/password-generator.png",
    },
    {
        "url": "pdf_tools",
        "title": "PDF vositalar (Konvertatsiya va birlashtirish)",
        "source": "0b0040d43c285926eb01.png",
        "target_rel": "projects/images/0b0040d43c285926eb01.png",
    },
    {
        "url": "market",
        "title": "Kripto bozorlar (Treyding tahlil va grafiklar)",
        "source": "photo_5388719227059423968_y.jpg",
        "target_rel": "projects/images/photo_5388719227059423968_y.jpg",
    },
    {
        "url": "ip",
        "title": "IP manzil (Geolokatsiya va tarmoq ma'lumoti)",
        "source": "ipfinder.png",
        "target_rel": "projects/images/ipfinder.png",
    },
    {
        "url": "changetext",
        "title": "Lotin ↔ Kirill (2026 yangi alifbo ögirgiçi)",
        "source": "changetext.jpg",
        "target_rel": "projects/images/changetext.jpg",
    },
    {
        "url": "exchangerates",
        "title": "Valyuta kurslari (Markaziy bank va konvertor)",
        "source": "exchangerates.png",
        "target_rel": "projects/images/exchangerates.png",
    },
    {
        "url": "imagecompare",
        "title": "Rasm soliştiriş (Vizual taqqoslaş)",
        "source": "imagecompare.png",
        "target_rel": "projects/images/imagecompare.png",
    },
    {
        "url": "translate",
        "title": "Tarjimon (Köptilli AI tarjima)",
        "source": "translate.jpg",
        "target_rel": "projects/images/translate.jpg",
    },
    {
        "url": "coins",
        "title": "Kripto narxlar (Bitcoin, Ethereum, USDT)",
        "source": "btc.png",
        "target_rel": "projects/images/btc.png",
    },
    {
        "url": "youtube_downloader",
        "title": "YouTube yuklovçi (Video va audio)",
        "source": "youtube.png",
        "target_rel": "projects/images/youtube.png",
    },
    {
        "url": "sitemap",
        "title": "Sitemap generator (XML sitemap va SEO)",
        "source": "sitemap.png",
        "target_rel": "projects/images/sitemap.png",
    },
]

# Loyihalarga mos blog maqolalari rasmlari
MATCHING_POST_BANNERS = [
    {
        "slug": "avto-test",
        "title": "Avtotest: Avtomaktab imtihonlari biletlari",
        "source": "avtotest.png",
        "target_rel": "post/images/avtotest.png",
    },
    {
        "slug": "ozbekistondagi-avtotestlar-2024-yangiliklar-va-ozgarishlar",
        "title": "Özbekistonda avtotest tizimi yangiliklari",
        "source": "avtotest.jpg",
        "target_rel": "post/images/avtotest.jpg",
    },
    {
        "slug": "lotin-kirill-ogirgich-changetext",
        "title": "Lotin-Kirill ögirgiç va alifbo islohoti",
        "source": "lotin_kirill_ogirgich.jpg",
        "target_rel": "post/images/lotin_kirill_ogirgich.jpg",
    },
]

ALL_DEPLOY_ITEMS = PROJECT_BANNERS + MATCHING_POST_BANNERS


def format_size(size_bytes):
    """Baytlarni KB yoki MB da chiroyli chiqarish."""
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    return f"{size_bytes / 1024:.1f} KB"


def show_status():
    """Hozirgi holatni ko'rsatish: mavjud fayllar, staged fayllar va o'lchamlar."""
    print("=" * 76)
    print("  LOYIHALAR VA MAQOLALAR BANNERLARINING HOZIRGI HOLATI")
    print("=" * 76)

    print("\n📦 1. 16 TA FAOL LOYIHA BANNERLARI (media/projects/images/):")
    print("-" * 76)
    for idx, item in enumerate(PROJECT_BANNERS, 1):
        target_path = MEDIA_DIR / item["target_rel"]
        staged_path = STAGED_DIR / item["source"]

        target_info = "❌ Mavjud emas"
        if target_path.is_file():
            target_info = f"✅ Mavjud ({format_size(target_path.stat().st_size)})"

        staged_info = "❌ Tayyorlanmagan"
        if staged_path.is_file():
            staged_info = f"🌟 Yangi tayyor ({format_size(staged_path.stat().st_size)})"

        print(f" {idx:2d}. [{item['url']}] {item['title']}")
        print(f"     Nışon:    media/{item['target_rel']} -> {target_info}")
        print(f"     Staged:   media/projects/staged_banners/{item['source']} -> {staged_info}")

    print("\n📄 2. MOS BLOG MAQOLALARI BANNERLARI (media/post/images/):")
    print("-" * 76)
    for idx, item in enumerate(MATCHING_POST_BANNERS, 1):
        target_path = MEDIA_DIR / item["target_rel"]
        staged_path = STAGED_DIR / item["source"]

        target_info = "❌ Mavjud emas"
        if target_path.is_file():
            target_info = f"✅ Mavjud ({format_size(target_path.stat().st_size)})"

        staged_info = "❌ Tayyorlanmagan"
        if staged_path.is_file():
            staged_info = f"🌟 Yangi tayyor ({format_size(staged_path.stat().st_size)})"

        print(f" {idx:2d}. [blog/{item['slug']}] {item['title']}")
        print(f"     Nışon:    media/{item['target_rel']} -> {target_info}")
        print(f"     Staged:   media/projects/staged_banners/{item['source']} -> {staged_info}")

    print("\n" + "=" * 76)
    print("🔒 BAZA HOLATI: BAZAGA HEÇ QANDAY ÖZGARİŞ KIRITILMAYDI (Zero-DB change).")
    print("=" * 76)


def create_backup():
    """Mavjud barcha nishon rasmlaridan zaxira nusxa yaratish."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_BASE_DIR / ts
    backup_dir.mkdir(parents=True, exist_ok=True)

    backed_up_count = 0
    for item in ALL_DEPLOY_ITEMS:
        target_path = MEDIA_DIR / item["target_rel"]
        if target_path.is_file():
            rel_dest = backup_dir / item["target_rel"]
            rel_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_path, rel_dest)
            backed_up_count += 1

    print(f"💾 Zaxira nusxa yaratildi: {backup_dir} ({backed_up_count} ta fayl)")
    return backup_dir


def restore_backup(backup_name):
    """Zaxira papkasidan avvalgi holatga qaytarish."""
    backup_dir = BACKUP_BASE_DIR / backup_name
    if not backup_dir.is_dir():
        print(f"❌ Xatolik: Zaxira papkasi topilmadi: {backup_dir}")
        print("\nMavjud zaxiralar:")
        if BACKUP_BASE_DIR.is_dir():
            for d in sorted(BACKUP_BASE_DIR.iterdir()):
                if d.is_dir():
                    print(f"  - {d.name}")
        return False

    restored = 0
    for item in ALL_DEPLOY_ITEMS:
        backed_file = backup_dir / item["target_rel"]
        target_path = MEDIA_DIR / item["target_rel"]
        if backed_file.is_file():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backed_file, target_path)
            restored += 1
            print(f" ↩ Qaytarildi: {item['target_rel']}")

    print(f"\n✅ Jami {restored} ta fayl zaxiradan tiklandi!")
    trigger_reload()
    return True


def trigger_reload():
    """Passenger/WSGI reload va keshni tozalash."""
    restart_txt = ROOT_DIR / "tmp" / "restart.txt"
    try:
        restart_txt.parent.mkdir(parents=True, exist_ok=True)
        restart_txt.touch()
        print("🔄 Server qayta yuklaniş signali yuborildi (tmp/restart.txt touch qilindi).")
    except Exception as exc:
        print(f"⚠️ tmp/restart.txt ga yozib bölmadi: {exc}")

    # Django keshi mavjud bo'lsa tozalash
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        import django
        django.setup()
        from django.core.cache import cache
        cache.clear()
        print("🧹 Django sahifa va API keshlari tozalandi (cache.clear).")
    except Exception:
        # Django muhiti yuklanmasa ham muhim emas, fayllar allaqachon almashtirilgan
        pass


def deploy_banners(dry_run=False):
    """Barcha tayyorlangan staged bannerlarni nishon yo'llarga ko'chirish."""
    print("=" * 76)
    mode_str = "TEKŞIRUV REJIMI (DRY-RUN - fayllar özgarmaydi)" if dry_run else "AMALGA OŞIRIŞ REJIMI"
    print(f"  LOYIHA BANNERLARINI SERVERGA JORIY ETİŞ: {mode_str}")
    print("  Qoida: BAZAGA TEGILMAYDI (Zero-DB change)")
    print("=" * 76)

    # Staged papkani tekshirish
    if not STAGED_DIR.is_dir():
        print(f"❌ Xatolik: Staging papkasi topilmadi: {STAGED_DIR}")
        sys.exit(1)

    missing_staged = []
    for item in ALL_DEPLOY_ITEMS:
        staged_file = STAGED_DIR / item["source"]
        if not staged_file.is_file():
            missing_staged.append(item["source"])

    if missing_staged:
        print(f"❌ Xatolik: Quyidagi staged fayllar topilmadi: {', '.join(missing_staged)}")
        sys.exit(1)

    if not dry_run:
        create_backup()

    deployed_count = 0
    print("\n🚀 Fayllarni yangilaş:")
    print("-" * 76)
    for item in ALL_DEPLOY_ITEMS:
        src = STAGED_DIR / item["source"]
        dest = MEDIA_DIR / item["target_rel"]
        src_size = src.stat().st_size

        if dry_run:
            status_text = "[DRY-RUN KO'ÇIRILADI]"
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            status_text = "[MUVAOFFAQ KO'ÇIRILDI]"

        deployed_count += 1
        print(f" ✅ {status_text} media/{item['target_rel']} ({format_size(src_size)})")

    print("-" * 76)
    print(f"🎉 Jami: {deployed_count} ta rasm fayli muvaffaqiyatli almashtirildi!")

    if not dry_run:
        trigger_reload()
        print("\n✨ Barcha loyihalar va maqolalar rasmlari yangilandi. Foydalanuvçilar yangi rasmlarni darhol köradilar!")


def main():
    parser = argparse.ArgumentParser(
        description="Loyiha va maqola bannerlarini serverda almashtiriş (bazaga tegilmaydi)."
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Hozirgi mavjud va tayyorlangan rasmlar holatini körsatiş",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fayllarni köçirmasdan sinovdan ötkaziş",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Faqat mavjud fayllardan zaxira oliş",
    )
    parser.add_argument(
        "--restore",
        metavar="TIMESTAMP",
        help="Belgilangan zaxiradan avvalgi holatga qaytariş",
    )

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.backup:
        create_backup()
    elif args.restore:
        restore_backup(args.restore)
    else:
        deploy_banners(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

