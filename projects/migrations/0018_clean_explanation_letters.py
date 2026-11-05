"""AI izohlaridagi begona harflarni tuzatiş (körä → köra, öрнатилган → örnatilgan, üçun → uçun va h.k.).

Asosiy manba — tests.Questions (kitob 49/50), /avtotest/ (AvtoTest) undan sinxronlanadi; ikkalasi ham şu yerda
yangilanadi, kirill varianti qayta yaratiladi. Faqat matni özgargan qatorlar yoziladi.
"""

from django.db import migrations


def clean(apps, schema_editor):
    from core.translit import clean_uz_latin, latin_to_cyrillic

    Questions = apps.get_model("tests", "Questions")
    for q in Questions.objects.exclude(explanation_uz_uz="").only("id", "explanation_uz_uz").iterator():
        fixed = clean_uz_latin(q.explanation_uz_uz)
        if fixed != q.explanation_uz_uz:
            Questions.objects.filter(pk=q.pk).update(explanation_uz_uz=fixed, explanation_uz_crl=latin_to_cyrillic(fixed))

    AvtoTest = apps.get_model("projects", "AvtoTest")
    for row in AvtoTest.objects.exclude(izoh="").only("id", "izoh").iterator():
        fixed = clean_uz_latin(row.izoh)
        if fixed != row.izoh:
            AvtoTest.objects.filter(pk=row.pk).update(izoh=fixed)


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0017_sync_avtotest_to_tests"),
        ("tests", "0019_question_explanations_road_signs"),
    ]

    operations = [migrations.RunPython(clean, migrations.RunPython.noop)]
