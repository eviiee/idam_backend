# populate_dummy.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "canobox.settings")
django.setup()

from factories import UserFactory, ProductFactory, ProductOptionFactory, PhoneModelFactory, ProductTagFactory

# -------------------- Users --------------------
# users = UserFactory.create_batch(10)
# print(f"Users: {len(users)}개 생성")

# # -------------------- PhoneModels --------------------
# phone_models = PhoneModelFactory.create_batch(5)
# print(f"PhoneModels: {len(phone_models)}개 생성")

# # -------------------- Tags --------------------
# tags = ProductTagFactory.create_batch(10)
# print(f"Tags: {len(tags)}개 생성")

# -------------------- Products --------------------
products = ProductFactory.create_batch(20)
# print(f"Products: {len(products)}개 생성")

# -------------------- ProductOptions --------------------
options = []
for product in products:
    # 제품당 1~5개 옵션 생성
    opts = ProductOptionFactory.create_batch(fake.random_int(min=1, max=5), product=product)
    options.extend(opts)
print(f"ProductOptions: {len(options)}개 생성")

print("더미 데이터 생성 완료!")
