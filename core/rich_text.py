"""Admin'da matn muharriri: CKEditor 5 (o'rnatilgan bo'lsa), aks holda eski CKEditor 4.

CKEditor 4 ning bepul versiyasi 2023-yildan yangilanmaydi (xavfsizlik tuzatishlari yo'q). Model maydonlari
(``RichTextUploadingField``) o'zgarmaydi — ular oddiy HTML matn saqlaydi, shuning uchun migratsiya kerak emas.
Faqat admin formadagi muharrir almashadi:

    pip install django-ckeditor-5      # serverda bir marta; keyin saytni qayta ishga tushirish

Paket o'rnatilmagan bo'lsa hammasi avvalgidek CKEditor 4 bilan ishlayveradi.
"""

from django import forms
from django.conf import settings

try:
    from ckeditor_uploader.fields import RichTextUploadingField
except ImportError:  # pragma: no cover
    RichTextUploadingField = None


class _RichTextFormField(forms.CharField):
    """HTML'da ``required`` atributisiz (CKEditor 5 asl textarea'ni yashiradi va brauzer tekshiruvi formani jimgina
    to'xtatib qo'yadi), lekin bo'sh qiymat server tomonda baribir rad etiladi."""

    def __init__(self, *args, must_fill=False, **kwargs):
        self.must_fill = must_fill
        super().__init__(*args, required=False, **kwargs)

    def validate(self, value):
        super().validate(value)
        if self.must_fill and value in self.empty_values:
            raise forms.ValidationError(self.error_messages["required"], code="required")


class RichTextAdminMixin:
    """ModelAdmin uchun: RichTextUploadingField maydonlarida CKEditor 5 muharririni ko'rsatadi."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if getattr(settings, "CKEDITOR5_ENABLED", False) and RichTextUploadingField and isinstance(
            db_field, RichTextUploadingField
        ):
            from django_ckeditor_5.widgets import CKEditor5Widget

            return _RichTextFormField(
                label=db_field.verbose_name.capitalize(),
                help_text=db_field.help_text,
                must_fill=not db_field.blank,
                widget=CKEditor5Widget(config_name="default"),
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)
