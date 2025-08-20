from django.urls import path
from . import views

app_name = 'arxiv'

urlpatterns = [
	path('arxiv/', views.archive_list, name='archive_list'),
]
