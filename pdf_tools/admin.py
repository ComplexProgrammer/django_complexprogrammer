from django.contrib import admin

from pdf_tools.models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display=['existingPath', 'name', 'eof']
    list_filter=['existingPath', 'name', 'eof']
    search_fields=['existingPath', 'name', 'eof']
    ordering=['id']
