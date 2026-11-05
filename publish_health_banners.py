#!/usr/bin/env python
"""Salomatlik rukni (categorie_id=6, 1-4 sahifalar) maqolalari bannerlarini
serverda xavfsiz va tizimli almashtiriş skripti.

DIQQAT (TALAB): BAZAGA HEÇ QANDAY ÖZGARİŞ KIRITILMAYDI (Zero-DB change)!
Ma'lumotlar bazasidagi mavjud rasm yöllari özgarmagan holda, diskdagi fayllar
(media/post/images papkasida) sifatli yangi bannerlar bilan yangilanadi.

1-4 sahifalardagi 31 ta maqola:
  1. [1-sahifa] homiladorlarga-foydali-oziq-ovqat-mahsulotlari            -> media/post/images/31.png
  2. [1-sahifa] bolalarning-telefonlarga-qaramliligiga-qanday-kurashish-kerak -> media/post/images/30.png
  3. [1-sahifa] bolani-erta-uxlatishning-foydalari                         -> media/post/images/29.png
  4. [1-sahifa] nega-bola-tirnogini-tishlaydi                             -> media/post/images/28.png
  5. [1-sahifa] bolada-tez-tez-shamollash-sabablari                       -> media/post/images/27.png
  6. [1-sahifa] bolaning-harorati-kotarilganda-nima-qilish-kerak          -> media/post/images/26.png
  7. [1-sahifa] bola-yotalganda-nima-qilish-kerak                         -> media/post/images/25.png
  8. [1-sahifa] uy-sharoitida-koz-atrofidagi-ajinlarni-kamaytirish        -> media/post/images/24.png
  9. [1-sahifa] bodom-yogi-bilan-yanada-gozallashing                      -> media/post/images/23.png
 10. [2-sahifa] har-kuni-boshni-yuvish-zararlimi                          -> media/post/images/22.png
 11. [2-sahifa] yosh-korinish-sirlari                                    -> media/post/images/21.png
 12. [2-sahifa] osh-sodasining-gozallik-va-salomatlik-uchun-foydasi       -> media/post/images/20.png
 13. [2-sahifa] aloening-foydali-xususiyatlari-gozallik-va-salomatlik...  -> media/post/images/19.png
 14. [2-sahifa] uy-sharoitida-kipriklarni-ostirish-usullari              -> media/post/images/18.png
 15. [2-sahifa] uy-sharoitida-tishlarni-oqartirishning-8-usuli            -> media/post/images/17.png
 16. [2-sahifa] quruq-yuz-terisini-parvarish-qilish-sirlari              -> media/post/images/16.png
 17. [2-sahifa] uy-sharoitida-tayyorlanadigan-limonli-niqoblar           -> media/post/images/15.png
 18. [2-sahifa] qorindagi-yogni-yoqotishning-eng-samarali-usullari        -> media/post/images/14.png
 19. [3-sahifa] yuz-terisini-yoshartirish-uchun-niqob-tayyorlash         -> media/post/images/13.png
 20. [3-sahifa] banan-postining-biz-bilmagan-foydalari                    -> media/post/images/12.png
 21. [3-sahifa] vitaminlar-yetishmovchiligi-va-ularning-ornini-toldirish  -> media/post/images/11.png
 22. [3-sahifa] uy-sharoitida-yotaldan-qutulish                          -> media/post/images/10.png
 23. [3-sahifa] bolalarda-gijja-kasalligi-alomatlari                     -> media/post/images/9.png
 24. [3-sahifa] bolani-ovqatlantirishda-tavsiyalar                       -> media/post/images/8.png
 25. [3-sahifa] bola-nutqini-rivojlantiruvchi-metodik-oyinlar            -> media/post/images/7.png
 26. [3-sahifa] sizga-glyutensiz-mahsulotlar-kerakmi-va-ularning-narxi   -> media/post/images/6.png
 27. [3-sahifa] anemiyani-davolash-uchun-necha-pul-ketadi                -> media/post/images/5.png
 28. [4-sahifa] jigar-uchun-dorilarning-arzon-analoglari-bormi           -> media/post/images/55b5c4cca480a5ccfb742e61e2da9317.png
 29. [4-sahifa] kozning-lazer-operatsiyasi-qancha-turadi                 -> media/post/images/4.png
 30. [4-sahifa] tishga-breket-qoyish-qancha-turadi                       -> media/post/images/3.png
 31. [4-sahifa] gemoglobinni-oshirish-uchun-qancha-xarajat-qilish-kerak  -> media/post/images/2.png

Işlatiş:
    python publish_health_banners.py             # Rasmlarni yangilaş (avtomatik zaxira olinadi)
    python publish_health_banners.py --dry-run   # Amallarni sinovdan ötkaziş (fayllarga tegilmaydi)
    python publish_health_banners.py --status    # Hozirgi mavjud fayllar va o'lchamlarni tekşiriş
    python publish_health_banners.py --backup    # Faqat mavjud fayllardan zaxira oliş
    python publish_health_banners.py --restore <TIMESTAMP> # Zaxiradan avvalgi holatga qaytariş
"""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys

