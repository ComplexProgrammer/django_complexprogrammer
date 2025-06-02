from django.urls import path
from . import views

urlpatterns = [
    path('add-comment/', views.add_comment, name='add_comment'),
]