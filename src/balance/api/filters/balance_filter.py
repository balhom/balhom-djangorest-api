from django_filters import rest_framework as filters
from src.balance.models.balance_model import Balance
from src.balance.models.balance_type_model import BalanceTypeChoices


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

    balance_type = filters.CharFilter(method="filter_balance_type")

    class Meta:
        model = Balance
        fields = ["currency_type",]

    def filter_balance_type(self, queryset, name, value):
        if value is not None and value in BalanceTypeChoices:
            queryset = Balance.objects.filter(balance_type__type=value)
        return queryset
