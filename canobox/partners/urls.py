from django.contrib import admin
from django.urls import path
import partners.views as views

urlpatterns = [
    path('company/', views.CompanyAdminAPI.as_view(), name='company'),
    path('companies/', views.CompaniesAdminAPI.as_view(), name='companies'),
]

