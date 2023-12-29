"""Cache Keycloak client."""
from functools import lru_cache
from django.conf import settings
from src.keycloak_client.keycloak_client import KeycloakClient
from src.keycloak_client.keycloak_client_mock import KeycloakClientMock


@lru_cache
def get_keycloak_client() -> KeycloakClientMock | KeycloakClient:
    """Create an instance of a KeycloakClient using singleton pattern."""
    if settings.TESTING:
        return KeycloakClientMock()
    return KeycloakClient()
