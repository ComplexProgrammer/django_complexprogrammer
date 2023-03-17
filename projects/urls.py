from django.urls import path
from .views import base, projects, project_item, cartoonize

urlpatterns=[
    path('', base, name='base'),
    path('cartoonize/', cartoonize, name='cartoonize' ),
    path('projects/', projects, name='projects'),
    path('project/<int:id>/', project_item, name='item')
]
