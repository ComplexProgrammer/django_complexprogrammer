# Generated by Django 5.1.1 on 2025-06-04 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0004_alter_comment_options_comment_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="email",
            field=models.EmailField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
