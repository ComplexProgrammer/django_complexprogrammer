from django.contrib import admin

from core.admin_base import ModelAdmin
from pdf_tools.models import File


@admin.register(File)
class FileAdmin(ModelAdmin):
    list_display = ["name", "existingPath", "eof"]
    search_fields = ["existingPath", "name"]
    ordering = ["-id"]
