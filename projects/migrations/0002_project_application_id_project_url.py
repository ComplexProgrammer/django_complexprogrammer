# Generated by Django 4.1.7 on 2023-03-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='application_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='url',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
