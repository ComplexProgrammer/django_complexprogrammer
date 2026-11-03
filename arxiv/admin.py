from django.contrib import admin
from django.utils.html import format_html

from core.admin_base import ModelAdmin, action, date_range, display, dropdown

from .models import ArchiveItem, ArchiveStatus, ArchiveType, Cabinet, Room


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ("number",)
    search_fields = ("number",)


@admin.register(Cabinet)
class CabinetAdmin(ModelAdmin):
    list_display = ("number",)
    search_fields = ("number",)


@admin.register(ArchiveType)
class ArchiveTypeAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ArchiveStatus)
class ArchiveStatusAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ArchiveItem)
class ArchiveItemAdmin(ModelAdmin):
    list_display = (
        "register_number", "request_number", "patent_number", "room", "cabinet", "cabinet_floor",
        "type", "status", "is_public", "document_link", "created_at",
    )
    list_display_links = ("register_number",)
    list_filter = (dropdown("room"), dropdown("cabinet"), dropdown("type"), dropdown("status"), "is_public",
                   date_range("created_at"))
    search_fields = ("register_number", "request_number", "patent_number")
    autocomplete_fields = ("room", "cabinet", "type", "status")
    list_editable = ("is_public",)
    list_select_related = ("room", "cabinet", "type", "status")
    readonly_fields = ("created_at",)
    list_per_page = 25
    ordering = ("-created_at",)
    actions = ("make_public", "make_private")
    fieldsets = (
        ("Asosiy ma'lumotlar", {"fields": ("room", "cabinet", "cabinet_floor", "type", "status")}),
        ("Hujjat ma'lumotlari", {"fields": ("register_number", "request_number", "patent_number", "document")}),
        ("Ruxsatlar", {"fields": ("is_public",), "description": "Foydalanuvçilar bu hujjatni köra oladimi yoki yöqmi"}),
        ("Vaqt ma'lumotlari", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    @display(description="Hujjat")
    def document_link(self, obj):
        if obj.document:
            return format_html('<a href="{}" target="_blank" rel="noopener">Hujjatni köriş ↗</a>', obj.document.url)
        return "Hujjat yöq"

    @action(description="Tanlangan hujjatlarni public qiliş", icon="public")
    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f"{updated} ta hujjat foydalanuvçilar körişiga oçildi")

    @action(description="Tanlangan hujjatlarni private qiliş", icon="lock")
    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f"{updated} ta hujjat foydalanuvçilar körişidan yaşirildi")

    def save_model(self, request, obj, form, change):
        """Hujjatning körinişi özgarganda xabar beriş."""
        if change and "is_public" in form.changed_data:
            state = "körişiga oçildi" if obj.is_public else "körişidan yaşirildi"
            self.message_user(request, f'"{obj.register_number}" hujjati foydalanuvçilar {state}')
        super().save_model(request, obj, form, change)
