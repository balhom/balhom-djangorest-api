from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from src.balance.models.balance_type_model import BalanceType
from src.app_auth.models.user_model import User


class Balance(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=40
    )
    description = models.CharField(
        verbose_name=_("description"),
        blank=True,
        max_length=2000,
        default=""
    )
    real_quantity = models.FloatField(
        verbose_name=_("real quantity"),
        validators=[MinValueValidator(0.0)],
    )
    converted_quantity = models.FloatField(
        verbose_name=_("converted quantity"),
        validators=[MinValueValidator(0.0)],
    )
    date = models.DateTimeField(
        verbose_name=_("date")
    )
    currency_type = models.CharField(
        verbose_name=_("currency type"),
        max_length=4
    )
    balance_type = models.ForeignKey(
        BalanceType,
        verbose_name=_("balance type"),
        on_delete=models.DO_NOTHING
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_("owner"),
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")
        # Greater to lower date
        ordering = ["-date"]

    def __str__(self) -> str:
        return str(self.name)
