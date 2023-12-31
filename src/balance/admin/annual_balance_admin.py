from django.contrib import admin
from src.balance.models import AnnualBalance


@admin.register(AnnualBalance)
class AnnualBalanceAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "year",
        ("gross_quantity", "expected_quantity",),
        "currency_type",
        "owner",
        "created",
        "updated"
    )
    readonly_fields = (
        "id",
        "created",
        "updated"
    )
