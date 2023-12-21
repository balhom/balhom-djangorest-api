from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from src.balance.api.serializers.balance_type_serializer import BalanceTypeSerializer
from src.balance.models.balance_type_model import BalanceType
from src.balance.models.balance_model import Balance
from src.currency_conversion_client.django_client import get_currency_conversion_client


class BalanceSerializer(serializers.ModelSerializer):
    converted_quantity = serializers.FloatField(
        min_value=0.0,
        required=False,
    )
    balance_type = BalanceTypeSerializer()

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

    def validate_currency_type(self, currency_type):
        """
        Validate pref currency type param.
        """
        codes = get_currency_conversion_client().get_currency_codes()
        if currency_type not in codes:
            raise ValidationError(_("Currency type not supported"))
        return currency_type

    def create(self, validated_data):
        stored_balance_type = BalanceType.objects.filter(  # pylint: disable=no-member
            name=validated_data["balance_type"]["name"],
            type=validated_data["balance_type"]["type"],
        )
        if not stored_balance_type.exists():
            raise ValidationError(
                {"balance_type": [_("Provided balance type does not exists")]})
        validated_data["balance_type"] = stored_balance_type.first()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if validated_data.get("balance_type"):
            stored_balance_type = BalanceType.objects.filter(  # pylint: disable=no-member
                name=validated_data["balance_type"]["name"],
                type=validated_data["balance_type"]["type"],
            )
            if not stored_balance_type.exists():
                raise ValidationError(
                    {"balance_type": [_("Provided balance type does not exists")]})
            validated_data["balance_type"] = stored_balance_type.first()
        return super().update(instance, validated_data)
