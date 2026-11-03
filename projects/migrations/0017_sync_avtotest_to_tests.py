"""Bir martalik: /tests/ dagi 49/50-kitoblarni AvtoTest bilan töliq tenglaştiriş (tests'dagi nusxa buzilgan edi).

Bundan keyin yagona manba — tests (kitob 49/50): AvtoTest undan ``projects/signals.py`` orqali avtomatik
hosil qilinadi (qölda: ``python manage.py sync_avtotest``). Mantiq ``projects/avtotest_sync.py`` da.
"""
from pathlib import Path

from django.conf import settings
from django.db import migrations


def forwards(apps, schema_editor):
    from projects.avtotest_sync import AvtoTestBuilder, TestsBootstrap

    try:
        models = [apps.get_model("tests", name) for name in ("Books", "Topics", "Questions", "Answers")]
    except LookupError:
        return
    AvtoTest = apps.get_model("projects", "AvtoTest")
    roots = {"static_root": Path(settings.BASE_DIR) / "static", "media_root": settings.MEDIA_ROOT}
    TestsBootstrap(AvtoTest, *models, **roots).sync_all()
    AvtoTestBuilder(AvtoTest, *models, **roots).sync_all()  # endi yönaliş teskari: tests -> AvtoTest


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0016_fix_broken_avtotest_answers"),
        ("tests", "0024_fix_legacy_datetimes"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
