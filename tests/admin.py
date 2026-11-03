from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.forms.models import BaseInlineFormSet
from django.urls import reverse
from django.utils.html import format_html

from core.admin_base import (
    UNFOLD,
    ModelAdmin,
    TabularInline,
    action,
    autocomplete_filter,
    choices_dropdown,
    display,
    dropdown,
)
from core.translit import convert

if UNFOLD:
    from unfold.widgets import UnfoldAdminTextInputWidget as TextInput
from projects.avtotest_sync import SYNCED_BOOK_IDS, question_problem
from projects.signals import sync_bilets, topic_bilets

from .models import Answers, Books, BookTypes, Groups, Questions, RoadSignCategories, RoadSigns, Topics, Types

STATUS_LABELS = {"approved": "success", "draft": "warning", "": "info"}


def _thumb(image):
    return format_html('<img src="{}" class="cp-thumb" loading="lazy" alt="">', image.url) if image else "—"


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


def _copy_parents(obj, parent):
    """Takroriy bog'lanişlar (type/group/book) ota yozuvdan olinadi — bir-biriga zid bölib qolmasin."""
    for field in ("type_id", "group_id", "book_id"):
        setattr(obj, field, getattr(parent, field))


# =================================================================================================
# Javoblar (savol ičida)
# =================================================================================================
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


class AnswersInline(TabularInline):
    model = Answers
    formset = AnswersInlineFormSet
    fk_name = "question"
    fields = ["number", "name_uz_uz", "name_uz_crl", "name_ru_ru", "name_en_us", "image", "right", "is_deleted"]
    ordering = ["number", "id"]
    extra = 0
    can_delete = False  # öçiriş örniga "Öçirilgan" belgisi (yumşoq öçiriş)
    show_title = False  # Unfold: har bir qator ustida javob matnini takrorlamaslik
    verbose_name = "javob varianti"
    verbose_name_plural = "Javob variantlari"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name.startswith("name_"):  # javob matni qisqa — bir qatorli maydon
            kwargs["widget"] = TextInput() if UNFOLD else forms.TextInput()
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "number" and formfield is not None:
            formfield.widget.attrs["style"] = "width:64px"
        return formfield

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


# =================================================================================================
# Savollar
# =================================================================================================
@admin.register(Questions)
class QuestionsAdmin(ModelAdmin):
    list_display = ["thumb", "question_text", "ticket", "number", "variants", "status_badge", "explanation_confidence", "is_deleted"]
    list_display_links = ["thumb", "question_text"]
    list_filter = [
        dropdown("topic__book"),
        autocomplete_filter("topic"),
        choices_dropdown("explanation_status"),
        "explanation_confidence",
        "is_deleted",
    ]
    search_fields = ["name_uz_uz", "name_uz_crl", "name_ru_ru", "name_en_us", "explanation_uz_uz", "=id"]
    search_help_text = "Savol matni (istalgan tilda), izoh yoki =id böyiça qidiriş"
    list_select_related = ["topic__book__book_type"]
    autocomplete_fields = ["topic"]
    exclude = ["type", "group", "book"]  # bilet (topic) orqali avtomatik töldiriladi
    ordering = ["topic__book_id", "topic__number", "number"]
    actions = ["approve_explanations", "reset_explanations"]
    inlines = [AnswersInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            live_answers=Count("answers", filter=Q(answers__is_deleted=False), distinct=True)
        )

    @display(description="Rasm")
    def thumb(self, obj):
        return _thumb(obj.image)

    @display(description="Savol", ordering="name_uz_uz")
    def question_text(self, obj):
        return obj.name_uz_uz[:110] + ("…" if len(obj.name_uz_uz) > 110 else "")

    @display(description="Bilet", ordering="topic__number", header=True)
    def ticket(self, obj):
        return [obj.topic.name_uz_uz, str(obj.topic.book)] if obj.topic_id else ["—", ""]

    @display(description="Variant", ordering="live_answers")
    def variants(self, obj):
        return obj.live_answers

    @display(description="Izoh", ordering="explanation_status", label=STATUS_LABELS)
    def status_badge(self, obj):
        return obj.explanation_status, obj.get_explanation_status_display()

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)
        if request.method == "GET" and obj is not None and _is_synced(obj):
            messages.info(request, SYNCED_INFO)
        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if obj.topic_id:
            _copy_parents(obj, obj.topic)
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        if formset.model is not Answers:
            return super().save_formset(request, form, formset, change)
        question = form.instance
        for answer in formset.save(commit=False):
            answer.topic_id = question.topic_id
            _copy_parents(answer, question.topic)
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

    @action(description="Izohni tasdiqlaş (saytda körsatiş)", icon="check_circle")
    def approve_explanations(self, request, queryset):
        self.message_user(request, f"{self._update_explanations(queryset, 'approved')} ta izoh tasdiqlandi.")

    @action(description="Izohni qoralamaga qaytariş (saytdan yaşiriş)", icon="undo")
    def reset_explanations(self, request, queryset):
        self.message_user(request, f"{self._update_explanations(queryset, 'draft')} ta izoh qoralamaga qaytarildi.")


