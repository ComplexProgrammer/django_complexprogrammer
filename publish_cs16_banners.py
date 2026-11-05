#!/usr/bin/env python
"""CS 1.6 turkumi (pricel, FPS, headshot) maqolalariga yangi generatsiya qilingan
banner rasmlarini biriktiriş va serverda qöllaş skripti.

Maqolalar va rasmlar:
  1. /blog/cs-16-pricel-sozlamalari/   -> post/images/cs16_pricel_sozlamalari.jpg
  2. /blog/cs-16-fps-oshirish/          -> post/images/cs16_fps_oshirish.jpg
  3. /blog/cs-16-headshot-sozlamalari/  -> post/images/cs16_headshot_sozlamalari.jpg

Işlatiş:
    python publish_cs16_banners.py             # Bazadagi rasmlarni yangilaş
    python publish_cs16_banners.py --dry-run   # Bazaga yozmasdan tekşiriş
    python publish_cs16_banners.py --status    # Hozirgi holatni köriş
"""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
import sys

# Server (CloudLinux / cPanel) xotira va thread limitlarini saqlaş
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / "db.sqlite3"

BANNERS = [
    {
        "slug": "cs-16-pricel-sozlamalari",
        "title": "CS 1.6 pricel (crosshair) sozlamalari",
        "image_rel": "post/images/cs16_pricel_sozlamalari.jpg",
    },
    {
        "slug": "cs-16-fps-oshirish",
        "title": "CS 1.6 da FPS oşiriş",
        "image_rel": "post/images/cs16_fps_oshirish.jpg",
    },
    {
        "slug": "cs-16-headshot-sozlamalari",
        "title": "CS 1.6 headshot va tarmoq sozlamalari",
        "image_rel": "post/images/cs16_headshot_sozlamalari.jpg",
    },
]


