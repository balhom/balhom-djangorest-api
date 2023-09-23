import logging
import core.tests.utils as test_utils
from rest_framework.test import APITestCase
from django.utils.timezone import now
from django.urls import reverse
from coin.models import CoinType
from app_auth.models import InvitationCode, User
from expense.models import ExpenseType
from keycloak_client.django_client import get_keycloak_client


class ExpensePaginationTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        self.expense_url = reverse("expense-list")

        self.keycloak_client_mock = get_keycloak_client()

        # Create InvitationCodes
        self.inv_code = InvitationCode.objects.create(  # pylint: disable=no-member
            usage_left=400
        )
        # Create CurrencyType
        self.currency_type = CoinType.objects.create(code="EUR")
        # User data
        self.user_data = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id,
            "username": self.keycloak_client_mock.username,
            "email": self.keycloak_client_mock.email,
            "password": self.keycloak_client_mock.password,
            "inv_code": str(self.inv_code.code),
            "locale": self.keycloak_client_mock.locale,
            "pref_currency_type": str(self.currency_type.code),
        }
        # User creation
        self.user = User.objects.create(
            keycloak_id=self.user_data["keycloak_id"],
            pref_currency_type=self.currency_type,
            inv_code=self.inv_code,
        )
        self.exp_type = ExpenseType.objects.create(name="test")
        return super().setUp()

    def get_expense_data(self):
        return {
            "name": "Test name",
            "description": "Test description",
            "real_quantity": 2.0,
            "currency_type": self.currency_type.code,
            "exp_type": self.exp_type.name,
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
        test_utils.post(self.client, self.expense_url, data)
        # Get expense data
        response = test_utils.get(self.client, self.expense_url)
        scheme = dict(response.data)
        scheme["results"] = []
        results = dict(response.data)["results"]

        for result in results:
            result = dict(result)
            result["exp_type"] = dict(result["exp_type"])
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
                    "exp_type": {
                        "name": "test",
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
        for i in range(20):
            data = self.get_expense_data()
            # Add new expense
            test_utils.post(self.client, self.expense_url, data)
        # Get First page expense data
        response = test_utils.get(self.client, self.expense_url)
        data = dict(response.data)
        self.assertEqual(data["count"], 20)
        # 10 expenses in the first page
        self.assertEqual(len(data["results"]), 10)
        # Second page
        response = test_utils.get(self.client, data["next"])
        self.assertEqual(data["count"], 20)
        # 10 expenses in the first page
        self.assertEqual(len(data["results"]), 10)
