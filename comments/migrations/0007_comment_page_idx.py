from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0006_normalize_page_urls"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(fields=["page_url", "-created_at"], name="comment_page_idx"),
        ),
    ]
