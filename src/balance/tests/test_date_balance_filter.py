import logging
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import now
from django.urls import reverse
import src.core.tests.utils as test_utils
from src.app_auth.models.user_model import User
from src.balance.models import AnnualBalance, MonthlyBalance
from src.keycloak_client.django_client import get_keycloak_client


class DateBalanceFilterTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        self.annual_balance_list = reverse("annual-balance-list")
        self.monthly_balance_list = reverse("monthly-balance-list")

        self.keycloak_client_mock = get_keycloak_client()

        # User data
        self.user_data = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id,
            "username": self.keycloak_client_mock.username,
            "email": self.keycloak_client_mock.email,
            "password": self.keycloak_client_mock.password,
            "locale": self.keycloak_client_mock.locale,
            "pref_currency_type": "EUR",
        }
        # User creation
        self.user = User.objects.create(
            keycloak_id=self.user_data["keycloak_id"],
            pref_currency_type="EUR",
        )
        return super().setUp()

    def get_annual_balance_data(self):
        return {
            "gross_quantity": 1.1,
            "expected_quantity": 2.2,
            "currency_type": "EUR",
            "owner": self.user,
            "year": now().date().year,
        }

    def get_monthly_balance_data(self):
        return {
            "gross_quantity": 1.1,
            "expected_quantity": 2.2,
            "currency_type": "EUR",
            "owner": self.user,
            "year": now().date().year,
            "month": now().date().month,
        }

    def authenticate_add_annual_balance(self):
        test_utils.authenticate_user(self.client)
        data = self.get_annual_balance_data()
        AnnualBalance.objects.create(  # pylint: disable=no-member
            gross_quantity=data["gross_quantity"],
            expected_quantity=data["expected_quantity"],
            currency_type=data["currency_type"],
            owner=data["owner"],
            year=data["year"],
        )

    def authenticate_add_monthly_balance(self):
        test_utils.authenticate_user(self.client)
        data = self.get_monthly_balance_data()
        MonthlyBalance.objects.create(  # pylint: disable=no-member
            gross_quantity=data["gross_quantity"],
            expected_quantity=data["expected_quantity"],
            currency_type=data["currency_type"],
            owner=data["owner"],
            year=data["year"],
            month=data["month"],
        )

    def test_annual_balance_filter_currency_type(self):
        """
        Checks AnnualBalance filter by currency_type
        """
        self.authenticate_add_annual_balance()
        url = self.annual_balance_list + "?currency_type=EUR"
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)

    def test_monthly_balance_filter_currency_type(self):
        """
        Checks MonthlyBalance filter by currency_type
        """
        self.authenticate_add_monthly_balance()
        url = self.monthly_balance_list + "?currency_type=EUR"
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)

    def test_annual_balance_filter_gross_quantity_min_and_max(self):
        """
        Checks AnnualBalance filter by gross_quantity min and max
        """
        self.authenticate_add_annual_balance()
        url = (
            self.annual_balance_list + "?gross_quantity_min=1.0&gross_quantity_max=3.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)
        url = (
            self.annual_balance_list + "?gross_quantity_min=6.0&gross_quantity_max=8.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 0)

    def test_monthly_balance_filter_gross_quantity_min_and_max(self):
        """
        Checks MonthlyBalance filter by gross_quantity min and max
        """
        self.authenticate_add_monthly_balance()
        url = (
            self.monthly_balance_list + "?gross_quantity_min=1.0&gross_quantity_max=3.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)
        url = (
            self.monthly_balance_list + "?gross_quantity_min=6.0&gross_quantity_max=8.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 0)

    def test_annual_balance_filter_expected_quantity_min_and_max(self):
        """
        Checks AnnualBalance filter by expected_quantity min and max
        """
        self.authenticate_add_annual_balance()
        url = (
            self.annual_balance_list
            + "?expected_quantity_min=1.0&expected_quantity_max=3.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)
        url = (
            self.annual_balance_list
            + "?expected_quantity_min=6.0&expected_quantity_max=8.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 0)

    def test_monthly_balance_filter_expected_quantity_min_and_max(self):
        """
        Checks MonthlyBalance filter by expected_quantity min and max
        """
        self.authenticate_add_monthly_balance()
        url = (
            self.monthly_balance_list
            + "?expected_quantity_min=1.0&expected_quantity_max=3.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)
        url = (
            self.monthly_balance_list
            + "?expected_quantity_min=6.0&expected_quantity_max=8.0"
        )
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 0)

    def test_annual_balance_filter_year(self):
        """
        Checks AnnualBalance filter by year
        """
        self.authenticate_add_annual_balance()
        url = self.annual_balance_list + "?year=" + str(now().date().year)
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)

    def test_annual_filter_year(self):
        """
        Checks MonthlyBalance filter by year
        """
        self.authenticate_add_monthly_balance()
        url = self.monthly_balance_list + "?year=" + str(now().date().year)
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)

    def test_monthly_filter_year(self):
        """
        Checks MonthlyBalance filter by month
        """
        self.authenticate_add_monthly_balance()
        url = self.monthly_balance_list + "?month=" + str(now().date().month)
        response = test_utils.get(self.client, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(response.data)
        self.assertEqual(data["count"], 1)
