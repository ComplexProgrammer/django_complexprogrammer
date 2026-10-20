from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.tests, name="tests"),
    # Eski sahifa (tests/index3.html shabloni yo'q, doim 500 berardi)
    path("index/", RedirectView.as_view(url="/tests/", permanent=True), name="index"),
    path("GetGroups/", views.GetGroups, name="GetGroups"),
    path("GetBooks/", views.GetBooks, name="GetBooks"),
    path("GetTopics/", views.GetTopics, name="GetTopics"),
    path("GetQuestions/", views.GetQuestions, name="GetQuestions"),
    path("GetAnswers/", views.GetAnswers, name="GetAnswers"),
    path("GetCounts/", views.GetCounts, name="GetCounts"),
    path("GetAllData/", views.GetAllData, name="GetAllData"),
    path("GetRoadSigns/", views.GetRoadSigns, name="GetRoadSigns"),
    path("GetQuestionsByIds/", views.GetQuestionsByIds, name="GetQuestionsByIds"),
    # path('tests/<int:bilet>/', views.test_item, name='tests'),
]
