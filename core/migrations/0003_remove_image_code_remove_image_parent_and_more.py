# Generated by Django 4.2 on 2024-09-08 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_type_created_by_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='code',
        ),
        migrations.RemoveField(
            model_name='image',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='image',
            name='value',
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to='core/images'),
        ),
    ]