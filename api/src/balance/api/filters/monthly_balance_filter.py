from balance.api.filters.annual_balance_filter import AnnualBalanceFilterSet
from balance.models import MonthlyBalance


class MonthlyBalanceFilterSet(AnnualBalanceFilterSet):
    class Meta:
        model = MonthlyBalance
        fields = ["currency_type", "year", "month"]
