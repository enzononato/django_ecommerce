from django.urls import path
from .views import product_list, product_detail
from . import views

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
