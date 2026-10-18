from django.contrib import admin

from driving.models import ActivityDay, ExamResult, Progress, TelegramAccount


@admin.register(TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ("display_name", "username", "telegram_id", "created_at", "last_login_at")
    search_fields = ("username", "first_name", "last_name", "telegram_id")
    readonly_fields = ("created_at", "last_login_at")


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at")
    search_fields = ("user__username",)


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ("user", "correct", "total", "passed", "seconds", "created_at")
    list_filter = ("passed",)


@admin.register(ActivityDay)
class ActivityDayAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "answered", "correct")
    list_filter = ("date",)
