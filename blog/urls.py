from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="blog"),
    path("rss/", views.LatestPostsFeed(), name="blog_rss"),
    path("<slug:slug>/", views.detail, name="blog_post"),
]
