from django.db import models

# 판매처
class Channel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    fee = models.DecimalField(default=0) # 수수료율, 퍼센트 수치를 그대로 입력 (예 : 9.8% => 9.8)

# 업체
class Company(models.Model):
    name = models.CharField(max_length=50, unique=True) # 업체명
    address = models.CharField(blank=True,null=True) # 주소
    contact = models.CharField(blank=True,null=True) # 전화번호
    biz_reg_num = models.CharField(blank=True,null=True) # 사업자번호

# 주문
class Order(models.Model):

    ORDER_STATE_CHOICES = [
        ('결제대기','결제대기'),
        ('결제완료','결제완료'),
        ('배송준비중','배송준비중'),
        ('배송중','배송중')
    ]

    orderd_at = models.DateTimeField(auto_now_add=True) # 주문일시
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE, related_name='orders') # 판매처
    buyer = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='orders') # 거래업체
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE, related_name='orders')

    deadline = models.DateField(blank=True)

# 인쇄정보
class PrintInfo(models.Model):

    PRINT_TYPE_CHOICES = [
        ('레이저각인','레이저각인'),
        ('컬러인쇄','컬러인쇄'),
    ]

    PRINT_STATE_CHOICES = [
        ('시안확인중','시안확인중'),
        ('인쇄대기','인쇄대기'),
        ('인쇄완료','인쇄완료'),
    ]

    print_type = models.CharField(choices=PRINT_TYPE_CHOICES)
    print_state = models.CharField(choices=PRINT_STATE_CHOICES)

    from datetime import datetime
    print_image = models.ImageField(upload_to=f'prints/{datetime.now().strftime('%y%m%d')}/')
    print_design = models.FileField(upload_to=f'prints/{datetime.now().strftime('%y%m%d')}/')

# 배송정보
class Shipment(models.Model):

    SHIPMENT_TYPE_CHOICES = [
        ('courier', '택배'),
        ('quick', '퀵/화물'),
        ('deliver', '직배송'),
        ('pickup', '방문수령'),
        ('none', '배송없음'),
    ]

    shipment_type = models.CharField(choices=SHIPMENT_TYPE_CHOICES)

    # 발송인 정보
    shipper = models.ForeignKey('Company',on_delete=models.CASCADE,related_name='shipments')
    shipper_name = models.CharField(max_length=50)
    shipper_contact = models.CharField(blank=True)
    shipper_contact_alt = models.CharField(blank=True,null=True)
    shipper_address = models.CharField(blank=True)

    # 수취인 정보
    receiver_name = models.CharField(max_length=30)
    receiver_contact = models.CharField()
    receiver_contact_alt = models.CharField(blank=True,null=True)
    receiver_address = models.CharField()
    receiver_message = models.CharField(blank=True, null=True)

    shipment_fee = models.PositiveSmallIntegerField(default=3000) # 배송비

# 택배사
class Courier(models.Model):
    courier_name = models.CharField(unique=True)
    tracker_url = models.CharField()

# 송장
class Invoice(models.Model):
    shipment = models.ForeignKey('Shipment',on_delete=models.CASCADE,related_name='invoices')
    courier = models.ForeignKey('Courier',on_delete=models.CASCADE)
    invoice_number = models.CharField()

# 입고정보
class Inbound(models.Model):

    INBOUND_TYPE_CHOICES = [
        ('inbound', '입고'),
        ('return', '반품'),
    ]

    inbound_type = models.CharField(choices=INBOUND_TYPE_CHOICES)
    sku = models.ForeignKey('ProductOption',on_delete=models.CASCADE,related_name='inbounds')
    quantity = models.PositiveIntegerField(default=1)
    purchase_price = models.PositiveIntegerField(default=0)
    received_at = models.DateTimeField(auto_now_add=True)

# 출고정보
class Outbound(models.Model):

    order = models.ForeignKey('Order',on_delete=models.CASCADE,related_name='items')
    sku = models.ForeignKey('ProductOption',on_delete=models.CASCADE,related_name='outbounds')
    price = models.PositiveIntegerField()