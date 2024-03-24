from django.urls import path
from . import views

urlpatterns = [
    path('', views.tests, name='tests'),
    path('index/', views.index, name='index'),
    path('GetGroups/', views.GetGroups, name='GetGroups'),
    path('GetBooks/', views.GetBooks, name='GetBooks'),
    path('GetTopics/', views.GetTopics, name='GetTopics'),
    path('GetQuestions/', views.GetQuestions, name='GetQuestions'),
    path('GetAnswers/', views.GetAnswers, name='GetAnswers'),
    path('GetCounts/', views.GetCounts, name='GetCounts'),
    path('GetAllData/', views.GetAllData, name='GetAllData'),
    # path('tests/<int:bilet>/', views.test_item, name='tests'),
]