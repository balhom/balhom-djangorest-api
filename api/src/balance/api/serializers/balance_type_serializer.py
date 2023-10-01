from rest_framework import serializers
from balance.models.balance_type_model import BalanceType


class BalanceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BalanceType
        fields = [
            "name",
            "type",
            "image",
        ]
        read_only_fields = [
            'image',
        ]
