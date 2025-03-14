from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('market/<int:market_id>/', views.store_list, name='store_list'),
    path('store/<int:store_id>/', views.product_list, name='product_list'),
]
