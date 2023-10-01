"""
Provide view classes.
"""
from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from keycloak_client.django_client import get_keycloak_client
from app_auth.models.invitation_code_model import InvitationCode
from app_auth.models.user_model import User
from app_auth.api.serializers.user_creation_serializer import (
    UserCreationSerializer,
)
from app_auth.exceptions import (
    UserEmailConflictException,
    CannotCreateUserException,
)


class UserCreationView(generics.CreateAPIView):
    """
    View for User creation (register)
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserCreationSerializer
    parser_classes = (
        FormParser,
        JSONParser,
    )

    @transaction.atomic
    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        inv_code = validated_data["inv_code"]
        pref_currency_type = validated_data["pref_currency_type"]

        keycloak_client = get_keycloak_client()

        created, res_code, _ = keycloak_client.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            locale=validated_data["locale"]
        )

        if not created:
            if res_code == 409:
                raise UserEmailConflictException()
            raise CannotCreateUserException()

        keycloak_id = keycloak_client.get_user_id(
            email=validated_data["email"])
        if not keycloak_id:
            raise CannotCreateUserException()

        user = User.objects.create(
            keycloak_id=keycloak_id,
            inv_code=inv_code,
            pref_currency_type=pref_currency_type
        )
        user.set_password(validated_data["password"])

        # Invitation code decrease, race condition
        inv_codes = InvitationCode.objects.select_for_update().filter(  # pylint: disable=no-member
            code=inv_code.code
        )
        for inv_code in inv_codes:
            inv_code.usage_left = inv_code.usage_left - 1
            if inv_code.usage_left <= 0:
                inv_code.is_active = False
            inv_code.save()
        # Alternative:
        # inv_code.usage_left = F("usage_left") - 1
        user.save()
