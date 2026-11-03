from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from blog.models import Categories, Posts
from core.admin_base import ModelAdmin, date_range, display, dropdown
from core.rich_text import RichTextAdminMixin


@admin.register(Categories)
class CategoriesAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "name_ru_ru", "sort_order", "is_deleted"]
    list_editable = ["sort_order"]
    search_fields = ["name_uz_uz", "name_ru_ru", "name_en_us"]
    ordering = ["-sort_order", "-created_at"]


@admin.register(Posts)
class PostAdmin(RichTextAdminMixin, ModelAdmin):
    list_display = ["thumb", "name_uz_uz", "categorie", "state", "publish_time", "view_count", "open_link"]
    list_display_links = ["thumb", "name_uz_uz"]
    list_filter = [dropdown("categorie"), "is_deleted", date_range("publish_time")]
    list_select_related = ["categorie"]
    search_fields = ["name_uz_uz", "name_ru_ru", "name_en_us", "title_uz_uz", "title_ru_ru", "title_en_us", "slug"]
    date_hierarchy = "publish_time"
    ordering = ["-sort_order", "-publish_time"]
    prepopulated_fields = {"slug": ("name_uz_uz",)}
    readonly_fields = ["view_count", "telegram_posted_at"]
    list_per_page = 30

    @display(description="Rasm")
    def thumb(self, obj):
        if not obj.image:
            return "—"
        return format_html('<img src="{}" class="cp-thumb" loading="lazy" alt="">', obj.image.url)

    @display(description="Holat", label={"Naşr qilingan": "success", "Rejalaştirilgan": "info", "Öçirilgan": "danger"})
    def state(self, obj):
        if obj.is_deleted:
            return "Öçirilgan"
        return "Rejalaştirilgan" if obj.publish_time and obj.publish_time > timezone.now() else "Naşr qilingan"

    @display(description="Saytda")
    def open_link(self, obj):
        return format_html('<a href="{}" target="_blank" rel="noopener">oçiş ↗</a>', obj.get_absolute_url())
