from rest_framework import serializers
from balance.models.balance_model import Balance
from balance.api.serializers.balance_type_serializer import BalanceTypeSerializer


class BalanceSerializer(serializers.ModelSerializer):
    balance_type = BalanceTypeSerializer(many=False)

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
