from django.db import models

# 주문상태
class OrderState(models.TextChoices):
    PENDING = 'pending', '결제대기'
    PAID = 'paid', '결제완료'
    PREPARING = 'preparing', '배송준비중'
    SHIPPED = 'shipped', '처리완료'

# 인쇄/각인
class PrintType(models.TextChoices):
    LASER = 'laser', '레이저 각인'
    COLOR = 'color', '컬러 인쇄'

# 인쇄 진행상황
class PrintState(models.TextChoices):
    PREPARING = 'preparing', '시안 확인중'
    PENDING = 'pending', '인쇄 대기'
    PRINTED = 'printed', '인쇄 완료'

# 배송 타입
class ShipmentType(models.TextChoices):
    COURIER = 'courier', '택배'
    QUICK = 'quick', '퀵/화물'
    DELIVER = 'deliver', '직배송'
    PICKUP = 'pickup', '방문수령'
    NONE = 'none', '배송없음'

# 결제 타입
class PurchaseType(models.TextChoices):
    CREDIT = 'credit', '신용거래'
    DEPOSIT = 'deposit', '무통장'
    
# 결제 상황
class PurchaseState(models.TextChoices):
    PENDING = 'pending', '입금 대기'
    RECEIVABLE = 'receivable', '미수금'
    PAID = 'paid', '결제완료'