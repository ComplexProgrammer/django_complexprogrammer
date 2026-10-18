from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import Auditable, Translatable

from blog.utils import make_slug


class Categories(Translatable):
    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
        ordering = ["-sort_order", "-created_at"]

    def __str__(self):
        return f"{self.name_uz_uz}"


class Posts(Translatable):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="blog_posts"
    )
    categorie = models.ForeignKey(
        Categories,
        null=True,
        default=None,
        related_name="categories",
        on_delete=models.DO_NOTHING,
    )
    title_en_us = models.TextField()
    title_ru_ru = models.TextField()
    title_uz_crl = models.TextField()
    title_uz_uz = models.TextField()
    body_en_us = RichTextUploadingField()
    body_ru_ru = RichTextUploadingField()
    body_uz_crl = RichTextUploadingField()
    body_uz_uz = RichTextUploadingField()
    image = models.ImageField(upload_to="post/images", blank=True)
    publish_time = models.DateTimeField(
        default=timezone.now,
        help_text="Kelajakdagi sana qo'yilsa, maqola shu vaqtgacha saytda ko'rinmaydi.",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Manzil: /blog/<slug>/. Bo'sh qoldirilsa sarlavhadan avtomatik yaratiladi.",
    )
    view_count = models.PositiveIntegerField(default=0, editable=False)
    source_url = models.URLField(
        blank=True, default="", help_text="Maqola boshqa saytdan olingan bo'lsa — manba havolasi."
    )
    telegram_posted_at = models.DateTimeField(null=True, blank=True, editable=False)
    seo_title = models.CharField(
        max_length=70, blank=True, default="",
        help_text="Qidiruvdagi sarlavha (o'zbekcha, ≈60 belgi). Bo'sh bo'lsa maqola nomi ishlatiladi.",
    )
    seo_description = models.CharField(
        max_length=200, blank=True, default="",
        help_text="Qidiruvda sarlavha ostidagi matn (o'zbekcha, ≈150 belgi). Bo'sh bo'lsa kirish matnidan olinadi.",
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-sort_order", "-publish_time"]

    def __str__(self):
        return self.name_uz_uz or self.title_uz_uz

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.unique_slug()
        super().save(*args, **kwargs)

    def unique_slug(self):
        base = make_slug(self.name_uz_uz or self.title_uz_uz) or str(self.pk)[:8]
        slug, n = base, 2
        while Posts.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    @classmethod
    def published(cls):
        return cls.objects.filter(
            is_deleted=False, publish_time__lte=timezone.now()
        ).select_related("categorie")
