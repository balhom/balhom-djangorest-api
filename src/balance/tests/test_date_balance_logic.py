import logging
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta
from src.app_auth.models.user_model import User
from src.balance.models import AnnualBalance, MonthlyBalance
from src.balance.models.balance_model import Balance
from src.balance.models.balance_type_model import BalanceType, BalanceTypeChoices
import src.core.tests.utils as test_utils
from src.keycloak_client.django_client import get_keycloak_client


class DateBalanceLogicTests(APITestCase):
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
            "pref_currency_type": "EUR",
            "expected_annual_balance": 10.0,
            "expected_monthly_balance": 10.0,
        }
        # User creation
        User.objects.create(
            keycloak_id=self.user_data["keycloak_id"],
            pref_currency_type="EUR",
            expected_annual_balance=self.user_data["expected_annual_balance"],
            expected_monthly_balance=self.user_data["expected_monthly_balance"],
        )
        return super().setUp()

    def get_expense_data(self):
        exp_type = BalanceType.objects.create(  # pylint: disable=no-member
            name="test",
            type=BalanceTypeChoices.EXPENSE
        )
        return {
            "name": "Test name exp",
            "description": "Test description",
            "real_quantity": 2.0,
            "currency_type": "EUR",
            "balance_type": {
                "name": exp_type.name,
                "type": exp_type.type,
            },
            "date": str(now().date()),
        }

    def get_revenue_data(self):
        rev_type = BalanceType.objects.create(  # pylint: disable=no-member
            name="test",
            type=BalanceTypeChoices.REVENUE
        )
        return {
            "name": "Test name rev",
            "description": "Test description",
            "real_quantity": 2.0,
            "currency_type": "EUR",
            "balance_type": {
                "name": rev_type.name,
                "type": str(rev_type.type)
            },
            "date": str(now().date()),
        }

    def test_revenue_post_date_balances(self):
        """
        Checks that posting a revenue creates a monthly and annual balance
        with the revenue quantity
        """
        # Authenticate user
        test_utils.authenticate_user(self.client)
        data = self.get_revenue_data()
        # Post revenue
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(data["real_quantity"],
                         last_monthly_balance.gross_quantity)
        self.assertEqual(10.0, last_monthly_balance.expected_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(data["real_quantity"],
                         last_annual_balance.gross_quantity)
        self.assertEqual(10.0, last_annual_balance.expected_quantity)

    def test_expense_post_date_balances(self):
        """
        Checks that posting a expense creates a monthly and annual balance
        with the expense quantity
        """
        # Authenticate user
        test_utils.authenticate_user(self.client)
        data = self.get_expense_data()
        # Post expense
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(-data["real_quantity"],
                         last_monthly_balance.gross_quantity)
        self.assertEqual(10.0, last_monthly_balance.expected_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(-data["real_quantity"],
                         last_annual_balance.gross_quantity)
        self.assertEqual(10.0, last_annual_balance.expected_quantity)

    def test_revenue_delete_date_balances(self):
        """
        Checks that deleting a revenue creates a monthly and annual balance
        with the revenue quantity
        """
        # Authenticate user
        test_utils.authenticate_user(self.client)
        data = self.get_revenue_data()
        # Post revenue
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Delete revenue
        rev = Balance.objects.get(  # pylint: disable=no-member
            name=data["name"])
        response = test_utils.delete(
            self.client, self.balance_url + "/" + str(rev.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(0, last_monthly_balance.gross_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(0, last_annual_balance.gross_quantity)

    def test_expense_delete_date_balances(self):
        """
        Checks that deleting a expense creates a monthly and annual balance
        with the expense quantity
        """
        # Authenticate user
        test_utils.authenticate_user(self.client)
        data = self.get_expense_data()
        # Post expense
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Delete expense
        exp = Balance.objects.get(  # pylint: disable=no-member
            name=data["name"]
        )
        response = test_utils.delete(
            self.client, self.balance_url + "/" + str(exp.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(0, last_monthly_balance.gross_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(0, last_annual_balance.gross_quantity)

    def test_revenue_update_date_balances(self):
        """
        Checks that updating a revenue creates a monthly and annual balance
        with the revenue quantity
        """
        # Authenticate user
        test_utils.authenticate_user(self.client)
        data = self.get_revenue_data()
        # Post revenue
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Update revenue dfiferent date
        rev = Balance.objects.get(  # pylint: disable=no-member
            name=data["name"]
        )
        past_date = (now() - timedelta(days=32)).date()
        response = test_utils.patch(
            self.client, self.balance_url + "/" +
            str(rev.id), {"date": str(past_date)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        second_to_last_monthly_balance = MonthlyBalance.objects.get(  # pylint: disable=no-member
            month=past_date.month
        )
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(0, last_monthly_balance.gross_quantity)
        self.assertEqual(past_date.year, second_to_last_monthly_balance.year)
        self.assertEqual(past_date.month, second_to_last_monthly_balance.month)
        self.assertEqual(
            data["real_quantity"], second_to_last_monthly_balance.gross_quantity
        )
        last_annual_balance = AnnualBalance.objects.get(  # pylint: disable=no-member
            year=past_date.year)
        self.assertEqual(past_date.year, last_annual_balance.year)
        self.assertEqual(data["real_quantity"],
                         last_annual_balance.gross_quantity)
        # Test update diferent quantity and date
        response = test_utils.patch(
            self.client,
            self.balance_url + "/" + str(rev.id),
            {"date": str(now().date()), "real_quantity": 10.14},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        second_to_last_monthly_balance = MonthlyBalance.objects.get(  # pylint: disable=no-member
            month=past_date.month
        )
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(10.14, last_monthly_balance.gross_quantity)
        self.assertEqual(past_date.year, second_to_last_monthly_balance.year)
        self.assertEqual(past_date.month, second_to_last_monthly_balance.month)
        self.assertEqual(0, second_to_last_monthly_balance.gross_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(10.14, last_annual_balance.gross_quantity)
        # Test update diferent quantity
        response = test_utils.patch(
            self.client, self.balance_url + "/" +
            str(rev.id), {"real_quantity": 20.86}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(20.86, last_monthly_balance.gross_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(20.86, last_annual_balance.gross_quantity)

    def test_expense_update_date_balances(self):
        """
        Checks that updating a expense creates a monthly and annual balance
        with the expense quantity
        """
        # Authenticate user
        test_utils.authenticate_user(self.client)
        data = self.get_expense_data()
        # Post expense
        response = test_utils.post(self.client, self.balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Update expense dfiferent date
        exp = Balance.objects.get(  # pylint: disable=no-member
            name=data["name"]
        )
        past_date = (now() - timedelta(days=32)).date()
        response = test_utils.patch(
            self.client, self.balance_url + "/" +
            str(exp.id), {"date": str(past_date)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        second_to_last_monthly_balance = MonthlyBalance.objects.get(  # pylint: disable=no-member
            month=past_date.month
        )
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(0, last_monthly_balance.gross_quantity)
        self.assertEqual(past_date.year, second_to_last_monthly_balance.year)
        self.assertEqual(past_date.month, second_to_last_monthly_balance.month)
        self.assertEqual(
            -data["real_quantity"], second_to_last_monthly_balance.gross_quantity
        )
        last_annual_balance = AnnualBalance.objects.get(  # pylint: disable=no-member
            year=past_date.year)
        self.assertEqual(past_date.year, last_annual_balance.year)
        self.assertEqual(-data["real_quantity"],
                         last_annual_balance.gross_quantity)
        # Test update diferent quantity and date
        response = test_utils.patch(
            self.client,
            self.balance_url + "/" + str(exp.id),
            {"date": str(now().date()), "real_quantity": 10.14},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        second_to_last_monthly_balance = MonthlyBalance.objects.get(  # pylint: disable=no-member
            month=past_date.month
        )
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(-10.14, last_monthly_balance.gross_quantity)
        self.assertEqual(past_date.year, second_to_last_monthly_balance.year)
        self.assertEqual(past_date.month, second_to_last_monthly_balance.month)
        self.assertEqual(0, second_to_last_monthly_balance.gross_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(-10.14, last_annual_balance.gross_quantity)
        # Test update diferent quantity
        response = test_utils.patch(
            self.client, self.balance_url + "/" +
            str(exp.id), {"real_quantity": 20.86}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        last_monthly_balance = MonthlyBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_monthly_balance.year)
        self.assertEqual(now().date().month, last_monthly_balance.month)
        self.assertEqual(-20.86, last_monthly_balance.gross_quantity)
        last_annual_balance = AnnualBalance.objects.last()  # pylint: disable=no-member
        self.assertEqual(now().date().year, last_annual_balance.year)
        self.assertEqual(-20.86, last_annual_balance.gross_quantity)