# Server (CloudLinux / cPanel) resurs va thread limitlari
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

ROOT_DIR = Path(__file__).resolve().parent
MEDIA_DIR = ROOT_DIR / "media"
POST_IMG_DIR = MEDIA_DIR / "post" / "images"
STAGED_DIR = MEDIA_DIR / "post" / "staged_health_banners"
BACKUP_BASE_DIR = MEDIA_DIR / "post" / "backups" / "health"

# Salomatlik ruknidagi 31 ta maqolaning to'liq ro'yxati
HEALTH_ARTICLES = [
    {
        "page": 1,
        "slug": "homiladorlarga-foydali-oziq-ovqat-mahsulotlari",
        "title": "Homiladorlarga foydali oziq-ovqat mahsulotlari",
        "file": "31.png",
    },
    {
        "page": 1,
        "slug": "bolalarning-telefonlarga-qaramliligiga-qanday-kurashish-kerak",
        "title": "Bolalarning telefonlarga qaramliligiga qanday kuraşiş kerak?",
        "file": "30.png",
    },
    {
        "page": 1,
        "slug": "bolani-erta-uxlatishning-foydalari",
        "title": "Bolani erta uxlatişning foydalari",
        "file": "29.png",
    },
    {
        "page": 1,
        "slug": "nega-bola-tirnogini-tishlaydi",
        "title": "Nega bola tirnoğini tişlaydi?",
        "file": "28.png",
    },
    {
        "page": 1,
        "slug": "bolada-tez-tez-shamollash-sabablari",
        "title": "Bolada tez-tez şamollaş sabablari",
        "file": "27.png",
    },
    {
        "page": 1,
        "slug": "bolaning-harorati-kotarilganda-nima-qilish-kerak",
        "title": "Bolaning harorati kötarilganda nima qiliş kerak?",
        "file": "26.png",
    },
    {
        "page": 1,
        "slug": "bola-yotalganda-nima-qilish-kerak",
        "title": "Bola yötalganda nima qiliş kerak?",
        "file": "25.png",
    },
    {
        "page": 1,
        "slug": "uy-sharoitida-koz-atrofidagi-ajinlarni-kamaytirish",
        "title": "Uy şaroitida köz atrofidagi ajinlarni kamaytiriş",
        "file": "24.png",
    },
    {
        "page": 1,
        "slug": "bodom-yogi-bilan-yanada-gozallashing",
        "title": "Bodom yoği bilan yanada gözallaşing",
        "file": "23.png",
    },
    {
        "page": 2,
        "slug": "har-kuni-boshni-yuvish-zararlimi",
        "title": "Har kuni boşni yuviş zararlimi?",
        "file": "22.png",
    },
    {
        "page": 2,
        "slug": "yosh-korinish-sirlari",
        "title": "Yoş köriniş sirlari",
        "file": "21.png",
    },
    {
        "page": 2,
        "slug": "osh-sodasining-gozallik-va-salomatlik-uchun-foydasi",
        "title": "Oş sodasining gözallik va salomatlik uçun foydasi",
        "file": "20.png",
    },
    {
        "page": 2,
        "slug": "aloening-foydali-xususiyatlari-gozallik-va-salomatlik-uchun-retseptlar",
        "title": "Aloening foydali xususiyatlari - gözallik va salomatlik uçun retseptlar",
        "file": "19.png",
    },
    {
        "page": 2,
        "slug": "uy-sharoitida-kipriklarni-ostirish-usullari",
        "title": "Uy şaroitida kipriklarni östiriş usullari",
        "file": "18.png",
    },
    {
        "page": 2,
        "slug": "uy-sharoitida-tishlarni-oqartirishning-8-usuli",
        "title": "Uy şaroitida tişlarni oqartirişning 8 usuli",
        "file": "17.png",
    },
    {
        "page": 2,
        "slug": "quruq-yuz-terisini-parvarish-qilish-sirlari",
        "title": "Quruq yuz terisini parvariş qiliş sirlari",
        "file": "16.png",
    },
    {
        "page": 2,
        "slug": "uy-sharoitida-tayyorlanadigan-limonli-niqoblar",
        "title": "Uy şaroitida tayyorlanadigan limonli niqoblar",
        "file": "15.png",
    },
    {
        "page": 2,
        "slug": "qorindagi-yogni-yoqotishning-eng-samarali-usullari",
        "title": "Qorindagi yoğni yöqotişning eng samarali usullari",
        "file": "14.png",
    },
    {
        "page": 3,
        "slug": "yuz-terisini-yoshartirish-uchun-niqob-tayyorlash",
        "title": "Yuz terisini yoşartiriş uçun niqob tayyorlaş",
        "file": "13.png",
    },
    {
        "page": 3,
        "slug": "banan-postining-biz-bilmagan-foydalari",
        "title": "Banan pöstining biz bilmagan foydalari",
        "file": "12.png",
    },
    {
        "page": 3,
        "slug": "vitaminlar-yetishmovchiligi-va-ularning-ornini-toldirish-yollari",
        "title": "Vitaminlar yetişmovçiligi va ularning örnini töldiriş yöllari",
        "file": "11.png",
    },
    {
        "page": 3,
        "slug": "uy-sharoitida-yotaldan-qutulish",
        "title": "Uy şaroitida yötaldan qutuliş",
        "file": "10.png",
    },
    {
        "page": 3,
        "slug": "bolalarda-gijja-kasalligi-alomatlari",
        "title": "Bolalarda gijja kasalligi alomatlari",
        "file": "9.png",
    },
    {
        "page": 3,
        "slug": "bolani-ovqatlantirishda-tavsiyalar",
        "title": "Bolani ovqatlantirişda tavsiyalar",
        "file": "8.png",
    },
    {
        "page": 3,
        "slug": "bola-nutqini-rivojlantiruvchi-metodik-oyinlar",
        "title": "Bola nutqini rivojlantiruvçi metodik öyinlar",
        "file": "7.png",
    },
    {
        "page": 3,
        "slug": "sizga-glyutensiz-mahsulotlar-kerakmi-va-ularning-narxi-qancha",
        "title": "Sizga glyutensiz mahsulotlar kerakmi va ularning narxi qança?",
        "file": "6.png",
    },
    {
        "page": 3,
        "slug": "anemiyani-davolash-uchun-necha-pul-ketadi",
        "title": "Anemiyani davolaş uçun neça pul ketadi?",
        "file": "5.png",
    },
    {
        "page": 4,
        "slug": "jigar-uchun-dorilarning-arzon-analoglari-bormi",
        "title": "Jigar uçun dorilarning arzon analoglari bormi?",
        "file": "55b5c4cca480a5ccfb742e61e2da9317.png",
    },
    {
        "page": 4,
        "slug": "kozning-lazer-operatsiyasi-qancha-turadi",
        "title": "Közning lazer operatsiyasi qança turadi?",
        "file": "4.png",
    },
    {
        "page": 4,
        "slug": "tishga-breket-qoyish-qancha-turadi",
        "title": "Tişga breket qöyiş qança turadi?",
        "file": "3.png",
    },
    {
        "page": 4,
        "slug": "gemoglobinni-oshirish-uchun-qancha-xarajat-qilish-kerak",
        "title": "Gemoglobinni oşiriş uçun qança xarajat qiliş kerak?",
        "file": "2.png",
    },
]


