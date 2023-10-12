from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsCurrentVerifiedUser
from balance.models.balance_model import Balance
from balance.api.serializers.balance_serializer import BalanceSerializer
from balance.api.filters.balance_filter import BalanceFilterSet
from currency_conversion_client.django_client import get_currency_conversion_client


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
        queryset = Balance.objects.filter(  # pylint: disable=no-member
            owner=self.request.user)

        sorting_param = self.request.query_params.get('sorting')
        if sorting_param:
            if sorting_param in [
                "name",
                "real_quantity",
                "-real_quantity", 
                "converted_quantity",
                "-converted_quantity",
                "date",
                "-date",
            ]:
                queryset = queryset.order_by(sorting_param)
        return queryset

    def perform_create(self, serializer):
        currency_conversion_client = get_currency_conversion_client()

        validated_data = serializer.validated_data
        owner = self.request.user

        with transaction.atomic():
            if "converted_quantity" not in list(validated_data):
                real_quantity = validated_data["real_quantity"]
                serializer.validated_data["converted_quantity"] = round(
                    real_quantity * currency_conversion_client.get_conversion(
                        validated_data["currency_type"],
                        self.request.user.pref_currency_type
                    ), 2
                )

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
    "patch": "partial_update",
    "delete": "destroy",
})
