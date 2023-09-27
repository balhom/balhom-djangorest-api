import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from app_auth.models import User


class DateBalance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    # All revenues and expenses
    gross_quantity = models.FloatField(
        verbose_name=_("gross quantity"),
        default=0
    )
    # expected_quantity
    expected_quantity = models.FloatField(
        verbose_name=_("expected quantity"),
        default=0
    )
    currency_type = models.CharField(
        verbose_name=_("currency type"),
        max_length=4
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_("owner"),
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Date balance")
        verbose_name_plural = _("Date balances")
        abstract = True
        ordering = ["-created"]

    def __str__(self) -> str:
        return str(self.created)
