# Generated by Django 4.2 on 2023-11-04 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_tools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='existingPath',
            field=models.CharField(max_length=100),
        ),
    ]
