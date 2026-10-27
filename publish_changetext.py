#!/usr/bin/env python
"""Lotin-kirill ögirgiç maqolasini rasmlari bilan birga naşr qiliş skripti.

Işlatiş:
    python publish_changetext.py            # Naşr qiliş (yoki yangilaş)
    python publish_changetext.py --draft    # Qoralama qilib saqlaş
"""

import os
import sys


def main():
    # CloudLinux / cPanel thread limitini saqlash
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

    call_command("publish_changetext_post", *args)

    # tmp/restart.txt agar mavjud bölsa yangilaymiz (Passenger uçun)
    if os.path.isdir("tmp"):
        try:
            with open(os.path.join("tmp", "restart.txt"), "a"):
                os.utime(os.path.join("tmp", "restart.txt"), None)
            print("🔄 tmp/restart.txt yangilandi.")
        except Exception:
            pass


if __name__ == "__main__":
    main()
