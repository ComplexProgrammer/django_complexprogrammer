from django.contrib import admin
from .models import Type, Image

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