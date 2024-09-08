from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import Auditable, Translatable

class Categories(Translatable):
    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
        ordering=['-sort_order', '-created_at']
    def __str__(self):
        return f"{self.name_uz_uz}"

class Posts(Translatable):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='blog_posts')
    categorie = models.ForeignKey(Categories,
                            null=True,
                            default=None,
                            related_name='categories',
                            on_delete=models.DO_NOTHING)
    title_en_us = models.TextField()
    title_ru_ru = models.TextField()
    title_uz_crl = models.TextField()
    title_uz_uz = models.TextField()
    body_en_us = RichTextUploadingField()
    body_ru_ru = RichTextUploadingField()
    body_uz_crl = RichTextUploadingField()
    body_uz_uz = RichTextUploadingField()
    image = models.ImageField(upload_to='post/images', blank=True)
    publish_time=models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering=['-sort_order', '-publish_time']
    def __str__(self):
        return self.title_uz_uz
