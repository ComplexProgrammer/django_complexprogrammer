# Generated by Django 4.2 on 2024-09-09 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_image_content_type_image_object_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='name_en_us',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='name_ru_ru',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='type',
            name='name_uz_crl',
        ),
        migrations.RemoveField(
            model_name='type',
            name='name_uz_uz',
        ),
    ]