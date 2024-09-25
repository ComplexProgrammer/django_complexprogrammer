from django.contrib import admin

from core.admin import CoreModelAdmin

# from markets.forms import ProductImageForm
from .models import Category, Market, ProductVariant, ProductVariantImage, Store, Product, ProductImage

class ProductDetailInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    class Media:
        js = ('admin/js/dynamic_inline.js',)
admin.site.register(Category)
admin.site.register(Market)
admin.site.register(Store)
# admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductDetailInline]
    exclude = ('created_by',)
    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt yaratishda
            obj.created_by = request.user
        obj.save()

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, CoreModelAdmin)
admin.site.register(ProductVariantImage, CoreModelAdmin)
# admin.site.register(ProductImage)
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