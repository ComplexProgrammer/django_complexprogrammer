"""Barça admin sinflari uçun umumiy asos (mavzu: django-unfold).

Unfold örnatilmagan bölsa (masalan, serverda ``pip install`` hali qilinmagan), hammasi oddiy Django admin
bilan işlayveradi — sayt yiqilmaydi, faqat körinişi soddaroq böladi.

``ModelAdmin`` qöşimça qiladi:

* avtomatik nomlangan maydonlarga özbekça yorliq beradi (``name_uz_uz`` -> "Nomi (özbekça)"), formada ham,
  röyxat ustunlarida ham;
* tarjima maydonlari bor modellarda formani tablarga ajratadi: Asosiy / Özbekça / Kirill / Ruscha / Inglizça / Tizim;
* matn (``TextField``) maydonlarini ixçam, özi kattalaşadigan qiladi;
* ``created_by`` ni majburiy emas qiladi va böş qolsa joriy foydalanuvçini yozadi.
"""
from django.contrib.admin.utils import display_for_field
from django.db import models
from django.utils.text import Truncator

try:
    from unfold.admin import ModelAdmin as _ModelAdmin
    from unfold.admin import StackedInline as _StackedInline
    from unfold.admin import TabularInline as _TabularInline
    from unfold.decorators import action as _action
    from unfold.decorators import display as _display
    from unfold.widgets import UnfoldAdminExpandableTextareaWidget as _Textarea

    UNFOLD = True
except ImportError:  # pragma: no cover — zaxira: oddiy Django admin
    from django.contrib.admin import ModelAdmin as _ModelAdmin
    from django.contrib.admin import StackedInline as _StackedInline
    from django.contrib.admin import TabularInline as _TabularInline
    from django.contrib.admin import action as _action
    from django.contrib.admin import display as _display
    from django.contrib.admin.widgets import AdminTextareaWidget as _Textarea

    UNFOLD = False

_DJANGO_DISPLAY_ARGS = {"function", "boolean", "ordering", "description", "empty_value"}
_DJANGO_ACTION_ARGS = {"function", "permissions", "description"}


def display(function=None, **kwargs):
    """``unfold.decorators.display`` (label= rangli belgi va h.k.); Unfold yöq bölsa — Django'niki."""
    if not UNFOLD:
        kwargs = {k: v for k, v in kwargs.items() if k in _DJANGO_DISPLAY_ARGS}
    return _display(function, **kwargs) if function else _display(**kwargs)


def action(function=None, **kwargs):
    if not UNFOLD:
        kwargs = {k: v for k, v in kwargs.items() if k in _DJANGO_ACTION_ARGS}
    return _action(function, **kwargs) if function else _action(**kwargs)


# --- yorliqlar --------------------------------------------------------------------------------------
LANGS = (  # (qöşimça, yorliq, tab nomi)
    ("uz_uz", "özbekça", "Özbekça"),
    ("uz_crl", "kirill", "Kirill"),
    ("ru_ru", "ruscha", "Ruscha"),
    ("en_us", "inglizça", "Inglizça"),
)
PREFIXES = {
    "name": "Nomi", "title": "Sarlavha", "body": "Matn", "description": "Tavsif", "explanation": "Izoh",
    "text": "Matn", "content": "Matn", "short": "Qisqa matn", "meta_description": "Meta tavsif",
}
LABELS = {
    "created_by": "Muallif", "created_at": "Yaratilgan", "updated_at": "Yangilangan", "is_deleted": "Öçirilgan",
    "sort_order": "Tartib", "number": "Raqam", "image": "Rasm", "right": "Töğri javob", "type": "Tur",
    "group": "Guruh", "book": "Kitob", "topic": "Bilet / mavzu", "question": "Savol", "book_type": "Kitob turi",
    "code": "Kod", "category": "Kategoriya", "categorie": "Kategoriya", "slug": "URL (slug)",
    "publish_time": "Naşr vaqti", "view_count": "Körişlar", "status": "Holat", "email": "Email",
    "username": "Foydalanuvçi", "page_url": "Sahifa", "parent": "Ota yozuv", "value": "Qiymat",
    "explanation_status": "Izoh holati", "explanation_confidence": "AI işonçi", "order": "Tartib",
    "source_url": "Manba manzili", "seo_title": "SEO sarlavha", "seo_description": "SEO tavsif",
    "location": "Manzil", "logo": "Logotip", "market": "Market", "store": "Dökon", "product": "Mahsulot",
    "price": "Narx", "quantity": "Soni", "size": "Ölçam", "color": "Rang",
}
SYSTEM_FIELDS = ("created_by", "sort_order", "is_deleted", "created_at", "updated_at")


def _lang_of(name):
    for suffix, _, tab in LANGS:
        if name.endswith("_" + suffix):
            return suffix, tab
    return None, None


