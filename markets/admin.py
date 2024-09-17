from django.contrib import admin

# from markets.forms import ProductImageForm
from .models import Category, Market, Store, Product, ProductImage

admin.site.register(Category)
admin.site.register(Market)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductImage)
# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1
#     form = ProductImageForm

# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductImageInline]

# admin.site.register(Product, ProductAdmin)
# class ProductImageAdmin(admin.ModelAdmin):
#     form = ProductImageForm

#     def save_model(self, request, obj, form, change):
#         images = request.FILES.getlist('image')
#         for image in images:
#             ProductImage.objects.create(product=obj.product, type=obj.type, image=image)

# admin.site.register(ProductImage, ProductImageAdmin)