import logging
from django.utils.timezone import now
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import core.tests.utils as test_utils
from balance.models.annual_balance_model import AnnualBalance
from balance.models.monthly_balance_model import MonthlyBalance
from app_auth.models.user_model import User
from keycloak_client.django_client import get_keycloak_client


class BalanceUrlsPermissionsTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        self.annual_balance_list = reverse("annual-balance-list")
        self.monthly_balance_list = reverse("monthly-balance-list")

        self.keycloak_client_mock = get_keycloak_client()

        # Test user data
        self.user_data1 = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id,
            "username": self.keycloak_client_mock.username,
            "email": self.keycloak_client_mock.email,
            "password": self.keycloak_client_mock.password,
            "locale": self.keycloak_client_mock.locale,
            "pref_currency_type": "EUR",
        }
        self.user_data2 = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id + "1",
            "username": "username2",
            "email": "email2@test.com",
            "password": "password1@212",
            "locale": "en",
            "pref_currency_type": "EUR",
        }

        # User creation
        self.user1 = User.objects.create(
            keycloak_id=self.user_data1["keycloak_id"],
        )
        self.user2 = User.objects.create(
            keycloak_id=self.user_data2["keycloak_id"],
        )
        return super().setUp()

    def get_annual_balance_data(self, user):
        return {
            "gross_quantity": 1.1,
            "expected_quantity": 2.2,
            "currency_type": "EUR",
            "owner": user,
            "year": now().date().year,
        }

    def get_monthly_balance_data(self, user):
        return {
            "gross_quantity": 1.1,
            "expected_quantity": 2.2,
            "currency_type": "EUR",
            "owner": user,
            "year": now().date().year,
            "month": now().date().month,
        }

    def add_annual_balance(self, user):
        data = self.get_annual_balance_data(user)
        return AnnualBalance.objects.create(  # pylint: disable=no-member
            gross_quantity=data["gross_quantity"],
            expected_quantity=data["expected_quantity"],
            currency_type=data["currency_type"],
            owner=data["owner"],
            year=data["year"],
        ).id

    def add_monthly_balance(self, user):
        data = self.get_monthly_balance_data(user)
        return MonthlyBalance.objects.create(  # pylint: disable=no-member
            gross_quantity=data["gross_quantity"],
            expected_quantity=data["expected_quantity"],
            currency_type=data["currency_type"],
            owner=data["owner"],
            year=data["year"],
            month=data["month"],
        ).id

    def test_annual_balance_get_list_url(self):
        """
        Checks permissions with AnnualBalance get and list
        """
        test_utils.authenticate_user(self.client, self.user1.keycloak_id)
        # Add new AnnualBalance as user1
        self.add_annual_balance(self.user1)
        # Get AnnualBalance data as user1
        response = test_utils.get(self.client, self.annual_balance_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["count"], 1)

        # Get AnnualBalance data as user2
        test_utils.authenticate_user(self.client, self.user2.keycloak_id)
        response = test_utils.get(self.client, self.annual_balance_list)
        # Gets an empty dict
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["count"], 0)
        # Try with an specific expense
        response = test_utils.get(
            self.client, self.annual_balance_list + "/" + str(id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_monthly_balance_get_list_url(self):
        """
        Checks permissions with MonthlyBalance get and list
        """
        test_utils.authenticate_user(self.client, self.user1.keycloak_id)
        # Add new MonthlyBalance as user1
        self.add_monthly_balance(self.user1)
        # Get MonthlyBalance data as user1
        response = test_utils.get(self.client, self.monthly_balance_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["count"], 1)

        # Get MonthlyBalance data as user2
        test_utils.authenticate_user(self.client, self.user2.keycloak_id)
        response = test_utils.get(self.client, self.monthly_balance_list)
        # Gets an empty dict
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["count"], 0)
        # Try with an specific expense
        response = test_utils.get(
            self.client, self.monthly_balance_list + "/" + str(id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
