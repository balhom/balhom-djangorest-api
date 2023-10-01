from django.contrib import admin
from balance.models.balance_model import Balance


@admin.register(Balance)
class ExpenseAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "description",
        ("real_quantity", "converted_quantity", "date",),
        ("currency_type", "balance_type",),
        "owner",
        ("created", "updated",),
    )
    readonly_fields = (
        "created", "updated",
    )
    list_display = (
        "name",
        "real_quantity",
        "converted_quantity",
        "date",
        "owner",
    )
    search_fields = ("owner",)
    ordering = ("owner", "date",)
