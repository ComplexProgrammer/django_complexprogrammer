from django.db import migrations, models

from blog.utils import make_slug


def fill_slugs(apps, schema_editor):
    Posts = apps.get_model("news", "Posts")
    used = set()
    for post in Posts.objects.order_by("publish_time"):
        base = make_slug(post.title_uz_uz or post.name_uz_uz) or str(post.pk)[:8]
        slug, n = base, 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        Posts.objects.filter(pk=post.pk).update(slug=slug)


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0006_posts_created_by_alter_posts_name_en_us_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="slug",
            field=models.SlugField(blank=True, default="", max_length=120),
            preserve_default=False,
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="posts",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Manzil: /news/<slug>/. Bo'sh qoldirilsa sarlavhadan avtomatik yaratiladi.",
                max_length=120,
                unique=True,
            ),
        ),
    ]
