from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from balance.models.balance_model import Balance
from balance.models.balance_type_model import BalanceTypeChoices
from balance.utils import (
    check_dates_and_update_date_balances,
    update_or_create_annual_balance,
    update_or_create_monthly_balance
)
from currency. import convert_or_fetch
from app_auth.models import User


@receiver(pre_save, sender=Balance)
def balance_pre_save(sender, instance: Balance, **kwargs):
    new_instance = instance
    try:
        old_instance = Balance.objects.get(id=new_instance.id)
    except ObjectDoesNotExist:
        old_instance = None
    
    owner = User.objects.get(id=new_instance.owner.id)
    sign = -1 if instance.balance_type.type == BalanceTypeChoices.EXPENSE \
        else 1

    # Create action
    if not old_instance:
        currency_from = new_instance.currency_type
        currency_to = owner.pref_currency_type

        real_quantity = new_instance.real_quantity
        converted_quantity = convert_or_fetch(
            currency_from, currency_to, real_quantity)
        new_instance.converted_quantity = converted_quantity
        
        owner.balance += converted_quantity * sign
        owner.balance = round(owner.balance, 2)
        owner.save()
        
        # Create AnnualBalance or update it
        update_or_create_annual_balance(
            converted_quantity, owner,
            new_instance.date.year,
            instance.balance_type.type == BalanceTypeChoices.REVENUE
        )
        # Create MonthlyBalance or update it
        update_or_create_monthly_balance(
            converted_quantity, owner,
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

            converted_quantity = convert_or_fetch(
                currency_from, currency_to, real_quantity
            )
            new_instance.converted_quantity = converted_quantity
            converted_old_quantity = convert_or_fetch(
                old_instance.currency_type,
                currency_to,
                old_instance.real_quantity
            )

            owner.balance += (converted_quantity \
                - converted_old_quantity) * sign
            owner.balance = round(owner.balance, 2)
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
    owner = User.objects.get(id=instance.owner.id)
    sign = -1 if instance.balance_type.type == BalanceTypeChoices.EXPENSE \
        else 1
    
    currency_to = owner.pref_currency_type
    converted_quantity = convert_or_fetch(
        instance.currency_type,
        currency_to,
        instance.real_quantity
    )

    owner.balance -= converted_quantity * sign
    owner.balance = round(owner.balance, 2)
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