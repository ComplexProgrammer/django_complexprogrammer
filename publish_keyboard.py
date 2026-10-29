#!/usr/bin/env python
"""Yangi Özbek alifbosi klaviaturasi maqolasini rasmlari bilan birga naşr qiliş skripti.

Işlatiş:
    python publish_keyboard.py            # Naşr qiliş (yoki yangilaş)
    python publish_keyboard.py --draft    # Qoralama qilib saqlaş (2099-yil)
    python publish_keyboard.py --dry-run  # Bazaga yozmasdan tekşiriş
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
    if "--update" not in args:
        args.append("--update")

    call_command("publish_keyboard_post", *args)

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

