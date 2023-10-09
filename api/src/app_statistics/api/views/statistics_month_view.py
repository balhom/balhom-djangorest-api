from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from balance.models.balance_type_model import BalanceTypeChoices
from balance.models.balance_model import Balance
from core.permissions import IsCurrentVerifiedUser


class StatisticsMonthView(APIView):
    permission_classes = (IsCurrentVerifiedUser,)

    def validate(self):
        if "year" not in list(self.kwargs):
            raise ValidationError({"year": [_("year not provided")]})
        if "month" not in list(self.kwargs):
            raise ValidationError({"month": [_("month not provided")]})
        if 1 > int(self.kwargs["month"]) > 12:
            raise ValidationError({"month": [_("month not valid")]})

    def get(self, request, **kwargs):
        self.validate()

        year = int(self.kwargs["year"])
        month = int(self.kwargs["month"])
        filtered_balances = Balance.objects.filter(  # pylint: disable=no-member
            date__year=year,
            date__month=month
        )

        day_balance_dict = {}
        for balance in filtered_balances:
            day = balance.date.day
            if day in list(day_balance_dict):
                if balance.balance_type.type == BalanceTypeChoices.EXPENSE:
                    day_balance_dict[day]["expense"] += balance.converted_quantity
                elif balance.balance_type.type == BalanceTypeChoices.REVENUE:
                    day_balance_dict[day]["revenue"] += balance.converted_quantity
            else:
                day_balance_dict[day] = {}
                if balance.balance_type.type == BalanceTypeChoices.EXPENSE:
                    day_balance_dict[day]["expense"] = balance.converted_quantity
                    day_balance_dict[day]["revenue"] = 0
                elif balance.balance_type.type == BalanceTypeChoices.REVENUE:
                    day_balance_dict[day]["expense"] = 0
                    day_balance_dict[day]["revenue"] = balance.converted_quantity

        return Response(
            data={
                "statistics": [
                    {
                        "day": day,
                        "expense": day_balance_dict[day]["expense"],
                        "revenue": day_balance_dict[day]["revenue"]
                    }
                    for day in list(day_balance_dict.keys())
                ]
            },
        )
