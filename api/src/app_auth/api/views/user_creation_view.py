"""
Provide view classes.
"""
from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from keycloak_client.django_client import get_keycloak_client
from app_auth.models.user_model import User
from app_auth.api.serializers.user_creation_serializer import (
    UserCreationSerializer,
)
from app_auth.exceptions import (
    UserEmailConflictException,
    CannotCreateUserException,
    UnverifiedEmailException,
    WrongCredentialsException,
    UserNameConflictException,
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

        pref_currency_type = validated_data["pref_currency_type"]

        keycloak_client = get_keycloak_client()

        user = keycloak_client.get_user_info_by_username(
            username=validated_data["username"]
        )
        if user:
            raise UserNameConflictException()

        created, res_code, _ = keycloak_client.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            locale=validated_data["locale"]
        )

        if not created and res_code != 409:
            raise CannotCreateUserException()

        keycloak_id = keycloak_client.get_user_id(
            email=validated_data["email"])
        if not keycloak_id:
            raise CannotCreateUserException()

        # In case keycloak user already exists
        if not created:
            try:
                try:
                    # Check credentials
                    keycloak_client.access_tokens(
                        email=validated_data["email"],
                        password=validated_data["password"]
                    )
                except WrongCredentialsException as exc:
                    raise UserEmailConflictException() from exc
                except UnverifiedEmailException:
                    pass
                # Check if user already exists
                user = User.objects.get(
                    keycloak_id=keycloak_id
                )
                raise UserEmailConflictException()
            except ObjectDoesNotExist:
                pass

        user = User.objects.create(
            keycloak_id=keycloak_id,
            pref_currency_type=pref_currency_type
        )
        user.set_password(validated_data["password"])
        user.save()
