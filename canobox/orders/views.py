from rest_framework import generics

from permissions import IsAdminOrSuperUser
from .models import Order
from .serializers import OrderListSerializer
from django.shortcuts import render

# Create your views here.
class OrderListAdmin(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAdminOrSuperUser]
    queryset = Order.objects.select_related(
        'seller', 'buyer', 'shipment', 'channel'
    ).prefetch_related(
        'shipment__invoices'
    )

    def get_queryset(self):
        qs = super().get_queryset()
        for order in qs:
            order.shipment.prefetched_invoices = list(order.shipment.invoices.all())
        return qs