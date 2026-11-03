from django.contrib import admin

from core.admin_base import ModelAdmin, date_range
from core.rich_text import RichTextAdminMixin

from .models import Posts


@admin.register(Posts)
class PostAdmin(RichTextAdminMixin, ModelAdmin):
    list_display = ["title_uz_uz", "publish_time"]
    list_filter = [date_range("publish_time")]
    search_fields = ["title_uz_uz", "title_ru_ru", "title_en_us", "title_uz_crl", "body_uz_uz"]
    date_hierarchy = "publish_time"
    ordering = ["-publish_time"]
