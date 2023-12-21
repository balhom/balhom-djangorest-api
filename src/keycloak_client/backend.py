"""
Provides a Keycloak authentication backend class for django.
"""
import logging
from django.contrib.auth.backends import ModelBackend
from django.db.utils import OperationalError
from src.app_auth.models.user_model import User
from src.keycloak_client.django_client import get_keycloak_client

logger = logging.getLogger(__name__)


class KeycloakAuthenticationBackend(ModelBackend):
    """
    Authenticate with keycloak.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate backend."""
        keycloak_client = get_keycloak_client()
        res = keycloak_client.access_tokens(username, password)
        if res:
            try:
                keycloak_id = keycloak_client.get_user_id(email=username)
                user = User.objects.get(keycloak_id=keycloak_id)
            except OperationalError:
                logger.debug("User does not exists")
                return None
            return user
        logger.debug("Wrong credentials")
        return None
