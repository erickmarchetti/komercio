from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

from users.models import User

from mocks.user import (
    data_seller,
    data_adm_user,
)
from mocks.product import mocked_product


class ProductRoutesTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_list_create_url = reverse("user_list_create")
        cls.login_url = reverse("login")
        cls.product_list_create_url = reverse("product_list_create")

        user_adm = User.objects.create_superuser(**data_adm_user)
        user_seller = User.objects.create_user(**data_seller)

        cls.token_adm = Token.objects.get_or_create(user=user_adm)[0]
        cls.token_seller = Token.objects.get_or_create(user=user_seller)[0]

    def test_can_create_a_product(self):

        expected_fields_in_body = {
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        }

        expected_fields_in_seller = {
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        response_OK = self.client.post(self.product_list_create_url, mocked_product)

        for key in expected_fields_in_body:
            self.assertIn(key, response_OK.json())

        for key in expected_fields_in_seller:
            self.assertIn(key, response_OK.json().get("seller"))

        self.assertIs(response_OK.status_code, status.HTTP_201_CREATED)

    def test_errors_create_product_non_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_adm.key)

        response_non_seller = self.client.post(
            self.product_list_create_url, mocked_product
        )

        self.assertEqual(
            response_non_seller.json(),
            {"detail": "You do not have permission to perform this action."},
        )
        self.assertIs(response_non_seller.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        response_without_fields = self.client.post(self.product_list_create_url)

        required_fields = {
            "description",
            "price",
            "quantity",
        }

        for key in required_fields:
            self.assertIn(
                "This field is required.",
                response_without_fields.json().get(
                    key, "campo não foi retornado no body"
                ),
                f"campo {key} é obrigatório",
            )
        self.assertIs(response_without_fields.status_code, status.HTTP_400_BAD_REQUEST)

        response_negative_quantity = self.client.post(
            self.product_list_create_url, {**mocked_product, "quantity": -5}
        )

        self.assertIn(
            "Ensure this value is greater than or equal to 0.",
            response_negative_quantity.json().get("quantity"),
        )
        self.assertIs(
            response_negative_quantity.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_can_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        product_test = self.client.post(self.product_list_create_url, mocked_product)

        response_OK = self.client.patch(
            f"/api/products/{product_test.json().get('id')}/",
            {"description": "Um rpg de mesa de demon slayer Update"},
        )

        self.assertEqual(
            response_OK.json().get("description"),
            "Um rpg de mesa de demon slayer Update",
        )
        self.assertIs(response_OK.status_code, status.HTTP_200_OK)

    def test_errors_update_a_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        product_test = self.client.post(self.product_list_create_url, mocked_product)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_adm.key)

        response_other_user_try_update = self.client.patch(
            f"/api/products/{product_test.json().get('id')}/",
            {"description": "Um rpg de mesa de demon slayer Update"},
        )

        self.assertEqual(
            response_other_user_try_update.json(),
            {"detail": "You do not have permission to perform this action."},
        )
        self.assertIs(
            response_other_user_try_update.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_anyone_can_list_and_filter_products(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        product_test = self.client.post(self.product_list_create_url, mocked_product)

        self.client.credentials()

        expected_fields = {
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        }

        response_Ok_list = self.client.get(self.product_list_create_url)

        self.assertIs(type(response_Ok_list.json().get("results")), list)
        self.assertIs(response_Ok_list.json().get("count"), 1)
        self.assertIs(response_Ok_list.status_code, status.HTTP_200_OK)

        item_to_test = response_Ok_list.json().get("results")[0]

        for key in item_to_test.keys():
            self.assertIn(
                key,
                expected_fields,
                f"{key} não deve ser retornado no body da response",
            )

        for field in expected_fields:
            self.assertIn(
                field, item_to_test, f"{field} deve ser mostrada no body da response"
            )

        response_Ok_filtered = self.client.get(
            f"/api/products/{product_test.json().get('id')}/"
        )

        self.assertIs(response_Ok_filtered.status_code, status.HTTP_200_OK)
