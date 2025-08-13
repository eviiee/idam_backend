from django.db import models

# Create your models here.

# 판매처
class Channel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    fee = models.DecimalField(default=0,max_digits=4,decimal_places=2) # 수수료율, 퍼센트 수치를 그대로 입력 (예 : 9.8% => 9.8)

# 업체
class Company(models.Model):
    name = models.CharField(max_length=50, unique=True) # 업체명
    address = models.CharField(max_length=300,blank=True) # 주소
    contact = models.CharField(max_length=12,blank=True) # 전화번호
    biz_reg_num = models.CharField(max_length=10,blank=True) # 사업자번호

    
# 택배사
class Courier(models.Model):
    courier_name = models.CharField(max_length=20,unique=True)
    tracker_url = models.URLField()