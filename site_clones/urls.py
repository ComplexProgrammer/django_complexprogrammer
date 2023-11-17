from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uzinfobiz.ru/', views.uzinfobiz_ru, name='uzinfobiz.ru'),
    path('uzinterbiz.com/', views.uzinterbiz_com, name='uzinterbiz.com'),
    path('postda.uz/', views.postda_uz, name='postda.uz'),
]
