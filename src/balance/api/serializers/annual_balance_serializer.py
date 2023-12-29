from rest_framework import serializers
from src.balance.models import AnnualBalance


class AnnualBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnualBalance
        fields = [
            "gross_quantity",
            "expected_quantity",
            "currency_type",
            "year",
            "created"
        ]
