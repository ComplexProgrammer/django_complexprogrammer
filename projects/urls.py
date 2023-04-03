from django.urls import path
from .views import base, projects, project_item, instagram_downloader_, youtube_downloader_, coins, C0mplexTranslate, ImageCompare, avtotest

urlpatterns=[
    path('', base, name='base'),
    # path('cartoonize/', cartoonize, name='cartoonize' ),
    path('instagram-downloader/', instagram_downloader_, name='instagram_downloader_' ),
    path('youtube_downloader/', youtube_downloader_, name='youtube_downloader'),
    path('coins/', coins, name='coins'),
    path('translate/', C0mplexTranslate, name='translate'),
    path('imagecompare/', ImageCompare, name='imagecompare'),
    path('avtotest/', avtotest, name='avtotest'),
    path('projects/', projects, name='projects'),
    path('project/<int:id>/', project_item, name='item')
]
