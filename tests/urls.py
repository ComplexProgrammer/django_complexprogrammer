from django.urls import path
from . import views

urlpatterns = [
    path('', views.tests, name='tests'),
    path('index/', views.index, name='index'),
    path('GetGroups/', views.GetGroups, name='GetGroups'), # type: ignore
    path('GetBooks/', views.GetBooks, name='GetBooks'), # type: ignore
    path('GetTopics/', views.GetTopics, name='GetTopics'), # type: ignore
    path('GetQuestions/', views.GetQuestions, name='GetQuestions'), # type: ignore
    path('GetAnswers/', views.GetAnswers, name='GetAnswers'), # type: ignore
    path('GetCounts/', views.GetCounts, name='GetCounts'), # type: ignore
    path('GetAllData/', views.GetAllData, name='GetAllData'), # type: ignore
    # path('tests/<int:bilet>/', views.test_item, name='tests'),
]