"""Yo'l belgilariga rasmiy raqam, nom va tavsif (YHQ 1-ilovasi, VM 172-son qarori, lex.uz).

Rasmiy matn ``driving/data/yhq_uz.json`` da (``manage.py import_yhq``). Rasm -> raqam moslik rasmlarni ko'rib, rasmiy
ro'yxatdagi nom va yo'nalish bo'yicha belgilangan. Faqat raqami hali bo'sh (admin'da tegilmagan) belgilar yangilanadi.
"""

import importlib
import json
from pathlib import Path

from django.conf import settings
from django.db import migrations

IMAGE_DIR = "tests/road_signs/images"

# rasm -> (ko'rsatiladigan raqam, rasmiy ro'yxatdagi kalit raqam)
NUMBERS = {
    "b1.jpg": ("1.1", "1.1"), "b2.jpg": ("1.2", "1.2"), "b3.jpg": ("1.3.1", "1.3.1"), "b4.jpg": ("1.3.2", "1.3.2"),
    "b5.jpg": ("1.4.1–1.4.6", "1.4.1"), "b8.jpg": ("1.5", "1.5"), "b9.jpg": ("1.6", "1.6"), "b10.jpg": ("1.7", "1.7"),
    "b11.jpg": ("1.8", "1.8"), "b12.jpg": ("1.9", "1.9"), "b13.jpg": ("1.10", "1.10"), "b14.jpg": ("1.11.1", "1.11.1"),
    "b15.jpg": ("1.11.2", "1.11.1"), "b16.jpg": ("1.12.1", "1.12.1"), "b18.jpg": ("1.13", "1.13"),
    "b19.jpg": ("1.14", "1.14"), "b20.jpg": ("1.15", "1.15"), "b21.jpg": ("1.16", "1.16"), "b22.jpg": ("1.17", "1.17"),
    "b23.jpg": ("1.18.1", "1.18.1"), "b24.jpg": ("1.18.2", "1.18.1"), "b25.jpg": ("1.18.3", "1.18.1"),
    "b26.jpg": ("1.19", "1.19"), "b27.jpg": ("1.20", "1.20"), "b28.jpg": ("1.21", "1.21"), "b29.jpg": ("1.22", "1.22"),
    "b30.jpg": ("1.23", "1.23"), "b31.jpg": ("1.24", "1.24"), "b32.jpg": ("1.25.1", "1.25.1"), "b33.jpg": ("1.26", "1.26"),
    "b34.jpg": ("1.27", "1.27"), "b36.jpg": ("1.29", "1.29"), "b37.jpg": ("1.31.1, 1.31.2", "1.31.1"),
    "b39.jpg": ("1.31.3", "1.31.3"),
    "b41.jpg": ("2.3.1", "2.3.1"), "b42.jpg": ("2.3.2", "2.3.2"), "b44.jpg": ("2.4", "2.4"), "b45.jpg": ("2.5", "2.5"),
    "b46.jpg": ("2.6", "2.6"), "b47.jpg": ("2.7", "2.7"), "b48.jpg": ("2.1", "2.1"), "b49.jpg": ("2.2", "2.2"),
    "b50.jpg": ("3.1", "3.1"), "b52.jpg": ("3.2", "3.2"), "b54.jpg": ("3.4", "3.4"), "b55.jpg": ("3.5", "3.5"),
    "b57.jpg": ("3.7", "3.7"), "b60.jpg": ("3.10", "3.10"), "b61.jpg": ("3.11", "3.11"), "b62.jpg": ("3.12", "3.12"),
    "b63.jpg": ("3.13", "3.13"), "b64.jpg": ("3.14", "3.14"), "b65.jpg": ("3.15", "3.15"), "b66.jpg": ("3.18.1", "3.18.1"),
    "b67.jpg": ("3.18.2", "3.18.2"), "b69.jpg": ("3.20", "3.20"), "b73.jpg": ("3.24", "3.24"), "b78.jpg": ("3.29", "3.29"),
    "b79.jpg": ("3.30", "3.30"),
    "b81.jpg": ("4.1.1", "4.1.1"), "b82.jpg": ("4.1.2", "4.1.2"), "b83.jpg": ("4.1.3", "4.1.3"), "b84.jpg": ("4.1.4", "4.1.4"),
}
# Bir nom ostida bir nechta belgi bo'lsa (1.11.1/1.11.2 kabi), umumiy nom o'rniga bazadagi aniq nom qoladi
KEEP_OWN_NAME = {"b14.jpg", "b15.jpg", "b16.jpg", "b24.jpg", "b25.jpg", "b37.jpg", "b39.jpg"}


def _official():
    path = Path(settings.BASE_DIR) / "driving" / "data" / "yhq_uz.json"
    try:
        signs = json.loads(path.read_text(encoding="utf-8"))["signs"]
    except (OSError, ValueError, KeyError):
        return {}
    return {s["num"]: s for s in signs}


def apply(apps, schema_editor):
    RoadSigns = apps.get_model("tests", "RoadSigns")
    to_cyrillic = importlib.import_module("tests.migrations.0021_seed_road_signs").to_cyrillic
    official = _official()
    for image, (number, key) in NUMBERS.items():
        sign = RoadSigns.objects.filter(image=f"{IMAGE_DIR}/{image}", number="").first()
        if sign is None:
            continue
        sign.number = number
        entry = official.get(key)
        if entry:
            name = entry["name"].replace("ʻ", "'").replace("ʼ", "'").rstrip("!")
            if image not in KEEP_OWN_NAME:
                sign.name_uz_uz = name
                sign.name_uz_crl = to_cyrillic(name)
            text = entry["text"].replace("ʻ", "'").replace("ʼ", "'").strip()
            # Rasmiy tavsif birinchi, keyin avtotest savollaridan olingan izoh (bir xil bo'lmasa)
            if text and text not in sign.description_uz_uz:
                sign.description_uz_uz = (text + ("\n\n" + sign.description_uz_uz if sign.description_uz_uz else "")).strip()
                sign.description_uz_crl = to_cyrillic(sign.description_uz_uz)
        sign.save()


def revert(apps, schema_editor):
    RoadSigns = apps.get_model("tests", "RoadSigns")
    RoadSigns.objects.filter(image__in=[f"{IMAGE_DIR}/{i}" for i in NUMBERS]).update(number="")


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0021_seed_road_signs"),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
