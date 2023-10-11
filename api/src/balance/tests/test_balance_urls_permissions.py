import logging
from django.utils.timezone import now
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import core.tests.utils as test_utils
from app_auth.models.user_model import User
from balance.models.balance_model import Balance
from balance.models.balance_type_model import BalanceType, BalanceTypeChoices
from keycloak_client.django_client import get_keycloak_client


class BalanceUrlsPermissionsTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        self.balance_url = reverse("balance-list-create")
        self.exp_type_list_url = reverse(
            "balance-type-list",
            args=[BalanceTypeChoices.EXPENSE]
        )

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
            "pref_currency_type": "USD",
        }
        # User creation
        User.objects.create(
            keycloak_id=self.user_data1["keycloak_id"],
            pref_currency_type="EUR",
        )
        User.objects.create(
            keycloak_id=self.user_data2["keycloak_id"],
            pref_currency_type="USD",
        )
        return super().setUp()

    def get_expense_type_data(self):
        exp_type = BalanceType.objects.create(  # pylint: disable=no-member
            name="test",
            type=BalanceTypeChoices.EXPENSE
        )
        return {"name": exp_type.name, "image": exp_type.image}

    def get_expense_data(self):
        exp_type = BalanceType.objects.create(  # pylint: disable=no-member
            name="test",
            type=BalanceTypeChoices.EXPENSE
        )
        return {
            "name": "Test name",
            "description": "Test description",
            "real_quantity": 2.0,
            "currency_type": self.user_data1["pref_currency_type"],
            "balance_type": {
                "name": exp_type.name,
                "type": exp_type.type
            },
            "date": str(now().date()),
        }

    def test_expense_type_get_list_url(self):
        """
        Checks permissions with Expense Type get and list
        """
        data = self.get_expense_type_data()
        # Get expense type data without authentication
        response = test_utils.get(self.client, self.exp_type_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Try with an specific expense
        response = test_utils.get(
            self.client, self.exp_type_list_url + "/" + str(data["name"])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Get expense type data with authentication
        test_utils.authenticate_user(self.client)
        response = test_utils.get(self.client, self.exp_type_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Try with an specific expense
        response = test_utils.get(
            self.client, self.exp_type_list_url + "/" + str(data["name"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expense_post_url(self):
        """
        Checks permissions with Expense post
        """
        data = self.get_expense_data()
        # Try without authentication
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Try with authentication
        test_utils.authenticate_user(self.client)
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Compare owner
        expense = Balance.objects.get(  # pylint: disable=no-member
            name="Test name")
        self.assertEqual(expense.owner.keycloak_id,
                         self.user_data1["keycloak_id"])

    def test_expense_get_list_url(self):
        """
        Checks permissions with Expense get and list
        """
        data = self.get_expense_data()
        # Add new expense as user1
        test_utils.authenticate_user(
            self.client, self.user_data1["keycloak_id"])
        test_utils.post(self.client, self.balance_url, data)
        # Get expense data as user1
        response = test_utils.get(self.client, self.balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["count"], 1)
        # Get expense data as user2
        test_utils.authenticate_user(
            self.client, self.user_data2["keycloak_id"])
        response = test_utils.get(self.client, self.balance_url)
        # Gets an empty dict
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["count"], 0)
        # Try with an specific expense
        expense = Balance.objects.get(  # pylint: disable=no-member
            name="Test name")
        response = test_utils.get(
            self.client, self.balance_url + "/" + str(expense.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_expense_put_url(self):
        """
        Checks permissions with Expense patch (almost same as put)
        """
        data = self.get_expense_data()
        # Add new expense as user1
        test_utils.authenticate_user(
            self.client, self.user_data1["keycloak_id"])
        test_utils.post(self.client, self.balance_url, data)
        expense = Balance.objects.get(  # pylint: disable=no-member
            name="Test name")
        # Try update as user1
        response = test_utils.patch(
            self.client,
            self.balance_url + "/" + str(expense.id),
            {"real_quantity": 35.0},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check expense
        expense = Balance.objects.get(  # pylint: disable=no-member
            name="Test name")
        self.assertEqual(expense.real_quantity, 35.0)
        # Try update as user2
        test_utils.authenticate_user(
            self.client, self.user_data2["keycloak_id"])
        response = test_utils.patch(
            self.client,
            self.balance_url + "/" + str(expense.id),
            {"real_quantity": 30.0},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_expense_delete_url(self):
        """
        Checks permissions with Expense delete
        """
        data = self.get_expense_data()
        # Add new expense as user1
        test_utils.authenticate_user(
            self.client, self.user_data1["keycloak_id"])
        test_utils.post(self.client, self.balance_url, data)
        # Delete expense data as user2
        test_utils.authenticate_user(
            self.client, self.user_data2["keycloak_id"])
        expense = Balance.objects.get(  # pylint: disable=no-member
            name="Test name")
        response = test_utils.delete(
            self.client, self.balance_url + "/" + str(expense.id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Delete expense data as user1
        test_utils.authenticate_user(
            self.client, self.user_data1["keycloak_id"])
        response = test_utils.delete(
            self.client, self.balance_url + "/" + str(expense.id)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
