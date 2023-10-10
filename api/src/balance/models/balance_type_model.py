from django.db import models
from django.utils.translation import gettext_lazy as _


class BalanceTypeChoices(models.TextChoices):
    REVENUE = 'REVENUE', _('revenue')
    EXPENSE = 'EXPENSE', _('expense')


class BalanceType(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=15
    )
    type = models.CharField(
        max_length=10,
        choices=BalanceTypeChoices.choices
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to="balance/type",
        default="core/default_image.jpg"
    )

    class Meta:
        verbose_name = _("Balance type")
        verbose_name_plural = _("Balance types")
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)
