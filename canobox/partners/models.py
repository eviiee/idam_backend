from django.db import models

# Create your models here.

# 판매처
class Channel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    fee = models.DecimalField(default=0,max_digits=4,decimal_places=2) # 수수료율, 퍼센트 수치를 그대로 입력 (예 : 9.8% => 9.8)

    # 엑셀 파일명 정규식
    excel_file_name = models.CharField(max_length=100, blank=True)

    # 엑셀 정보
    excel_sheet_num = models.PositiveSmallIntegerField(blank=True,null=True)
    excel_start_row = models.PositiveSmallIntegerField(blank=True,null=True)
    order_id_column = models.PositiveSmallIntegerField(blank=True,null=True)
    product_name_column = models.PositiveSmallIntegerField(blank=True,null=True)
    product_option_column = models.PositiveSmallIntegerField(blank=True, null=True)
    product_code_column = models.PositiveSmallIntegerField(blank=True, null=True)
    price_column = models.PositiveSmallIntegerField(blank=True, null=True)
    quantity_column = models.PositiveSmallIntegerField(blank=True, null=True)
    total_price_column = models.PositiveSmallIntegerField(blank=True, null=True)
    ordered_at_column = models.PositiveSmallIntegerField(blank=True, null=True)
    buyer_name_column = models.PositiveSmallIntegerField(blank=True, null=True)
    buyer_contact_column = models.PositiveSmallIntegerField(blank=True, null=True)
    buyer_message_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_name_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_contact_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_contact_alt_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_zip_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_address_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_message_column = models.PositiveSmallIntegerField(blank=True, null=True)
    invoice_column = models.PositiveSmallIntegerField(blank=True, null=True)
    fee_column = models.PositiveSmallIntegerField(blank=True, null=True)

    # 발송 엑셀 정보
    s_order_id_column = models.PositiveSmallIntegerField(blank=True,null=True)
    s_invoice_column = models.PositiveSmallIntegerField(blank=True, null=True)
    s_courier_column = models.PositiveSmallIntegerField(blank=True, null=True)


# 업체
class Company(models.Model):
    name = models.CharField(max_length=50, unique=True) # 업체명
    address = models.CharField(max_length=300,blank=True) # 주소
    email = models.EmailField(blank=True) # 이메일
    contact = models.CharField(max_length=12,blank=True) # 전화번호
    biz_reg_num = models.CharField(max_length=10,blank=True) # 사업자번호


# 택배사
class Courier(models.Model):
    courier_name = models.CharField(max_length=20,unique=True)
    tracker_url = models.URLField()

    # 수취 엑셀 정보
    key_column = models.PositiveSmallIntegerField(blank=True, null=True)
    invoice_column = models.PositiveSmallIntegerField(blank=True, null=True)

    # 발송 엑셀 정보
    sender_name_column = models.PositiveSmallIntegerField(blank=True, null=True)
    sender_contact_column = models.PositiveSmallIntegerField(blank=True, null=True)
    sender_address_column = models.PositiveSmallIntegerField(blank=True, null=True)
    
    receiver_name_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_contact_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_contact_alt_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_address_column = models.PositiveSmallIntegerField(blank=True, null=True)
    receiver_message_column = models.PositiveSmallIntegerField(blank=True, null=True)

    shipment_key_column = models.PositiveSmallIntegerField(blank=True, null=True) # 묶음배송 키

    product_name_column = models.PositiveSmallIntegerField(blank=True, null=True)
    product_quantity_column = models.PositiveSmallIntegerField(blank=True, null=True)
    box_count_column = models.PositiveSmallIntegerField(blank=True, null=True)

