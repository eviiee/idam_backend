from django.contrib import admin
from django.urls import path
import products.views as views

urlpatterns = [
    path('', views.ProductListAdmin.as_view(), name='product-list'),
    path('phone-models/', views.PhoneModels.as_view(), name='phone-models')
]

