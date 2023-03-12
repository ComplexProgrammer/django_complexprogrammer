
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
        choices=Status.choices,
        default=Status.Draft
    )
    is_service=models.BooleanField(default=False)
    order=models.IntegerField()
    objects=models.Manager()
    services=IsService()
    actives=IsActive()
    class Meta:
        ordering=['-publish_time']
    def __str__(self):
        return self.title
