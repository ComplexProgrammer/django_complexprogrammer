from django.contrib import admin
from .models import Posts

@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display=['name_uz_uz', 'title_uz_uz']
    list_filter=['name_en_us', 'name_ru_ru', 'name_uz_crl', 'name_uz_uz', 'title_en_us', 'title_ru_ru', 'title_uz_crl', 'title_uz_uz', 'body_en_us', 'body_ru_ru', 'body_uz_crl', 'body_uz_uz']
    search_fields=['name_en_us', 'name_ru_ru', 'name_uz_crl', 'name_uz_uz', 'title_en_us', 'title_ru_ru', 'title_uz_crl', 'title_uz_uz', 'body_en_us', 'body_ru_ru', 'body_uz_crl', 'body_uz_uz']
    ordering=['id']