def try_init_django():
    """Django muhitini yuklashga urinish. Agar topilmasa, SQLite3 rejimiga o'tiladi."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_complexprogrammer.settings")
    try:
        import django
        django.setup()
        return True
    except Exception:
        return False


def show_status(use_django=False):
    print("=" * 68)
    print("  CS 1.6 MAQOLALARINING HOZIRGI HOLATI VA RASMLARI")
    print("=" * 68)

    db_images = {}
    if use_django:
        from blog.models import Posts
        for item in BANNERS:
            p = Posts.objects.filter(slug=item["slug"]).first()
            if p:
                db_images[item["slug"]] = str(p.image or "")
    else:
        if DB_PATH.is_file():
            conn = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
            cur = conn.cursor()
            for item in BANNERS:
                cur.execute("SELECT image FROM blog_posts WHERE slug = ?", (item["slug"],))
                row = cur.fetchone()
                if row:
                    db_images[item["slug"]] = row[0] or ""
            conn.close()

    for item in BANNERS:
        slug = item["slug"]
        file_path = ROOT_DIR / "media" / item["image_rel"]
        file_exists = file_path.is_file()

        print(f"\n📄 Maqola: {item['title']}")
        print(f"   Manzil:   https://complexprogrammer.uz/blog/{slug}/")
        if slug in db_images:
            print(f"   Bazada:   {db_images[slug] or '(böş)'}")
        else:
            print("   Bazada:   ⚠️ Maqola topilmadi!")

        status_icon = "✅ Mavjud" if file_exists else "❌ Fayl topilmadi"
        print(f"   Faylda:   media/{item['image_rel']} ({status_icon})")


def apply_banners_django(dry_run=False):
    from django.core.cache import cache
    from blog.models import Posts

    updated_count = 0
    missing_files = []

    for item in BANNERS:
        slug = item["slug"]
        image_rel = item["image_rel"]
        full_path = ROOT_DIR / "media" / image_rel

        if not full_path.is_file():
            missing_files.append(image_rel)
            print(f"⚠️ DIQQAT: media/{image_rel} fayli topilmadi!")

        post = Posts.objects.filter(slug=slug).first()
        if not post:
            print(f"❌ Xatolik: /blog/{slug}/ maqolasi bazadan topilmadi!")
            continue

        old_img = str(post.image or "")
        print(f"\n🎯 Maqola: {item['title']} (/blog/{slug}/)")
        print(f"   Eski rasm: {old_img or '(biriktirilmagan)'}")
        print(f"   Yangi rasm: {image_rel}")

        if dry_run:
            print("   [DRY-RUN] Baza yangilanmadi.")
            continue

        if old_img == image_rel:
            print("   ℹ️ Bu rasm allaqaçon biriktirilgan.")
        else:
            post.image = image_rel
            post.save(update_fields=["image", "updated_at"])
            print("   ✅ Baza muvaffaqiyatli yangilandi!")
            updated_count += 1

    if not dry_run:
        try:
            cache.clear()
            print("\n🧹 Django keş xotirasi tozalandi.")
        except Exception as e:
            print(f"⚠️ Keş tozalana olmadi: {e}")

    return updated_count, missing_files


def apply_banners_sqlite(dry_run=False):
    if not DB_PATH.is_file():
        sys.exit(f"❌ Xatolik: Baza fayli topilmadi: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    updated_count = 0
    missing_files = []

    for item in BANNERS:
        slug = item["slug"]
        image_rel = item["image_rel"]
        full_path = ROOT_DIR / "media" / image_rel

        if not full_path.is_file():
            missing_files.append(image_rel)
            print(f"⚠️ DIQQAT: media/{image_rel} fayli topilmadi!")

        cur.execute("SELECT id, image FROM blog_posts WHERE slug = ?", (slug,))
        row = cur.fetchone()
        if not row:
            print(f"❌ Xatolik: /blog/{slug}/ maqolasi bazadan topilmadi!")
            continue

        post_id, old_img = row[0], row[1] or ""
        print(f"\n🎯 Maqola: {item['title']} (/blog/{slug}/)")
        print(f"   Eski rasm: {old_img or '(biriktirilmagan)'}")
        print(f"   Yangi rasm: {image_rel}")

        if dry_run:
            print("   [DRY-RUN] Baza yangilanmadi.")
            continue

        if old_img == image_rel:
            print("   ℹ️ Bu rasm allaqaçon biriktirilgan.")
        else:
            now_iso = datetime.now(timezone.utc).isoformat()
            cur.execute("UPDATE blog_posts SET image = ?, updated_at = ? WHERE id = ?", (image_rel, now_iso, post_id))
            print("   ✅ Baza muvaffaqiyatli yangilandi!")
            updated_count += 1

    if not dry_run:
        conn.commit()
    conn.close()

    return updated_count, missing_files


def main():
    parser = argparse.ArgumentParser(description="CS 1.6 maqolalari bannerlarini yangilaş")
    parser.add_argument("--dry-run", action="store_true", help="Bazaga yozmasdan tekşiriş")
    parser.add_argument("--status", action="store_true", help="Hozirgi holatni körsatiş")
    args = parser.parse_args()

    use_django = try_init_django()

    if args.status:
        show_status(use_django=use_django)
        return

    print("=" * 68)
    print("  CS 1.6 MAQOLALARI UÇUN YANGI BANNERLARNI BIRIKTIRIŞ")
    if args.dry_run:
        print("  Holat: TEKŞIRUV REJIMI (DRY-RUN, bazaga tegilmaydi)")
    mode_text = "Django ORM" if use_django else "SQLite3 töğridan-töğri ulanış"
    print(f"  Rejim: {mode_text}")
    print("=" * 68)

    if use_django:
        updated_count, missing_files = apply_banners_django(dry_run=args.dry_run)
    else:
        updated_count, missing_files = apply_banners_sqlite(dry_run=args.dry_run)

    if not args.dry_run:
        # Passenger qayta yuklanişi uçun restart.txt
        restart_file = ROOT_DIR / "tmp" / "restart.txt"
        if restart_file.parent.is_dir():
            try:
                restart_file.touch(exist_ok=True)
                print("\n🔄 tmp/restart.txt yangilandi (Passenger ilovasi qayta yuklanadi).")
            except Exception as e:
                print(f"⚠️ restart.txt yangilanmadi: {e}")

        print(f"\n✨ Yakunlandi! Jami {updated_count} ta maqola rasmi yangilandi.")
        if missing_files:
            print("⚠️ Eslatma: Serverga quyidagi rasm fayllarini ham yuklaşni unutmang:")
            for mf in missing_files:
                print(f"   - media/{mf}")


if __name__ == "__main__":
    main()
