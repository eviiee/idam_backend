from rest_framework import serializers
from .models import CompatiblePhoneModel, PhoneModel, Product, ProductImages, ProductOption, ProductPhoneModelOption, ProductTag

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

class ProductPhoneModelOptionSerializer(serializers.Serializer):

    compatible_phone_models = PhoneModelSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ProductPhoneModelOption
        fields = ['id', 'compatible_phone_models']

class ProductSerializerAdmin(serializers.Serializer):

    available_phone_models = serializers.SerializerMethodField()
    min_purchase_price = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_available_phone_models(self, obj):
        phone_model_ids = set()
        for ppo in obj.phone_model_options.all():
            for cpm in ppo.compatible_phone_models.all():
                phone_model_ids.add(cpm)
        return phone_model_ids
    
    def get_min_purchase_price(self, obj):
        purchase_prices = set()
        for po in obj.product_options.all():
            purchase_prices.add(po.inbound_price)
        return min(purchase_prices)
    
    def get_min_price(self, obj):
        prices = set()
        for po in obj.product_options.all():
            prices.add(po.price)
        return min(prices)



from django.db import transaction

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ["id", "order", "image"]


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ["id", "name"]

class PhoneModelNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneModel
        fields = ['id', 'model_type', 'model_name', 'model_number']


class CompatiblePhoneModelSerializer(serializers.ModelSerializer):
    # phone_model을 id로만 받음
    phone_model = serializers.PrimaryKeyRelatedField(
        queryset=PhoneModel.objects.all()
    )

    class Meta:
        model = CompatiblePhoneModel
        fields = ['phone_model']


class ProductPhoneModelOptionSerializer(serializers.ModelSerializer):
    compatible_phone_models = CompatiblePhoneModelSerializer(many=True)

    class Meta:
        model = ProductPhoneModelOption
        fields = ['id', 'product', 'compatible_phone_models']

    def create(self, validated_data):
        comps_data = validated_data.pop('compatible_phone_models', [])
        product = self.context.get('product')
        instance = ProductPhoneModelOption.objects.create(**validated_data)
        
        for comp_data in comps_data:
            # comp_data는 이제 {'phone_model': PhoneModel instance} 형태
            CompatiblePhoneModel.objects.create(
                phone_model=comp_data['phone_model'],
                phone_model_option=instance
            )
        return instance


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ["id", "phone_model", "option1", "option2", "option3", "stock", "inbound_price", "price"]


class ProductSerializer(serializers.ModelSerializer):

    tags = ProductTagSerializer(many=True, required=False)
    additional_images = ProductImagesSerializer(many=True, required=False)
    options = ProductOptionSerializer(many=True, required=False)
    phone_model_options = ProductPhoneModelOptionSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id", "product_name", "product_alias", "use_options", "use_phone_models",
            "option1", "option2", "option3", "thumbnail", "thumbnail_hover",
            "detail_image", "tags", "additional_images", "options", "phone_model_options",
            "purchase_link", "engravable", "printable", "created_at", "updated_at"
        ]

    def create(self, validated_data):

        tags_data = validated_data.pop("tags", [])
        images_data = validated_data.pop("additional_images", [])
        phone_models_data = validated_data.pop("phone_model_options", [])
        options_data = validated_data.pop("options", [])

        with transaction.atomic():
            product = Product.objects.create(**validated_data)

            phone_model_map = {}

            # Tags
            for tag in tags_data:
                tag_obj, _ = ProductTag.objects.get_or_create(name=tag["name"])
                product.tags.add(tag_obj)

            # Images
            for img in images_data:
                ProductImages.objects.create(product=product, **img)

            # PhoneModelOptions
            for pm_data in phone_models_data:
                temp_id = pm_data.pop("temp_id", None)
                compatible_data = pm_data.pop("compatible_phone_models", [])
                pm_option = ProductPhoneModelOption.objects.create(product=product, **pm_data)
                phone_model_map[temp_id] = pm_option

                for comp in compatible_data:
                    CompatiblePhoneModel.objects.create(
                        phone_model_option=pm_option,
                        phone_model=comp["phone_model"]
                    )

            print(phone_model_map)

            # Options
            for opt in options_data:
                phone_model_temp_id = opt.pop("phone_model_temp", None)
                if phone_model_temp_id:
                    opt["phone_model"] = phone_model_map.get(phone_model_temp_id)
                ProductOption.objects.create(product=product, **opt)

        return product

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        images_data = validated_data.pop("additional_images", [])
        options_data = validated_data.pop("options", [])
        phone_models_data = validated_data.pop("phone_model_options", [])

        with transaction.atomic():
            # 기본 필드 업데이트
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Tags 갱신
            if tags_data:
                tag_objs = [ProductTag.objects.get_or_create(name=tag["name"])[0] for tag in tags_data]
                instance.tags.set(tag_objs)

            # Images 갱신 (싹 갈아엎는 방식)
            if images_data:
                instance.additional_images.all().delete()
                for img in images_data:
                    ProductImages.objects.create(product=instance, **img)

            # PhoneModelOptions 갱신
            if phone_models_data:
                instance.phone_model_options.all().delete()
                for pm_data in phone_models_data:
                    compatible_data = pm_data.pop("compatible_phone_models", [])
                    pm_option = ProductPhoneModelOption.objects.create(product=instance, **pm_data)
                    for comp in compatible_data:
                        CompatiblePhoneModel.objects.create(
                            phone_model_option=pm_option,
                            phone_model=comp["phone_model"]
                        )

            # Options 갱신
            if options_data:
                instance.options.all().delete()
                for opt in options_data:
                    ProductOption.objects.create(product=instance, **opt)

        return instance
