from django.contrib import admin
from django.urls import path, include
import products.views as views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', views.ProductListAdmin.as_view(), name='product-list'),
    path('phone-models/', views.PhoneModels.as_view(), name='phone-models'),
    path('phone-models-admin/', views.PhoneModelsAdmin.as_view(), name='phone-models'),

    # 관리자용 상품 등록 / 수정 / 상세조회
    path('admin/', include(router.urls))
]

