from rest_framework import viewsets
from balance.api.filters.monthly_balance_filter import AnnualBalanceFilterSet
from balance.models import AnnualBalance
from balance.api.serializers.annual_balance_serializer import AnnualBalanceSerializer
from core.permissions import IsCurrentVerifiedUser


class AnnualBalanceViewSet(viewsets.ModelViewSet):
    queryset = AnnualBalance.objects.all()  # pylint: disable=no-member
    serializer_class = AnnualBalanceSerializer
    permission_classes = (IsCurrentVerifiedUser,)
    filterset_class = AnnualBalanceFilterSet

    def get_queryset(self):
        """
        Filter objects by owner
        """
        if getattr(self, "swagger_fake_view", False):
            return AnnualBalance.objects.none()  # return empty queryset
        return AnnualBalance.objects.filter(owner=self.request.user)  # pylint: disable=no-member


annual_balance_view = AnnualBalanceViewSet.as_view({
    "get": "retrieve",
})
annual_balance_list_view = AnnualBalanceViewSet.as_view({
    "get": "list",
})
