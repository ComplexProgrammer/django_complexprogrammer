from django.db import models

class File(models.Model):
    existingPath = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()