def format_size(size_bytes):
    """Baytlarni KB yoki MB da chiroyli ko'rsatish."""
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    return f"{size_bytes / 1024:.1f} KB"


def show_status():
    """Hozirgi holatni ko'rsatish: mavjud fayllar va yangi tayyorlangan staged fayllar."""
    print("=" * 78)
    print("  SALOMATLIK RUKNI (1-4 SAHIFALAR) MAQOLALARI BANNERLARI HOLATI")
    print("=" * 78)

    by_page = {}
    for item in HEALTH_ARTICLES:
        by_page.setdefault(item["page"], []).append(item)

    for p_num in sorted(by_page.keys()):
        print(f"\n📑 {p_num}-SAHIFA (https://complexprogrammer.uz/blog/?categorie_id=6&page={p_num}):")
        print("-" * 78)
        for item in by_page[p_num]:
            target_path = POST_IMG_DIR / item["file"]
            staged_path = STAGED_DIR / item["file"]

            t_info = f"✅ Mavjud ({format_size(target_path.stat().st_size)})" if target_path.is_file() else "❌ Yo'q"
            s_info = f"🌟 Yangi tayyor ({format_size(staged_path.stat().st_size)})" if staged_path.is_file() else "❌ Tayyorlanmagan"

            print(f" • [/{item['slug']}/] {item['title'][:45]}...")
            print(f"    Fayl: media/post/images/{item['file']} -> {t_info} | Yangi: {s_info}")

    print("\n" + "=" * 78)
    print("🔒 BAZA HOLATI: BAZAGA HEÇ QANDAY ÖZGARİŞ KIRITILMAYDI (Zero-DB change).")
    print("=" * 78)


