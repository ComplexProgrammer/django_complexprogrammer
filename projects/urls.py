from django.urls import path
from .views import base, projects, project_item

urlpatterns=[
    path('', base, name='base'),
    path('projects/', projects, name='projects'),
    path('project/<int:id>/', project_item, name='item')
]
