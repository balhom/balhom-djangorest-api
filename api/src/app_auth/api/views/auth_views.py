from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from keycloak_client.django_client import get_keycloak_client
from app_auth.api.serializers.credentials_serializer import CredentialsSerializer


def get_refresh_token(request) -> str:
    """
    Get `token` str based on a request.

    Returns `None` if no authentication details were provided.
    """
    if 'refresh_token' in request.COOKIES:
        return request.COOKIES['refresh_token']
    # If no cookie, http data will be used instead
    if 'refresh_token' in request.data:
        return request.data['refresh_token']
    return None


def set_resfresh_token_cookie(response, refresh_token):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Strict",
    )
    return response


class AccessView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CredentialsSerializer

    def post(self, request, format=None):  # pylint: disable=unused-argument redefined-builtin
        keycloak_client = get_keycloak_client()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            tokens = keycloak_client.access_tokens(
                email=email,
                password=password
            )
            return set_resfresh_token_cookie(
                Response(
                    data=tokens
                ), tokens["refresh_token"]
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
            },
        )
    )
    def post(self, request, format=None):  # pylint: disable=unused-argument redefined-builtin
        keycloak_client = get_keycloak_client()
        refresh_token = get_refresh_token(request=request)
        if refresh_token:
            tokens = keycloak_client.refresh_tokens(
                refresh_token=refresh_token
            )
            return set_resfresh_token_cookie(
                Response(
                    data=tokens
                ), tokens["refresh_token"]
            )
        raise ValidationError(
            {
                "refresh_token": [_("Refresh token not provided")]
            }
        )


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
            },
        )
    )
    def post(self, request, format=None):  # pylint: disable=unused-argument redefined-builtin
        keycloak_client = get_keycloak_client()
        refresh_token = get_refresh_token(request=request)
        if refresh_token:
            return Response(
                data=keycloak_client.logout(
                    refresh_token=refresh_token
                )
            )
        raise ValidationError(
            {
                "refresh_token": [_("Refresh token not provided")]
            }
        )
