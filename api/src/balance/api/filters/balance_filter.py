from django_filters import rest_framework as filters
from balance.models.balance_model import Balance


class BalanceFilterSet(filters.FilterSet):
    converted_quantity_min = filters.NumberFilter(
        field_name="converted_quantity",
        lookup_expr="gte",
        label="Min converted quantity",
    )
    converted_quantity_max = filters.NumberFilter(
        field_name="converted_quantity",
        lookup_expr="lte",
        label="Max converted quantity",
    )
    real_quantity_min = filters.NumberFilter(
        field_name="real_quantity",
        lookup_expr="gte",
        label="Min real quantity",
    )
    real_quantity_max = filters.NumberFilter(
        field_name="real_quantity",
        lookup_expr="lte",
        label="Max real quantity",
    )
    date_from = filters.DateFilter(
        field_name="date", lookup_expr="gte", label="Date From"
    )
    date_to = filters.DateFilter(
        field_name="date", lookup_expr="lte", label="Date To")

    class Meta:
        model = Balance
        fields = ["balance_type", "currency_type"]
