import logging
from django.db import transaction
from celery import shared_task
from src.app_auth.models.user_model import User
from src.balance.models.annual_balance_model import AnnualBalance
from src.balance.models.monthly_balance_model import MonthlyBalance
from src.balance.models.balance_model import Balance
from src.keycloak_client.django_client import get_keycloak_client
from src.currency_conversion_client.django_client import get_currency_conversion_client

logger = logging.getLogger(__name__)


@shared_task
def remove_unverified_users():
    keycloak_client = get_keycloak_client()
    for user in User.objects.all():
        with transaction.atomic():
            user_info = keycloak_client.get_user_info_by_id(
                keycloak_id=user.keycloak_id
            )
            if not user_info["emailVerified"]:
                user.delete()
                keycloak_client.delete_user_by_id(keycloak_id=user.keycloak_id)


@shared_task
def change_converted_quantities(
    owner_keycloak_id, currency_from, currency_to
):
    currency_conversion_client = get_currency_conversion_client()

    with transaction.atomic():

        for balance in Balance.objects.filter(  # pylint: disable=no-member
            owner=User.objects.get(keycloak_id=owner_keycloak_id)
        ):
            balance.converted_quantity = round(
                currency_conversion_client.get_conversion(
                    currency_from,
                    currency_to
                ) * balance.converted_quantity, 2
            )
            balance.save()

        for date_balance in MonthlyBalance.objects.filter(  # pylint: disable=no-member
            owner=User.objects.get(keycloak_id=owner_keycloak_id)
        ):
            date_balance.gross_quantity = round(
                currency_conversion_client.get_conversion(
                    currency_from,
                    currency_to
                ) * date_balance.gross_quantity, 2
            )
            date_balance.expected_quantity = round(
                currency_conversion_client.get_conversion(
                    currency_from,
                    currency_to
                ) * date_balance.expected_quantity, 2
            )
            date_balance.save()

        for date_balance in AnnualBalance.objects.filter(  # pylint: disable=no-member
            owner=User.objects.get(keycloak_id=owner_keycloak_id)
        ):
            date_balance.gross_quantity = round(
                currency_conversion_client.get_conversion(
                    currency_from,
                    currency_to
                ) * date_balance.gross_quantity, 2
            )
            date_balance.expected_quantity = round(
                currency_conversion_client.get_conversion(
                    currency_from,
                    currency_to
                ) * date_balance.expected_quantity, 2
            )
            date_balance.save()
