from django.db import models

# Create your models here.

# 입고정보
class Inbound(models.Model):

    INBOUND_TYPE_CHOICES = [
        ('inbound', '입고'),
        ('return', '반품'),
    ]

    inbound_type = models.CharField(max_length=10,choices=INBOUND_TYPE_CHOICES)
    product_option = models.ForeignKey('products.ProductOption',on_delete=models.CASCADE,related_name='inbounds')
    quantity = models.PositiveIntegerField(default=1)
    purchase_price = models.PositiveIntegerField(default=0)
    received_at = models.DateTimeField(auto_now_add=True)

    description = models.CharField(max_length=100,blank=True)

# 출고정보
class Outbound(models.Model):

    order = models.ForeignKey('orders.Order',on_delete=models.CASCADE,related_name='ordered_items')
    product_option = models.ForeignKey('products.ProductOption',on_delete=models.CASCADE,related_name='outbounds')
    price = models.PositiveIntegerField()
    
    quantity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=100,blank=True)