"""
Provide view classes.
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.utils.timezone import now
from keycloak_client.django_client import get_keycloak_client
from core.permissions import IsCurrentVerifiedUser
from app_auth.models import User
from app_auth.api.serializers.user_serializers import (
    UserRetrieveUpdateDestroySerializer,
)
from app_auth.tasks import change_converted_quantities
from app_auth.exceptions import (
    CannotUpdateUserException,
    CannotDeleteUserException,
    CurrencyTypeChangedException,
)
from currency_conversion_client.django_client import get_currency_conversion_client


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for User retrieve, update and destroy
    """

    queryset = User.objects.all()
    permission_classes = (IsCurrentVerifiedUser,)
    serializer_class = UserRetrieveUpdateDestroySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self, queryset=None):  # pylint: disable=unused-argument
        return self.request.user

    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        keycloak_client = get_keycloak_client()

        user_data = keycloak_client.get_user_info_by_id(
            keycloak_id=request.user.keycloak_id)
        last_login = keycloak_client.get_user_last_login(
            keycloak_id=request.user.keycloak_id
        )
        locale = "en" if not user_data["attributes"]["locale"] \
            else user_data["attributes"]["locale"][0]

        response = dict(serializer.data)
        response["username"] = user_data["firstName"]
        response["email"] = user_data["email"]
        response["last_login"] = last_login
        response["locale"] = locale

        return Response(response)

    @transaction.atomic
    def perform_update(self, serializer):
        currency_conversion_client = get_currency_conversion_client()

        # The user balance should only be converted if
        # the same balance is provided in the request
        # and the pref_currency_type is changed, same for
        # expected_annual_balance and expected_monthly_balance
        if (
            "pref_currency_type" in serializer.validated_data
            and serializer.validated_data["pref_currency_type"]
            != serializer.instance.pref_currency_type
        ):
            if "balance" in serializer.validated_data:
                user = self.request.user
                if user.date_currency_change:
                    duration_s = (
                        now() - user.date_currency_change).total_seconds()
                    if duration_s < 24 * 60 * 60:
                        raise CurrencyTypeChangedException()
                serializer.validated_data["balance"] = round(
                    currency_conversion_client.get_conversion(
                        serializer.instance.pref_currency_type,
                        serializer.validated_data["pref_currency_type"]
                    ) * serializer.validated_data["balance"], 2
                )
                # Change expected annual balance
                if "expected_annual_balance" not in serializer.validated_data:
                    serializer.validated_data[
                        "expected_annual_balance"
                    ] = self.request.user.expected_annual_balance
                serializer.validated_data[
                    "expected_annual_balance"
                ] = round(
                    currency_conversion_client.get_conversion(
                        serializer.instance.pref_currency_type,
                        serializer.validated_data["pref_currency_type"]
                    ) * serializer.validated_data["expected_annual_balance"], 2
                )
                # Change expected monthly balance
                if "expected_monthly_balance" not in serializer.validated_data:
                    serializer.validated_data[
                        "expected_monthly_balance"
                    ] = self.request.user.expected_monthly_balance
                serializer.validated_data[
                    "expected_monthly_balance"
                ] = round(
                    currency_conversion_client.get_conversion(
                        serializer.instance.pref_currency_type,
                        serializer.validated_data["pref_currency_type"]
                    ) * serializer.validated_data["expected_monthly_balance"], 2
                )
                change_converted_quantities.delay(
                    user.keycloak_id,
                    user.pref_currency_type.code,
                    serializer.validated_data["pref_currency_type"].code,
                )
                serializer.validated_data["date_currency_change"] = now()
            if "expected_annual_balance" in serializer.validated_data:
                serializer.validated_data[
                    "expected_annual_balance"
                ] = round(
                    currency_conversion_client.get_conversion(
                        serializer.instance.pref_currency_type,
                        serializer.validated_data["pref_currency_type"]
                    ) * serializer.validated_data["expected_annual_balance"], 2
                )
            if "expected_monthly_balance" in serializer.validated_data:
                serializer.validated_data[
                    "expected_monthly_balance"
                ] = round(
                    currency_conversion_client.get_conversion(
                        serializer.instance.pref_currency_type,
                        serializer.validated_data["pref_currency_type"]
                    ) * serializer.validated_data["expected_monthly_balance"], 2
                )
        serializer.save()

        # Keycloak update
        keycloak_client = get_keycloak_client()
        keycloak_id = self.request.user.keycloak_id
        if "username" in serializer.validated_data \
                or "locale" in serializer.validated_data:
            updated, _, _ = keycloak_client.update_user_by_id(
                keycloak_id=keycloak_id,
                username=serializer.validated_data.get("username"),
                locale=serializer.validated_data.get("locale")
            )
            if not updated:
                raise CannotUpdateUserException()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        res = super().update(request, args, kwargs)
        res = res.data

        keycloak_client = get_keycloak_client()

        user_data = keycloak_client.get_user_info_by_id(
            keycloak_id=request.user.keycloak_id)
        last_login = keycloak_client.get_user_last_login(
            keycloak_id=request.user.keycloak_id
        )
        locale = "en" if not user_data["attributes"]["locale"] \
            else user_data["attributes"]["locale"][0]

        res["username"] = user_data["username"]
        res["email"] = user_data["email"]
        res["last_login"] = last_login
        res["locale"] = locale
        return Response(res)

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.delete()
        keycloak_client = get_keycloak_client()
        keycloak_id = self.request.user.keycloak_id
        deleted, _, _ = keycloak_client.delete_user_by_id(
            keycloak_id=keycloak_id)
        if not deleted:
            raise CannotDeleteUserException()
