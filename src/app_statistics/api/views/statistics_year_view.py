from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.balance.models.balance_type_model import BalanceTypeChoices
from src.balance.models.balance_model import Balance
from src.core.permissions import IsCurrentVerifiedUser


class StatisticsYearView(APIView):
    permission_classes = (IsCurrentVerifiedUser,)

    def validate(self):
        if "year" not in list(self.kwargs):
            raise ValidationError({"year": [_("year not provided")]})

    def get(self, request, **kwargs):
        self.validate()

        year = int(self.kwargs["year"])
        filtered_balances = Balance.objects.filter(  # pylint: disable=no-member
            date__year=year
        )

        month_balance_dict = {}
        for balance in list(filtered_balances):
            month = balance.date.month
            if month in list(month_balance_dict):
                if balance.balance_type.type == BalanceTypeChoices.EXPENSE:
                    month_balance_dict[month]["expense"] += balance.converted_quantity
                elif balance.balance_type.type == BalanceTypeChoices.REVENUE:
                    month_balance_dict[month]["revenue"] += balance.converted_quantity
            else:
                month_balance_dict[month] = {}
                if balance.balance_type.type == BalanceTypeChoices.EXPENSE:
                    month_balance_dict[month]["expense"] = balance.converted_quantity
                    month_balance_dict[month]["revenue"] = 0
                elif balance.balance_type.type == BalanceTypeChoices.REVENUE:
                    month_balance_dict[month]["expense"] = 0
                    month_balance_dict[month]["revenue"] = balance.converted_quantity

        return Response(
            data=[
                {
                    "month": month,
                    "expense": month_balance_dict[month]["expense"],
                    "revenue": month_balance_dict[month]["revenue"]
                }
                for month in list(month_balance_dict.keys())
            ]
        )
