# Generated by Django 4.2 on 2024-09-08 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_remove_posts_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='name_en_us',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='posts',
            name='name_ru_ru',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='posts',
            name='name_uz_crl',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='posts',
            name='name_uz_uz',
            field=models.TextField(),
        ),
    ]