# Generated by Django 4.2 on 2023-04-11 10:19

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_avtotest_alter_project_options'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='avtotest',
            managers=[
                ('all', django.db.models.manager.Manager()),
            ],
        ),
    ]
