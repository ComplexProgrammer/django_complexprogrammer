#!/usr/bin/env python
"""Generatsiya qilingan öyin rasmlarini https://complexprogrammer.uz/projects/ bölimi uçun joriy qiliş skripti.

Işlatiş:
    python update_projects_images.py                  # Barça 8 ta öyin rasmini /projects/ da yangilaş
    python update_projects_images.py --update-titles  # Rasmlar bilan birga sarlavhalarni ham yangilaş
    python update_projects_images.py --dry-run        # Bazaga özgartiriş kiritmasdan tekşiriş
    python update_projects_images.py --game tetris    # Faqat bitta öyinni yangilaş
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
    call_command("update_projects_game_images", *args)

    # tmp/restart.txt agar mavjud bölsa yangilaymiz (Passenger uçun)
    if os.path.isdir("tmp"):
        try:
            restart_file = os.path.join("tmp", "restart.txt")
            with open(restart_file, "a"):
                os.utime(restart_file, None)
            print("🔄 tmp/restart.txt yangilandi.")
        except Exception:
            pass


if __name__ == "__main__":
    main()

