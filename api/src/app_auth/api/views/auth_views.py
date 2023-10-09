from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from rest_framework import authentication
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
    # If no cookie, auth header will be used instead
    header = authentication.get_authorization_header(request)
    if not header:
        return None
    header = header.decode(authentication.HTTP_HEADER_ENCODING)
    auth = header.split()
    if len(auth) != 2 or auth[0].lower() != "bearer":
        return None
    return auth[1]


class AccessView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CredentialsSerializer

    def post(self, request, format=None):  # pylint: disable=unused-argument redefined-builtin
        keycloak_client = get_keycloak_client()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            return Response(
                data=keycloak_client.access_tokens(
                    email=email,
                    password=password
                )
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):  # pylint: disable=unused-argument redefined-builtin
        keycloak_client = get_keycloak_client()
        refresh_token = get_refresh_token(request=request)
        if refresh_token:
            return Response(
                data=keycloak_client.refresh_tokens(
                    refresh_token=refresh_token
                )
            )
        raise ValidationError(
            {
                "refresh_token": [_("Refresh token not provided")]
            }
        )


class LogoutView(APIView):
    permission_classes = (AllowAny,)

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
