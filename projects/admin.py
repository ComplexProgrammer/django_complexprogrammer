from django.contrib import admin
from . models import Project
# Register your models here.
# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title', 'publish_time', 'status']
    list_filter=['status', 'created_time', 'publish_time']
    prepopulated_fields={'sub_title': ('title',)}
    date_hierarchy='publish_time'
    search_fields=['title', 'status']
    ordering=['status', 'publish_time']
