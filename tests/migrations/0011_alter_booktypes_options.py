# Generated by Django 4.2 on 2023-12-21 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_booktypes_alter_books_options_alter_types_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booktypes',
            options={'ordering': ['sort_order'], 'verbose_name': 'BookType', 'verbose_name_plural': 'Book_Types'},
        ),
    ]