# Generated by Django 5.1 on 2024-08-10 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_posts_sort_number_remove_posts_view_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['-sort_order', '-created_at'], 'verbose_name': 'Categorie', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-sort_order', '-publish_time'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
    ]