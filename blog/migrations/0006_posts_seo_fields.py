"""Maqolaga qidiruv uchun alohida sarlavha va tavsif (o'zbekcha sahifa uchun).

Eng ko'p ko'rsatilayotgan maqolalar Search Console hisobotidagi (2026-07..10) haqiqiy so'rovlar asosida to'ldiriladi:
masalan "ijara shartnomasi qanday tuziladi", "isitma tushmasa nima qilish kerak", "kontr 1.6 kodlari".
"""

from django.db import migrations, models

SEO = {
    "cf8acdcb-7e10-4ca3-a34c-fdd70d4c8d04": (
        "CS 1.6 kodlari: kontr chitlari va konsol buyruqlari ro'yxati",
        "Counter Strike 1.6 (kontr) kodlari o'zbekcha: pul, qurol, gravitatsiya, tezlik va raund sozlamalari "
        "uchun konsol buyruqlari — har birining tushuntirishi bilan.",
    ),
    "1f33e5b5-6e85-4b5b-a06e-4884596e1647": (
        "Ijara shartnomasi qanday tuziladi: uyni ijaraga berish tartibi",
        "Kvartirani ijaraga berish va olish: ijara shartnomasi qanday tuziladi, namunaviy shartnomani qayerdan "
        "olish mumkin va qonundagi muddat cheklovlari.",
    ),
    "66702a1e-71b3-404f-9245-4fcdc4354270": (
        "Banan po'stining foydalari: yuz, tish va teri parvarishida",
        "Banan po'stining foydali xususiyatlari: kletchatka va vitaminlar, yuz va ko'z osti parvarishi, "
        "tishlarni oqartirish, yaralar va xona gullari uchun foydasi.",
    ),
    "e16b1a15-8cd6-4692-af9a-10ae1a85bb75": (
        "Bolada isitma chiqqanda nima qilish kerak?",
        "Bolaning harorati ko'tarilganda: isitmani qachon tushirish kerak (38,5°C), uy sharoitida haroratni "
        "qanday pasaytirish va isitma tushiruvchi dori qachon beriladi.",
    ),
    "bf85280b-67b3-450d-bcc2-ffc5c0da7446": (
        "Kiprik va qoshni uy sharoitida o'stirish va qalinlashtirish",
        "Kipriklarni uy sharoitida o'stirish va qalinlashtirish: o'sma moyi, surma va boshqa tabiiy vositalar "
        "hamda ularni qanday qo'llash.",
    ),
    "956ccf1e-414a-4987-a8c5-0c6eea028780": (
        "Bola nega tirnog'ini tishlaydi: sabablari va oldini olish",
        "Tirnoq tishlash sabablari: stress, charchoq va asabiylik. Bu odat nega zararli va bolani undan qanday "
        "qutqarish mumkin — ota-onalar uchun maslahatlar.",
    ),
}


def fill(apps, schema_editor):
    Posts = apps.get_model("blog", "Posts")
    for pk, (title, description) in SEO.items():
        Posts.objects.filter(pk=pk, seo_title="").update(seo_title=title, seo_description=description)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_posts_slug_views_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="seo_title",
            field=models.CharField(
                blank=True, default="", max_length=70,
                help_text="Qidiruvdagi sarlavha (o'zbekcha, ≈60 belgi). Bo'sh bo'lsa maqola nomi ishlatiladi.",
            ),
        ),
        migrations.AddField(
            model_name="posts",
            name="seo_description",
            field=models.CharField(
                blank=True, default="", max_length=200,
                help_text="Qidiruvda sarlavha ostidagi matn (o'zbekcha, ≈150 belgi). Bo'sh bo'lsa kirish matnidan olinadi.",
            ),
        ),
        migrations.RunPython(fill, migrations.RunPython.noop),
    ]
