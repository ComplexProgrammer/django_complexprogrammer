# Generated by Django 5.1.1 on 2024-09-17 13:24

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0004_product_description_en_us_product_description_ru_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None),
        ),
    ]