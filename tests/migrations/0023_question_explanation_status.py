from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0022_road_sign_official_numbers"),
    ]

    operations = [
        migrations.AddField(
            model_name="questions",
            name="explanation_status",
            field=models.CharField(
                blank=True,
                choices=[("", "Yo'q"), ("draft", "Qoralama"), ("approved", "Tasdiqlangan")],
                db_index=True,
                default="",
                help_text="«Qoralama» izoh saytda ko'rinmaydi. Qo'lda yozilgan izoh uchun bo'sh yoki «Tasdiqlangan».",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="explanation_confidence",
            field=models.CharField(
                blank=True,
                default="",
                help_text="AI qoralamaning o'z bahosi (high/medium/low) — past bo'lsa diqqat bilan tekshiring.",
                max_length=10,
            ),
        ),
    ]
