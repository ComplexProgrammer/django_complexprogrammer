from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("arxiv", "0003_archiveitem_is_public"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="archiveitem",
            index=models.Index(fields=["-created_at"], name="archiveitem_created_idx"),
        ),
        migrations.AddIndex(
            model_name="archiveitem",
            index=models.Index(fields=["document"], name="archiveitem_document_idx"),
        ),
    ]
