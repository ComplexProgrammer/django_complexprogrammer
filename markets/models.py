from django.db import models
from core.models import Auditable,Translatable, Type
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django_complexprogrammer.settings import COLOR_PALETTE
class Category(Translatable):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='markets/categories/images', blank=True)

    def __str__(self):
        return self.name_uz_uz

class Market(Translatable):
    location = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    logo = models.ImageField(upload_to='markets/logos', blank=True)

    def __str__(self):
        return self.name_uz_uz

class Store(Translatable):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    logo = models.ImageField(upload_to='markets/stores/logos', blank=True)

    def __str__(self):
        return self.name_uz_uz

class Product(Translatable):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='markets/stores/products/images', blank=True)
    description_en_us = RichTextUploadingField(null=True)
    description_ru_ru = RichTextUploadingField(null=True)
    description_uz_crl = RichTextUploadingField(null=True)
    description_uz_uz = RichTextUploadingField(null=True)

    def __str__(self):
        return self.name_uz_uz

class ProductDetail(Auditable):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Type, on_delete=models.CASCADE)
    color = ColorField(samples=COLOR_PALETTE, default='#000000') # type: ignore
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.product.name_uz_uz+" "+self.size.description+" "+self.size.name+" "+str(self.price)+" so`m "+str(self.quantity)+" dona"

class ProductDetailImage(Auditable):
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='markets/stores/products/details/images', blank=True)
    def __str__(self):
        return self.product_detail.product.name_uz_uz
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='markets/stores/products/images', blank=True)

    def __str__(self):
        return self.image.name
    