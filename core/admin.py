from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from .admin_base import UNFOLD, ModelAdmin, display
from .models import Image, Type

admin.site.site_header = "ComplexProgrammer"
admin.site.site_title = "Complex Admin"
admin.site.index_title = "Dashboard"


class CoreModelAdmin(ModelAdmin):
    """``created_by`` formada körsatilmaydi — yangi yozuvda joriy foydalanuvçi yoziladi."""

    exclude = ("created_by",)


@admin.register(Type)
class TypeAdmin(ModelAdmin):
    list_display = ["name", "code", "value", "parent", "sort_order"]
    list_filter = ["parent"]
    search_fields = ["name", "description", "code", "value"]
    ordering = ["-sort_order", "-created_at"]


@admin.register(Image)
class ImageAdmin(ModelAdmin):
    list_display = ["preview", "content_type", "object_id", "sort_order"]
    list_filter = ["content_type"]
    search_fields = ["image", "object_id"]
    ordering = ["-sort_order", "-created_at"]

    @display(description="Rasm")
    def preview(self, obj):
        from django.utils.html import format_html

        return format_html('<img src="{}" class="cp-thumb" alt="">', obj.image.url) if obj.image else "—"


# --- Foydalanuvçilar: Unfold uslubidagi formalar bilan qayta röyxatdan ötkaziş --------------------
if UNFOLD:
    from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

    admin.site.unregister(User)
    admin.site.unregister(Group)

    @admin.register(User)
    class UserAdmin(BaseUserAdmin, ModelAdmin):
        form = UserChangeForm
        add_form = UserCreationForm
        change_password_form = AdminPasswordChangeForm
        list_display = ["username", "full_name", "email", "is_staff", "is_active", "date_joined", "last_login"]
        list_filter = ["is_staff", "is_superuser", "is_active", "date_joined"]
        ordering = ["-date_joined"]

        @display(description="Ism", ordering="first_name")
        def full_name(self, obj):
            return obj.get_full_name() or "—"

    @admin.register(Group)
    class GroupAdmin(BaseGroupAdmin, ModelAdmin):
        pass
