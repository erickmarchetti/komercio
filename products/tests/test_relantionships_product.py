from django.test import TestCase
from django.db.utils import IntegrityError

from products.models import Product
from users.models import User


class ProductRelantionshipsTest(TestCase):
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

        cls.product_instance_list = [
            Product.objects.create(**cls.product_data, seller=cls.instance_user_1)
            for _ in range(10)
        ]

    def test_error_if_seller_isnt_passed(self):
        with self.assertRaisesMessage(
            IntegrityError,
            'null value in column "seller_id" violates not-null constraint',
        ):
            Product.objects.create(
                **{
                    "description": "Smartband XYZ 3.0",
                    "price": 100.99,
                    "quantity": 15,
                }
            )

    def test_relantionships_many_to_one(self):
        for product in self.product_instance_list:
            self.assertIs(product.seller, self.instance_user_1)

    def test_relantionships_one_to_many(self):
        self.assertIs(len(self.instance_user_1.products.all()), 10)

        for product in self.product_instance_list:
            self.assertIn(product, self.instance_user_1.products.all())
