from django.urls import path
from . import views

urlpatterns = [
    path('pdf_tools/', views.index, name='pdf_tools'), # type: ignore
]