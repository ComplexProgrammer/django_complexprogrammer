#!/usr/bin/env python
"""Bazadagi barça özbekça matnlarni 2026-yilgi yangi lotin alifbosiga ötkaziş skripti.

Işlatiş:
    python migrate_db_to_2026.py           # Tekşiriş (Dry-run: bazaga tegilmaydi)
    python migrate_db_to_2026.py --dry-run # Tekşiriş
    python migrate_db_to_2026.py --apply   # Haqiqatda bazaga saqlaş
    python migrate_db_to_2026.py --model posts --apply # Faqat bitta modelni saqlaş
"""

import os
import sys


def main():
    # CloudLinux / cPanel thread limitini saqlaş
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"
    os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_complexprogrammer.settings")
    try:
        import django
        django.setup()
    except Exception as exc:
        print(f"Xatolik: Django yuklanmadi ({exc}). Virtual muhit faollaştirilganligini tekşiring.")
        sys.exit(1)

    from django.core.management import call_command

    args = sys.argv[1:]
    call_command("migrate_db_to_2026", *args)

    # tmp/restart.txt agar mavjud bölsa va --apply berilgan bölsa yangilaymiz
    if "--apply" in args and os.path.isdir("tmp"):
        try:
            restart_file = os.path.join("tmp", "restart.txt")
            with open(restart_file, "a"):
                os.utime(restart_file, None)
            print("🔄 tmp/restart.txt yangilandi.")
        except Exception:
            pass


if __name__ == "__main__":
    main()

