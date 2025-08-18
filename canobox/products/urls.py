from django.contrib import admin
from django.urls import path
from products.views import ProductListAdmin

urlpatterns = [
    path('', ProductListAdmin.as_view(), name='product-list')
]

