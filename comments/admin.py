from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'text', 'page_url', 'created_at']
    list_filter = ['created_at', 'page_url']
    search_fields = ['username', 'email', 'text', 'page_url']
    readonly_fields = ['created_at']
    ordering = ['-created_at']