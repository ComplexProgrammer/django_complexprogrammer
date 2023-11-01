from django.contrib import admin
from . models import Answers, Books, Groups, Questions, Topics
# Register your models here.
# admin.site.register(Project)


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number']
    list_filter=['name_en_us', 'number']
    search_fields=['name_en_us', 'number']
    ordering=['id']

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'book_type', 'group']
    list_filter=['name_en_us', 'book_type', 'group']
    search_fields=['name_en_us', 'book_type', 'group']
    ordering=['id']

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number', 'book']
    list_filter=['name_en_us', 'number', 'book']
    search_fields=['name_en_us', 'number', 'book']
    ordering=['id']

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number', 'topic', 'image']
    list_filter=['name_en_us', 'number', 'topic', 'image']
    search_fields=['name_en_us', 'number', 'topic', 'image']
    ordering=['id']
    
@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display=['name_en_us', 'number', 'question', 'image', 'right']
    list_filter=['name_en_us', 'number', 'question', 'image', 'right']
    search_fields=['name_en_us', 'number', 'question', 'image', 'right']
    ordering=['id']