def create_backup():
    """Mavjud maqola rasmlaridan zaxira nusxa yaratish."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_BASE_DIR / ts
    backup_dir.mkdir(parents=True, exist_ok=True)

    backed_count = 0
    for item in HEALTH_ARTICLES:
        src_path = POST_IMG_DIR / item["file"]
        if src_path.is_file():
            shutil.copy2(src_path, backup_dir / item["file"])
            backed_count += 1

    print(f"💾 Zaxira nusxa saqlandi: {backup_dir} ({backed_count} ta fayl)")
    return backup_dir


def restore_backup(backup_name):
    """Zaxiradan avvalgi rasmlarni qaytarish."""
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
    for item in HEALTH_ARTICLES:
        backed_file = backup_dir / item["file"]
        target_path = POST_IMG_DIR / item["file"]
        if backed_file.is_file():
            shutil.copy2(backed_file, target_path)
            restored += 1
            print(f" ↩ Qaytarildi: {item['file']}")

    print(f"\n✅ Jami {restored} ta maqola rasmi zaxiradan muvaffaqiyatli tiklandi!")
    trigger_reload()
    return True


def trigger_reload():
    """Passenger/WSGI reload va Django keshini tozalash."""
    restart_txt = ROOT_DIR / "tmp" / "restart.txt"
    try:
        restart_txt.parent.mkdir(parents=True, exist_ok=True)
        restart_txt.touch()
        print("🔄 Server qayta yuklaniş signali yuborildi (tmp/restart.txt touch qilindi).")
    except Exception as exc:
        print(f"⚠️ tmp/restart.txt ga yozib bölmadi: {exc}")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        import django
        django.setup()
        from django.core.cache import cache
        cache.clear()
        print("🧹 Django blog va sahifalar keshlari tozalandi (cache.clear).")
    except Exception:
        pass


def deploy_banners(dry_run=False):
    """Barcha 31 ta yangi staged bannerlarni nishon yo'llarga ko'chirish."""
    print("=" * 78)
    mode_str = "TEKŞIRUV REJIMI (DRY-RUN - fayllar özgarmaydi)" if dry_run else "AMALGA OŞIRIŞ REJIMI"
    print(f"  SALOMATLIK RUKNI BANNERLARINI JORIY ETİŞ: {mode_str}")
    print("  Qoida: BAZAGA TEGILMAYDI (Zero-DB change)")
    print("=" * 78)

    if not STAGED_DIR.is_dir():
        print(f"❌ Xatolik: Staging papkasi topilmadi: {STAGED_DIR}")
        sys.exit(1)

    missing = []
    for item in HEALTH_ARTICLES:
        staged_file = STAGED_DIR / item["file"]
        if not staged_file.is_file():
            missing.append(item["file"])

    if missing:
        print(f"❌ Xatolik: Quyidagi tayyorlangan fayllar topilmadi: {', '.join(missing)}")
        sys.exit(1)

    if not dry_run:
        create_backup()

    deployed_count = 0
    print("\n🚀 Fayllarni yangilaş (31 ta maqola):")
    print("-" * 78)
    for item in HEALTH_ARTICLES:
        src = STAGED_DIR / item["file"]
        dest = POST_IMG_DIR / item["file"]
        src_size = src.stat().st_size

        if dry_run:
            status_text = "[DRY-RUN KO'ÇIRILADI]"
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            status_text = "[MUVAFFAQ KO'ÇIRILDI]"

        deployed_count += 1
        print(f" ✅ {status_text} media/post/images/{item['file']} ({format_size(src_size)}) - [{item['title'][:35]}...]")

    print("-" * 78)
    print(f"🎉 Jami: {deployed_count} ta maqola rasmi muvaffaqiyatli yangilandi!")

    if not dry_run:
        trigger_reload()
        print("\n✨ Salomatlik ruknidagi barcha 1-4 sahifalar maqolalari bannerlari yangilandi!")


def main():
    parser = argparse.ArgumentParser(
        description="Salomatlik rukni (1-4 sahifalar) maqolalari bannerlarini serverda yangilaş."
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Hozirgi mavjud va yangi tayyorlangan rasmlar holatini körsatiş",
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
