# Generated by Django 4.2 on 2024-02-09 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='sort_number',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='view_count',
        ),
    ]