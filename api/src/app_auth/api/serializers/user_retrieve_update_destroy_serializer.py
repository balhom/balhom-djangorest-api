"""
Provide serializer classes.
"""
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import check_for_language, gettext_lazy as _
from app_auth.models.user_model import User


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
