from django.contrib import admin
from . models import Answers, Books, Groups, Questions, Topics, Types, BookTypes
# Register your models here.
# admin.site.register(Project)


@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz']
    list_filter=['name_uz_uz']
    search_fields=['name_uz_uz']
    ordering=['sort_order']
@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number', 'type']
    list_filter=['name_uz_uz', 'number', 'type']
    search_fields=['name_uz_uz', 'number', 'type']
    ordering=['sort_order']

@admin.register(BookTypes)
class BookTypesAdmin(admin.ModelAdmin):
    list_display=['code', 'description']
    list_filter=['code', 'description']
    search_fields=['code', 'description']
    ordering=['sort_order']
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display=['book_type', 'type', 'group']
    list_filter=['book_type', 'type', 'group']
    search_fields=['book_type', 'type', 'group']
    ordering=['sort_order']

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number', 'type', 'group', 'book']
    list_filter=['name_uz_uz', 'number', 'type', 'group', 'book']
    search_fields=['name_uz_uz', 'number', 'type', 'group', 'book']
    ordering=['sort_order']

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number', 'type', 'group', 'book', 'topic', 'image']
    list_filter=['name_uz_uz', 'number', 'type', 'group', 'book', 'topic', 'image']
    search_fields=['name_uz_uz', 'number', 'type', 'group', 'book', 'topic', 'image']
    ordering=['sort_order']
    
@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number', 'question_id', 'type', 'group', 'book', 'topic', 'question', 'image', 'right']
    list_filter=['name_uz_uz', 'number', 'type', 'group', 'book', 'topic', 'question', 'image', 'right']
    search_fields=['name_uz_uz', 'number', 'type', 'group', 'book', 'topic', 'question', 'image', 'right']
    ordering=['sort_order']