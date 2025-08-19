from rest_framework import serializers
from .models import Order, Shipment, Invoice, PrintInfo, PrintItem

# 주문목록
class OrderListSerializer(serializers.ModelSerializer):

    seller = serializers.CharField(source = 'seller.name', read_only=True)
    buyer = serializers.SerializerMethodField()
    receiver_name = serializers.CharField(source = 'shipment.receiver_name', read_only=True)
    shipment_type = serializers.CharField(source='shipment.shipment_type', read_only = True)
    invoice_number = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_state',
            'seller',
            'channel',
            'buyer',
            'receiver_name',
            'shipment_type',
            'invoice_numbers',
        ]
    
    def get_buyer(self, obj):
        return obj.buyer.name if obj.buyer else obj.buyer_name
    
    def get_invoice_numbers(self, obj):
        return [invoice.invoice_number for invoice in getattr(obj.shipment, 'prefetched_invoices', [])]