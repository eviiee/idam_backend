from django.db import models
from django.forms import ValidationError
from django.utils.html import format_html

# 휴대폰 기종
class PhoneModel(models.Model):
    MODEL_TYPE_CHOICES = [
       ('갤럭시', "갤럭시"),
        ('아이폰', "아이폰"),
    ]

    model_type = models.CharField(max_length=10, choices=MODEL_TYPE_CHOICES)
    model_name = models.CharField(max_length=50) # 예: S25 Ultra, S25, 플립7 등
    model_number = models.CharField(max_length=10, blank=True) # 예: G938, F977 등

    order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('model_type', 'model_name')
        ordering = ['model_type', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=["model_number"],
                condition=~models.Q(model_number=""),
                name="unique_code_when_not_blank",
            )
        ]

    # def clean(self):
    #     super().clean()
    #     if self.code != "" and PhoneModel.objects.filter(code=self.code).exclude(pk=self.pk).exists():
    #         raise ValidationError({"code":"이미 존재하는 모델 번호입니다"})

    def __str__(self):
        return f"{self.model_type} {self.model_name}{f' ({self.model_number})' if self.model_number else ''}"
    
    # 모델번호는 대문자로 고정
    def save(self, *args, **kwargs):
        if self.model_number:
            self.model_number = self.model_number.upper()
        super().save(*args,**kwargs)


# 추가이미지
class ProductImages(models.Model):
    product = models.ForeignKey('Product', related_name='additional_images', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='media/product/thumbnails/')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.product_name} 이미지 {self.order}"
    

# 상품
class Product(models.Model):
    product_name = models.CharField(max_length=50) # 상품명
    product_alias = models.CharField(max_length=20) # 상품명 (송장용)

    use_options = models.BooleanField(default=False) # 옵션 사용여부
    use_phone_models = models.BooleanField(default=False) # 휴대폰 모델 옵션 사용여부

    # 옵션1 명칭
    option1 = models.CharField(max_length=50, blank=True, null=True)

    # 옵션2 명칭
    option2 = models.CharField(max_length=50, blank=True, null=True)

    # 옵션3 명칭
    option3 = models.CharField(max_length=50, blank=True, null=True)

    thumbnail = models.ImageField(upload_to='media/products/thumbnails/') # 대표이미지
    thumbnail_hover = models.ImageField(upload_to='media/products/thumbnails/', null=True, blank=True) # 마우스 호버시 대표이미지

    detail_image = models.TextField() # 상세페이지 (에디터로 작성)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField("ProductTag", related_name='products', blank=True)

    purchase_link = models.URLField(blank=True,null=True) # 구매 페이지 링크

    engravable = models.BooleanField(default=False) # 각인 가능 여부
    printable = models.BooleanField(default=False) # 인쇄 가능 여부

    def thumbnail_tag(self):
        if self.thumbnail:
            return format_html('<img src="{}" style="width:80px;"/>', self.thumbnail.url)
        return "-"
    thumbnail_tag.short_description = '대표이미지 미리보기'

    class Meta:
        verbose_name_plural = "상품 목록"

    def __str__(self):
        return self.product_name
    

# 상품 옵션 (SKU)
class ProductOption(models.Model):

    product = models.ForeignKey('Product', related_name='options', on_delete=models.CASCADE) # 이 SKU가 종속된 Product
    phone_model = models.ForeignKey('ProductPhoneModelOption',blank=True,null=True, on_delete=models.CASCADE) # 휴대폰 기종을 사용하는 Product의 Option일 경우, 해당하는 기종 - 미사용시 null

    option1 = models.CharField(max_length=20, blank=True, null=True) # 옵션1 값
    option2 = models.CharField(max_length=20, blank=True, null=True) # 옵션2 값
    option3 = models.CharField(max_length=20, blank=True, null=True) # 옵션3 값

    stock = models.IntegerField(default=0) # 현 재고
    inbound_price = models.PositiveIntegerField() # 입고가
    price = models.PositiveIntegerField() # 판매가

    def __str__(self):
        parts = [self.product.product_alias]
        if self.phone_model:
            parts.append(str(self.phone_model))
        if self.option1:
            parts.append(self.option1)
        if self.option2:
            parts.append(self.option2)
        if self.option3:
            parts.append(self.option3)
        return " ".join(parts)
    
    class Meta:
        verbose_name = "옵션"
        verbose_name_plural = "옵션 목록"
        
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # 휴대폰 기종을 쓰는 Product인데 기종이 없는 경우
        if self.product.use_phone_models and not self.phone_model:
            raise ValidationError("기종을 한 개 이상 선택해주세요")
        
        # 반대로 휴대폰 기종을 안 쓰는데 값이 들어간 경우
        if not self.product.use_phone_models and self.phone_model:
            raise ValidationError("이 상품은 휴대폰 기종을 사용하지 않습니다.")

    
    
# 분류 태그
class ProductTag(models.Model):
    name = models.CharField(max_length=50, unique=True) # 태그명
    
    class Meta:
        ordering = ['name']  # 태그를 이름순 정렬
        verbose_name = "태그"
        verbose_name_plural = "태그 목록"

    def __str__(self):
        return self.name
    

# Product 종속 PhoneModel 리스트
class ProductPhoneModelOption(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='phone_model_options')
    compatible_phone_models = models.ManyToManyField(
        PhoneModel,
        through='CompatiblePhoneModel',
        related_name='product_phone_model_options'
    )

# ProductPhoneModels - PhoneModel 중개 클래스
class CompatiblePhoneModel(models.Model):
    phone_model_option = models.ForeignKey(
        ProductPhoneModelOption,
        related_name="phone_models",
        on_delete=models.CASCADE
    )
    phone_model = models.ForeignKey(PhoneModel, on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['product_phone_model_option', 'phone_model'],
    #             name='unique_product_phone_model'
    #         )
    #     ]
    
    # def validate_unique(self, exclude = None):
    #     super().validate_unique(exclude)
    #     product = self.product_phone_model_option.product
    #     phone_model = self.phone_model
    #     exists = ProductPhoneModelOption.objects.filter(
    #         product_phone_model_option__product=product,
    #         phone_model=phone_model,
    #     ).exclude(product_phone_model_option=self.product_phone_model_option).exists()

    #     if exists: raise ValidationError("중복 기종입니다")