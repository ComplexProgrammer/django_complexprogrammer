# Generated by Django 4.2 on 2023-04-11 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvtoTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('savol', models.TextField()),
                ('savol_en', models.TextField()),
                ('savol_ru', models.TextField()),
                ('javob_a', models.TextField()),
                ('javob_a_en', models.TextField()),
                ('javob_a_ru', models.TextField()),
                ('javob_b', models.TextField()),
                ('javob_b_en', models.TextField()),
                ('javob_b_ru', models.TextField()),
                ('javob_c', models.TextField()),
                ('javob_c_en', models.TextField()),
                ('javob_c_ru', models.TextField()),
                ('javob_d', models.TextField()),
                ('javob_d_en', models.TextField()),
                ('javob_d_ru', models.TextField()),
                ('javob', models.CharField(max_length=1)),
                ('bilet', models.IntegerField()),
                ('raqam', models.IntegerField()),
                ('rasm', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['order']},
        ),
    ]
