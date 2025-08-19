# factories.py
import factory
from faker import Faker
from users.models import User
from products.models import Product, ProductOption, ProductTag, PhoneModel

fake = Faker()

# -------------------- User Factory --------------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: fake.user_name())
    email = factory.LazyAttribute(lambda x: fake.email())
    name = factory.LazyAttribute(lambda x: fake.name())
    is_corporate = factory.LazyAttribute(lambda x: fake.boolean())

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        obj.set_password('password123')
        if create:
            obj.save()

# -------------------- PhoneModel Factory --------------------
class PhoneModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhoneModel

    model_type = factory.LazyAttribute(lambda x: fake.random_element(['갤럭시', '아이폰']))
    model_name = factory.LazyAttribute(lambda x: fake.word().title())
    model_number = factory.LazyAttribute(lambda x: fake.bothify(text='??###').upper())

# -------------------- ProductTag Factory --------------------
class ProductTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductTag

    name = factory.LazyAttribute(lambda x: fake.unique.word().title())

# -------------------- Product Factory --------------------
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_name = factory.LazyAttribute(lambda x: fake.word().title())
    product_alias = factory.LazyAttribute(lambda x: fake.word().title())
    use_options = factory.LazyAttribute(lambda x: fake.boolean())
    use_phone_models = factory.LazyAttribute(lambda x: fake.boolean())
    option1 = factory.LazyAttribute(lambda x: "기종" if x.use_phone_models else "색상")
    option2 = factory.LazyAttribute(lambda x: "색상" if x.use_phone_models else None)
    option3 = None
    detail_image = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=100))
    purchase_link = factory.LazyAttribute(lambda x: fake.url())
    engravable = factory.LazyAttribute(lambda x: fake.boolean())
    printable = factory.LazyAttribute(lambda x: fake.boolean())

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        if not create:
            return
        # 랜덤 1~3개의 태그 연결
        tags = ProductTagFactory.create_batch(fake.random_int(min=1, max=3))
        obj.tags.set(tags)

# -------------------- ProductOption Factory --------------------
class ProductOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductOption

    product = factory.SubFactory(ProductFactory)
    phone_model = factory.SubFactory(PhoneModelFactory)
    option1 = factory.LazyAttribute(lambda x: fake.color_name())
    option2 = factory.LazyAttribute(lambda x: fake.color_name())
    option3 = factory.LazyAttribute(lambda x: fake.word())
    stock = factory.LazyAttribute(lambda x: fake.random_int(min=0, max=100))
    inbound_price = factory.LazyAttribute(lambda x: fake.random_int(min=1000, max=50000))
    price = factory.LazyAttribute(lambda x: fake.random_int(min=5000, max=100000))
