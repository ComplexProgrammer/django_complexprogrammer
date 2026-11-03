from django.contrib import admin, messages
from .models import AvtoTest, Project


# Register your models here.
# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "publish_time", "status", "order"]
    list_filter = ["status", "created_time", "publish_time"]
    prepopulated_fields = {"sub_title": ("title",)}
    date_hierarchy = "publish_time"
    search_fields = ["title", "status"]
    ordering = ["order", "status", "publish_time"]


AVTOTEST_HELP = (
    "AvtoTest faqat körişga oçiq: u Tests → Questions'dagi 49 (1–108-biletlar) va 50 (109-bilet va keyingilari) "
    "kitoblardan avtomatik hosil qilinadi. Savol, javob va izohlarni Tests → Questions böliminda tahrirlang."
)


@admin.register(AvtoTest)
class AvtoTestAdmin(admin.ModelAdmin):
    """Yagona manba — tests (projects/avtotest_sync.py). Bu yerdagi özgariş keyingi sinxronlaşda yöqoladi."""

    list_display = ["savol", "javob", "bilet", "raqam", "izoh_holati", "izoh_ishonch"]
    list_filter = ["izoh_holati", "izoh_ishonch", "bilet"]
    search_fields = ["savol", "javob", "izoh"]
    ordering = ["id"]

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
