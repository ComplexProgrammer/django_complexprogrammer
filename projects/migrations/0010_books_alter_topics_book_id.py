# Generated by Django 4.2 on 2023-05-01 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_groups_topics_questions_answers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('name_en_us', models.TextField()),
                ('name_ru_ru', models.TextField()),
                ('name_uz_crl', models.TextField()),
                ('name_uz_uz', models.TextField()),
                ('book_type', models.CharField(choices=[('none', 'None'), ('alifbe', 'Alifbe'), ('adabiyot', 'Adabiyot'), ('algebra', 'Algebra'), ('biologiya', 'Biologiya'), ('dasturlash_asoslari', 'Dasturlash Asoslari'), ('english', 'English'), ('fizika', 'Fizika'), ('geografiya', 'Geografiya'), ('geometriya', 'Geometriya'), ('informatika', 'Informatika'), ('kimyo', 'Kimyo'), ('matematika', 'Matematika'), ('onatili', 'Onatili'), ('oqish', 'Oqish'), ('ozbek_tili', 'Ozbek Tili'), ('rustili', 'Rustili'), ('yozuv', 'Yozuv'), ('uzb_tarix', 'Uzb Tarix'), ('jahon_tarix', 'Jahon Tarix')], default='none', max_length=20)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='projects.groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='topics',
            name='book_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='projects.books'),
        ),
    ]