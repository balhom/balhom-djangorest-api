"""
Provides a Keycloak client class.
"""
import logging
from jose import JWTError
from django.conf import settings
from django.utils.timezone import datetime
from keycloak import (
    KeycloakOpenID,
    KeycloakAdmin,
    KeycloakOpenIDConnection,
    KeycloakPostError,
    KeycloakPutError,
    KeycloakDeleteError,
)
from keycloak.exceptions import KeycloakAuthenticationError

logger = logging.getLogger(__name__)


class KeycloakClient:
    """
    Keycloak service client for user crud and authentication.
    """

    def __init__(self):
        logger.info(
            "Using:\n%s\n%s\n%s\n%s",
            settings.KEYCLOAK_URL,
            settings.KEYCLOAK_CLIENT_ID,
            settings.KEYCLOAK_CLIENT_SECRET,
            settings.KEYCLOAK_REALM
        )
        # OpenIDClient
        self.keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
            realm_name=settings.KEYCLOAK_REALM,
            verify="https" in settings.KEYCLOAK_URL,
        )
        self.public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + self.keycloak_openid.public_key()
            + "\n-----END PUBLIC KEY-----"
        )
        # Admin client
        keycloak_connection = KeycloakOpenIDConnection(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
            realm_name=settings.KEYCLOAK_REALM,
            verify="https" in settings.KEYCLOAK_URL,
        )
        self.keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

    def verify_access_token(self, access_token: str) -> tuple[bool, dict]:
        """Tries to decode `acces_token` using keycloak's public key."""
        options = {
            "verify_signature": True,
            "verify_aud": False,
            "verify_exp": True
        }
        try:
            res = self.keycloak_openid.decode_token(
                access_token, key=self.public_key, options=options
            )
            return (True, res)
        except JWTError as ex:
            print(ex)
            return (False, {})

    def get_user_info_by_id(self, keycloak_id: str) -> dict | None:
        """Get user info by keycloak id."""
        return self.keycloak_admin.get_user(user_id=keycloak_id)

    def get_user_info_by_email(self, email: str) -> dict | None:
        """Get user info by email."""
        users = self.keycloak_admin.get_users({"email": email})
        return None if not users else list(users)[0]

    def get_user_sessions(self, keycloak_id: str) -> list | None:
        """Get user sessions."""
        sessions = self.keycloak_admin.get_sessions(user_id=keycloak_id)
        return sessions

    def get_user_last_login(self, keycloak_id: str) -> datetime | None:
        """Get user last login date time based on user sessions."""
        sessions = self.get_user_sessions(keycloak_id)
        if not sessions:
            return None
        if "start" not in sessions[0]:
            return None
        return datetime.fromtimestamp(float(sessions[0]["start"]) / 1000)

    def get_user_id(self, email: str) -> str | None:
        """Get user keycloak id."""
        user = self.get_user_info_by_email(email)
        if user:
            return user.get("id")
        return None

    def create_user(
        self, email: str, username: str, password: str, locale: str
    ) -> tuple[bool, int, dict]:
        """
        User creation.
        """
        print(username)
        print(email)
        try:
            self.keycloak_admin.create_user(
                payload={
                    "firstName": username,
                    "username": username,
                    "email": email,
                    "enabled": True,
                    "emailVerified": False,
                    "attributes": {"locale": locale},
                    "credentials": [
                        {
                            "type": "password",
                            "value": password,
                            "temporary": False
                        }
                    ],
                },
                exist_ok=False,
            )
            return True, 200, {}
        except KeycloakPostError as ex:
            return False, ex.response_code, ex.response_body

    def update_user_by_id(
        self, keycloak_id: str, username: str | None = None, locale: str | None = None
    ) -> tuple[bool, int, dict]:
        """
        Update user by keycloak id.
        """
        try:
            payload = {}
            if username:
                payload["firstName"] = username
            if locale:
                payload["attributes"] = {"locale": locale}
            if not payload:
                return False
            self.keycloak_admin.update_user(
                user_id=keycloak_id,
                payload=payload
            )
            return True, 200, {}
        except KeycloakPutError as ex:
            return False, ex.response_code, ex.response_body

    def delete_user_by_id(self, keycloak_id: str) -> tuple[bool, int, dict]:
        """
        Delete user by keycloak id.
        """
        try:
            self.keycloak_admin.delete_user(user_id=keycloak_id)
            return True, 200, {}
        except KeycloakDeleteError as ex:
            return False, ex.response_code, ex.response_code

    def send_verify_email(self, keycloak_id: str) -> bool:
        """
        Send verification mail.
        """
        try:
            self.keycloak_admin.send_verify_email(user_id=keycloak_id)
            return True
        except KeycloakPutError:
            return False

    def send_reset_password_email(self, keycloak_id: str) -> bool:
        """
        Send password reset mail.
        """
        try:
            self.keycloak_admin.send_update_account(
                user_id=keycloak_id, payload=["UPDATE_PASSWORD"])
            return True
        except KeycloakPutError:
            return False

    def change_user_password(self, keycloak_id: str, password: str) -> bool:
        """
        Change user password.
        """
        try:
            self.keycloak_admin.set_user_password(
                user_id=keycloak_id, password=password, temporary=False)
            return True
        except KeycloakPutError:
            return False

    def access_tokens(self, email: str, password: str) -> dict:
        """
        Get access and refresh tokens.
        """
        try:
            response = self.keycloak_openid.token(
                username=email,
                password=password,
                grant_type=["password"],
            )
            return {
                "access_token": response["access_token"],
                "expires_in": response["expires_in"],
                "refresh_token": response["refresh_token"],
                "refresh_expires_in": response["refresh_expires_in"],
            }
        except KeycloakAuthenticationError as exc:
            from app_auth.exceptions import WrongCredentialsException
            raise WrongCredentialsException() from exc
        except KeycloakPostError as exc:
            from app_auth.exceptions import UnverifiedEmailException
            raise UnverifiedEmailException() from exc

    def refresh_tokens(self, refresh_token: str) -> dict:
        """
        Refresh tokens.
        """
        try:
            response = self.keycloak_openid.refresh_token(
                refresh_token=refresh_token,
                grant_type=["refresh_token"],
            )
            return {
                "access_token": response["access_token"],
                "expires_in": response["expires_in"],
                "refresh_token": response["refresh_token"],
                "refresh_expires_in": response["refresh_expires_in"],
            }
        except KeycloakPostError as exc:
            from core.exceptions import AppUnauthorizedException
            raise AppUnauthorizedException(
                detail=exc.error_message,
            ) from exc

    def logout(self, refresh_token: str):
        """
        Logout refresh token.
        """
        try:
            self.keycloak_openid.logout(
                refresh_token=refresh_token,
            )
        except KeycloakAuthenticationError as exc:
            from core.exceptions import AppUnauthorizedException
            raise AppUnauthorizedException(
                detail=exc.error_message,
            ) from exc
