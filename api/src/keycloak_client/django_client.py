"""Cache Keycloak client."""
from functools import lru_cache
from django.conf import settings
from keycloak_client.abstract_keycloak_client import AbstractKeycloakClient
from keycloak_client.keycloak_client import KeycloakClient
from keycloak_client.keycloak_client_mock import KeycloakClientMock


@lru_cache
def get_keycloak_client() -> AbstractKeycloakClient:
    """Create an instance of a KeycloakClient using singleton pattern."""
    if settings.TESTING:
        return KeycloakClientMock()
    return KeycloakClient()
