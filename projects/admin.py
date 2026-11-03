from django.contrib import admin, messages
from django.utils.html import format_html

from core.admin_base import ModelAdmin, display

from .models import AvtoTest, Project


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ["thumb", "title", "category", "publish_time", "status", "is_service", "order"]
    list_display_links = ["thumb", "title"]
    list_editable = ["order"]
    list_filter = ["status", "is_service", "category", "publish_time"]
    prepopulated_fields = {"sub_title": ("title",)}
    date_hierarchy = "publish_time"
    search_fields = ["title", "sub_title", "category", "url"]
    ordering = ["order", "status", "publish_time"]

    @display(description="Rasm")
    def thumb(self, obj):
        return format_html('<img src="{}" class="cp-thumb" loading="lazy" alt="">', obj.image.url) if obj.image else "—"


AVTOTEST_HELP = (
    "AvtoTest faqat körişga oçiq: u Tests → Questions'dagi 49 (1–108-biletlar) va 50 (109-bilet va keyingilari) "
    "kitoblardan avtomatik hosil qilinadi. Savol, javob va izohlarni Tests → Questions böliminda tahrirlang."
)


@admin.register(AvtoTest)
class AvtoTestAdmin(ModelAdmin):
    """Yagona manba — tests (projects/avtotest_sync.py). Bu yerdagi özgariş keyingi sinxronlaşda yöqoladi."""

    list_display = ["savol_short", "bilet", "raqam", "javob", "izoh_holati", "izoh_ishonch"]
    list_filter = ["izoh_holati", "izoh_ishonch", "bilet"]
    search_fields = ["savol", "savol_ru", "izoh", "=bilet", "=id"]
    ordering = ["bilet", "raqam"]

    @display(description="Savol", ordering="savol")
    def savol_short(self, obj):
        return obj.savol[:110] + ("…" if len(obj.savol) > 110 else "")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        messages.info(request, AVTOTEST_HELP)
        return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        messages.info(request, AVTOTEST_HELP)
        return super().change_view(request, object_id, form_url, extra_context)
