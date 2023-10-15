from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from balance.models.balance_model import Balance
from balance.models.balance_type_model import BalanceType
from core.permissions import IsCurrentVerifiedUser


class BalanceSummaryYearView(APIView):
    permission_classes = (IsCurrentVerifiedUser,)

    def validate(self):
        if "type" not in list(self.kwargs):
            raise ValidationError({"type": [_("type not provided")]})
        if not BalanceType.objects.filter(  # pylint: disable=no-member
            type=self.kwargs["type"]
        ).exists():
            raise ValidationError({"type": [_("type not valid")]})
        if "year" not in list(self.kwargs):
            raise ValidationError({"year": [_("year not provided")]})

    def get(self, request, **kwargs):
        self.validate()

        year = int(self.kwargs["year"])
        balance_type = str(self.kwargs["type"])
        filtered_balances = Balance.objects.filter(  # pylint: disable=no-member
            date__year=year,
            balance_type__type=balance_type
        )

        summary_dict = {}
        for balance in list(filtered_balances):
            type_name = balance.balance_type.name
            if type_name in list(summary_dict):
                summary_dict[type_name] += balance.converted_quantity
            else:
                summary_dict[type_name] = balance.converted_quantity

        return Response(
            data=[
                {
                    "type": type_name,
                    "quantity": summary_dict[type_name]
                }
                for type_name in list(summary_dict.keys())
            ]
        )
