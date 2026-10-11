from django.contrib import admin
from django.utils.html import format_html

from blog.models import Categories, Posts


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ["name_uz_uz", "sort_order"]
    search_fields = ["name_uz_uz", "name_ru_ru", "name_en_us"]
    ordering = ["-sort_order", "-created_at"]


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ["thumb", "name_uz_uz", "categorie", "publish_time", "view_count", "is_deleted", "open_link"]
    list_display_links = ["thumb", "name_uz_uz"]
    list_filter = ["categorie", "is_deleted", "publish_time"]
    list_select_related = ["categorie"]
    search_fields = ["name_uz_uz", "name_ru_ru", "name_en_us", "title_uz_uz", "title_ru_ru", "title_en_us", "slug"]
    date_hierarchy = "publish_time"
    ordering = ["-sort_order", "-publish_time"]
    prepopulated_fields = {"slug": ("name_uz_uz",)}
    readonly_fields = ["view_count", "telegram_posted_at"]
    list_per_page = 30

    @admin.display(description="Rasm")
    def thumb(self, obj):
        if not obj.image:
            return "—"
        return format_html('<img src="{}" style="width:64px;height:40px;object-fit:cover;border-radius:4px">', obj.image.url)

    @admin.display(description="Saytda")
    def open_link(self, obj):
        return format_html('<a href="{}" target="_blank">ochish ↗</a>', obj.get_absolute_url())
