# Generated by Django 4.2 on 2023-12-21 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0006_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='groups', to='tests.types'),
        ),
    ]