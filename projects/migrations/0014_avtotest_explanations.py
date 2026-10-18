from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0013_remove_books_group_remove_questions_topic_and_more"),
    ]

    operations = [
        migrations.AddField(model_name="avtotest", name="izoh", field=models.TextField(blank=True, default="")),
        migrations.AddField(model_name="avtotest", name="izoh_ru", field=models.TextField(blank=True, default="")),
        migrations.AddField(model_name="avtotest", name="izoh_en", field=models.TextField(blank=True, default="")),
        migrations.AddField(
            model_name="avtotest",
            name="izoh_holati",
            field=models.CharField(
                blank=True, choices=[("", "Yo'q"), ("draft", "Qoralama"), ("approved", "Tasdiqlangan")], db_index=True,
                default="", help_text="Saytda faqat «Tasdiqlangan» izoh ko'rsatiladi.", max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="avtotest",
            name="izoh_ishonch",
            field=models.CharField(
                blank=True, default="", max_length=10,
                help_text="AI qoralamaning o'z bahosi (high/medium/low) — past bo'lsa diqqat bilan tekshiring.",
            ),
        ),
    ]
