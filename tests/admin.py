from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import (
    Answers,
    Books,
    Groups,
    Questions,
    Topics,
    Types,
    BookTypes,
    RoadSignCategories,
    RoadSigns,
)
from core.translit import convert
from projects.avtotest_sync import SYNCED_BOOK_IDS, question_problem
from projects.signals import sync_bilets, topic_bilets


def _is_synced(question):
    topic = question.topic if question.topic_id else None
    return topic is not None and topic.book_id in SYNCED_BOOK_IDS


def _warn_if_unsynced(request, question):
    """49/50-kitob savoli AvtoTest'ga siğmasa (masalan, 2 ta töğri javob) — ogohlantiriş."""
    if question is None or not _is_synced(question):
        return
    answers = list(Answers.objects.filter(question=question, is_deleted=False).order_by("number", "id"))
    problem = question_problem(question, answers)
    if problem:
        messages.warning(request, f"«{question}» /avtotest/ ga yozilmadi: {problem}. Tuzatilgunça eski nusxa qoladi.")


class AnswersInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors) or not _is_synced(self.instance):
            return
        live = [
            f.cleaned_data for f in self.forms
            if f.cleaned_data and not f.cleaned_data.get("is_deleted") and (f.cleaned_data.get("name_uz_uz") or "").strip()
        ]
        if len(live) > 4:
            raise ValidationError("Avtotest savolida 4 tadan ortiq variant bölişi mumkin emas (/avtotest/ va mobil ilova 4 tagaça körsatadi).")
        if sum(1 for d in live if d.get("right")) != 1:
            raise ValidationError("Avtotest savolida aniq bitta töğri javob belgilanişi kerak.")
        if any(d.get("image") for d in live):
            raise ValidationError("Avtotest savolida javob variantiga rasm qöyib bölmaydi — rasmni savolning öziga qöying.")


class AnswersInline(admin.TabularInline):
    model = Answers
    formset = AnswersInlineFormSet
    fk_name = "question"
    fields = ["number", "name_uz_uz", "name_uz_crl", "name_ru_ru", "name_en_us", "image", "right", "is_deleted"]
    ordering = ["number", "id"]
    extra = 0
    can_delete = False  # öçiriş örniga "is deleted" (yumşoq öçiriş)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_deleted=False)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for name in ("name_uz_crl", "name_ru_ru", "name_en_us"):
            formset.form.base_fields[name].required = False  # kirill böş bölsa lotindan hosil qilinadi
        return formset


SYNCED_INFO = (
    "Bu savol /avtotest/, mobil ilova va bot uçun asosiy manba: saqlangandan keyin AvtoTest avtomatik yangilanadi."
)
@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display = ["name_uz_uz"]
    list_filter = ["name_uz_uz"]
    search_fields = ["name_uz_uz"]
    ordering = ["sort_order"]


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ["name_uz_uz", "number", "type"]
    list_filter = ["name_uz_uz", "number", "type"]
    search_fields = ["name_uz_uz", "number", "type"]
    ordering = ["sort_order"]


@admin.register(BookTypes)
class BookTypesAdmin(admin.ModelAdmin):
    list_display = ["code", "description"]
    list_filter = ["code", "description"]
    search_fields = ["code", "description"]
    ordering = ["sort_order"]


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ["book_type", "type", "group"]
    list_filter = ["book_type", "type", "group"]
    search_fields = ["book_type", "type", "group"]
    ordering = ["sort_order"]


@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ["name_uz_uz", "number", "type", "group", "book"]
    list_filter = ["name_uz_uz", "number", "type", "group", "book"]
    search_fields = ["name_uz_uz", "number", "type", "group", "book"]
    ordering = ["sort_order"]


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["name_uz_uz", "number", "type", "group", "book", "topic", "image", "explanation_status", "explanation_confidence"]
    list_filter = ["explanation_status", "explanation_confidence", "type", "group", "book", "topic"]
    search_fields = ["name_uz_uz", "number", "type", "group", "book", "topic", "image", "explanation_uz_uz"]
    ordering = ["sort_order"]
    actions = ["approve_explanations", "reset_explanations"]
    inlines = [AnswersInline]

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)
        if request.method == "GET" and obj is not None and _is_synced(obj):
            messages.info(request, SYNCED_INFO)
        return super().change_view(request, object_id, form_url, extra_context)

    def save_formset(self, request, form, formset, change):
        if formset.model is not Answers:
            return super().save_formset(request, form, formset, change)
        question = form.instance
        for answer in formset.save(commit=False):
            # Takroriy bog'lanişlar savoldan olinadi — bir-biriga zid bölib qolmasin
            answer.topic_id, answer.book_id = question.topic_id, question.topic.book_id
            answer.group_id, answer.type_id = question.topic.group_id, question.topic.type_id
            if not answer.created_by_id:
                answer.created_by = request.user
            if not answer.name_uz_crl:
                answer.name_uz_crl = convert(answer.name_uz_uz, "cyr")
            answer.save()
        formset.save_m2m()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        _warn_if_unsynced(request, form.instance)

    def _update_explanations(self, queryset, status):
        n = queryset.exclude(explanation_uz_uz="").update(explanation_status=status)
        sync_bilets(*topic_bilets(set(queryset.values_list("topic_id", flat=True))))  # update() signal yubormaydi
        return n

    @admin.action(description="Izohni tasdiqlaş (saytda körsatiş)")
    def approve_explanations(self, request, queryset):
        self.message_user(request, f"{self._update_explanations(queryset, 'approved')} ta izoh tasdiqlandi.")

    @admin.action(description="Izohni qoralamaga qaytariş (saytdan yaşiriş)")
    def reset_explanations(self, request, queryset):
        self.message_user(request, f"{self._update_explanations(queryset, 'draft')} ta izoh qoralamaga qaytarildi.")


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = [
        "name_uz_uz",
        "number",
        "question_id",
        "type",
        "group",
        "book",
        "topic",
        "question",
        "image",
        "right",
    ]
    list_filter = [
        "name_uz_uz",
        "number",
        "type",
        "group",
        "book",
        "topic",
        "question",
        "image",
        "right",
    ]
    search_fields = [
        "name_uz_uz",
        "number",
        "type",
        "group",
        "book",
        "topic",
        "question",
        "image",
        "right",
    ]
    ordering = ["sort_order"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        _warn_if_unsynced(request, obj.question)


@admin.register(RoadSignCategories)
class RoadSignCategoriesAdmin(admin.ModelAdmin):
    list_display = ["name_uz_uz", "code", "sort_order", "is_deleted"]
    list_editable = ["sort_order", "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru", "code"]
    ordering = ["sort_order"]


@admin.register(RoadSigns)
class RoadSignsAdmin(admin.ModelAdmin):
    list_display = ["number", "name_uz_uz", "category", "sort_order", "is_deleted"]
    list_filter = ["category", "is_deleted"]
    search_fields = ["number", "name_uz_uz", "name_ru_ru", "description_uz_uz"]
    ordering = ["category__sort_order", "sort_order"]
