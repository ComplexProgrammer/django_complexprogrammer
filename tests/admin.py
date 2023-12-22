from django.contrib import admin
from . models import Answers, Books, Groups, Questions, Topics, Types, BookTypes
# Register your models here.
# admin.site.register(Project)


@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display=['name_en_us']
    list_filter=['name_en_us']
    search_fields=['name_en_us']
    ordering=['sort_order']
@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number', 'type']
    list_filter=['name_en_us', 'number', 'type']
    search_fields=['name_en_us', 'number', 'type']
    ordering=['sort_order']

@admin.register(BookTypes)
class BookTypesAdmin(admin.ModelAdmin):
    list_display=['code', 'description']
    list_filter=['code', 'description']
    search_fields=['code', 'description']
    ordering=['sort_order']
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'type', 'group']
    list_filter=['name_en_us', 'type', 'group']
    search_fields=['name_en_us', 'type', 'group']
    ordering=['sort_order']

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number', 'book']
    list_filter=['name_en_us', 'number', 'book']
    search_fields=['name_en_us', 'number', 'book']
    ordering=['sort_order']

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number', 'topic', 'image']
    list_filter=['name_en_us', 'number', 'topic', 'image']
    search_fields=['name_en_us', 'number', 'topic', 'image']
    ordering=['sort_order']
    
@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number', 'question_id', 'question', 'image', 'right']
    list_filter=['name_en_us', 'number', 'question', 'image', 'right']
    search_fields=['name_en_us', 'number', 'question', 'image', 'right']
    ordering=['sort_order']