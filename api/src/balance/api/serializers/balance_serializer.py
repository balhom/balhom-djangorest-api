from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from balance.api.serializers.balance_type_serializer import BalanceTypeSerializer
from balance.models.balance_model import Balance
from balance.models.balance_type_model import BalanceType


class BalanceSerializer(serializers.ModelSerializer):
    converted_quantity = serializers.FloatField(
        min_value=0.0,
        required=False,
    )

    class Meta:
        model = Balance
        fields = [
            "id",
            "name",
            "description",
            "real_quantity",
            "converted_quantity",
            "date",
            "currency_type",
            "balance_type"
        ]
        read_only_fields = [
            "id"
        ]

    def is_valid(self, *, raise_exception=False):
        if "balance_type" in list(self.initial_data):
            if (
                not isinstance(self.initial_data["balance_type"], dict)
                or "name" not in list(self.initial_data["balance_type"])
                or "type" not in list(self.initial_data["balance_type"])
            ):
                raise ValidationError(
                    {"balance_type": [_("Balance type not provided")]})
            balance_type = self.initial_data["balance_type"]
            stored_balance_type = BalanceType.objects.filter(
                name=balance_type["name"],
                type=balance_type["type"],
            )
            if not stored_balance_type.exists():
                raise ValidationError(
                    {"balance_type": [_("Provided balance type does not exists")]})
            self.initial_data["balance_type"] = stored_balance_type.first().id
        return super().is_valid(raise_exception=raise_exception)


class BalanceGetSerializer(BalanceSerializer):
    balance_type = BalanceTypeSerializer()
