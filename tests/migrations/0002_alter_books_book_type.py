# Generated by Django 4.2 on 2023-11-01 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='book_type',
            field=models.CharField(choices=[('none', 'None'), ('uzb_avto_test', 'Uzb Avto Test'), ('usa_avto_test', 'Usa Avto Test')], default='none', max_length=20),
        ),
    ]
