"""Eski importdan qolgan "01/19/2024, 12:46:20" formatidagi sanalarni ISO formatga ögiriş.

Django bunday qiymatni ``None`` deb öqiydi, natijada şu qatorlarni admin'da saqlab bölmasdi
(``NOT NULL constraint failed: tests_answers.created_at``). Endi /avtotest/ savollari ham tests'da
tahrirlanadi, şuning uçun bu muhim.
"""
from datetime import datetime

from django.db import migrations

LEGACY = "%m/%d/%Y, %H:%M:%S"
MODELS = ("Groups", "Topics", "Questions", "Answers")


def forwards(apps, schema_editor):
    qn = schema_editor.quote_name
    with schema_editor.connection.cursor() as cursor:
        for name in MODELS:
            table = qn(apps.get_model("tests", name)._meta.db_table)
            for column in ("created_at", "updated_at"):
                col = qn(column)
                # CAST: aks holda SQLite drayveri ustun turiga qarab qiymatni None qilib qaytaradi
                cursor.execute(f"SELECT DISTINCT CAST({col} AS TEXT) FROM {table} WHERE {col} LIKE %s", ["__/__/____, %"])
                for (value,) in cursor.fetchall():
                    try:
                        fixed = datetime.strptime(value, LEGACY).strftime("%Y-%m-%d %H:%M:%S")
                    except (TypeError, ValueError):
                        continue
                    cursor.execute(f"UPDATE {table} SET {col} = %s WHERE {col} = %s", [fixed, value])


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0023_question_explanation_status"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
