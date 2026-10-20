#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

# CloudLinux / cPanel thread limitini saqlash:
# Server 64 yadroli bo'lgani uchun OpenBLAS/NumPy sukut bo'yicha 64 ta thread ochishga urinadi.
# Bu esa hostingning NPROC (threads) limitiga urilib, "Resource temporarily unavailable" xatosini keltirib chiqaradi.
# Quyidagi o'zgaruvchilar uni faqat 1 ta thread ishlatishga majburlaydi.
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_complexprogrammer.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
