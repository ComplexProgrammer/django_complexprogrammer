
from django.utils import timezone
from django.db import models

class IsService(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_service=True)
class IsActive(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)
class Project(models.Model):
    class Status(models.IntegerChoices):
        Draft = 0, "Draft"
        Active = 1, "Active"
    category=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    sub_title=models.CharField(max_length=255)
    url=models.CharField(max_length=255, blank=True)
    application_id=models.CharField(max_length=255, blank=True)
    image=models.ImageField(upload_to='projects/images')
    publish_time=models.DateTimeField(default=timezone.now)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)
    status=models.BooleanField(
        choices=Status.choices, # type: ignore
        default=Status.Draft # type: ignore
    )
    is_service=models.BooleanField(default=False)
    order=models.IntegerField()
    objects=models.Manager()
    services=IsService()
    actives=IsActive()
    class Meta:
        ordering=['order']
    def __str__(self):
        return self.title

class AvtoTest(models.Model):
    savol=models.TextField()
    savol_en=models.TextField()
    savol_ru=models.TextField()
    javob_a=models.TextField()
    javob_a_en=models.TextField()
    javob_a_ru=models.TextField()
    javob_b=models.TextField()
    javob_b_en=models.TextField()
    javob_b_ru=models.TextField()
    javob_c=models.TextField()
    javob_c_en=models.TextField()
    javob_c_ru=models.TextField()
    javob_d=models.TextField()
    javob_d_en=models.TextField()
    javob_d_ru=models.TextField()
    javob=models.CharField(max_length=1)
    bilet=models.IntegerField()
    raqam=models.IntegerField()
    rasm=models.CharField(max_length=255, blank=True)
    objects = models.Manager()
    class Meta:
        ordering=['raqam']
    def __str__(self):
        return f"{self.bilet} {self.savol}"


class Auditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True

class Translatable(Auditable):
    name_en_us = models.TextField()
    name_ru_ru = models.TextField()
    name_uz_crl = models.TextField()
    name_uz_uz = models.TextField()
    class Meta:
        abstract = True