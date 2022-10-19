from django.test import TestCase

from products.models import Product
from users.models import User

import uuid


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_data = {
            "username": "erick",
            "password": "1234",
            "first_name": "erick",
            "last_name": "marchetti",
            "is_seller": True,
        }

        cls.instance_user_1 = User.objects.create(**cls.user_data)

        cls.product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.instance_product_1 = Product.objects.create(
            **cls.product_data, seller=cls.instance_user_1
        )

    def test_attributes_model_product(self):
        id = Product._meta.get_field("id")
        price = Product._meta.get_field("price")
        is_active = Product._meta.get_field("is_active")

        self.assertIs(id.default, uuid.uuid4)
        self.assertIs(id.primary_key, True)
        self.assertIs(id.editable, False)
        self.assertIs(price.max_digits, 10)
        self.assertIs(price.decimal_places, 2)
        self.assertIs(is_active.default, True)

    def test_attributes_model_product_arent_nullable(self):
        id = Product._meta.get_field("id")
        description = Product._meta.get_field("description")
        price = Product._meta.get_field("price")
        quantity = Product._meta.get_field("quantity")
        is_active = Product._meta.get_field("is_active")
        seller = Product._meta.get_field("seller")

        self.assertIs(id.null, False)
        self.assertIs(description.null, False)
        self.assertIs(price.null, False)
        self.assertIs(quantity.null, False)
        self.assertIs(is_active.null, False)
        self.assertIs(seller.null, False)
