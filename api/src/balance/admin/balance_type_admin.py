from django.contrib import admin
from balance.models.balance_type_model import BalanceType


@admin.register(BalanceType)
class BalanceTypeAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "type",
        "image",
    )
