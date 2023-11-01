from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.tests, name='tests'),
]