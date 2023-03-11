from django.urls import path
from .views import projects, project_item

urlpatterns=[
    path('projects/', projects, name='projects'),
    path('project/<int:id>/', project_item, name='item')
]
