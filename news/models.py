from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import Auditable, Translatable

class Posts(Translatable):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    title_en_us = models.TextField()
    title_ru_ru = models.TextField()
    title_uz_crl = models.TextField()
    title_uz_uz = models.TextField()
    body_en_us = RichTextUploadingField()
    body_ru_ru = RichTextUploadingField()
    body_uz_crl = RichTextUploadingField()
    body_uz_uz = RichTextUploadingField()
    image = models.ImageField(upload_to='news/images', blank=True)
    publish_time=models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering=['sort_order']
    def __str__(self):
        return self.title_en_us
