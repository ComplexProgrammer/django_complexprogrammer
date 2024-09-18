from django.contrib import admin
from .models import Type, Image

class CoreModelAdmin(admin.ModelAdmin):
    # 'created_by' maydonini admin formadan yashirish
    exclude = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not change:  # Agar yangi obyekt bo'lsa
            obj.created_by = request.user
        obj.save()
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display=['name', 'description', 'sort_order']
    list_filter=['name', 'description', 'sort_order']
    search_fields=['name', 'description', 'sort_order']
    ordering=['-sort_order', '-created_at']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['image', 'content_type', 'object_id', 'sort_order']
    list_filter=['image', 'content_type', 'object_id', 'sort_order']
    search_fields=['image', 'content_type', 'object_id', 'sort_order']
    ordering=['-sort_order', '-created_at']