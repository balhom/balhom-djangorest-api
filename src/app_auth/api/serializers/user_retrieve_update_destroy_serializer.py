"""
Provide serializer classes.
"""
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import check_for_language, gettext_lazy as _
from src.app_auth.models.user_model import User
from src.currency_conversion_client.django_client import get_currency_conversion_client


class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Serializer to get, update or delete user data
    """

    username = serializers.CharField(
        required=False,
        max_length=15,
        validators=[RegexValidator(regex=r"^[A-Za-z0-9]+$")],
        write_only=True
    )
    locale = serializers.CharField(
        max_length=5,
        required=False,
        write_only=True
    )
    pref_currency_type = serializers.CharField(
        max_length=4,
        required=False
    )

    class Meta:  # pylint: disable=missing-class-docstring too-few-public-methods
        model = User
        fields = [
            "username",
            "locale",
            "receive_email_balance",
            "current_balance",
            "expected_annual_balance",
            "expected_monthly_balance",
            "pref_currency_type",
            "image",
            "last_login",
        ]
        read_only_fields = [
            "last_login",
        ]

    def validate_locale(self, locale):
        """
        Validate locale param.
        """
        if not check_for_language(locale):
            raise ValidationError(_("Locale not supported"))
        return locale

    def validate_pref_currency_type(self, pref_currency_type):
        """
        Validate pref currency type param.
        """
        codes = get_currency_conversion_client().get_currency_codes()
        if pref_currency_type not in codes:
            raise ValidationError(_("Currency type not supported"))
        return pref_currency_type
