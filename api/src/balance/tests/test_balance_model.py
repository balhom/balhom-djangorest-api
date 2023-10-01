from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase
from balance.models.balance_model import Balance
from balance.models.balance_type_model import BalanceType, BalanceTypeChoices
from app_auth.models.user_model import User
from app_auth.models.invitation_code_model import InvitationCode
from keycloak_client.django_client import get_keycloak_client


class BalanceModelTests(APITestCase):
    def setUp(self):
        self.keycloak_client_mock = get_keycloak_client()

        # Create InvitationCodes
        self.inv_code = InvitationCode.objects.create()
        # Test user data
        self.user_data = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id,
            "username": "username1",
            "email": "email1@test.com",
            "password": "password1@212",
            "inv_code": str(self.inv_code.code),
            "pref_currency_type": "EUR",
        }
        self.exp_type = BalanceType.objects.create(
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
            "balance_type": self.exp_type,
            "date": now().date(),
            "owner": self.create_user(),
        }

    def create_user(self):
        return User.objects.create(
            keycloak_id=self.user_data["keycloak_id"],
            inv_code=self.inv_code,
            pref_currency_type="EUR",
        )

    def test_creates_exp_type(self):
        """
        Checks if exp_type is created
        """
        exp_type = BalanceType.objects.create(
            name="test2",
            type=BalanceTypeChoices.EXPENSE
        )
        self.assertEqual(exp_type.name, "test2")

    def test_creates_expense(self):
        """
        Checks if expense is created
        """
        data = self.get_expense_data()
        data["converted_quantity"] = 2.0
        expense = Balance.objects.create(**data)
        self.assertEqual(expense.name, data["name"])
        self.assertEqual(expense.description, data["description"])
        self.assertEqual(expense.real_quantity, data["real_quantity"])
        self.assertEqual(expense.converted_quantity,
                         data["converted_quantity"])
        self.assertEqual(expense.currency_type, data["currency_type"])
        self.assertEqual(expense.balance_type, data["balance_type"])
        self.assertEqual(expense.date, data["date"])
        self.assertEqual(expense.owner, data["owner"])
