from django.contrib import admin
from django.utils.html import format_html

from core.admin_base import ModelAdmin, action, date_range, display

from .models import Comment

STATUS_LABELS = {
    Comment.Status.APPROVED: "success",
    Comment.Status.PENDING: "warning",
    Comment.Status.HIDDEN: "danger",
}


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ["username", "short_text", "page", "status_badge", "moderation_note", "created_at"]
    list_display_links = ["username", "short_text"]
    list_filter = ["status", date_range("created_at")]
    actions = ["approve", "hide"]
    search_fields = ["username", "email", "text", "page_url"]
    search_help_text = "Ism, email, matn yoki sahifa manzili böyiça"
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]

    @display(description="Izoh", ordering="text")
    def short_text(self, obj):
        return obj.text[:120] + ("…" if len(obj.text) > 120 else "")

    @display(description="Sahifa", ordering="page_url")
    def page(self, obj):
        return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', obj.page_url, obj.page_url[:40])

    @display(description="Holat", ordering="status", label=STATUS_LABELS)
    def status_badge(self, obj):
        return obj.status, obj.get_status_display()

    @action(description="Tasdiqlaş (saytda körsatiş)", icon="check_circle")
    def approve(self, request, queryset):
        n = queryset.update(status=Comment.Status.APPROVED)
        self.message_user(request, f"{n} ta izoh tasdiqlandi.")

    @action(description="Yaşiriş (spam)", icon="block")
    def hide(self, request, queryset):
        n = queryset.update(status=Comment.Status.HIDDEN)
        self.message_user(request, f"{n} ta izoh yaşirildi.")
