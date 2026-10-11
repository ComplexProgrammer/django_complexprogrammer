from django.db import migrations

# YHQ 1-ilovasidagi yo'l belgilari toifalari. Belgilarning o'zi admin panel orqali kiritiladi.
CATEGORIES = [
    ('warning', "Ogohlantiruvchi belgilar", "Огоҳлантирувчи белгилар", "Предупреждающие знаки", "Warning signs"),
    ('priority', "Imtiyoz belgilari", "Имтиёз белгилари", "Знаки приоритета", "Priority signs"),
    ('prohibitory', "Taqiqlovchi belgilar", "Тақиқловчи белгилар", "Запрещающие знаки", "Prohibitory signs"),
    ('mandatory', "Buyuruvchi belgilar", "Буюрувчи белгилар", "Предписывающие знаки", "Mandatory signs"),
    ('information', "Axborot-ishora belgilari", "Ахборот-ишора белгилари", "Информационно-указательные знаки", "Information signs"),
    ('service', "Servis belgilari", "Сервис белгилари", "Знаки сервиса", "Service signs"),
    ('additional', "Qo'shimcha axborot belgilari", "Қўшимча ахборот белгилари", "Знаки дополнительной информации", "Additional information plates"),
    ('markings', "Yo'l chiziqlari", "Йўл чизиқлари", "Дорожная разметка", "Road markings"),
]


def seed(apps, schema_editor):
    RoadSignCategories = apps.get_model('tests', 'RoadSignCategories')
    for index, (code, uz, crl, ru, en) in enumerate(CATEGORIES, start=1):
        RoadSignCategories.objects.get_or_create(
            code=code,
            defaults={
                'name_uz_uz': uz,
                'name_uz_crl': crl,
                'name_ru_ru': ru,
                'name_en_us': en,
                'sort_order': index,
            },
        )


def unseed(apps, schema_editor):
    RoadSignCategories = apps.get_model('tests', 'RoadSignCategories')
    RoadSignCategories.objects.filter(code__in=[c[0] for c in CATEGORIES], signs__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0019_question_explanations_road_signs'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
