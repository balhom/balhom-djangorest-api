from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from balance.models.date_balance_model import DateBalance


class AnnualBalance(DateBalance):
    year = models.PositiveIntegerField(
        verbose_name=_("year"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5000),
        ]
    )

    class Meta(DateBalance.Meta):
        verbose_name = _("Annual balance")
        verbose_name_plural = _("Annual balances")

    def __str__(self) -> str:
        return str(self.year)
