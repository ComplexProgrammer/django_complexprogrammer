from django.contrib import admin
from . models import Answers, AvtoTest, Books, Groups, Project, Questions, Topics
# Register your models here.
# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title', 'publish_time', 'status', 'order']
    list_filter=['status', 'created_time', 'publish_time']
    prepopulated_fields={'sub_title': ('title',)}
    date_hierarchy='publish_time'
    search_fields=['title', 'status']
    ordering=['order', 'status', 'publish_time']

@admin.register(AvtoTest)
class AvtoTestAdmin(admin.ModelAdmin):
    list_display=['savol', 'javob', 'bilet', 'raqam']
    list_filter=['bilet', 'raqam']
    search_fields=['savol', 'javob']
    ordering=['id']

@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number']
    list_filter=['name_uz_uz', 'number']
    search_fields=['name_uz_uz', 'number']
    ordering=['id']

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'book_type']
    list_filter=['name_uz_uz', 'book_type']
    search_fields=['name_uz_uz', 'book_type']
    ordering=['id']

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number']
    list_filter=['name_uz_uz', 'number']
    search_fields=['name_uz_uz', 'number']
    ordering=['id']

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number', 'image']
    list_filter=['name_uz_uz', 'number', 'image']
    search_fields=['name_uz_uz', 'number', 'image']
    ordering=['id']
    
@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'number', 'image', 'right']
    list_filter=['name_uz_uz', 'number', 'image', 'right']
    search_fields=['name_uz_uz', 'number', 'image', 'right']
    ordering=['id']