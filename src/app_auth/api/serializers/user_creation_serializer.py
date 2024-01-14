"""
Provide serializer classes.
"""
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import check_for_language, gettext_lazy as _
from src.app_auth.models.user_model import User
from src.app_auth.api.serializers.utils import check_username_pass
from src.currency_conversion_client.django_client import get_currency_conversion_client


class UserCreationSerializer(serializers.ModelSerializer):
    """
    Serializer for User creation (register)
    """

    username = serializers.CharField(
        required=True,
        max_length=15,
        validators=[RegexValidator(regex=r"^[A-Za-z0-9]+$")],
    )
    email = serializers.EmailField(required=True)
    locale = serializers.CharField(
        max_length=5,
        required=True
    )
    password = serializers.CharField(
        required=True, write_only=True, max_length=30, validators=[validate_password]
    )

    class Meta:  # pylint: disable=missing-class-docstring too-few-public-methods
        model = User
        fields = [
            "username",
            "email",
            "current_balance",
            "receive_email_balance",
            "expected_annual_balance",  # not required
            "expected_monthly_balance",  # not required
            "locale",
            "pref_currency_type",
            "password",
            "image",
        ]
        extra_kwargs = {
            "pref_currency_type": {"required": True}
        }

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

    def validate(self, attrs):
        check_username_pass(
            attrs["username"], attrs["email"], attrs["password"]
        )
        return attrs
