from rest_framework.viewsets import ModelViewSet
from src.balance.models import MonthlyBalance
from src.balance.api.serializers.monthly_balance_serializer import MonthlyBalanceSerializer
from src.balance.api.filters.monthly_balance_filter import MonthlyBalanceFilterSet
from src.core.permissions import IsCurrentVerifiedUser


class MonthlyBalanceViewSet(ModelViewSet):
    queryset = MonthlyBalance.objects.all()  # pylint: disable=no-member
    serializer_class = MonthlyBalanceSerializer
    permission_classes = (IsCurrentVerifiedUser,)
    filterset_class = MonthlyBalanceFilterSet

    def get_queryset(self):
        """
        Filter objects by owner
        """
        if getattr(self, "swagger_fake_view", False):
            return MonthlyBalance.objects.none()  # return empty queryset
        return MonthlyBalance.objects.filter(owner=self.request.user)  # pylint: disable=no-member


monthly_balance_list_view = MonthlyBalanceViewSet.as_view({
    "get": "list",
})
monthly_balance_view = MonthlyBalanceViewSet.as_view({
    "get": "retrieve",
})
