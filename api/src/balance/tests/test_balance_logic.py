import logging
from django.utils.timezone import now
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import core.tests.utils as test_utils
from app_auth.models.user_model import User
from app_auth.models.invitation_code_model import InvitationCode
from balance.models.balance_model import Balance
from balance.models.balance_type_model import BalanceType, BalanceTypeChoices
from keycloak_client.django_client import get_keycloak_client


class BalanceLogicTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        self.balance_url = reverse("balance-list-create")

        self.keycloak_client_mock = get_keycloak_client()

        # Create InvitationCodes
        self.inv_code = InvitationCode.objects.create(  # pylint: disable=no-member
            usage_left=400
        )
        # User data
        self.user_data = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id,
            "username": self.keycloak_client_mock.username,
            "email": self.keycloak_client_mock.email,
            "password": self.keycloak_client_mock.password,
            "inv_code": str(self.inv_code.code),
            "locale": self.keycloak_client_mock.locale,
            "pref_currency_type": "EUR",
        }
        # User creation
        self.user = User.objects.create(
            keycloak_id=self.user_data["keycloak_id"],
            pref_currency_type="EUR",
            current_balance=10,
            inv_code=self.inv_code,
        )

        self.exp_type = BalanceType.objects.create(  # pylint: disable=no-member
            name="test",
            type=BalanceTypeChoices.EXPENSE
        )

    def get_expense_data(self):
        return {
            "name": "Test name",
            "description": "",
            "real_quantity": 2.0,
            "currency_type": "EUR",
            "balance_type": {
                "name": self.exp_type.name,
                "type": self.exp_type.type
            },
            "date": str(now().date()),
            "owner": str(self.user),
        }

    def authenticate_add_expense(self):
        test_utils.authenticate_user(self.client)
        data = self.get_expense_data()
        # Add new expense
        test_utils.post(self.client, self.balance_url, data)

    def test_expense_post(self):
        """
        Checks balance gets updated with Expense post
        """
        data = self.get_expense_data()
        test_utils.authenticate_user(self.client)
        test_utils.post(self.client, self.balance_url, data)
        user = User.objects.get(keycloak_id=self.user_data["keycloak_id"])
        self.assertEqual(user.current_balance, 8)
        # Negative quantity not allowed
        data["real_quantity"] = -10.0
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "real_quantity", [field["name"]
                              for field in response.data["fields"]]
        )

    def test_expense_patch(self):
        """
        Checks balance gets updated with Expense patch (similar to put)
        """
        data = self.get_expense_data()
        test_utils.authenticate_user(self.client)
        test_utils.post(self.client, self.balance_url, data)
        expense = Balance.objects.get(  # pylint: disable=no-member
            name="Test name"
        )
        # Patch method
        test_utils.patch(
            self.client,
            self.balance_url + "/" + str(expense.id),
            {"real_quantity": 5.0},
        )
        user = User.objects.get(keycloak_id=self.user_data["keycloak_id"])
        self.assertEqual(user.current_balance, 5)

    def test_expense_delete_url(self):
        """
        Checks balance gets updated with Expense delete
        """
        # Add first expense
        data = self.get_expense_data()
        test_utils.authenticate_user(self.client)
        test_utils.post(self.client, self.balance_url, data)
        data2 = data
        data2["name"] = "test"
        # Add second expense
        test_utils.post(self.client, self.balance_url, data2)
        expense = Balance.objects.get(  # pylint: disable=no-member
            name="Test name"
        )
        # Delete second expense
        test_utils.delete(self.client, self.balance_url +
                          "/" + str(expense.id))
        user = User.objects.get(keycloak_id=self.user_data["keycloak_id"])
        self.assertEqual(user.current_balance, 8)
