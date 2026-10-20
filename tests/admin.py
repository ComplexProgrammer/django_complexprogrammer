from django.contrib import admin
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
# Register your models here.
# admin.site.register(Project)


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

    @admin.action(description="Izohni tasdiqlash (saytda ko'rsatish)")
    def approve_explanations(self, request, queryset):
        n = queryset.exclude(explanation_uz_uz="").update(explanation_status="approved")
        self.message_user(request, f"{n} ta izoh tasdiqlandi.")

    @admin.action(description="Izohni qoralamaga qaytarish (saytdan yashirish)")
    def reset_explanations(self, request, queryset):
        n = queryset.exclude(explanation_uz_uz="").update(explanation_status="draft")
        self.message_user(request, f"{n} ta izoh qoralamaga qaytarildi.")


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
