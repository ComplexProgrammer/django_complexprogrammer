# Generated by Django 5.1.1 on 2024-09-17 12:59

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_remove_category_name_remove_market_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_en_us',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_ru_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_uz_crl',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_uz_uz',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
