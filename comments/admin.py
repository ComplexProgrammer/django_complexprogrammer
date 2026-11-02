from django.contrib import admin
from .models import Comment


@admin.action(description="Tasdiqlaş (saytda körsatiş)")
def approve(modeladmin, request, queryset):
    queryset.update(status=Comment.Status.APPROVED)


@admin.action(description="Yaşiriş (spam)")
def hide(modeladmin, request, queryset):
    queryset.update(status=Comment.Status.HIDDEN)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "text", "page_url", "status", "moderation_note", "created_at"]
    list_filter = ["status", "created_at", "page_url"]
    actions = [approve, hide]
    search_fields = ["username", "email", "text", "page_url"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]
