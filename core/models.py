from email.headerregistry import Group
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

def get_current_user(request):
    return getattr(request, 'current_user', None)
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

class Type(Auditable):
  parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')
  name = models.TextField()
  description = models.TextField()
  code = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  def __str__(self):
    return self.name +' -> '+ self.description

class Image(Auditable):
    image = models.ImageField(upload_to='core/images', blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Image for {self.content_object} - {self.image.name}"

def no_spaces_validator(value):
    if ' ' in value:
        raise ValidationError("Text cannot contain spaces.")