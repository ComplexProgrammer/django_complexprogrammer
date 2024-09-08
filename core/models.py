from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


class Auditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    class Meta:
        abstract = True

class Translatable(Auditable):
    name_en_us = models.TextField()
    name_ru_ru = models.TextField()
    name_uz_crl = models.TextField()
    name_uz_uz = models.TextField()
    class Meta:
        abstract = True

class Type(Translatable):
  parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')
  code = models.CharField(max_length=255)
  value = models.CharField(max_length=255)

class Image(Auditable):
    image = models.ImageField(upload_to='core/images', blank=True)

def no_spaces_validator(value):
    if ' ' in value:
        raise ValidationError("Text cannot contain spaces.")