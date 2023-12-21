from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from src.balance.models.balance_model import Balance
from src.balance.models.balance_type_model import BalanceTypeChoices
from src.balance.utils import (
    check_dates_and_update_date_balances,
    update_or_create_annual_balance,
    update_or_create_monthly_balance
)
from src.currency_conversion_client.django_client import get_currency_conversion_client
from src.app_auth.models.user_model import User


@receiver(pre_save, sender=Balance)
def balance_pre_save(sender, instance: Balance, **kwargs):
    currency_conversion_client = get_currency_conversion_client()

    new_instance = instance
    try:
        old_instance = Balance.objects.get(  # pylint: disable=no-member
            id=new_instance.id
        )
    except ObjectDoesNotExist:
        old_instance = None

    owner = User.objects.get(id=new_instance.owner.id)
    sign = -1 if instance.balance_type.type == BalanceTypeChoices.EXPENSE \
        else 1

    # Create action
    if not old_instance:
        owner.current_balance += new_instance.converted_quantity * sign
        owner.current_balance = round(owner.current_balance, 2)
        owner.save()

        # Create AnnualBalance or update it
        update_or_create_annual_balance(
            new_instance.converted_quantity,
            owner,
            new_instance.date.year,
            instance.balance_type.type == BalanceTypeChoices.REVENUE
        )
        # Create MonthlyBalance or update it
        update_or_create_monthly_balance(
            new_instance.converted_quantity,
            owner,
            new_instance.date.year,
            new_instance.date.month,
            instance.balance_type.type == BalanceTypeChoices.REVENUE
        )
    # Update action
    else:
        # In case there is a real quantity update
        if (
            new_instance.real_quantity != old_instance.real_quantity
            or new_instance.currency_type != old_instance.currency_type
        ):
            currency_from = new_instance.currency_type
            currency_to = owner.pref_currency_type
            real_quantity = new_instance.real_quantity

            converted_quantity = round(
                real_quantity * currency_conversion_client.get_conversion(
                    currency_from, currency_to
                ), 2
            )
            new_instance.converted_quantity = converted_quantity

            converted_old_quantity = round(
                old_instance.real_quantity * currency_conversion_client.get_conversion(
                    old_instance.currency_type,
                    currency_to
                ), 2
            )

            owner.current_balance += (converted_quantity
                                      - converted_old_quantity) * sign
            owner.current_balance = round(owner.current_balance, 2)
            owner.save()

            # Create DateBalance or update it
            check_dates_and_update_date_balances(
                old_instance,
                converted_old_quantity,
                converted_quantity,
                new_instance.date
            )
        # In case there is only a change of date
        # month and year needs to be checked
        elif new_instance.date != old_instance.date:
            converted_quantity = new_instance.converted_quantity
            # Create DateBalance or update it
            check_dates_and_update_date_balances(
                old_instance,
                converted_quantity,
                None,
                new_instance.date
            )


@receiver(pre_delete, sender=Balance)
def balance_pre_delete(sender, instance: Balance, **kwargs):
    currency_conversion_client = get_currency_conversion_client()

    owner = User.objects.get(id=instance.owner.id)
    sign = -1 if instance.balance_type.type == BalanceTypeChoices.EXPENSE \
        else 1

    currency_to = owner.pref_currency_type
    converted_quantity = round(
        instance.real_quantity * currency_conversion_client.get_conversion(
            instance.currency_type, currency_to
        ), 2
    )

    owner.current_balance -= converted_quantity * sign
    owner.current_balance = round(owner.current_balance, 2)
    owner.save()

    # Create AnnualBalance or update it
    update_or_create_annual_balance(
        - converted_quantity,
        owner,
        instance.date.year,
        instance.balance_type.type == BalanceTypeChoices.REVENUE
    )
    # Create MonthlyBalance or update it
    update_or_create_monthly_balance(
        - converted_quantity,
        owner,
        instance.date.year,
        instance.date.month,
        instance.balance_type.type == BalanceTypeChoices.REVENUE
    )
