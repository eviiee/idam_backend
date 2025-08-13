from django.db import models


from .enums import OrderState, PrintType, PrintState, ShipmentType



# 주문
class Order(models.Model):

    ordered_at = models.DateTimeField(auto_now_add=True) # 주문일시
    order_state = models.CharField(max_length=20,choices=OrderState.choices)
    channel = models.ForeignKey('partners.Channel', on_delete=models.CASCADE, related_name='orders') # 판매처
    buyer = models.ForeignKey('partners.Company', on_delete=models.CASCADE, related_name='purchased_orders') # 거래업체
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE, related_name='shipping_orders')

    deadline = models.DateField(blank=True,null=True)

# 인쇄정보
class PrintInfo(models.Model):

    print_name = models.CharField(max_length=50)

    print_type = models.CharField(max_length=20,choices=PrintType.choices)
    print_state = models.CharField(max_length=20,choices=PrintState.choices)

    from .utils import printUploadPath
    print_image = models.ImageField(upload_to=printUploadPath)
    print_design = models.FileField(upload_to=printUploadPath)

# 인쇄목록
class PrintItem(models.Model):

    print_info = models.ForeignKey('PrintInfo', on_delete=models.CASCADE, related_name='print_items')
    product_option = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

# 배송정보
class Shipment(models.Model):

    shipment_type = models.CharField(max_length=10,choices=ShipmentType.choices)

    # 발송인 정보
    shipper = models.ForeignKey('partners.Company',on_delete=models.CASCADE,related_name='shipments')
    shipper_name = models.CharField(max_length=50)
    shipper_contact = models.CharField(max_length=12,blank=True)
    shipper_contact_alt = models.CharField(max_length=12,blank=True)
    shipper_address = models.CharField(max_length=300,blank=True)

    # 수취인 정보
    receiver_name = models.CharField(max_length=30)
    receiver_contact = models.CharField(max_length=12)
    receiver_contact_alt = models.CharField(max_length=12,blank=True)
    receiver_address = models.CharField(max_length=300)
    receiver_message = models.CharField(max_length=100,blank=True)

    shipment_fee = models.PositiveSmallIntegerField(default=3000) # 배송비


# 송장
class Invoice(models.Model):
    shipment = models.ForeignKey('Shipment',on_delete=models.CASCADE,related_name='invoices')
    courier = models.ForeignKey('partners.Courier',on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=12)
