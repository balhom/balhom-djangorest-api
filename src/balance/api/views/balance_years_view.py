from datetime import date
from django.db.models.functions import ExtractYear
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.balance.models.balance_type_model import BalanceType
from src.balance.models.balance_model import Balance
from src.core.permissions import IsCurrentVerifiedUser


class BalanceYearsRetrieveView(APIView):
    permission_classes = (IsCurrentVerifiedUser,)

    def validate(self):
        if "type" not in list(self.kwargs):
            raise ValidationError({"type": [_("type not provided")]})
        if not BalanceType.objects.filter(  # pylint: disable=no-member
            type=self.kwargs["type"]
        ).exists():
            raise ValidationError({"type": [_("type not valid")]})

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, **kwargs):
        """
        This view will be cached for 1 minute
        """
        self.validate()

        balance_type = self.kwargs["type"]
        filtered_balances = Balance.objects.filter(  # pylint: disable=no-member
            balance_type__type=balance_type
        )

        years_dict = filtered_balances.annotate(  # pylint: disable=no-member
            year=ExtractYear('date')
        ).values('year').distinct()

        years = [year['year'] for year in years_dict]

        if years:
            return Response(
                data=years,
            )
        return Response(
            data=[date.today().year],
        )
