from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import Auditable, Translatable
from blog.utils import make_slug


class Posts(Translatable):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_en_us = models.TextField()
    title_ru_ru = models.TextField()
    title_uz_crl = models.TextField()
    title_uz_uz = models.TextField()
    body_en_us = RichTextUploadingField()
    body_ru_ru = RichTextUploadingField()
    body_uz_crl = RichTextUploadingField()
    body_uz_uz = RichTextUploadingField()
    image = models.ImageField(upload_to="news/images", blank=True)
    publish_time = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Manzil: /news/<slug>/. Bo'sh qoldirilsa sarlavhadan avtomatik yaratiladi.",
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["sort_order"]

    def __str__(self):
        return self.title_en_us

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.unique_slug()
        super().save(*args, **kwargs)

    def unique_slug(self):
        base = make_slug(self.title_uz_uz or self.name_uz_uz) or str(self.pk)[:8]
        slug, n = base, 2
        while Posts.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    def get_absolute_url(self):
        return f"/news/{self.slug}/"
