from django.contrib import admin
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


@admin.register(AvtoTest)
class AvtoTestAdmin(admin.ModelAdmin):
    list_display = ["savol", "javob", "bilet", "raqam", "izoh_holati", "izoh_ishonch"]
    list_filter = ["izoh_holati", "izoh_ishonch", "bilet"]
    search_fields = ["savol", "javob", "izoh"]
    ordering = ["id"]
    actions = ["approve_explanations", "reset_explanations"]

    @admin.action(description="Izohni tasdiqlash (saytda ko'rsatish)")
    def approve_explanations(self, request, queryset):
        n = queryset.exclude(izoh="").update(izoh_holati="approved")
        self.message_user(request, f"{n} ta izoh tasdiqlandi.")

    @admin.action(description="Izohni qoralamaga qaytarish (saytdan yashirish)")
    def reset_explanations(self, request, queryset):
        n = queryset.exclude(izoh="").update(izoh_holati="draft")
        self.message_user(request, f"{n} ta izoh qoralamaga qaytarildi.")
