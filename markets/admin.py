from django.contrib import admin

from core.admin import CoreModelAdmin
from core.admin_base import ModelAdmin, TabularInline, dropdown
from core.rich_text import RichTextAdminMixin

from .models import Category, Market, Product, ProductVariant, ProductVariantImage, Store


class ProductDetailInline(TabularInline):
    model = ProductVariant
    extra = 1
    exclude = ("created_by",)

    class Media:
        js = ("admin/js/dynamic_inline.js",)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "parent", "sort_order", "is_deleted"]
    list_filter = [dropdown("parent"), "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru"]


@admin.register(Market)
class MarketAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "location", "parent", "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru", "location"]


@admin.register(Store)
class StoreAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "market", "type", "is_deleted"]
    list_filter = [dropdown("market"), dropdown("type"), "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru"]
    list_select_related = ["market", "type"]


@admin.register(Product)
class ProductAdmin(RichTextAdminMixin, CoreModelAdmin):
    list_display = ["name_uz_uz", "store", "category", "is_deleted"]
    list_filter = [dropdown("store"), dropdown("category"), "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru"]
    list_select_related = ["store", "category"]
    inlines = [ProductDetailInline]

    def save_formset(self, request, form, formset, change):
        for obj in formset.save(commit=False):
            if not obj.created_by_id:
                obj.created_by = request.user
            obj.save()
        formset.save_m2m()
        for obj in formset.deleted_objects:
            obj.delete()


@admin.register(ProductVariant)
class ProductVariantAdmin(CoreModelAdmin):
    list_display = ["product", "size", "color", "price", "quantity"]
    list_filter = [dropdown("product")]
    list_select_related = ["product", "size"]


@admin.register(ProductVariantImage)
class ProductVariantImageAdmin(CoreModelAdmin):
    list_display = ["product_variant", "image"]
    list_select_related = ["product_variant"]
