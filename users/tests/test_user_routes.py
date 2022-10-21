from urllib import response
from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse

from users.models import User

from .mocks.user import (
    data_seller,
    data_common_user,
    data_adm_user,
    login_seller,
    login_common_user,
    login_adm_user,
)

import ipdb


class UserModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_list_create_url = reverse("user_list_create")
        cls.login_url = reverse("login")

        cls.adm_user = User.objects.create_superuser(**data_adm_user)

    def test_can_create_a_seller(self):
        response_OK = self.client.post(self.user_list_create_url, data_seller)

        expected_fields = {
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "is_superuser",
            "is_active",
            "date_joined",
        }

        for key in expected_fields:
            self.assertIn(key, response_OK.json())

        self.assertNotIn("password", response_OK.json())

        self.assertEqual(response_OK.json().get("is_seller"), True)
        self.assertEqual(response_OK.json().get("is_superuser"), False)

        self.assertIs(response_OK.status_code, status.HTTP_201_CREATED)

    def test_can_create_a_common_user(self):
        response_OK = self.client.post(self.user_list_create_url, data_common_user)

        self.assertEqual(response_OK.data.get("is_seller"), False)
        self.assertEqual(response_OK.data.get("is_superuser"), False)
        self.assertIs(response_OK.status_code, status.HTTP_201_CREATED)

    def test_errors_in_create_user(self):
        self.client.post(self.user_list_create_url, data_common_user)
        response_with_repeat_user = self.client.post(
            self.user_list_create_url, data_common_user
        )

        response_without_fields = self.client.post(self.user_list_create_url)

        required_fields = {
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
        }

        self.assertIs(response_without_fields.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIs(
            response_with_repeat_user.status_code, status.HTTP_400_BAD_REQUEST
        )

        for key in required_fields:
            self.assertIn(
                "This field is required.",
                response_without_fields.json().get(
                    key, "campo não foi retornado no body"
                ),
                f"campo {key} é obrigatório",
            )

        self.assertIn(
            "user with this username already exists.",
            response_with_repeat_user.json().get("username"),
        )

    def test_can_take_token_with_login(self):
        self.client.post(self.user_list_create_url, data_seller)
        self.client.post(self.user_list_create_url, data_common_user)

        response_login_seller = self.client.post(self.login_url, login_seller)
        response_login_commom_user = self.client.post(self.login_url, login_common_user)

        self.assertIn("token", response_login_seller.json())
        self.assertIn("token", response_login_commom_user.json())
        self.assertIs(response_login_seller.status_code, status.HTTP_200_OK)
        self.assertIs(response_login_commom_user.status_code, status.HTTP_200_OK)

    def test_errors_in_login(self):
        response_without_fields = self.client.post(self.login_url)
        response_wrong_email_or_password = self.client.post(
            self.login_url,
            {
                "username": "random_username",
                "password": "random_password",
            },
        )

        required_fields = {
            "username",
            "password",
        }

        for key in required_fields:
            self.assertIn(
                "This field is required.",
                response_without_fields.json().get(
                    key, "campo não foi retornado no body"
                ),
                f"campo {key} é obrigatório",
            )

        self.assertEqual(
            {"detail": "invalid username or password"},
            response_wrong_email_or_password.json(),
        )

        self.assertIs(
            response_without_fields.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIs(
            response_wrong_email_or_password.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_just_owner_can_update_account(self):
        seller = self.client.post(self.user_list_create_url, data_seller)

        token_seller = self.client.post(self.login_url, login_seller)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token_seller.json().get("token")
        )

        response_OK = self.client.patch(
            f"/api/accounts/{seller.json().get('id')}/",
            {"username": "erick updated"},
        )

        self.assertEqual(response_OK.json().get("username"), "erick updated")

    def test_errors_in_update_of_the_user(self):

        seller = self.client.post(self.user_list_create_url, data_seller)
        self.client.post(self.user_list_create_url, data_common_user)

        token_common_user = self.client.post(self.login_url, login_common_user)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token_common_user.json().get("token")
        )

        response_try_update_other_user = self.client.patch(
            f"/api/accounts/{seller.json().get('id')}/",
            {"username": "erick updated"},
        )

        self.client.credentials()

        response_without_token = self.client.patch(
            f"/api/accounts/{seller.json().get('id')}/",
            {"username": "erick updated"},
        )

        response_non_existent_user = self.client.patch(
            f"/api/accounts/1wtugntinhyih5oç/",
            {"username": "erick updated"},
        )

        self.assertIs(
            response_try_update_other_user.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            response_try_update_other_user.json(),
            {"detail": "You do not have permission to perform this action."},
        )
        self.assertIs(response_without_token.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response_without_token.json(),
            {"detail": "Authentication credentials were not provided."},
        )
        self.assertIs(response_non_existent_user.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response_non_existent_user.json(),
            {"detail": "Not found."},
        )

    def test_adm_can_change_is_active(self):
        seller = self.client.post(self.user_list_create_url, data_seller)

        token_adm = self.client.post(self.login_url, login_adm_user)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token_adm.json().get("token")
        )

        response_Ok_1 = self.client.patch(
            f"/api/accounts/{seller.json().get('id')}/management/", {"is_active": False}
        )

        response_Ok_2 = self.client.patch(
            f"/api/accounts/{seller.json().get('id')}/management/", {"is_active": True}
        )

        self.assertIs(seller.json().get("is_active"), True)

        self.assertIs(response_Ok_1.json().get("is_active"), False)
        self.assertIs(response_Ok_1.status_code, status.HTTP_200_OK)

        self.assertIs(response_Ok_2.json().get("is_active"), True)
        self.assertIs(response_Ok_2.status_code, status.HTTP_200_OK)

    def test_errors_change_is_active(self):
        seller = self.client.post(self.user_list_create_url, data_seller)

        token_seller = self.client.post(self.login_url, login_seller)
        token_adm_user = self.client.post(self.login_url, login_adm_user)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token_seller.json().get("token")
        )

        response_non_adm = self.client.patch(
            f"/api/accounts/{seller.json().get('id')}/management/", {"is_active": False}
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token_adm_user.json().get("token")
        )

        response_non_existent_user = self.client.patch(
            f"/api/accounts/1wtugntinhyih5oç/management/",
            {"username": "erick updated"},
        )

        self.client.credentials()

        response_without_token = self.client.patch(
            f"/api/accounts/{seller.json().get('id')}/management/",
            {"username": "erick updated"},
        )

        self.assertEqual(
            response_non_adm.json(),
            {"detail": "You do not have permission to perform this action."},
        )
        self.assertIs(response_non_adm.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(
            response_without_token.json(),
            {"detail": "Authentication credentials were not provided."},
        )
        self.assertIs(response_without_token.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(response_non_existent_user.json(), {"detail": "Not found."})
        self.assertIs(response_non_existent_user.status_code, status.HTTP_404_NOT_FOUND)

    def test_anyone_can_list_users(self):
        self.client.post(self.user_list_create_url, data_seller)
        self.client.post(self.user_list_create_url, data_common_user)

        response_OK_1 = self.client.get(self.user_list_create_url)
        response_OK_2 = self.client.get("/api/accounts/newest/2/")

        self.assertIs(
            type(response_OK_1.json().get("results")),
            list,
        )
        self.assertIs(response_OK_1.json().get("count"), 3)
        self.assertIs(response_OK_1.status_code, status.HTTP_200_OK)

        self.assertIs(
            type(response_OK_2.json().get("results")),
            list,
        )
        self.assertIs(response_OK_2.json().get("count"), 2)
        self.assertIs(response_OK_2.status_code, status.HTTP_200_OK)
