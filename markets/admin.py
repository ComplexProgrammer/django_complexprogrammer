from django.contrib import admin
from .models import Category, Market, Store, Product, ProductImage

admin.site.register(Category)
admin.site.register(Market)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductImage)