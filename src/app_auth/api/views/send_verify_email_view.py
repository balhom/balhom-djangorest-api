"""
Provide view classes.
"""
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.db import transaction
from src.keycloak_client.django_client import get_keycloak_client
from src.app_auth.api.serializers.email_serializer import (
    EmailSerializer
)
from src.app_auth.exceptions import (
    UserNotFoundException,
    CannotSendVerifyEmailException,
)


class SendVerifyEmailView(generics.CreateAPIView):
    """
    View to send verification email
    """

    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer
    parser_classes = (JSONParser,)

    @transaction.atomic
    def perform_create(self, serializer):
        email = serializer.validated_data["email"]

        keycloak_client = get_keycloak_client()

        user_info = keycloak_client.get_user_info_by_email(
            email=email)
        if not user_info:
            raise UserNotFoundException()
        if dict(user_info)["emailVerified"]:
            raise CannotSendVerifyEmailException()

        keycloak_id = dict(user_info)["id"]
        sent = keycloak_client.send_verify_email(
            keycloak_id=keycloak_id
        )
        if not sent:
            raise CannotSendVerifyEmailException()
