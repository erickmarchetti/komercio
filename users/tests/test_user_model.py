from django.test import TestCase
from users.models import User
import uuid


class UserModelTest(TestCase):
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

    def test_attributes_model_user(self):
        id = User._meta.get_field("id")
        username = User._meta.get_field("username")
        first_name = User._meta.get_field("first_name")
        last_name = User._meta.get_field("last_name")
        is_seller = User._meta.get_field("is_seller")

        self.assertIs(id.default, uuid.uuid4)
        self.assertIs(id.primary_key, True)
        self.assertIs(id.editable, False)
        self.assertIs(username.unique, True)
        self.assertIs(first_name.max_length, 50)
        self.assertIs(last_name.max_length, 50)
        self.assertIs(is_seller.default, False)

    def test_attributes_model_user_arent_nullable(self):
        id = User._meta.get_field("id")
        username = User._meta.get_field("username")
        first_name = User._meta.get_field("first_name")
        last_name = User._meta.get_field("last_name")
        is_seller = User._meta.get_field("is_seller")

        self.assertIs(id.null, False)
        self.assertIs(username.null, False)
        self.assertIs(first_name.null, False)
        self.assertIs(last_name.null, False)
        self.assertIs(is_seller.null, False)
