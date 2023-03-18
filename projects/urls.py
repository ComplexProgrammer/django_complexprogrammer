from django.urls import path
from .views import base, projects, project_item, cartoonize, instagram_downloader_

urlpatterns=[
    path('', base, name='base'),
    path('cartoonize/', cartoonize, name='cartoonize' ),
    path('instagram-downloader/', instagram_downloader_, name='instagram_downloader_' ),
    path('projects/', projects, name='projects'),
    path('project/<int:id>/', project_item, name='item')
]
