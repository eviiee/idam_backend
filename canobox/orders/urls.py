from django.urls import path
import orders.views as views

urlpatterns = [
    path('list-admin/', views.OrderListAdmin.as_view(), name='order-list-admin'),
]

