from rest_framework import serializers
from .models import PhoneModel, Product, ProductImages, ProductOption, ProductTag

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = '__all__'

# 필수정보 API
class PhoneModelSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()

    class Meta:
        model=PhoneModel
        fields = ['id','model_type','display_name']
    
    def get_display_name(self, obj):
        return str(obj)

# 관리자용 수정용 상세 API
class PhoneModelSerializerAdmin(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()

    class Meta:
        model=PhoneModel
        fields = '__all__'
    
    def get_display_name(self, obj):
        return str(obj)