def label_for(field):
    """Avtomatik (``name_uz_uz`` -> "name uz uz") nomlangan maydon uçun özbekça yorliq; aks holda None."""
    name = field.name
    if str(field.verbose_name) != name.replace("_", " "):
        return None  # modelda ataylab berilgan nom — tegmaymiz
    suffix, _ = _lang_of(name)
    if suffix:
        base = name[: -len(suffix) - 1]
        prefix = PREFIXES.get(base, base.replace("_", " ").capitalize())
        lang = next(label for s, label, _ in LANGS if s == suffix)
        return f"{prefix} ({lang})"
    return LABELS.get(name)


class _LabelledColumn:
    """Röyxat ustuni: maydon qiymati Django'ning özidek formatlanadi, sarlavha — özbekça, uzun matn qisqartiriladi."""

    def __init__(self, field, label):
        self.field = field
        self.short_description = label
        self.admin_order_field = field.name
        self.__name__ = field.name
        if isinstance(field, models.BooleanField):
            self.boolean = True  # Django/Unfold belgi (✓/✗) bilan körsatadi

    def __call__(self, obj):
        value = getattr(obj, self.field.name)
        if getattr(self, "boolean", False):
            return value
        if isinstance(self.field, models.TextField) and not self.field.choices and value:
            return Truncator(value).chars(90)
        return display_for_field(value, self.field, "—")


class LabelsMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.TextField) and not db_field.choices and "widget" not in kwargs:
            if db_field.__class__ is models.TextField:  # RichText va boşqa maxsus maydonlarga tegmaymiz
                kwargs["widget"] = _Textarea(attrs={"rows": 2})
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is not None:
            label = label_for(db_field)
            if label:
                formfield.label = label
            if db_field.name == "created_by":
                formfield.required = False
                formfield.help_text = "Böş qolsa — siz."
        return formfield

    def get_list_display(self, request):
        keep = set(self.list_editable or ()) | set(self.list_display_links or ())
        result = []
        for item in super().get_list_display(request):
            if isinstance(item, str) and item not in keep and item != "__str__":
                try:
                    field = self.model._meta.get_field(item)
                except Exception:
                    field = None
                # Bog'lanişlar (FK) satr holida qoladi — aks holda Django ular uçun select_related qilmaydi
                label = label_for(field) if field is not None and not field.is_relation else None
                if label:
                    item = _LabelledColumn(field, label)
            result.append(item)
        return result


class TabsMixin:
    """``fieldsets`` berilmagan, tarjima maydonlari bor modellarda formani tablarga ajratadi."""

    def get_fieldsets(self, request, obj=None):
        if self.fieldsets:
            return super().get_fieldsets(request, obj)
        fields = list(self.get_fields(request, obj))
        by_lang = {tab: [] for _, _, tab in LANGS}
        main, system = [], []
        for name in fields:
            _, tab = _lang_of(name)
            if tab:
                by_lang[tab].append(name)
            elif name in SYSTEM_FIELDS:
                system.append(name)
            else:
                main.append(name)
        if not any(by_lang.values()):
            if not system or not main:
                return super().get_fieldsets(request, obj)
            return [(None, {"fields": main}), ("Tizim", {"fields": system, "classes": ["collapse"]})]
        tab = ["tab"] if UNFOLD else []
        result = []
        if main:
            result.append(("Asosiy", {"fields": main, "classes": tab}))
        result += [(name, {"fields": names, "classes": tab}) for name, names in by_lang.items() if names]
        if system:
            result.append(("Tizim", {"fields": system, "classes": tab}))
        return result


class AuditMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by_id") and not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ModelAdmin(AuditMixin, TabsMixin, LabelsMixin, _ModelAdmin):
    list_per_page = 50
    list_filter_submit = True  # Unfold: filtrlar "Qölla" tugmasi bilan — har bir tanlovda sahifa qayta yuklanmaydi
    warn_unsaved_form = True  # saqlanmagan özgariş bilan sahifadan çiqişda ogohlantiriş
    compressed_fields = True


class TabularInline(LabelsMixin, _TabularInline):
    pass


class StackedInline(LabelsMixin, _StackedInline):
    pass


# --- filtrlar (Unfold yöq bölsa — oddiy Django filtri) ---------------------------------------------
def dropdown(field):
    """FK uçun oçiladigan röyxatli filtr (uzun röyxat yon panelni egallamaydi)."""
    if not UNFOLD:
        return field
    from unfold.contrib.filters.admin import RelatedDropdownFilter

    return field, RelatedDropdownFilter


def choices_dropdown(field):
    if not UNFOLD:
        return field
    from unfold.contrib.filters.admin import ChoicesDropdownFilter

    return field, ChoicesDropdownFilter


def autocomplete_filter(field):
    """Minglab yozuvli FK (masalan, bilet) uçun qidiruvli filtr. Bog'langan admin'da search_fields bölişi kerak."""
    if not UNFOLD:
        return field
    from unfold.contrib.filters.admin import AutocompleteSelectFilter

    return field, AutocompleteSelectFilter


def date_range(field):
    if not UNFOLD:
        return field
    from unfold.contrib.filters.admin import RangeDateFilter

    return field, RangeDateFilter
