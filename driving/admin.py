from django.contrib import admin

from core.admin_base import ModelAdmin, date_range, display
from driving.models import ActivityDay, ExamResult, Progress, TelegramAccount


@admin.register(TelegramAccount)
class TelegramAccountAdmin(ModelAdmin):
    list_display = ("display_name", "username", "telegram_id", "created_at", "last_login_at")
    list_filter = (date_range("created_at"),)
    search_fields = ("username", "first_name", "last_name", "=telegram_id")
    readonly_fields = ("created_at", "last_login_at")
    list_select_related = ("user",)


@admin.register(Progress)
class ProgressAdmin(ModelAdmin):
    list_display = ("user", "updated_at")
    search_fields = ("user__username",)
    list_select_related = ("user",)


@admin.register(ExamResult)
class ExamResultAdmin(ModelAdmin):
    list_display = ("user", "score", "result", "duration", "created_at")
    list_filter = ("passed", date_range("created_at"))
    search_fields = ("user__username",)
    list_select_related = ("user",)
    ordering = ("-created_at",)

    @display(description="Natija", ordering="correct")
    def score(self, obj):
        return f"{obj.correct} / {obj.total}"

    @display(description="Holat", ordering="passed", label={"Ötdi": "success", "Yiqildi": "danger"})
    def result(self, obj):
        return "Ötdi" if obj.passed else "Yiqildi"

    @display(description="Vaqt", ordering="seconds")
    def duration(self, obj):
        return f"{obj.seconds // 60}:{obj.seconds % 60:02d}"


@admin.register(ActivityDay)
class ActivityDayAdmin(ModelAdmin):
    list_display = ("user", "date", "answered", "correct", "accuracy")
    list_filter = (date_range("date"),)
    search_fields = ("user__username",)
    list_select_related = ("user",)
    date_hierarchy = "date"
    ordering = ("-date",)

    @display(description="Aniqlik")
    def accuracy(self, obj):
        return f"{round(100 * obj.correct / obj.answered)}%" if obj.answered else "—"
