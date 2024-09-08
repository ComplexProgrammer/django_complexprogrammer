from django.db import models
from core.models import Auditable, Translatable
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='markets/categories/images', blank=True)

    def __str__(self):
        return self.name

class Market(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    logo = models.ImageField(upload_to='markets/logos', blank=True)

    def __str__(self):
        return self.name

class Store(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    logo = models.ImageField(upload_to='markets/stores/logos', blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='markets/stores/products/images', blank=True)

    def __str__(self):
        return self.name
