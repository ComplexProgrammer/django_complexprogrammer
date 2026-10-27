from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0014_avtotest_explanations"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="avtotest",
            index=models.Index(fields=["bilet", "raqam"], name="avtotest_bilet_raqam_idx"),
        ),
    ]
