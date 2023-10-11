import logging
from rest_framework.test import APITestCase
from django.utils.timezone import now
from django.urls import reverse
import core.tests.utils as test_utils
from app_auth.models.user_model import User
from balance.models import BalanceType, BalanceTypeChoices
from keycloak_client.django_client import get_keycloak_client


class BalancePaginationTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        self.balance_url = reverse("balance-list-create")

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
        self.exp_type = BalanceType.objects.create(  # pylint: disable=no-member
            name="test",
            type=BalanceTypeChoices.EXPENSE
        )
        return super().setUp()

    def get_expense_data(self):
        return {
            "name": "Test name",
            "description": "Test description",
            "real_quantity": 2.0,
            "currency_type": "EUR",
            "balance_type": {
                "name": self.exp_type.name,
                "type": self.exp_type.type
            },
            "date": str(now().date()),
            "owner": str(self.user),
        }

    def test_expense_pagination_scheme(self):
        """
        Checks Expense pagination scheme is correct
        """
        data = self.get_expense_data()
        # Add new expense
        test_utils.authenticate_user(self.client)
        test_utils.post(self.client, self.balance_url, data)
        # Get expense data
        response = test_utils.get(self.client, self.balance_url)
        scheme = dict(response.data)
        scheme["results"] = []
        results = dict(response.data)["results"]

        for result in results:
            result = dict(result)
            result["balance_type"] = dict(result["balance_type"])
            scheme["results"] += [result]
        expected_scheme = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "Test name",
                    "description": "Test description",
                    "real_quantity": 2.0,
                    "converted_quantity": 2.0,
                    "date": str(now().date()),
                    "currency_type": "EUR",
                    "balance_type": {
                        "name": "test",
                        "type": "EXPENSE",
                        "image": "http://testserver/media/core/default_image.jpg",
                    },
                }
            ],
        }
        self.assertEqual(scheme, expected_scheme)

    def test_expense_two_pages(self):
        """
        Checks 2 pages of Expense data is correct
        """
        test_utils.authenticate_user(self.client)
        for _ in range(20):
            data = self.get_expense_data()
            # Add new expense
            test_utils.post(self.client, self.balance_url, data)
        # Get First page expense data
        response = test_utils.get(self.client, self.balance_url)
        data = dict(response.data)
        self.assertEqual(data["count"], 20)
        # 10 expenses in the first page
        self.assertEqual(len(data["results"]), 10)
        # Second page
        response = test_utils.get(self.client, data["next"])
        self.assertEqual(data["count"], 20)
        # 10 expenses in the first page
        self.assertEqual(len(data["results"]), 10)
