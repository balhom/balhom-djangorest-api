from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsCurrentVerifiedUser
from balance.models.balance_model import Balance
from balance.api.serializers.balance_serializer import (
    BalanceSerializer
)
from balance.api.filters.balance_filter import BalanceFilterSet
from currency_converter_integration import convert_or_fetch


class BalanceViewSet(ModelViewSet):
    queryset = Balance.objects.all()  # pylint: disable=no-member
    permission_classes = (IsCurrentVerifiedUser,)
    filterset_class = BalanceFilterSet
    serializer_class = BalanceSerializer

    def get_queryset(self):
        """
        Filter objects by owner
        """
        if getattr(self, "swagger_fake_view", False):
            return Balance.objects.none()  # pylint: disable=no-member
        return Balance.objects.filter(owner=self.request.user)  # pylint: disable=no-member

    def perform_create(self, serializer):
        owner = self.request.user
        with transaction.atomic():
            # Inject owner data to the serializer
            serializer.save(owner=owner)

    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()


balance_list_create_view = BalanceViewSet.as_view({
    "get": "list",
    "post": "create",
})
balance_get_update_view = BalanceViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "pacth": "partial_update",
})