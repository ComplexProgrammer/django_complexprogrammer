from django.db import migrations, models
from django.utils import timezone

from blog.utils import make_slug


def fill_slugs(apps, schema_editor):
    Posts = apps.get_model("blog", "Posts")
    used = set()
    for post in Posts.objects.order_by("publish_time"):
        base = make_slug(post.name_uz_uz or post.title_uz_uz) or str(post.pk)[:8]
        slug, n = base, 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        # Eski maqolalar Telegram kanalga qayta yuborilmasligi uchun "yuborilgan" deb belgilaymiz
        Posts.objects.filter(pk=post.pk).update(slug=slug, telegram_posted_at=timezone.now())


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_categories_created_by_posts_created_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="slug",
            field=models.SlugField(blank=True, default="", max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="posts",
            name="view_count",
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name="posts",
            name="source_url",
            field=models.URLField(
                blank=True, default="", help_text="Maqola boshqa saytdan olingan bo'lsa — manba havolasi."
            ),
        ),
        migrations.AddField(
            model_name="posts",
            name="telegram_posted_at",
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="posts",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Manzil: /blog/<slug>/. Bo'sh qoldirilsa sarlavhadan avtomatik yaratiladi.",
                max_length=120,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="posts",
            name="publish_time",
            field=models.DateTimeField(
                default=timezone.now,
                help_text="Kelajakdagi sana qo'yilsa, maqola shu vaqtgacha saytda ko'rinmaydi.",
            ),
        ),
    ]