@admin.register(Answers)
class AnswersAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "question_text", "number", "right", "book_name", "is_deleted"]
    list_display_links = ["name_uz_uz"]
    list_filter = ["right", "is_deleted", dropdown("question__topic__book")]
    search_fields = ["name_uz_uz", "name_ru_ru", "question__name_uz_uz", "=question__id", "=id"]
    search_help_text = "Javob yoki savol matni, =savol_id böyiça qidiriş"
    list_select_related = ["question__topic__book__book_type"]
    autocomplete_fields = ["question"]
    exclude = ["type", "group", "book", "topic"]  # savol orqali avtomatik töldiriladi
    ordering = ["question_id", "number"]

    @display(description="Savol", ordering="question__name_uz_uz")
    def question_text(self, obj):
        text = obj.question.name_uz_uz
        return text[:80] + ("…" if len(text) > 80 else "")

    @display(description="Kitob")
    def book_name(self, obj):
        topic = obj.question.topic
        return f"{topic.book} · {topic.name_uz_uz}" if topic else "—"

    def save_model(self, request, obj, form, change):
        if obj.question_id:
            obj.topic_id = obj.question.topic_id
            _copy_parents(obj, obj.question.topic)
        super().save_model(request, obj, form, change)
        _warn_if_unsynced(request, obj.question)


# =================================================================================================
# Biletlar, kitoblar, guruhlar, turlar
# =================================================================================================
@admin.register(Topics)
class TopicsAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "number", "book", "questions_link", "is_deleted"]
    list_filter = [dropdown("book"), "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru", "=number"]
    list_select_related = ["book__book_type"]
    exclude = ["type", "group"]  # kitob orqali avtomatik töldiriladi
    ordering = ["book_id", "number"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            live_questions=Count("questions", filter=Q(questions__is_deleted=False), distinct=True)
        )

    @display(description="Savollar", ordering="live_questions")
    def questions_link(self, obj):
        url = reverse("admin:tests_questions_changelist") + f"?topic__id__exact={obj.pk}"
        return format_html('<a href="{}">{} ta savol →</a>', url, obj.live_questions)

    def save_model(self, request, obj, form, change):
        if obj.book_id:
            obj.group_id, obj.type_id = obj.book.group_id, obj.book.type_id
        super().save_model(request, obj, form, change)


@admin.register(Books)
class BooksAdmin(ModelAdmin):
    list_display = ["__str__", "book_type", "group", "type", "topics_link", "is_deleted"]
    list_filter = [dropdown("group"), dropdown("type"), "is_deleted"]
    search_fields = ["book_type__code", "book_type__name_uz_uz", "group__name_uz_uz"]
    list_select_related = ["book_type", "group", "type"]
    ordering = ["sort_order"]

    @display(description="Biletlar")
    def topics_link(self, obj):
        url = reverse("admin:tests_topics_changelist") + f"?book__id__exact={obj.pk}"
        return format_html('<a href="{}">biletlar →</a>', url)


@admin.register(Groups)
class GroupsAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "number", "type", "is_deleted"]
    list_filter = [dropdown("type"), "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru", "=number"]
    list_select_related = ["type"]
    ordering = ["sort_order"]


@admin.register(Types)
class TypesAdmin(ModelAdmin):
    list_display = ["name_uz_uz", "name_ru_ru", "sort_order", "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru"]
    ordering = ["sort_order"]


@admin.register(BookTypes)
class BookTypesAdmin(ModelAdmin):
    list_display = ["code", "name_uz_uz", "description"]
    search_fields = ["code", "name_uz_uz", "description"]
    ordering = ["sort_order"]


# =================================================================================================
# Yöl belgilari
# =================================================================================================
@admin.register(RoadSignCategories)
class RoadSignCategoriesAdmin(ModelAdmin):
    list_display = ["thumb", "name_uz_uz", "code", "sort_order", "is_deleted"]
    list_display_links = ["thumb", "name_uz_uz"]
    list_editable = ["sort_order", "is_deleted"]
    search_fields = ["name_uz_uz", "name_ru_ru", "code"]
    ordering = ["sort_order"]

    @display(description="Rasm")
    def thumb(self, obj):
        return _thumb(obj.image)


@admin.register(RoadSigns)
class RoadSignsAdmin(ModelAdmin):
    list_display = ["thumb", "number", "name_uz_uz", "category", "sort_order", "is_deleted"]
    list_display_links = ["thumb", "number", "name_uz_uz"]
    list_filter = [dropdown("category"), "is_deleted"]
    search_fields = ["number", "name_uz_uz", "name_ru_ru", "description_uz_uz"]
    list_select_related = ["category"]
    ordering = ["category__sort_order", "sort_order"]

    @display(description="Rasm")
    def thumb(self, obj):
        return _thumb(obj.image)
