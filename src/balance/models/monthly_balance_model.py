from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from src.balance.models.date_balance_model import DateBalance


class MonthlyBalance(DateBalance):
    year = models.PositiveIntegerField(
        verbose_name=_("year"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5000),
        ]
    )
    month = models.PositiveIntegerField(
        verbose_name=_("month"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ]
    )

    class Meta(DateBalance.Meta):
        verbose_name = _("Monthly balance")
        verbose_name_plural = _("Monthly balances")

    def __str__(self) -> str:
        return str(self.month)+" - "+str(self.year)
