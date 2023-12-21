from django.contrib import admin
from src.balance.models import MonthlyBalance


@admin.register(MonthlyBalance)
class MonthlyBalanceAdmin(admin.ModelAdmin):
    fields = (
        "id",
        ("month", "year",),
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
