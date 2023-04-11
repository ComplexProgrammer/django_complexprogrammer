from django.contrib import admin
from . models import AvtoTest, Project
# Register your models here.
# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title', 'publish_time', 'status', 'order']
    list_filter=['status', 'created_time', 'publish_time']
    prepopulated_fields={'sub_title': ('title',)}
    date_hierarchy='publish_time'
    search_fields=['title', 'status']
    ordering=['order', 'status', 'publish_time']

@admin.register(AvtoTest)
class AvtoTestAdmin(admin.ModelAdmin):
    list_display=['savol', 'javob', 'bilet', 'raqam']
    list_filter=['bilet', 'raqam']
    search_fields=['savol', 'javob']
    ordering=['id']
