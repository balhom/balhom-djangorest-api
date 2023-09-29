from rest_framework import serializers
from balance.models import MonthlyBalance


class MonthlyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBalance
        fields = [
            "gross_quantity",
            "expected_quantity",
            "currency_type",
            "year",
            "month",
            "created"
        ]
